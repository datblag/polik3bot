from bot_config import QLPI_API_BASE_URL
from bot_config import TELEGRAM_GLPI_LIST
from requests import get, post, put, delete


def kill_session(prm_session_token):
    base_url = QLPI_API_BASE_URL
    app_token = ''
    target_url = 'killSession'
    sessiondata = {'Content-Type': 'application/json',
                   'Session-Token': prm_session_token, 'App-Token': app_token}
    get(base_url + target_url, headers=sessiondata)


def init_session(prm_cur_chat):
    session_token = None
    base_url = QLPI_API_BASE_URL
    app_token = ''

    match = next((l for l in TELEGRAM_GLPI_LIST if l['chat_id'] == prm_cur_chat), None)

    if match is not None:
        user_token = match['glpi_token']

        target_url = 'initSession/'
        sessiondata = {'Content-Type': 'application/json',
                       'Authorization': 'user_token ' + user_token, 'App-Token': app_token}
        session = get(base_url + target_url, headers=sessiondata)
        session_token = session.json()
        session_token = session_token['session_token']
    return session_token


def ticket_add(prm_session_token, prm_ticket_name):
    base_url = QLPI_API_BASE_URL
    item_type = 'ticket'
    target_url = item_type + '/'
    app_token = ''
    sessiondata = {'Content-Type': 'application/json',
                   'Session-Token': prm_session_token, 'App-Token': app_token}
    session = post(base_url + target_url, headers=sessiondata, json={"input": {"name": prm_ticket_name,
                                                                               # 'users_id_recipient': 7,
                                                                               'content': prm_ticket_name,
                                                                               'itilcategories_id': 1}})

    res_message = session.json()['message']

    ticket_id = session.json()['id']

    target_url = item_type + '/' + str(ticket_id) + '/' +'ticket_user/'
    sessiondata = {'Content-Type': 'application/json',
                   'Session-Token': prm_session_token, 'App-Token': app_token}
    session = get(base_url + target_url, headers=sessiondata)
    for s in session.json():
        if s['type'] == 2:
            s_id = s['id']
            target_url = item_type + '/' + str(ticket_id) + '/' +'ticket_user/'
            sessiondata = {'Content-Type': 'application/json',
                           'Session-Token': prm_session_token, 'App-Token': app_token}
            session = delete(base_url + target_url, headers=sessiondata, json={"input": {'tickets_id': 190, 'id': s_id}})
    # print(target_url)
    # sessiondata = {'Content-Type': 'application/json',
    #                'Session-Token': prm_session_token, 'App-Token': app_token}
    # session = put(base_url + target_url, headers=sessiondata, json={"input": {'users_id_recipient': 7}})
    # session = put(base_url + target_url, headers=sessiondata, json={"input": {'status': 1,
    #               'users_id_recipient': 7}})



    # target_url = item_type + '/' + str(session.json()['id'])
    # print(target_url)
    # sessiondata = {'Content-Type': 'application/json',
    #                'Session-Token': prm_session_token, 'App-Token': app_token}
    # session = put(base_url + target_url, headers=sessiondata, json={"input": {'users_id_recipient': 7}})
    # session = put(base_url + target_url, headers=sessiondata, json={"input": {'status': 1,
    #               'users_id_recipient': 7}})
    return res_message
