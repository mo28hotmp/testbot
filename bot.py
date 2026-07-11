import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

def get_gold_price():
    url = "https://data-asg.goldprice.org/dbXRates/USD"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Current gold price in USD per troy ounce
    price = data["items"][0]["xauPrice"]

    return f"${price:,.2f} USD per ounce"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello!\nType /gold to get the current gold price."
    )


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_gold_price()
        await update.message.reply_text(f"Current Gold Price:\n{price}")
    except Exception as e:
        await update.message.reply_text(f"Error:\n{e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
