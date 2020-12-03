import logs
from telegram.ext import Updater, CommandHandler, MessageHandler
from bot_config import BOT_TOKEN, REQUEST_KWARGS
from bot_config import QLPI_API_BASE_URL
from bot_config import CABINET_KEY
from requests import post, get, put, delete
from dat_telegram import check_telegram_client
import qsystem
import logging
from dat_glpi import init_session, ticket_add, kill_session


def terminal_reset(update, context):
    if check_telegram_client(update['message']['chat']['id'],update):
        res_message = qsystem.terminal_reset()
        update.message.reply_text(res_message)


def terminal_unlock(update,  context):
    if check_telegram_client(update['message']['chat']['id'], update):
        res_message = qsystem.terminal_unlock()
        update.message.reply_text(res_message)


def terminal_lock(update, context):
    if check_telegram_client(update['message']['chat']['id'], update):
        res_message = qsystem.terminal_lock()
        update.message.reply_text(res_message)


def talon(update, context):
    if check_telegram_client(update['message']['chat']['id'],update):
        res_message = qsystem.talon()
        update.message.reply_text(res_message)


def hello_world(update,  context):
    if check_telegram_client(update['message']['chat']['id'], update):
        logging.info('hi. i work')
        update.message.reply_text('hi. i work')


def error(update, context):
    """Log Errors caused by Updates."""
    logging.error(update)
    logging.error(context.error)


def handle_text(update, context):
    cur_chat = update['message']['chat']['id']
    if check_telegram_client(update['message']['chat']['id'], update):
        if update['message']['text'].startswith('/tadd'):
            message_list = update['message']['text'].split(' ')[1:]
            name_ticket = ' '.join(message_list)
            base_url = QLPI_API_BASE_URL
            app_token = ''
            if name_ticket is not None and name_ticket.strip() != '':
                session_token = init_session(cur_chat)
                if session_token is not None:
                    # args = None
                    # item_type = 'ticket'
                    # if args is None:
                    #     target_url = item_type + '/190/ticket_user/'
                    # else:
                    #     target_url = item_type + '/' + '?' + args
                    # sessiondata = {'Content-Type': 'application/json',
                    #                'Session-Token': session_token, 'App-Token': app_token}
                    # session = post(base_url + target_url, headers=sessiondata, json={"input": {'tickets_id': 190, 'users_id': 7, 'type': 2}})
                    # print(session.json())
                    # for ticket in session.json():
                    #     continue
                    #     print(ticket)

                    res_message = ticket_add(session_token, name_ticket)
                    update.message.reply_text(res_message)

                    kill_session(session_token)
                else:
                    update.message.reply_text('пользователь не авторизирован')
            else:
                update.message.reply_text('ошибка не указан заголовок тикета')
        elif update['message']['text'].startswith('/cabinet'):
            try:
                cabinet = update['message']['text'].split(' ')[1:][0]
                if cabinet.isdigit():
                    cabinet_prefix = ''
                    if int(cabinet) < 200:
                        cabinet_prefix = 'a'
                        cabinet = cabinet[1:]
                    elif int(cabinet) < 300:
                        cabinet_prefix = 'b'
                        cabinet = cabinet[1:]
                    elif int(cabinet) < 400:
                        cabinet_prefix = 'c'
                        cabinet = cabinet[1:]
                    elif int(cabinet) < 500:
                        cabinet_prefix = 'd'
                        cabinet = cabinet[1:]

                    cabinet = ''.join([cabinet_prefix, cabinet, CABINET_KEY])
                    update.message.reply_text(cabinet)
            except:
                update.message.reply_text('ошибка')


def help(update, context):
    cur_chat = update['message']['chat']['id']
    if check_telegram_client(cur_chat, update):
        update.message.reply_text('/tadd заголовок - добавить тикет')


def main():
    logs.run()

    qsystem.talon()

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
    logging.info('bot start')

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
