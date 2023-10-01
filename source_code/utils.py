"""
Created October 1, 2022
author: Dimitris Lymperopoulos
Description: A file containing some utility functions
"""


def logger_info(message):   # function to simply print the message
    print("[INFO]: " + message)


def logger_error(message):  # function that prints the error message and then exits
    print("[ERROR]: " + message)
    exit(1)
