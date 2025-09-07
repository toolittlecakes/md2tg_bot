import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from telegramify_markdown import markdownify

logger = logging.getLogger(__name__)
router = Router()



@router.errors()
async def unknown_error_handler(event: ErrorEvent):
    logger.exception(f"Unhandled exception caught in error handler: {event.exception}")
    if event.update.message:
        await event.update.message.answer(markdownify(f"Error occurred: {event.exception}"), parse_mode=ParseMode.MARKDOWN_V2)
