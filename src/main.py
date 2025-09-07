import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from src.config import settings
from src.handlers.error import router as error_router
from src.handlers.message import router as message_router


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    bot = Bot(
        token=settings.BOT_TOKEN,
        # default=DefaultBotProperties(parse_mode=None),
        default=DefaultBotProperties(parse_mode=None),
        # default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V),
    )
    dispatcher = Dispatcher()

    dispatcher.include_router(message_router)
    dispatcher.include_router(error_router)

    commands = [
        BotCommand(command="start", description="Начать сначала"),
    ]
    await bot.set_my_commands(commands)

    # Start the background worker
    # worker_task = asyncio.create_task(process_generation_tasks(bot, session_pool))

    # await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_webhook(drop_pending_updates=False)
    print("Started")
    try:
        await dispatcher.start_polling(bot)
    finally:
        ...

        # worker_task.cancel()
        # try:
        #     await worker_task
        # except asyncio.CancelledError:
        # logging.info("Worker task cancelled.")


if __name__ == "__main__":
    asyncio.run(main())
