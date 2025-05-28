from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from asgiref.sync import sync_to_async
from main_app.models import DirectionMod, TeachersMod, GroupsMod

@sync_to_async
def get_direction_buttons():
    buttons = []
    directions = DirectionMod.objects.all()
    for direction in directions:
        buttons.append(
            [InlineKeyboardButton(text=direction.name, callback_data=f"dir_{direction.name}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@sync_to_async
def get_teacher_buttons(direction_name):
    try:
        direction = DirectionMod.objects.get(name=direction_name)
        teachers = TeachersMod.objects.filter(direction=direction)
    except DirectionMod.DoesNotExist:
        teachers = []

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    for teacher in teachers:
        row.append(InlineKeyboardButton(
            text=teacher.full_name,
            callback_data=f"teacher_{teacher.full_name}"
        ))
        if len(row) == 2:
            keyboard.inline_keyboard.append(row)
            row = []
    if row:
        keyboard.inline_keyboard.append(row)
    return keyboard


@sync_to_async
def get_group_buttons(teacher_name: str):
    groups = GroupsMod.objects.filter(teacher__full_name=teacher_name)
    buttons = []

    for group in groups:
        buttons.append([
            InlineKeyboardButton(
                text=group.name,
                callback_data=f"group_{group.name}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

day_button = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Juft kunlari", callback_data = "juft"), InlineKeyboardButton(text = "Toq kunlari", callback_data = "toq")]
    ]
)

time_button = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="9:00", callback_data="9:00"), InlineKeyboardButton(text="14:00", callback_data="14:00")],
      [InlineKeyboardButton(text = "16:00", callback_data = "16:00"), InlineKeyboardButton(text = "19:00", callback_data = "19:00")]
    ]
)

confirm_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no")
        ]
    ]
)