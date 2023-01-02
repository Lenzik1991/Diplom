import datetime

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import GoalCategory
from goals.models import Goal
from todolist.settings import TG_BOT_API_TOKEN


class Command(BaseCommand):
    help = 'Run telegram bot'

    def __init__(self, *args: str, **kwargs: int):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(TG_BOT_API_TOKEN)
        self.offset = 0

    def handle(self, *args: str, **kwargs: int):

        while True:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                tg_user: TgUser | False = self.check_user(item.message)

                if not tg_user:
                    continue

                if item.message.text == '/goals':
                    self.get_goals(tg_user)
                elif item.message.text == '/create':
                    self.choice_category(tg_user)
                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Для просмотра списка задач введи /goals.\n'
                                                                    'Для создания задачи введи /create.\n'
                                                                    'Для отмены введи /cancel')

    def check_user(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=message.chat.id, tg_user_id=message.from_.id)

        if created or not tg_user.user:
            tg_user.set_verification_code()
            self.tg_client.send_message(tg_user.tg_chat_id,
                                        f'Подтверди, пожалуйста, свой аккаунт. '
                                        f'Для подтверждения необходимо ввести код в приложении: '
                                        f'{tg_user.verification_code} на сайте eportnova.ga')
            return False
        return tg_user

    def get_goals(self, tg_user: TgUser):
        goals = Goal.objects.filter(user=tg_user.user, status__in=[1, 2, 3])

        if goals.count() > 0:
            [self.tg_client.send_message(tg_user.tg_chat_id,
                                         f'Название {goal.title},\n'
                                         f'Категория {goal.category},\n'
                                         f'Статус {goal.get_status_display()},\n'
                                         f'Дедлайн {goal.due_date if goal.due_date else "Нет"} \n') for goal in goals]
        else:
            self.tg_client.send_message(tg_user.tg_chat_id, 'Нет задач')

    def choice_category(self, tg_user: TgUser):
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user, is_deleted=False)
        self.tg_client.send_message(tg_user.tg_chat_id,
                                    f'Выбери категорию: {[category.title for category in categories]}\n'
                                    f'Для отмены введи /cancel')
        dict_categories = {item.title: item for item in categories}

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                if item.message.text in dict_categories:
                    category = dict_categories.get(item.message.text)
                    self.create_goal(tg_user, category)
                    flag = False
                elif item.message.text == '/cancel':
                    flag = False
                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Категория не существует')

    def create_goal(self, tg_user: TgUser, category: GoalCategory):
        self.tg_client.send_message(chat_id=tg_user.tg_chat_id,
                                    text='Укажите название задачи. Для отмены введите /cancel'
                                    )

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                if item.message.text.strip().lower() == "/cancel":
                    self.tg_client.send_message(chat_id=item.message.chat.id, text='Cоздание цели прервано')
                    flag = False
                else:
                    due_date = datetime.date.today() + datetime.timedelta(days=14)
                    goal = Goal.objects.create(
                        category=category,
                        user=tg_user.user,
                        title=item.message.text,
                        description='Цель создана в Telegram',
                        due_date=due_date.strftime('%Y-%m-%d')
                    )
                    self.tg_client.send_message(
                        chat_id=item.message.chat.id, text=f'Цель [{goal.title}] успешно создана')
                    flag = False
