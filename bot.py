import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

#gets this from the VPS
TOKEN = os.getenv("BOT_TOKEN")


# get per_usd Function

def get_prices_per_usd():

    url = "https://api.yadio.io/exrates/USD"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # Bitcoin price in USD
    btc = data["BTC"]

    # 1 USD = x EUR
    eur = 1/data["USD"]["EUR"]

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



# get per_toman Function
def get_prices_per_toman():

    url = "https://api.yadio.io/exrates/irt"


    #get data
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Bitcoin price in irt
    btc = data["BTC"]



    message = (
        "💰 Prices per Toman\n\n"
        f" هر بیت کوین = {btc/1000000000:,.3f} میلیارد تومن  \n"
    )

    return message


# get all_prices Function
def get_all_prices():
    message= ( get_prices_per_toman() + "\n" + get_prices_per_usd() )

    return message



# /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Available commands:\n"
        "/prices_per_usd \n"
        "/prices_per_toman \n"
        "/all_prices \n"
    )

# /prices_per_usd Command

async def prices_per_usd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_prices_per_usd()

        await update.message.reply_text(
            f"Current Bitcoin Price:\n{price}"
        )

    except Exception as e:
     print(e)
     await update.message.reply_text(f"Error:\n{e}")


# /prices_per_toman Command

async def prices_per_toman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_prices_per_toman()

        await update.message.reply_text(
            f"Current Bitcoin Price:\n{price}"
        )

    except Exception as e:
     print(e)
     await update.message.reply_text(f"Error:\n{e}")



# /all_prices Command
async def all_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_all_prices()

        await update.message.reply_text(
            f"Current Price:\n\n{price}"
        )

    except Exception as e:
     print(e)
     await update.message.reply_text(f"Error:\n{e}")





def main():
    app = Application.builder().token(TOKEN).build()


# defining bot Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices_per_usd", prices_per_usd))
    app.add_handler(CommandHandler("prices_per_toman", prices_per_toman))
    app.add_handler(CommandHandler("all_prices", all_prices))
    
    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
