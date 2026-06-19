from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.service import create_task, get_tasks, complete_task, delete_task

router = Router()


class TaskState(StatesGroup):
    waiting_text = State()
    waiting_done = State()
    waiting_delete = State()


@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "/add - добавить задачу\n"
        "/tasks - список задач\n"
        "/done - выполнить задачу\n"
        "/delete - удалить задачу"
    )


@router.message(Command("add"))
async def add(msg: Message, state: FSMContext):
    await state.set_state(TaskState.waiting_text)
    await msg.answer("Введите задачу")


@router.message(TaskState.waiting_text)
async def save(msg: Message, state: FSMContext):
    await create_task(msg.text)
    await state.clear()
    await msg.answer("Задача добавлена")


@router.message(Command("tasks"))
async def tasks(msg: Message):
    data = await get_tasks()

    if not data:
        await msg.answer("Задач нет")
        return

    await msg.answer(
        "\n".join(
            f"{t.id}. {'[X]' if t.completed else '[ ]'} {t.text}"
            for t in data
        )
    )


@router.message(Command("done"))
async def done(msg: Message, state: FSMContext):
    await state.set_state(TaskState.waiting_done)
    await msg.answer("Введите ID")


@router.message(TaskState.waiting_done)
async def done_save(msg: Message, state: FSMContext):
    try:
        task_id = int(msg.text)
    except ValueError:
        await msg.answer("Введите число (ID)")
        return

    ok = await complete_task(task_id)
    await state.clear()
    await msg.answer("Готово" if ok else "Не найдено")


@router.message(Command("delete"))
async def delete(msg: Message, state: FSMContext):
    await state.set_state(TaskState.waiting_delete)
    await msg.answer("Введите ID")


@router.message(TaskState.waiting_delete)
async def delete_save(msg: Message, state: FSMContext):
    try:
        task_id = int(msg.text)
    except ValueError:
        await msg.answer("Введите число (ID)")
        return

    ok = await delete_task(task_id)
    await state.clear()
    await msg.answer("Удалено" if ok else "Не найдено")