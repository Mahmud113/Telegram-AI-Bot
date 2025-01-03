# Importing necessary libraries
from telebot import TeleBot  # For creating the Telegram bot
from telebot import types  # For defining bot commands and message types
from logic import Text2ImageAPI  # Custom module for handling AI-based text-to-image generation
from user_manager import *  # Custom module for managing user data
from config import *

# Importing additional libraries
import base64  # For encoding and decoding images in Base64 format
from PIL import Image  # For working with images
from io import BytesIO  # For handling byte streams
import time  # For adding delays

# Tokens
# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# AI_KEY_1 = os.getenv("AI_KEY_1")
# AI_KEY_2 = os.getenv("AI_KEY_2")
DATABASE = 'users.db'

# Initializing the Telegram bot with the token
bot = TeleBot(str(TELEGRAM_BOT_TOKEN))

# Setting bot commands
c1 = types.BotCommand(command='start', description='Start the Bot')  # Command to start the bot
c2 = types.BotCommand(command='genim', description='Generate an image')  # Command to generate an image
bot.set_my_commands([c1, c2])  # Setting these commands for the bot

# Handler for '/start' and '/help' commands
@bot.message_handler(commands=['help', 'start'])
def start_command(message):
    # Check if the user exists in the database
    users = user_manager.get_users_telegram_id()  # Retrieve all users' Telegram IDs
    users_id = message.from_user.id  # Get the ID of the current user

    # If the user is not found, add them to the database
    for i in users:
        if i[0] == users_id:
            break
    else:
        user_manager.add_user(users_id, message.from_user.username)

    # Sending a welcome/help message
    bot.send_chat_action(message.chat.id, 'typing')  # Indicating typing action
    time.sleep(0.5)  # Small delay
    bot.send_message(
        message.chat.id,
        '''I am a bot that generates images with the help of strong AI. To try my power on your own:
        
/genim - after executing this command, enter your prompt and wait.🧠
/help - if you need to remember my purpose.🙄'''
    )

# Handler for '/genim' command
@bot.message_handler(commands=['genim'])
def generate_image(message):
    # Prompt user for input to generate an image
    bot.send_chat_action(message.chat.id, 'typing')  # Indicating typing action
    time.sleep(0.5)  # Small delay
    bot.send_message(message.chat.id, 'Send your prompt:')  # Ask for the user's prompt
    bot.register_next_step_handler(message, generation_with_prompt)  # Connect to the next step

# Function to handle image generation based on user prompt
def generation_with_prompt(message):
    global api  # Using the global `api` object
    prompt_text = message.text  # Extract the user's prompt
    user_id = message.chat.id  # Get the user's chat ID

    # Informing the user about the generation process
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'Generating an image...')
    bot.send_chat_action(message.chat.id, 'typing')

    # Generating the image using AI
    model_id = api.get_model()  # Get the model ID for the AI
    uuid = api.generate(prompt_text, model_id)  # Generate the image and get its UUID
    images = api.check_generation(uuid)[0]  # Retrieve the Base64-encoded image

    # Decoding the Base64-encoded image
    decoded_data = base64.b64decode(images)  # Decode the image
    image = Image.open(BytesIO(decoded_data))  # Convert the image data to a PIL Image object

    # Sending the generated image to the user
    bot.delete_message(message.chat.id, message.message_id + 1)  # Delete the "Generating an image..." message
    bot.send_photo(user_id, image)  # Send the image to the user

# Main execution block
if __name__ == '__main__':
    # Initialize the AI and user manager objects
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', AI_KEY_1, AI_KEY_2)  # Connect to the AI service
    user_manager = User_manager(DATABASE)  # Initialize the user manager with the database

    # Start polling for messages indefinitely
    bot.infinity_polling()