class Lexicon:
    START_MESSAGE = """
🤖 **Telegram Markdown Converter Bot**

Загрузите файл в формате markdown (расширение .md, .markdown или .txt), и я конвертирую его в формат, поддерживаемый Telegram.

📎 **Как использовать:**
1. Прикрепите файл с markdown-разметкой
2. Получите готовый текст для Telegram

⚠️ **Поддерживаемые форматы:** .md, .markdown, .txt
""".strip()

    UNSUPPORTED_MESSAGE = """
❌ **Неподдерживаемый тип сообщения**

Пожалуйста, загрузите файл с markdown-разметкой (расширение .md, .markdown или .txt).

Текстовые сообщения не поддерживаются, так как Telegram автоматически конвертирует некоторые элементы markdown.
""".strip()
