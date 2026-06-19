from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.service import create_task, get_tasks, complete_task, delete_task

router = Router()


# ================= STATES =================
class TaskState(StatesGroup):
    waiting_text = State()
    waiting_done = State()
    waiting_delete = State()


# ================= MAIN MENU =================
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить", callback_data="add")],
        [InlineKeyboardButton(text="📋 Список", callback_data="list")],
        [InlineKeyboardButton(text="✔ Выполнить", callback_data="done")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")]
    ])


# ================= START =================
@router.message(CommandStart())
async def start(msg: Message):
    await msg.answer("Выбери действие:", reply_markup=main_menu())


# ================= MENU HANDLERS =================
@router.callback_query(F.data == "add")
async def add_menu(call: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.waiting_text)
    await call.message.answer("Введите задачу")
    await call.answer()


@router.callback_query(F.data == "list")
async def list_tasks(call: CallbackQuery):
    data = await get_tasks()

    if not data:
        await call.message.answer("Задач нет")
        await call.answer()
        return

    text = "\n".join(
        f"{t.id}. {'[X]' if t.completed else '[ ]'} {t.text}"
        for t in data
    )

    await call.message.answer(text)
    await call.answer()


@router.callback_query(F.data == "done")
async def done_menu(call: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.waiting_done)
    await call.message.answer("Введите ID задачи для выполнения")
    await call.answer()


@router.callback_query(F.data == "delete")
async def delete_menu(call: CallbackQuery, state: FSMContext):
    await state.set_state(TaskState.waiting_delete)
    await call.message.answer("Введите ID задачи для удаления")
    await call.answer()


# ================= FSM INPUT =================
@router.message(TaskState.waiting_text)
async def save_task(msg: Message, state: FSMContext):
    await create_task(msg.text)
    await state.clear()
    await msg.answer("Задача добавлена", reply_markup=main_menu())


@router.message(TaskState.waiting_done)
async def do_done(msg: Message, state: FSMContext):
    try:
        task_id = int(msg.text)
    except ValueError:
        await msg.answer("Введите число")
        return

    ok = await complete_task(task_id)
    await state.clear()
    await msg.answer("Готово" if ok else "Не найдено", reply_markup=main_menu())


@router.message(TaskState.waiting_delete)
async def do_delete(msg: Message, state: FSMContext):
    try:
        task_id = int(msg.text)
    except ValueError:
        await msg.answer("Введите число")
        return

    ok = await delete_task(task_id)
    await state.clear()
    await msg.answer("Удалено" if ok else "Не найдено", reply_markup=main_menu())