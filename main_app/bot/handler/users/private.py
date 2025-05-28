import asyncio
from aiogram import Router, F, html, Bot
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now
from asgiref.sync import sync_to_async

from ...filters.chat_type import chat_type_filter
from ...states.state_user.state_us import Form
from ...keyboards.inline.button import get_direction_buttons, get_teacher_buttons, get_group_buttons, day_button, time_button, confirm_buttons
from ...keyboards.reply.rep_button import Createreply
from main_app.models import DirectionMod, TeachersMod, UsersMod, QuestionMod, UserAnswersMod, RewardsMod

user_private_router = Router()
user_private_router.message.filter(chat_type_filter(['private']))

@sync_to_async
def register_user_to_django(telegram_id, full_name, direction_name, teacher_name, group_name, day_type, start_time):
    direction = DirectionMod.objects.get(name=direction_name)
    try:
        teacher = TeachersMod.objects.get(full_name=teacher_name)
    except TeachersMod.DoesNotExist:
        teacher = None

    UsersMod.objects.create(
        user_id=telegram_id,
        full_name=full_name,
        direction=direction,
        teacher=teacher,
        start_class_time=start_time,
        day_type=day_type,
        group_name=group_name,
        balance=0,
        quiz_sent_today=False
    )

@user_private_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    from_user_id = message.from_user.id
    existing_user = await sync_to_async(UsersMod.objects.filter(user_id=from_user_id).exists)()
    if existing_user:
        await message.answer("✅ Siz allaqachon ro‘yxatdan o‘tgansiz.")
        return
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\nIsm va familiyangizni kiriting:")
    await state.set_state(Form.full_name)

@user_private_router.message(Form.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    directions = await get_direction_buttons()
    if not directions:
        await message.answer("Yo'nalishlar topilmadi ❌")
        return
    await message.answer("Yo'nalishni tanlang:", reply_markup=directions)
    await state.set_state(Form.direction)

@user_private_router.callback_query(F.data.startswith("dir_"))
async def process_direction(call: CallbackQuery, state: FSMContext):
    direction_name = call.data.split("_", 1)[1]
    await state.update_data(direction_name=direction_name)
    teachers_markup = await get_teacher_buttons(direction_name)
    if not teachers_markup.inline_keyboard:
        await call.message.answer("❗ Ushbu yo‘nalishga ustozlar topilmadi.")
        return
    await call.message.answer("Ustozni tanlang:", reply_markup=teachers_markup)
    await state.set_state(Form.teacher)

@user_private_router.callback_query(F.data.startswith("teacher_"))
async def process_teacher(call: CallbackQuery, state: FSMContext):
    teacher_name = call.data.split("_", 1)[1]
    await state.update_data(teacher_name=teacher_name)
    groups = await get_group_buttons(teacher_name)
    if not groups.inline_keyboard:
        await call.message.answer("❗ Ushbu ustozga tegishli guruhlar topilmadi.")
        return
    await call.message.answer("📘 Guruhni tanlang:", reply_markup=groups)
    await state.set_state(Form.group)

@user_private_router.callback_query(F.data.startswith("group_"))
async def process_group(call: CallbackQuery, state: FSMContext):
    group_name = call.data.split("_", 1)[1]
    await state.update_data(group_name=group_name)
    await call.message.answer("📅 Dars kuni tanlang:", reply_markup=day_button)
    await state.set_state(Form.day_type)

@user_private_router.callback_query(Form.day_type)
async def process_day_type(call: CallbackQuery, state: FSMContext):
    day = call.data
    await state.update_data(day_type=day)
    await call.message.answer("Dars boshlanish vaqtini tanlang:", reply_markup=time_button)
    await state.set_state(Form.start_time)

@user_private_router.callback_query(Form.start_time)
async def process_start_time_callback(call: CallbackQuery, state: FSMContext):
    time_value = call.data
    await state.update_data(start_time=time_value)

    data = await state.get_data()
    await call.message.answer(
        f"✅ Ma'lumotlaringiz:\n"
        f"👤 Ism: {data['full_name']}\n"
        f"📚 Yo‘nalish nomi: {data['direction_name']}\n"
        f"👨‍🏫 Ustoz ismi: {data['teacher_name']}\n"
        f"👥 Guruh nomi: {data['group_name']}\n"
        f"📆 Kun: {data['day_type']}\n"
        f"⏰ Soat: {data['start_time']}\n\n"
        f"<b>Tasdiqlaysizmi?</b>",
        reply_markup=confirm_buttons
    )
    await state.set_state(Form.confirmation)
    await call.answer()

@user_private_router.callback_query(F.data == "confirm_yes")
async def process_confirmation_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await register_user_to_django(
        telegram_id=call.from_user.id,
        full_name=data['full_name'],
        direction_name=data['direction_name'],
        teacher_name=data['teacher_name'],
        group_name=data['group_name'],
        day_type=data['day_type'],
        start_time=data['start_time']
    )
    await call.message.answer("✅ Ma'lumotlaringiz Django models orqali saqlandi. Rahmat!")
    await state.clear()
    await call.answer()

@user_private_router.callback_query(F.data == "confirm_no")
async def process_confirmation_no(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("🔄 Qaytadan boshlaylik.\nIltimos, ism va familiyangizni kiriting:")
    await state.set_state(Form.full_name)
    await call.answer()

# @user_private_router.callback_query(F.data.startswith("ans_"))
# async def handle_answer(call: CallbackQuery, state: FSMContext):
#     _, qid, selected = call.data.split("_")
#     await state.update_data(qid=int(qid), selected=selected)
#     await state.set_state(Form.reward)
#     await call.message.answer("✍️ Taklif yoki shikoyatingiz bo‘lsa, yozib qoldiring. Bo‘lmasa, '-' belgisi bilan yuboring:")
#     await call.answer()

@user_private_router.message(Form.reward)
async def save_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    
    user = await sync_to_async(lambda: UsersMod.objects.get(user_id=message.from_user.id))()
    question = await sync_to_async(lambda: QuestionMod.objects.get(id=data['qid']))()

    await sync_to_async(UserAnswersMod.objects.create)(
        user=user,
        question=question,
        answer_A=question.answer_A,
        answer_B=question.answer_B,
        answer_C=question.answer_C,
        answer_D=question.answer_D,
        answer=data['selected'],
        comment=message.text
    )

    await message.answer("✅ Javobingiz va taklifingiz saqlandi.")
    await state.clear()

    total_questions = await sync_to_async(QuestionMod.objects.count)()
    user_answers = await sync_to_async(
        lambda: UserAnswersMod.objects.filter(user=user)
        .values_list("question_id", flat=True).distinct().count()
    )()

    if user_answers >= total_questions:
        reward = await sync_to_async(lambda: RewardsMod.objects.first())()
        if reward and reward.amount > 0:
            user.balance += reward.amount
            await sync_to_async(user.save)()

@user_private_router.message(F.text.lower() == "/balance")
async def show_balance(message: Message):
    user = await sync_to_async(lambda: UsersMod.objects.get(user_id=message.from_user.id))()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Yechib olish", callback_data="withdraw_balance")]
    ])
    await message.answer(f"💰 Sizning balansingiz: <b>{user.balance}</b>", reply_markup=markup)

@user_private_router.callback_query(F.data == "withdraw_balance")
async def withdraw_balance(call: CallbackQuery):
    user = await sync_to_async(lambda: UsersMod.objects.get(user_id=call.from_user.id))()
    if user.balance == 0:
        await call.answer("❗ Siz hali mukofotni olmagansiz", show_alert=True)
        return
    user.balance = 0
    await sync_to_async(user.save)()
    await call.message.edit_text("✅ Balansingiz muvaffaqiyatli yechildi. (0)")
    await call.answer("Yechildi")