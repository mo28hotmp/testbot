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

    message = (
        "💰 Prices per USD\n\n"
        f"₿ BTC: ${data['BTC']:,.2f}\n"
        f"Ξ ETH: ${data['ETH']:,.2f}\n"
        f"🟡 PAXG: ${data['PAXG']:,.2f}\n"
        f"🔶 BNB: ${data['BNB']:,.2f}"
    )

    return message


def get_prices_per_toman():

    url = "https://api.yadio.io/exrates/irt"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    
    message = (
        "💰 Prices per toman\n\n"
        f"$ USD: T{data['USD']:,.2f}\n"
        f"₿ BTC: T{data['BTC']:,.2f}\n"
        f"Ξ ETH: T{data['ETH']:,.2f}\n"
        f"🟡 PAXG: T{data['PAXG']:,.2f}\n"
        f"🔶 BNB: T{data['BNB']:,.2f}"
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
