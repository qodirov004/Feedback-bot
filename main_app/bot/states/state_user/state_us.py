from aiogram.fsm.state import StatesGroup,State

class Form(StatesGroup):
    full_name = State()
    direction = State()
    teacher = State()
    group = State()
    day_type = State()
    start_time = State()
    confirmation = State()
    reward = State()