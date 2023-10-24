# Anonymous Chat Bot

This project is an anonymous chat bot built with Python and Aiogram. The bot allows users to engage in anonymous conversations, providing a platform for open and secure communication. Users have the opportunity to create their own unique key and share it with others. With the help of such a key, this user can be contacted through an anonymous chat.

## Getting Started

These instructions will guide you on how to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed on your local system:

- Python 3.10 or higher with python in PATH required
- pip (The Python Package Installer)

### Installation

1. Clone the repository to your local machine using the following command:

```bash
git clone <repository_link>
```

2. Navigate to the project directory:

```bash
cd <project_directory>
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

1. Set up the bot token as an environment variable. The bot token is required for the bot to function properly. You can obtain a bot token from [BotFather](https://t.me/BotFather) on Telegram.

   - **Linux:** Open the terminal and enter the following command, replacing `<bot_token>` with your actual bot token:

     ```bash
     export BOT_TOKEN=<bot_token>
     ```

     To make the environment variable persistent, add the above command to your `~/.bashrc` file.

   - **Windows:** Open the command prompt and enter the following command, replacing `<bot_token>` with your actual bot token:

     ```bat
     setx BOT_TOKEN "<bot_token>"
     ```

     To make the environment variable persistent, use the following command instead:

     ```bat
     setx BOT_TOKEN "<bot_token>" /m
     ```

   - **Without using environment variables:** Open the `./bot/config.py` file and replace `<Your_Token_There>` to your `<bot_token>`:
    For example:
    ```py
    BOT_TOKEN = os.getenv("BOT_TOKEN", "<bot_token>")
    ```

2. Start the bot by running the following command in the project directory:

   ```bash
   python bot/main.py
   ```

3. To create a unique key, you need to click on the button with the corresponding text `🔐 Сгенерировать код подключения` in the chat bot. The bot will generate a unique key for you. You can change the maximum number of unique keys per user in the `./bot/config.py` file.

4. Users can share unique keys with other users who would like to contact them in the future.

5. To start an anonymous chat, click on the button with the corresponding text `🔎 Начать поиск` and the bot will start picking up a free random interlocutor for user.

6. If the user has a unique connection key, then he can click on the button with the text `🔓 Подключиться по ключу` and send this key to the bot. If the end user is free, then the bot will configure the connection between them.

6. Enjoy anonymous communication!

## Contributing

Contributions are welcome. Please feel free to fork the project, make changes, and submit a pull request.

## License

This project is free and unencumbered software released into the public domain. See the LICENSE file for details.
