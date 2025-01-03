# Visual Prompt Bot

Visual Prompt is a Telegram bot that generates AI-based images from user input prompts. This bot leverages the power of AI to create unique images based on the text provided by users.

## Features

- **Start the Bot**: Use the `/start` command to initialize the bot and get a welcome message.
- **Generate Images**: Use the `/genim` command to generate an image based on your text prompt.
- **Help**: Use the `/help` command to get information on how to use the bot.

## Installation

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```


3. **Set up environment variables**:
    Create a `config.py` file in the root directory and add your Telegram Bot Token and Fusion Brain API keys:
    ```env
    TELEGRAM_BOT_TOKEN='your-telegram-bot-token'
    AI_KEY_1='your-deepai-api-key-1'
    AI_KEY_2='your-deepai-api-key-2'
    ```

## Usage

1. **Run the bot**:
    ```sh
    python main.py
    ```

2. **Interact with the bot on Telegram**:
    - **Start the bot**: Send `/start` to the bot to initialize and get a welcome message.
    - **Generate an image**: Send `/genim` to the bot, then provide a text prompt to generate an image.
    - **Help**: Send `/help` to get information on how to use the bot.

## File Structure

- : Contains configuration variables such as API keys.
- : Contains the  class for interacting with the AI service to generate images.
- : The main script that initializes the bot, sets up commands, and handles user interactions.
- : Contains the  class for managing user data in an SQLite database.

## Acknowledgements

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Fusion Brain API](https://fusionbrain.ai/)
