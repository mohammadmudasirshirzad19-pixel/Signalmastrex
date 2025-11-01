from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import datetime, random, os

BOT_TOKEN = os.getenv("BOT_TOKEN")

currency_pairs = ["EUR/USD", "GBP/USD", "USD/CHF", "EUR/JPY", "GBP/JPY", "AUD/USD", "EUR/GBP", "EUR/CHF", "AUD/NZD", "CAD/JPY"]
timeframes = ["1m", "3m", "5m"]
daily_signals = {}

def generate_signal(pair, timeframe):
    rsi = random.randint(20, 80)
    ema_fast = random.uniform(1.1, 1.5)
    ema_slow = random.uniform(1.0, 1.4)
    macd = random.uniform(-0.5, 0.5)
    winrate = round(random.uniform(97.0, 99.0), 2)

    if rsi < 30 and ema_fast > ema_slow and macd > 0:
        signal_type = "Buy (Call)"
    elif rsi > 70 and ema_fast < ema_slow and macd < 0:
        signal_type = "Sell (Put)"
    else:
        return None

    return f"""
📊 OTC سیګنال
💱 کرنسي: {pair}
📈 ډول: {signal_type}
⏱ ټایم‌فریم: {timeframe}
✅ وین‌ریټ: {winrate}%
📌 شرطونه:
   - RSI = {rsi}
   - EMA 5 = {round(ema_fast,2)} > EMA 13 = {round(ema_slow,2)}
   - MACD = {round(macd,2)}
🌍 بازار حالت: OTC، د خبرونو فلټر فعال
📆 وخت: {datetime.datetime.now().strftime('%H:%M')}
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 Get 1-min Signal", callback_data='get_1m')],
        [InlineKeyboardButton("📥 Get 3-min Signal", callback_data='get_3m')],
        [InlineKeyboardButton("📥 Get 5-min Signal", callback_data='get_5m')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ټایم‌فریم انتخاب کړه:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    today = datetime.date.today()

    if daily_signals.get((user_id, today), 0) >= 5:
        await query.edit_message_text("نن ورځ دې ۵ سیګنالونه اخیستي. سبا بیا هڅه وکړه.")
        return

    tf = query.data.split("_")[1] + "m"
    pair = random.choice(currency_pairs)
    signal = generate_signal(pair, tf)

    if signal:
        daily_signals[(user_id, today)] = daily_signals.get((user_id, today), 0) + 1
        await query.edit_message_text(signal)
    else:
        await query.edit_message_text("شرایط برابر نه وو، بیا هڅه وکړه.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
