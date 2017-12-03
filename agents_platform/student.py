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
from spell_check import addhints

def send_solution(agent, student_board, student_element, solution_file):
    logger.debug('helloworld', 'student sending solution')
    ta_element = None
    ta_board = None
    for board in agent.get_boards():
        for element in board.get_elements():
            if element.get_name() == '@ta_' + student_element.get_name()[1:]:
                if ta_element is not None:
                    logger.error('helloworld', 'more than one ta found')
                ta_element = element
                ta_board = board
                break

    #TODO change to getting board creator name
    student_name = 'RustamGafarov' #student_board.get_name()
    file_link = agent.get_platform_access().get_platform_url() + solution_file.get_download_link()
    downloaded_file = urllib.request.urlopen(file_link)
    to_send = downloaded_file
    print(solution_file.get_name())

    g = None
    if solution_file.get_name()[-4:] == '.txt':
        text = str(downloaded_file.read())
        hints = addhints(text[2:-3])
        tmp_file = '/tmp/' + student_name + '.txt'
        f = open(tmp_file, 'w')
        f.write(hints)
        f.close()
        g = open(tmp_file)
        to_send = g


    logger.debug('helloworld', 'copypaste the solution')
    ta_element.put_file(solution_file.get_name(), to_send)

    if g is not None:
        g.close()

    message_for_ta = "Student " + student_name + " just sent his solution"
    ta_board.put_message(message_for_ta)

    message_for_student = "Assignment sucessfully sent"
    student_board.put_message(message_for_student)