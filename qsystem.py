from bot_config import QSYSTEM_ADDRESS
from dat_telegram import check_telegram_client
import json
import socket
import logging


def talon():
    try:
        sock = socket.socket()
        sock.connect(QSYSTEM_ADDRESS)
        sock.send(b'{"params":{"drop_tickets_cnt":false},"jsonrpc":"2.0","id":"1570170084856","method":"Empty"}')
        data = sock.recv(1024)
        data2 = json.loads(data.decode("cp1251"))
        logging.warning(data2)
        sock.close()
        return data2['result']
    except WindowsError as e:
        logging.error(e.strerror)
        return e.strerror

def terminal_lock():
    sock = socket.socket()
    sock.connect(QSYSTEM_ADDRESS)
    sock.send(b'{"params":{"drop_tickets_cnt":false},"jsonrpc":"2.0","id":"1570405953995","method":"#WELCOME_LOCK#"}')
    data = sock.recv(1024)
    data2 = json.loads(data.decode("cp1251"))
    logging.warning(data2)
    sock.close()
    return data2['result']


def terminal_reset():
    sock = socket.socket()
    sock.connect(QSYSTEM_ADDRESS)
    sock.send(b'{"params":{"drop_tickets_cnt":true},"jsonrpc":"2.0","id":"1570405953995","method":"#WELCOME_REINIT#"}')
    data = sock.recv(1024)
    data2 = json.loads(data.decode("cp1251"))
    logging.warning(data2)
    sock.close()
    return data2['result']


def terminal_unlock():
    sock = socket.socket()
    sock.connect(QSYSTEM_ADDRESS)
    sock.send(b'{"params":{"drop_tickets_cnt":false},"jsonrpc":"2.0","id":"1570405953995","method":"#WELCOME_UNLOCK#"}')
    data = sock.recv(1024)
    data2 = json.loads(data.decode("cp1251"))
    logging.warning(data2)
    sock.close()
    return data2['result']
