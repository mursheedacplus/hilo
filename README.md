# Bot Setup Guide

This README provides instructions for setting up the Bot environments. Follow the steps below to get started.

## Bot Setup

Replace 'YOUR_BOT_TOKEN' with the actual token you obtained from the BotFather when you created your Telegram bot. It typically looks like a long string of numbers and characters. In <A href="https://github.com/AaghaFazal/DDOS/blob/6b5154833e132db21014c6b061e5bdb52ea823c6/v1/alex.py#L8C14-L8C61">'alex.py Line 8'</a> and <A href="https://github.com/AaghaFazal/DDOS/blob/6b5154833e132db21014c6b061e5bdb52ea823c6/v1/bot.py#L10C24-L10C71">'bot.py Line 10'</a>

Replace with the actual Telegram user IDs of the users you want to designate as admins. These IDs are numeric and can be obtained using Bot like <A href="https://t.me/MissRose_bot">Rose</a> by /info on Telegram. In <A href="https://github.com/AaghaFazal/DDOS/blob/6b5154833e132db21014c6b061e5bdb52ea823c6/v1/bot.py#L13">bot.py Line 13</a> and <A href="https://github.com/AaghaFazal/DDOS/blob/6b5154833e132db21014c6b061e5bdb52ea823c6/v1/alex.py#L11C13-L11C23">alex.py Line 11</a>   

---

### Prerequisites

Ensure you have Python 3 and pip installed. You can check your Python version by running:
python3 --version

### Installation

1. Install Required Packages

                                        pip install telebot
   Installs the `telebot` library for creating Telegram bots using Python.
   
                                        pip install flask
   Installs `flask`, a lightweight web framework for Python, ideal for building web applications and APIs.

                                           pip install aiogram
   Installs `aiogram`, an asynchronous library for interacting with the Telegram Bot API, optimized for handling high message volumes.
   
                                              pip install pyTelegramBotAPI
   Installs the `pyTelegramBotAPI` library (also known as `telebot`), for creating and managing Telegram bots with Python.


2. Set Executable Permissions

   Ensure all files have the appropriate executable permissions:
   
                                        chmod +x *

3. Run the Bot

   Execute the main script to start the bot:
   
                                        python alex.py



## Bot Commands

### User Commands

- `/start` - Welcome message.
- `/help` - Display help information and available commands.
- `/ddos <target> <port> <time>` - Initiate a DDoS attack on the specified target.
- `/rules` - Display rules for using the bot.
- `/plan` - Display available plans and pricing.
- `/mylogs` - Show recent command logs for the user.


### Admin Commands

- `/add <userId>` - Add a user with a specified approval duration.
- `/remove <userId>` - Remove a user from the authorized list.
- `/allusers` - Display all authorized users.
- `/logs` - Display logs of all commands executed by users.
- `/clearlogs` - Clear the command logs.
- `/broadcast <message>` - Send a broadcast message to all authorized users.

## File Structure

- `bot.py` - Main bot script containing all functionalities.
- `users.txt` - File to store allowed user IDs.
- `log.txt` - File to store command logs.
- `alex.py` - Script to manage the bot.

## Logging

The bot logs details of each command executed by users, including user ID, command, target, port, and time. Logs are stored in the `log.txt` file.

## User Management

The bot supports adding and removing authorized users. Admins can view the list of all authorized users if needed.

## License

This project is licensed under the MIT License.

## Disclaimer

This bot is intended for educational purposes only. The misuse of this bot may result in legal consequences. The author is not responsible for any misuse of this bot.

---

**Note**: Replace `YOUR_BOT_TOKEN` and `YOUR_ADMIN_ID` with your actual bot token and admin user ID before running the bot. Ensure that you comply with all legal regulations and use this bot responsibly.

## Contributing

If you wish to contribute to this project, feel free to submit a pull request or open an issue on GitHub.

## Contact

For any queries or support, contact [Aagha Fazal](https://t.me/AaghaFazal) on Telegram. 

---


## Troubleshooting

- If you encounter any issues with the bot, ensure all dependencies are correctly installed and your Python version is compatible.


---

By following these instructions, you should be able to set up and run the Bot environments successfully. If you have any questions, please contact the repository maintainer.
