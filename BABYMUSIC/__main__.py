import asyncio
import importlib
import threading
from flask import Flask
import requests
import time

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BABYMUSIC import LOGGER, app, userbot
from BABYMUSIC.core.call import BABY
from BABYMUSIC.misc import sudo
from BABYMUSIC.plugins import ALL_MODULES
from BABYMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Flask app initialize kar rahe hain
flask_app = Flask(__name__)

# Health check endpoint for Koyeb
@flask_app.route('/health')
def health_check():
    return {"status": "healthy"}, 200

# Home route
@flask_app.route('/')
def home():
    return "Flask app running on port 8000"

# Flask app ko alag thread mein run karne ka function
def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

# Keep-alive function jo regular ping bhejta rahega
def keep_alive():
    while True:
        try:
            # Ping the health endpoint of the Flask app
            requests.get("http://0.0.0.0:8000/health")
        except Exception as e:
            print(f"Ping error: {e}")
        # Har 5 minute mein ping karein
        time.sleep(300)

async def init():
    if not config.STRING1:
        LOGGER(__name__).error("𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧")
        exit()

    await sudo()
    try:
        # Get banned users and add them to the BANNED_USERS list
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()

    # Import all plugins dynamically
    for all_module in ALL_MODULES:
        importlib.import_module("BABYMUSIC.plugins" + all_module)

    LOGGER("BABYMUSIC.plugins").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # Start userbot and BABY
    await userbot.start()
    await BABY.start()

    try:
        # Start streaming a media file
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error("𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗦𝗧𝗥𝗔𝗡𝗚𝗘𝗥 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........")
        exit()
    except:
        pass

    await BABY.decorators()

    LOGGER("BABYMUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗠𝗥 𝗦𝗛𝗜𝗩𝗔𝗡𝗦𝗛\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("𝗦𝗧𝗢𝗣 𝗦𝗧𝗥𝗔𝗡𝗚𝗘𝗥 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧..")

if __name__ == "__main__":
    # Start Flask and keep-alive in separate threads
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Ensure the Flask thread stops when the main program exits
    flask_thread.start()

    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.daemon = True  # Ensure the keep-alive thread stops when the main program exits
    keep_alive_thread.start()

    # Run the bot asynchronously
    asyncio.get_event_loop().run_until_complete(init())
