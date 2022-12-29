from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from goals.models import BoardParticipant, Goal, GoalCategory, Board, GoalComment


# class BoardPermissions(IsAuthenticated):
#     def has_object_permission(self, request, view, obj: Board):
#         filters: dict = {'user': request.user, 'board': obj}
#         if request.method not in permissions.SAFE_METHODS:
#             filters['role'] = BoardParticipant.Role.owner
#         return BoardParticipant.objects.filter(**filters).exists()
class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, category):
        if not request.user.is_authenticated:
            return False
        if permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer
            ]
        ).exists()
    # def has_object_permission(self, request, view, obj: GoalCategory):
    #     filters: dict = {'user': request.user, 'board': obj.board}
    #     if request.method not in permissions.SAFE_METHODS:
    #         filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
    #     return BoardParticipant.objects.filter(**filters).exists()


class GoalPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        filters: dict = {'user': request.user, 'board': obj.category.board}
        if request.method not in permissions.SAFE_METHODS:
            filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**filters).exists()


class CommentsPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj: GoalComment):
        return any((
            request.method in permissions.SAFE_METHODS,
            obj.user_id == request.user.id,
        ))

# from rest_framework import permissions
# from rest_framework.permissions import IsAuthenticated
#
# from goals.models import BoardParticipant, Goal, GoalCategory, Board, GoalComment
#
#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.user_id == request.user.id
#
#
# class BoardPermissions(IsAuthenticated):
#     def has_object_permission(self, request, view, obj: Board):
#         filters: dict = {'user': request.user, 'board': obj}
#         if request.method not in permissions.SAFE_METHODS:
#             filters['role'] = BoardParticipant.Role.owner
#         return BoardParticipant.objects.filter(**filters).exists()
#
#
# class GoalCategoryPermissions(IsAuthenticated):
#     def has_object_permission(self, request, view, obj: GoalCategory):
#         filters: dict = {'user': request.user, 'board': obj.board}
#         if request.method not in permissions.SAFE_METHODS:
#             filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
#         return BoardParticipant.objects.filter(**filters).exists()
#
#
# class GoalPermissions(IsAuthenticated):
#
#     def has_object_permission(self, request, view, obj: Goal):
#         filters: dict = {'user': request.user, 'board': obj.category.board}
#         if request.method not in permissions.SAFE_METHODS:
#             filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
#         return BoardParticipant.objects.filter(**filters).exists()
#
#
# class CommentsPermissions(IsAuthenticated):
#     def has_object_permission(self, request, view, obj: GoalComment):
#         return any((
#             request.method in permissions.SAFE_METHODS,
#             obj.user_id == request.user.id,
#         ))
