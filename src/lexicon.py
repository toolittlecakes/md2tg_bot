class Lexicon:
    START_MESSAGE = """
🤖 **Telegram Markdown Converter Bot**

Загрузите файл в формате markdown (расширение .md, .markdown или .txt), и я конвертирую его в Telegram сообщение. Также можно отправлять текст в формате кода:

```
# Header
**bold** *italic* ~~strikethrough~~ ||spoiler||
[link](https://www.google.com)
- [ ] Uncompleted task list item
- [x] Completed task list item
> Quote
```
⬇️⬇️⬇️

📌 Header
**bold** *italic* ~~strikethrough~~ ||spoiler||
[link](https://www.google.com)
◻ Uncompleted task list item
✔ Completed task list item
>Quote
""".strip()

    UNSUPPORTED_MESSAGE = """
❌ **Неподдерживаемый тип сообщения**

Пожалуйста, либо загрузите файл с markdown-разметкой (расширение .md, .markdown или .txt), либо отправьте текст в формате кода:
```
Вот **так** можно
```
""".strip()
