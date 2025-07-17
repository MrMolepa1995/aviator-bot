from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Pattern detection logic
def analyze_data(multipliers):
    try:
        multipliers = [float(x) for x in multipliers]
    except ValueError:
        return "Invalid numbers. Please input like this: /data 1.25 2.10 1.05 35.33"

    last_five = multipliers[-5:]

    if all(x < 2.0 for x in last_five):
        return "🟢 Safe to Bet Soon! Detected 5+ low rounds."
    elif multipliers[-1] > 10.0:
        return "🔴 High spike just hit. Expect cooldown. Bet cautiously."
    elif any(x > 20.0 for x in multipliers[-10:]):
        return "🟡 Volatile pattern. Consider waiting 1-2 rounds."
    else:
        return "🟢 Normal round. Auto cashout around 2x is statistically safer."

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Aviator Predictor Bot!\nSend recent multipliers using /data command.")

# /data handler
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please send multipliers like this:\n`/data 1.25 2.65 3.15 1.05`", parse_mode='Markdown')
        return
    
    response = analyze_data(context.args)
    await update.message.reply_text(response)

# Run bot
if __name__ == "__main__":
    import os
    TOKEN = os.environ["7752613205:AAE1TIrEFZKhEtLkLQjmc_GCsugEQQz8Q3U"]  # Replace with your bot token
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("data", data))

    app.run_polling()
