import io
import logging

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import BufferedInputFile, Message
from telegramify_markdown import (
    ContentTypes,
    File,
    Photo,
    Text,
    customize,
    markdownify,
    telegramify,
)

from src.lexicon import Lexicon

logger = logging.getLogger(__name__)
router = Router()

customize.get_runtime_config().cite_expandable = False
customize.get_runtime_config()._markdown_symbol.task_uncompleted = "◻"
customize.get_runtime_config()._markdown_symbol.task_completed = "✔"


def _extract_full_pre_entity_text(message: Message) -> str | None:
    """Return text if the entire message is a single PRE/CODE entity.

    Uses aiogram's parsed entities which already account for UTF-16 offsets.
    Accepts both 'pre' (multiline code block) and 'code' (inline) covering the full text.
    """
    if not message.text:
        return None
    entities = message.entities or []
    code_entities = [e for e in entities if e.type in ("pre", "code")]
    if len(code_entities) != 1:
        return None
    entity = code_entities[0]
    extracted = entity.extract_from(message.text)
    if entity.offset == 0 and extracted == message.text:
        return extracted
    return None


async def _send_telegramified_messages(message: Message, markdown_content: str) -> None:
    """Send a list of telegramified messages to the user."""
    telegram_content = markdownify(markdown_content)
    print(telegram_content)
    await message.answer(telegram_content, parse_mode=ParseMode.MARKDOWN_V2)


async def _handle_markdown_processing_error(
    message: Message, error: Exception, context: str
) -> None:
    """Handle errors that occur during markdown processing."""
    logger.error(f"Error processing {context}: {error}")
    await message.answer(
        markdownify(
            "❌ Произошла ошибка при обработке. Убедитесь, что содержимое корректно в кодировке UTF-8."
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        markdownify(Lexicon.START_MESSAGE), parse_mode=ParseMode.MARKDOWN_V2
    )


@router.message(F.document)
async def document_handler(message: Message):
    """Handle uploaded markdown files"""
    document = message.document
    if not document:
        return

    # Check if the file is a markdown file
    if not document.file_name or not document.file_name.lower().endswith(
        (".md", ".markdown", ".txt")
    ):
        await message.answer(
            markdownify(
                "❌ Пожалуйста, загрузите файл с расширением .md, .markdown или .txt"
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    # Download the file
    bot = message.bot
    if not bot:
        return

    file_info = await bot.get_file(document.file_id)
    if not file_info.file_path:
        await message.answer(
            markdownify("❌ Не удалось получить информацию о файле"),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    # Create a temporary file to store the downloaded content
    io_bytes = await bot.download_file(file_info.file_path)
    if not io_bytes:
        return

    # Read the markdown content
    with io_bytes as file:
        markdown_content = file.read().decode("utf-8")

    if not markdown_content.strip():
        await message.answer(
            markdownify("❌ Файл пустой или не содержит текста"),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    # Convert markdown to Telegram format
    await _send_telegramified_messages(message, markdown_content)

    logger.info(f"Successfully processed markdown file: {document.file_name}")


@router.message(F.text)
async def codeblock_text_handler(message: Message):
    """Handle text messages that are a single code entity by processing
    the inner content as markdown (same flow as file uploads)."""
    inner_markdown = _extract_full_pre_entity_text(message)
    if inner_markdown is None:
        await message.answer(
            markdownify(Lexicon.UNSUPPORTED_MESSAGE), parse_mode=ParseMode.MARKDOWN_V2
        )
        return

    await _send_telegramified_messages(message, inner_markdown)
    logger.info("Successfully processed markdown from code entity text message")
