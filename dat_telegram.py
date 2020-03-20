from bot_config import TELECRAM_CLIENT_WHITE_LIST


def check_telegram_client(prm_chat_id, prm_update):
    if not prm_chat_id in TELECRAM_CLIENT_WHITE_LIST:
        print('''sorry it's private bot''')
        prm_update.message.reply_text('''sorry it's private bot''')
        return False
    else:
        return True
