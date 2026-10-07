import os
import random
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

DB = "obingo.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def register_user(user):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO users
        (telegram_id, username, first_name)
        VALUES (?, ?, ?)
    """, (
        user.id,
        user.username,
        user.first_name
    ))

    conn.commit()
    conn.close()


def make_menu():
    keyboard = [
        [
            InlineKeyboardButton("🎱 Play Bingo", callback_data="play"),
            InlineKeyboardButton("🎟 My Cards", callback_data="cards")
        ],
        [
            InlineKeyboardButton("🏆 Winners", callback_data="winners"),
            InlineKeyboardButton("📜 History", callback_data="history")
        ],
        [
            InlineKeyboardButton("ℹ️ How to Play", callback_data="help"),
            InlineKeyboardButton("☎️ Support", callback_data="support")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    register_user(user)

    text = (
        "🎱 *WELCOME TO OBINGO!*\n\n"
        "Your Telegram Bingo platform.\n\n"
        "🎟 Planned card price: *5 ETB*\n\n"
        "⚠️ This is currently a DEMO version. "
        "No real-money payments are accepted.\n\n"
        "Choose an option below:"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=make_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "play":
        await query.edit_message_text(
            "🎱 *BINGO*\n\n"
            "Game #1001\n"
            "🎟 Card price: 5 ETB\n\n"
            "This is currently a demo game.\n\n"
            "Real-money play is disabled.",
            parse_mode="Markdown"
        )

    elif query.data == "cards":
        await query.edit_message_text(
            "🎟 *MY CARDS*\n\n"
            "You don't have any cards yet.\n\n"
            "Demo card purchasing will be added next.",
            parse_mode="Markdown"
        )

    elif query.data == "winners":
        await query.edit_message_text(
            "🏆 *WINNERS*\n\n"
            "No winners yet.",
            parse_mode="Markdown"
        )

    elif query.data == "history":
        await query.edit_message_text(
            "📜 *GAME HISTORY*\n\n"
            "No games completed yet.",
            parse_mode="Markdown"
        )

    elif query.data == "help":
        await query.edit_message_text(
            "ℹ️ *HOW TO PLAY*\n\n"
            "1. Register your Telegram account.\n"
            "2. Join an available Bingo game.\n"
            "3. Receive your Bingo card.\n"
            "4. Watch the numbers being called.\n"
            "5. The system automatically checks Bingo.\n\n"
            "This version is currently a demo.",
            parse_mode="Markdown"
        )

    elif query.data == "support":
        await query.edit_message_text(
            "☎️ *SUPPORT*\n\n"
            "Contact the OBingo administrator.",
            parse_mode="Markdown"
        )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    init_db()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))

    print("OBingo is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
