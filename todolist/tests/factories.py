import datetime
from django.contrib.auth import get_user_model
import factory

USER_MODEL = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL

    username = factory.Faker('name')
    password = 'Zaraza1991'
    email = factory.Faker('email')


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'goals.Board'

    title = factory.Faker('name')
    is_deleted = False


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'goals.GoalCategory'

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    title = 'Тестовая категория'
    is_deleted = False


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'goals.Goal'

    title = factory.Faker('name')
    description = 'Описание тестовой цели'
    due_date = str(datetime.datetime.now().date())
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'goals.GoalComment'

    text = 'Текст тестового комментария'
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'goals.BoardParticipant'

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = 1
