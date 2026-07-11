import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

#gets this from the VPS
TOKEN = os.getenv("BOT_TOKEN")


def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    response = requests.get(url)

    # If something goes wrong, raise an error
    response.raise_for_status()

    data = response.json()

    price = float(data["price"])

    return f"${price:,.2f} USD"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Available commands:\n"
        "/btc - Current Bitcoin price"
    )


async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_btc_price()

        await update.message.reply_text(
            f"🪙 Current Bitcoin Price:\n{price}"
        )

   except Exception as e:
    print(e)
    await update.message.reply_text(f"❌ Error:\n{e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
