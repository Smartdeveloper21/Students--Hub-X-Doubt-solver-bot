import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# CONFIGURE THESE WITH YOUR REAL DATA
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

openai.api_key = OPENAI_API_KEY

async def get_concise_answer(user_question: str) -> str:
    prompt = f"Answer the following question clearly and concisely, in 2-3 sentences:\n{user_question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[ {"role": "user", "content": prompt} ],
        max_tokens=100,
        temperature=0.5
    )
    return response.choices[0].message["content"].strip()

async def doubt_solver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if msg.startswith('/que') or '@doubt' in msg.lower():
        if msg.startswith('/que'):
            question = msg[len('/que'):].strip()
        else:
            question = msg.replace('@doubt', '').strip()
        if question:
            answer = await get_concise_answer(question)
            await update.message.reply_text(answer)
        else:
            await update.message.reply_text("Please provide a question after the command.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    handler = MessageHandler(filters.TEXT, doubt_solver)
    app.add_handler(handler)
    app.run_polling()
