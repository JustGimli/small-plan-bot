from aiogram.dispatcher.filters.state import StatesGroup, State


class FSM(StatesGroup):
    plan = State()
