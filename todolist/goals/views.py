from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, generics
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions, GoalPermissions, GoalCategoryPermissions, CommentsPermissions
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalCategoryCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardSerializer, BoardCreateSerializer, \
    BoardListSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    # FilterSet_fields = ['board']
    filterset_fields = ['board']
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = GoalDateFilter
    # FilterSet_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    # search_fields = ["title", "description"]
    # ordering = ["priority", "due_date"]
    # ordering_fields = ["priority", "due_date"]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user__id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user__id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=("status",))
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,]
    # FilterSet_class = GoalDateFilter
    filterset_class = GoalDateFilter
    ordering_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [CommentsPermissions]

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class BoardCreateView(CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [BoardPermissions]


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    # serializer_class = BoardListSerializer
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination
    # filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=("is_deleted",))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance
