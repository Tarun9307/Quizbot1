import asyncio
import re
from telethon import TelegramClient, events

# === Telegram API Credentials ===
API_ID = 28853790
API_HASH = 'c210bf562588336c29e98f8669d96ff7'
SESSION_NAME = 'session'

# === Target Group to Monitor ===
TARGET_GROUP = 'quiz007'  # Use only the group username (no @ or link)

# === Initialize Client ===
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# === Math Evaluator ===
def solve_question(text):
    if '?' not in text:
        return None

    # Find the part before the question mark (usually contains the math)
    before_q = text.split('?')[0]

    # Clean common suffix like '=', 'Answer:', etc.
    before_q = re.sub(r'=\s*$', '', before_q).strip()

    # Match only valid math expressions (digits and operators)
    if not re.fullmatch(r'[\d\s\+\-\*\/\.\(\)]+', before_q):
        return None

    try:
        return str(eval(before_q))
    except:
        return None

# === Message Handler ===
@client.on(events.NewMessage(chats=TARGET_GROUP))
async def handler(event):
    if '?' in event.raw_text:
        answer = solve_question(event.raw_text)
        if answer:
            await event.reply(answer)

# === Start Bot ===
async def main():
    await client.start()
    print("✅ Bot is running and watching for math questions...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())


