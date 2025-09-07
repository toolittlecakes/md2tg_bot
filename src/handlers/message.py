import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from telegramify_markdown import customize, markdownify

from src.lexicon import Lexicon

logger = logging.getLogger(__name__)
router = Router()

customize.get_runtime_config().cite_expandable = False
customize.get_runtime_config()._markdown_symbol.task_uncompleted = "◻"
customize.get_runtime_config()._markdown_symbol.task_completed = "✔"

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(markdownify(Lexicon.START_MESSAGE), parse_mode=ParseMode.MARKDOWN_V2)

@router.message()
async def message_handler(message: Message):

    await message.answer(markdownify(message.md_text or ""), parse_mode=ParseMode.MARKDOWN_V2)
