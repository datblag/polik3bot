from telegram.ext import Updater, CommandHandler, MessageHandler
from bot_config import BOT_TOKEN, REQUEST_KWARGS, QSYSTEM_ADDRESS, TELEGRAM_GLPI_LIST
import socket
from requests import post, get, put, delete
import json
from dat_telegram import check_telegram_client
from qsystem import terminal_lock, terminal_reset, terminal_unlock, talon


def hello_world(update,  context):
    if check_telegram_client(update['message']['chat']['id'], update):
        print('hi. i work')
        update.message.reply_text('hi. i work')


def error(update, context):
    """Log Errors caused by Updates."""
    print('error')
    print(update)
    print(context.error)


def handle_text(update, context):
    cur_chat = update['message']['chat']['id']
    if check_telegram_client(update['message']['chat']['id'], update):
        if update['message']['text'].startswith('/tadd'):
            message_list = update['message']['text'].split(' ')[1:]
            name_ticket = ' '.join(message_list)
            if name_ticket is not None and name_ticket.strip() != '':
                base_url = 'http://polik3.local/glpi/apirest.php/'
                app_token = ''

                match = next((l for l in TELEGRAM_GLPI_LIST if l['chat_id'] == cur_chat), None)

                if match is not None:
                    user_token = match['glpi_token']

                    target_url = 'initSession/'
                    sessiondata = {'Content-Type': 'application/json',
                                   'Authorization': 'user_token ' + user_token, 'App-Token': app_token}
                    session = get(base_url + target_url, headers=sessiondata)
                    session_token = session.json()
                    session_token = session_token['session_token']
                    args = None
                    item_type = 'ticket'
                    if args is None:
                        target_url = item_type + '/190/ticket_user/'
                    else:
                        target_url = item_type + '/' + '?' + args
                    sessiondata = {'Content-Type': 'application/json',
                                   'Session-Token': session_token, 'App-Token': app_token}
                    session = post(base_url + target_url, headers=sessiondata, json={"input": {'tickets_id': 190, 'users_id': 7, 'type': 2}})
                    print(session.json())
                    for ticket in session.json():
                        continue
                        print(ticket)

                    item_type = 'ticket'
                    target_url = item_type+'/'
                    sessiondata = {'Content-Type': 'application/json',
                                   'Session-Token': session_token, 'App-Token': app_token}
                    session = post(base_url + target_url, headers=sessiondata, json={"input": {"name": name_ticket,
                                   'users_id_recipient': 7, 'content': name_ticket, 'itilcategories_id': 1}})
                    update.message.reply_text(session.json()['message'])

                    target_url = item_type+'/'+str(session.json()['id'])
                    print(target_url)
                    sessiondata = {'Content-Type': 'application/json',
                                   'Session-Token': session_token, 'App-Token': app_token}
                    session = put(base_url + target_url, headers=sessiondata, json={"input": {'users_id_recipient': 7}})
                    # session = put(base_url + target_url, headers=sessiondata, json={"input": {'status': 1,
                    #               'users_id_recipient': 7}})

                    target_url = 'killSession'
                    sessiondata = {'Content-Type': 'application/json',
                                   'Session-Token': session_token, 'App-Token': app_token}
                    session = get(base_url + target_url, headers=sessiondata)
                else:
                    update.message.reply_text('пользователь не авторизирован')
            else:
                update.message.reply_text('ошибка не указан заголовок тикета')


def help(update, context):
    cur_chat = update['message']['chat']['id']
    if check_telegram_client(cur_chat, update):
        update.message.reply_text('/tadd заголовок - добавить тикет')


def main():
    # sock = socket.socket()
    # sock.connect(QSYSTEM_ADDRESS)
    # sock.send(b'{"params":{"drop_tickets_cnt":true},"jsonrpc":"2.0","id":"1570405953995","method":"#WELCOME_REINIT#"}')
    # data = sock.recv(1024)
    # data2 = json.loads(data.decode("cp1251"))
    # print(data2)
    # sock.close()01011960

    sock = socket.socket()
    sock.connect(QSYSTEM_ADDRESS)
    sock.send(b'{"params":{"drop_tickets_cnt":false},"jsonrpc":"2.0","id":"1570170084856","method":"Empty"}')
    data = sock.recv(1024)
    data2 = json.loads(data.decode("cp1251"))
    print(data2)

    # updater = Updater(BOT_TOKEN, use_context=True)
    updater = Updater(BOT_TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", hello_world))
    dp.add_handler(CommandHandler("terminal", talon))
    dp.add_handler(CommandHandler("l", terminal_lock))
    dp.add_handler(CommandHandler("u", terminal_unlock))
    dp.add_handler(CommandHandler("r", terminal_reset))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(None, handle_text))
    print('bot start')

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
