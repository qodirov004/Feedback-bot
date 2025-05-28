from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import DirectionMod, TeachersMod, GroupsMod, QuestionMod, UsersMod, UserAnswersMod, RewardsMod

# Register your models here.

@admin.register(DirectionMod) 
class DirectionAdmin(ModelAdmin) :
    list_display = ["name", "created_at"]
    list_filter = ["name"]

@admin.register(TeachersMod)
class TeachersAdmin(ModelAdmin) :
    list_display = ["full_name", "direction", "created_at"]
    list_filter = ["full_name", "direction"]

@admin.register(GroupsMod)
class GroupsAdmin(ModelAdmin) :
    list_display = ["name", "teacher", "created_at"]
    list_filter = ["teacher"]

@admin.register(QuestionMod)
class QuestionAdmin(ModelAdmin) :
    list_display = ["question", "answer_A", "answer_B", "answer_C", "answer_D", "created_at"]
    list_filter = ["question"]

@admin.register(UsersMod)
class UsersAdmin(ModelAdmin) :
    list_display = ["user_id", "full_name", "direction", "teacher", "group_name", "day_type", "start_class_time", "balance", "created_at"]
    list_filter = ["full_name", "direction", "teacher"]

@admin.register(UserAnswersMod)
class UserAnswersAdmin(ModelAdmin) :
    list_display = ["user", "question", "answer_A", "answer_B", "answer_C", "answer_D", "answer", "comment", "created_at"]
    list_filter = ["user__direction", "user__teacher", "user__group_name", "user__start_class_time"]

@admin.register(RewardsMod)
class RewardsAdmin(ModelAdmin) :
    list_display = ["amount", "created_at"] 