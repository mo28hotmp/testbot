import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

#gets this from the VPS
TOKEN = os.getenv("BOT_TOKEN")


def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    price = data["bitcoin"]["usd"]

    return f"${price:,.2f} USD"


def get_biggies_price():
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,pax-gold,binancecoin"
        "&vs_currencies=usd"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    btc = data["bitcoin"]["usd"]
    eth = data["ethereum"]["usd"]
    paxg = data["pax-gold"]["usd"]
    bnb = data["binancecoin"]["usd"]

    message = (
        "🪙 Biggies Price\n\n"
        f"₿ BTC: ${btc:,.2f}\n"
        f"Ξ ETH: ${eth:,.2f}\n"
        f"🟡 PAXG: ${paxg:,.2f}\n"
        f"🔶 BNB: ${bnb:,.2f}"
    )

    return message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Available commands:\n"
        "/btc - Current Bitcoin price"
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
