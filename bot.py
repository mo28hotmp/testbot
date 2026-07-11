import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

#gets this from the VPS
TOKEN = os.getenv("BOT_TOKEN")


def get_prices_per_usd():
    coins = {
        "BTC": "Bitcoin",
        "ETH": "Ethereum",
        "PAXG": "PAX Gold",
        "BNB": "BNB"
    }

    prices = {}

    for symbol in coins:
        url = f"https://api.yadio.io/rate/{symbol}/USD"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        prices[symbol] = data["rate"]

    message = (
        "🪙 Biggies Price\n\n"
        f"₿ BTC: ${prices['BTC']:,.2f}\n"
        f"Ξ ETH: ${prices['ETH']:,.2f}\n"
        f"🟡 PAXG: ${prices['PAXG']:,.2f}\n"
        f"🔶 BNB: ${prices['BNB']:,.2f}"
    )

    return message


def get_prices_per_toman():
    coins = {
        "USD": "Dollar",
        "BTC": "Bitcoin",
        "ETH": "Ethereum",
        "PAXG": "PAX Gold",
        "BNB": "BNB"
    }

    prices = {}

    for symbol in coins:
        url = f"https://api.yadio.io/rate/{symbol}/IRT"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        prices[symbol] = data["rate"]

    message = (
        "🪙 Prices per Toman\n\n"
        f"$ USD: T{prices['BTC']:,.2f}\n"
        f"₿ BTC: T{prices['BTC']:,.2f}\n"
        f"Ξ ETH: T{prices['ETH']:,.2f}\n"
        f"🟡 PAXG: T{prices['PAXG']:,.2f}\n"
        f"🔶 BNB: T{prices['BNB']:,.2f}"
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
    app.add_handler(CommandHandler("prices_per_usd", btc))
    app.add_handler(CommandHandler("prices_per_toman", biggies_price))
    
    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
