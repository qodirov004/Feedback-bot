import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext

from set_app.settings import BOT_TOKEN
from main_app.models import UsersMod, QuestionMod, UserAnswersMod, RewardsMod
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now
from asgiref.sync import sync_to_async

from main_app.bot.states.state_user.state_us import Form
from .handler.users.private import user_private_router

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(user_private_router)

user_question_progress = {}

@sync_to_async
def get_eligible_users():
    today = now().date()
    weekday = today.strftime("%A")
    juft = ["Tuesday", "Thursday", "Saturday"]
    toq = ["Monday", "Wednesday", "Friday"]
    users = UsersMod.objects.filter(quiz_sent_today=False)
    eligible = []

    for user in users:
        try:
            if (user.day_type == "juft" and weekday in juft) or (user.day_type == "toq" and weekday in toq):
                if isinstance(user.start_class_time, str):
                    start_time = datetime.strptime(user.start_class_time, "%H:%M").time()
                else:
                    start_time = user.start_class_time
                lesson_time = make_aware(datetime.combine(today, start_time))
                if now() >= lesson_time + timedelta(hours=3):
                    eligible.append(user)
        except Exception as e:
            print(f"Xatolik foydalanuvchi bilan ({user.user_id}): {e}")
    return eligible

@sync_to_async
def get_questions():
    return list(QuestionMod.objects.all())

@sync_to_async
def save_answer_to_db(user_id, qid, selected, comment="-"):
    try:
        user = UsersMod.objects.get(user_id=user_id)
        question = QuestionMod.objects.get(id=qid)
        UserAnswersMod.objects.create(
            user=user,
            question=question,
            answer_A=question.answer_A,
            answer_B=question.answer_B,
            answer_C=question.answer_C,
            answer_D=question.answer_D,
            answer=selected,
            comment=comment
        )
    except Exception as e:
        print(f"❌ Saqlashda xatolik: {e}")

def create_answer_keyboard(qid: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="A", callback_data=f"ans_{qid}_A"),
            InlineKeyboardButton(text="B", callback_data=f"ans_{qid}_B"),
            InlineKeyboardButton(text="C", callback_data=f"ans_{qid}_C"),
            InlineKeyboardButton(text="D", callback_data=f"ans_{qid}_D")
        ]
    ])

async def send_next_question(user_id: int, questions):
    index = user_question_progress.get(user_id, 0)
    if index < len(questions):
        q = questions[index]
        text = (
            f"❓ {q.question}\n"
            f"A) {q.answer_A}\n"
            f"B) {q.answer_B}\n"
            f"C) {q.answer_C}\n"
            f"D) {q.answer_D}"
        )
        await bot.send_message(chat_id=user_id, text=text, reply_markup=create_answer_keyboard(q.id))
    else:
        await bot.send_message(chat_id=user_id, text="✍️ Taklif yoki shikoyatingiz bo‘lsa, yozib qoldiring. Bo‘lmasa, '-' belgisi bilan yuboring:")
        user_question_progress[user_id] = "awaiting_comment"

async def send_daily_questions():
    users = await get_eligible_users()
    questions = await get_questions()
    for user in users:
        user_id = user.user_id
        user_question_progress[user_id] = 0
        await send_next_question(user_id, questions)
        user.quiz_sent_today = True
        await sync_to_async(user.save)()

@sync_to_async
def reset_daily_flags():
    UsersMod.objects.update(quiz_sent_today=False)

@dp.callback_query(lambda c: c.data.startswith("ans_"))
async def handle_answer(call: CallbackQuery):
    parts = call.data.split("_")
    qid = int(parts[1])
    selected = parts[2]
    user_id = call.from_user.id
    await save_answer_to_db(user_id, qid, selected)
    user_question_progress[user_id] += 1
    questions = await get_questions()
    await call.message.answer("✅ Javobingiz saqlandi.")
    await send_next_question(user_id, questions)

@user_private_router.message()
async def handle_comment(message: Message):
    user_id = message.from_user.id
    if user_question_progress.get(user_id) == "awaiting_comment":
        # Oxirgi javobni ORM orqali olish, lekin question bilan birga prefetch qilamiz
        last_answer = await sync_to_async(
            lambda: UserAnswersMod.objects.select_related("question").filter(user__user_id=user_id).order_by('-id').first()
        )()
        
        if last_answer:
            qid = last_answer.question_id  # 👈 bu to'g'ridan-to'g'ri integer
            await save_answer_to_db(user_id, qid=qid, selected="-", comment=message.text)
            await message.answer("✉️ Fikringiz uchun rahmat!")
        else:
            await message.answer("⚠️ Taklifni saqlab bo‘lmadi. Javob topilmadi.")
        
        user_question_progress.pop(user_id)

        # ✅ Mukofot tekshiruvi
        user = await sync_to_async(lambda: UsersMod.objects.get(user_id=user_id))()
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



# ✅ TEKSHIR
async def scheduler_loop():
    while True:
        print("⏱ Tekshiruv boshlandi...")
        await send_daily_questions()
        await asyncio.sleep(3600)

async def on_startup(bot):
    print("✅ Bot ishga tushdi.")

async def main():
    dp.startup.register(on_startup)
    asyncio.create_task(scheduler_loop())
    await dp.start_polling(bot)
