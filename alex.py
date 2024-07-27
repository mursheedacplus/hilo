import subprocess
import time
import logging
from aiogram import Bot
import asyncio

# insert your Telegram bot token here
API_TOKEN = '7018282415:AAGCpqMdkoZsg6KCTWdAwH4tYjTO_6fVbb4'

# Admin user ID
ADMIN_ID = '-1002177030613'
MAX_RESTARTS = 6
RESTART_PERIOD = 60  # Seconds

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
bot = Bot(API_TOKEN)

def start_bot():
    """Start the bot script as a subprocess."""
    return subprocess.Popen(['python', 'bot.py'])

async def notify_admin(message):
    """Send a notification message to the admin via Telegram."""
    try:
        await bot.send_message(ADMIN_ID, message)
        logging.info("Admin notified: %s", message)
    except Exception as e:
        logging.error("Failed to send message to admin: %s", e)

async def main():
    """Main function to manage bot process lifecycle."""
    restart_count = 0
    last_restart_time = time.time()
    
    while True:
        if restart_count >= MAX_RESTARTS:
            current_time = time.time()
            if current_time - last_restart_time < RESTART_PERIOD:
                wait_time = RESTART_PERIOD - (current_time - last_restart_time)
                logging.warning("Maximum restart limit reached. Waiting for %.2f seconds...", wait_time)
                await notify_admin(f"⚠️ 𝙼𝚊𝚡𝚒𝚖𝚞𝚖 𝚛𝚎𝚜𝚝𝚊𝚛𝚝 𝚕𝚒𝚖𝚒𝚝 𝚛𝚎𝚊𝚌𝚑𝚎𝚍. 𝚆𝚊𝚒𝚝𝚒𝚗𝚐 𝚏𝚘𝚛 {int(wait_time)} 𝚜𝚎𝚌𝚘𝚗𝚍𝚜 𝚋𝚎𝚏𝚘𝚛𝚎 𝚛𝚎𝚝𝚛𝚢𝚒𝚗𝚐.")
                await asyncio.sleep(wait_time)
            restart_count = 0
            last_restart_time = time.time()

        logging.info("Starting the bot...")
        process = start_bot()
        await notify_admin("🚀 𝚃𝚑𝚎 𝚋𝚘𝚝 𝚒𝚜 𝚜𝚝𝚊𝚛𝚝𝚒𝚗𝚐...")

        while process.poll() is None:
            await asyncio.sleep(5)
        
        logging.warning("Bot process terminated. Restarting in 10 seconds...")
        await notify_admin("⚠️ 𝚃𝚑𝚎 𝚋𝚘𝚝 𝚑𝚊𝚜 𝚌𝚛𝚊𝚜𝚑𝚎𝚍 𝚊𝚗𝚍 𝚠𝚒𝚕𝚕 𝚛𝚎𝚜𝚝𝚊𝚛𝚝 𝚒𝚗 𝟷𝟶 𝚜𝚎𝚌𝚘𝚗𝚍𝚜.")
        restart_count += 1
        await asyncio.sleep(10)
        

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
