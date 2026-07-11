import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

#gets this from the VPS
TOKEN = os.getenv("BOT_TOKEN")



def prices_per_usd():
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


def prices_per_toman():
    coins = {
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
        "🪙 Biggies Price\n\n"
        f"₿ BTC: ${prices['BTC']:,.2f}\n"
        f"Ξ ETH: ${prices['ETH']:,.2f}\n"
        f"🟡 PAXG: ${prices['PAXG']:,.2f}\n"
        f"🔶 BNB: ${prices['BNB']:,.2f}"
    )

    return message
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Available commands:\n"
        "/btc - Current Bitcoin price\n"
        "/biggiesprice - btc - eth - paxg - bnb"
    )


async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_btc_price()

        await update.message.reply_text(
            f"Current Bitcoin Price:\n{price}"
        )

    except Exception as e:
     print(e)
     await update.message.reply_text(f"Error:\n{e}")

async def biggies_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prices = get_biggies_price()

        await update.message.reply_text(prices)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("biggiesPrice", biggies_price))
    
    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
