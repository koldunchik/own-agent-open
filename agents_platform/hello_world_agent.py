import json
import re
import threading
import time
import traceback

import websocket

import logger
import student
import teacher

from own_adapter.agent import Agent
from own_adapter.board import Board
from own_adapter.element import Element
from own_adapter.platform_access import PlatformAccess, get_agent

def periodical_update():
    """Does periodical work with a predefined time interval"""
    time_interval = 86400

    while True:
        time.sleep(time_interval)
        logger.info('helloworld', 'Daily news update is done.')


def process_added_element(message_dict):
    element_caption = message_dict['newCaption']
    if re.match(pattern='@ta:.+', string=element_caption):
        student.get_new_assignment(message_dict)


def process_added_file(message_dict):
    file_link = message_dict['path']
    element_link = '/'.join(file_link.split('/')[:-2])
    board_link = '/'.join(file_link.split('/')[:-4])
    agent = get_agent()
    board = Board.get_board_by_id(board_link, agent.get_platform_access(), need_name=False)
    element = Element.get_element_by_id(element_link, agent.get_platform_access(), board)
    caption = element.get_name()

    added_file = None
    for file in element.get_files():
        platform_url = agent.get_platform_access().get_platform_url()
        if file.get_url()[len(platform_url):] == file_link:
            added_file = file
            break;

    logger.debug('helloworld', caption)
    if re.match(pattern='@ta_assignment:.+', string=caption) and len(element.get_files()) == 1:
        teacher.send_new_assignment(agent, board, element, added_file)
    if re.match(pattern='@assignment:.+', string=caption) and len(element.get_files()) > 1:
        student.send_solution(agent, board, element, added_file)
    if re.match(pattern='@ta_assignment:.+', string=caption) and len(element.get_files()) > 1:
        teacher.recieve_solution(agent, board, element, added_file)
    if re.match(pattern='@ta_assignment_graded:.+', string=caption):
        teacher.send_grades(agent, board, element, added_file)




def on_websocket_message(ws, message):
    """Processes websocket messages"""
    message_dict = json.loads(message)
    content_type = message_dict['contentType']
    message_type = content_type.replace('application/vnd.uberblik.', '')

    logger.debug('helloworld', message)

    if message_type == 'liveUpdateElementCaptionEdited+json':
        process_added_element(message_dict)
    if message_type == 'liveUpdateFileAdded+json':
        process_added_file(message_dict)


def on_websocket_error(ws, error):
    """Logs websocket errors"""
    logger.error('helloworld', error)


def on_websocket_open(ws):
    """Logs websocket openings"""
    logger.info('helloworld', 'Websocket is open')


def on_websocket_close(ws):
    """Logs websocket closings"""
    logger.info('helloworld', 'Websocket is closed')


def open_websocket():
    """Opens a websocket to receive messages from the boards about events"""
    agent = get_agent()
    # getting the service url without protocol name
    platform_url_no_protocol = agent.get_platform_access().get_platform_url().split('://')[1]
    access_token = agent.get_platform_access().get_access_token()
    url = 'ws://{}/opensocket?token={}'.format(platform_url_no_protocol, access_token)

    ws = websocket.WebSocketApp(url,
                                on_message=on_websocket_message,
                                on_error=on_websocket_error,
                                on_open=on_websocket_open,
                                on_close=on_websocket_close)
    ws.run_forever()


def run():
    websocket_thread = None
    updater_thread = None

    while True:
        # opening a websocket for catching server messages
        if websocket_thread is None or not websocket_thread.is_alive():
            try:
                websocket_thread = threading.Thread(target=open_websocket)
                websocket_thread.start()
            except Exception as e:
                logger.exception('helloworld', 'Could not open a websocket. Exception message: {}'.format(str(e)))

        # periodical updates
        if updater_thread is None or not updater_thread.is_alive():
            try:
                updater_thread = threading.Thread(target=periodical_update)
                updater_thread.start()
            except Exception as e:
                logger.exception('helloworld', 'Could not start updater. Exception message: {}'.format(str(e)))

        # wait until next check
        time.sleep(10)


if __name__ == '__main__':
    run()
