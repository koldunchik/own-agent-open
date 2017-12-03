import json
import re
import threading
import time
import traceback
import urllib

import websocket

import logger
from own_adapter.agent import Agent
from own_adapter.board import Board
from own_adapter.element import Element
from own_adapter.platform_access import PlatformAccess, get_agent


def __do_something(element):
    """Write your code here"""

    # examples:
    # put a message to a board
    message = 'Hello world!'
    element.get_board().put_message(message)

    # put a URL to an element
    url = 'https://www.own.space/'
    element.put_link(url)


def check_grammar(file):
    #TODO implement grammar checking
    path_to_corrected_file = ""
    return path_to_corrected_file



def send_new_assignment(agent, sender_board, assignment_element, assignment_file):
    logger.debug('helloworld', 'teacher sending an assignment')
    if assignment_element is None:
        logger.debug('helloworld', 'element is null')
        return

    if assignment_file is None:
        logger.debug('helloworld', 'file is null')
        return

    file_link = agent.get_platform_access().get_platform_url() + assignment_file.get_download_link()
    downloaded_file = urllib.request.urlopen(file_link)

    all_boards = agent.get_boards()
    for board in all_boards:
        if board.get_id() != sender_board.get_id():
            logger.debug('helloworld', 'teacher sending an assignment to ' + board.get_name())
            element_name = '@' + assignment_element.get_name()[4:]

            matrix = board.get_elements_matrix()
            for pos_y, pos_x in ((y, x) for y in range(len(matrix)) for x in range(len(matrix[y]))):
                if matrix[pos_y][pos_x] == 0:
                    # TODO: remove hardcoded string
                    board.add_element(pos_x + 1, pos_y + 1, caption=element_name)
                    break

            for element in board.get_elements():
                if element.get_name() == element_name:
                    logger.debug('helloworld', 'copypaste the assignment')
                    element.put_file(assignment_file.get_name(), downloaded_file)

            message_for_student = "You have a new assignment."
            board.put_message(message_for_student)



    message = 'Assignment ' + assignment_element.get_name() + ' have been sent'
    sender_board.put_message(message)


def recieve_solution(agent, board, element, file):
    logger.debug('helloworld', 'teacher recieving solution')
    pass


def send_grades(agent, board, element, file):
    logger.debug('helloworld', 'teacher sending grades')
    pass