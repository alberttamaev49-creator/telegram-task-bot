from app.database import async_session
from app.models import Task
from sqlalchemy import select


async def create_task(text: str):
    async with async_session() as session:
        task = Task(text=text)
        session.add(task)
        await session.commit()


async def get_tasks():
    async with async_session() as session:
        result = await session.execute(select(Task))
        return result.scalars().all()


async def complete_task(task_id: int):
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            return False

        task.completed = True
        await session.commit()
        return True


async def delete_task(task_id: int):
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task:
            return False

        await session.delete(task)
        await session.commit()
        return True