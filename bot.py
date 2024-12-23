from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ChatJoinRequestHandler
import google.generativeai as genai

# Configure Google Gemini
genai.configure(api_key="upload_your_geminiapikey_here")
model = genai.GenerativeModel("gemini-1.5-flash")

# Handle /start command
async def start_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text="Hello! I am your assistant bot. Add me to a group, and I'll welcome new members!"
    )
    print(f"Sent /start response to {chat_id}")

# Handle any message with Gemini API response
async def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    # Generate a response using Gemini
    try:
        response = model.generate_content(user_message)
        reply_text = response.text or "Hmm, I don't have a response for that right now!"
    except Exception as e:
        print(f"Gemini API error: {e}")
        reply_text = "Sorry, I couldn't understand that. Can you try again?"

    # Respond with a girlfriend-like tone
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Hey, {update.effective_user.first_name} ❤️\n{reply_text}"
    )
    print(f"Responded to {chat_id} with: {reply_text}")

# Handle join request: Approve and send a private message
async def handle_join_request(update: Update, context: CallbackContext):
    user = update.chat_join_request.from_user  # User info
    chat_id = update.chat_join_request.chat.id  # Channel ID

    # Approve the join request
    await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user.id)
    print(f"Approved join request for {user.full_name} ({user.id})")

    # Welcome message
    welcome_message = (
        f"Hello {user.full_name}! 👋\n"
        "Welcome to the channel. We're glad to have you here!\n\n"
        
        " Join our Channel @DARKTEAM_69 ✅\n\n"
         "Let's learn together 🤗"
    )

    # Send a private message to the user
    try:
        await context.bot.send_message(chat_id=user.id, text=welcome_message)
        print(f"Message sent to {user.full_name} ({user.id})")
    except Exception as e:
        print(f"Failed to send message to {user.full_name} ({user.id}): {e}")

# Main function to initialize the bot
def main():
    # Your bot token
    BOT_TOKEN = "upload_your_bot_token_here"

    # Initialize the application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command handler for /start
    app.add_handler(CommandHandler("start", start_command))

    # Add a general message handler for other texts
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add a handler for join requests
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    