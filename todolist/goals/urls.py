from django.urls import path

from goals import views

urlpatterns = [
    path("board/create", views.BoardCreateView.as_view(), name="create_board"),
    path("board/list", views.BoardListView.as_view(), name="list_board"),
    path("board/<pk>", views.BoardView.as_view(), name='detail_update_delete_board'),

    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='category_goal_create'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='category_goal_list'),
    path("goal_category/<pk>", views.GoalCategoryView.as_view(), name='detail_update_delete_goal_category'),

    path("goal/create", views.GoalCreateView.as_view(), name='create_goal'),
    path("goal/list", views.GoalListView.as_view(), name='list_goal'),
    path("goal/<pk>", views.GoalView.as_view(), name='detail_update_delete_goal'),

    path("goal_comment/create", views.GoalCommentCreateView.as_view(), name='comment_create_goal'),
    path("goal_comment/list", views.GoalCommentListView.as_view(), name='comment_list_goal'),
    path("goal_comment/<pk>", views.GoalCommentView.as_view(), name='comment_pk_goal'),
]