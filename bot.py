import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

#gets this from the VPS
TOKEN = os.getenv("BOT_TOKEN")


def get_prices_per_usd():

    url = "https://api.yadio.io/exrates/USD"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # Bitcoin price in USD
    btc = data["BTC"]

    # 1 USD = x EUR
    eur = data["USD"]["EUR"]

    # Gold (XAU)
    # Yadio gives ounces per USD, so invert it
    gold = 1 / data["USD"]["XAU"]

    message = (
        "💰 Prices per USD\n\n"
        f"₿ BTC : ${btc:,.2f}\n"
        f"🇪🇺 EUR : {eur:.4f}\n"
        f"🥇 Gold : ${gold:,.2f}/oz"
    )

    return message


def get_prices_per_toman():

    url = "https://api.yadio.io/exrates/IRT"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # Bitcoin price in irt
    btc = data["BTC"]

    # Gold (XAU)
    # Yadio gives ounces per USD, so invert it
    gold = 1 / data["irt"]["XAU"]

    message = (
        "💰 Prices per USD\n\n"
        f"₿ BTC : ${btc:,.2f}\n"
        f"🥇 Gold : ${gold:,.2f}/oz"
    )

    return message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Available commands:\n"
        "/prices_per_usd - Current Bitcoin price\n"
        "/prices_per_toman - btc - eth - paxg - bnb"
    )


async def prices_per_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_prices_per_usd()

        await update.message.reply_text(
            f"Current Bitcoin Price:\n{price}"
        )

    except Exception as e:
     print(e)
     await update.message.reply_text(f"Error:\n{e}")

async def prices_per_toman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prices = get_prices_per_toman()

        await update.message.reply_text(prices)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices_per_usd", prices_per_toman))
    app.add_handler(CommandHandler("prices_per_toman", prices_per_toman))
    
    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
