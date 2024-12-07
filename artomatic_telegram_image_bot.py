from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from together import Together
import base64
import logging

# Initialize Together client
client = Together()

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    update.message.reply_text(
        "Welcome! Send me a description, and I'll generate an image for you!"
    )

def generate_image(update: Update, context: CallbackContext) -> None:
    """Generate an image based on the user's prompt."""
    user_prompt = update.message.text

    if not user_prompt.strip():
        update.message.reply_text("Please provide a valid description.")
        return

    try:
        update.message.reply_text("Generating your image... Please wait.")

        # Call Together's API to generate an image
        response = client.images.generate(
            prompt=user_prompt,
            model="black-forest-labs/FLUX.1-schnell-Free",
            width=1024,
            height=768,
            steps=1,
            n=1,
            response_format="b64_json",
        )

        # Decode the base64 image response
        image_data = base64.b64decode(response.data[0].b64_json)

        # Save the image temporarily
        image_path = "generated_image.png"
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)

        # Send the image to the user
        update.message.reply_photo(photo=open(image_path, "rb"))

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        update.message.reply_text(
            "Sorry, I couldn't generate the image. Please try again later."
        )

def main():
    """Run the bot."""
    # Bot token from BotFather
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

    # Set up the Updater and Dispatcher
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Log all errors
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_image))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
