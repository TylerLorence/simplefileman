import os
import logging


"""
Tyler Lorence's Project #1 (Untitled)
Version Pre-Indev (SNAPSHOT 1 - 30 MINUTE MARK)

TODO: Add error handling with Try/Except.
TODO: Add error logging with the logging module.
TODO: Other ideas that come to me along the way.


"""



logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler("FourthPlayground.log", mode="w")

logger.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(name)s / %(levelname)s]: %(message)s")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.info("Program started!")

os.chdir("C:\\")

def list():
    with os.scandir() as dir_iter:
        for element in dir_iter:
            if element.is_file():
                print(f"{element.name}")
            elif element.is_dir():
                print(f"[DIR] {element.name}")
            else:
                logger.error("There was an error ")

def create_file(filename):
    with open(filename, "w") as f:
        pass
    logger.info(f"Created the file {filename} successfully.")

def change_directory(directory):
    os.chdir(directory)

def make_directory(directory_name):
    os.mkdir(directory_name)
    logger.info(f"Created the directory {directory_name} successfully.")

def remove_directory(directory_name):
    os.rmdir(directory_name)

def read(file):
    with open(file, "r") as f:
        print(f"""\
            ----- File {file} -----
{f.readlines()}
        """)

def remove_file(file):
    os.remove(file)

while True:
    user_input = input(f"{os.getcwd()}>").split(" ")
    if user_input[0].casefold() == "ls" or user_input[0].casefold() == "dir":
        list()
    elif user_input[0].casefold() == "cd":
        change_directory(user_input[1])
    elif user_input[0].casefold() == "createfile":
        create_file(user_input[1])
    elif user_input[0].casefold() == "md" or user_input[0].casefold() == "mkdir":
        make_directory(user_input[1])
    elif user_input[0].casefold() == "rd" or user_input[0].casefold() == "rmdir":
        while True:
            confirmation = input(f"WARNING: Are you sure you want to remove the directory \"{user_input[1]}\"? This action is permanent and cannot be undone. (Y/N)\n> ")
            if confirmation.casefold() == "y":
                remove_directory(user_input[1])
                break
            elif confirmation.casefold() == "n":
                logger.info("Cancelled operation.")
                break
            else:
                print("Invalid option! Please enter \"y\" or \"n\" for this prompt.")
    elif user_input[0].casefold() == "del" or user_input[0].casefold() == "delete":
            while True:
                confirmation = input(f"WARNING: Are you sure you want to remove the file \"{user_input[1]}\"? This action is permanent and cannot be undone. (Y/N)\n> ")
                if confirmation.casefold() == "y":
                    remove_file(user_input[1])
                    break
                elif confirmation.casefold() == "n":
                    logger.info("Cancelled operation.")
                    break
                else:
                    print("Invalid option! Please enter \"y\" or \"n\" for this prompt.")
    elif user_input[0].casefold() == "read" or user_input[0].casefold() == "more":
        read(user_input[1])
    elif user_input[0].casefold() == "exit":
        exit(0)
    else:
        print("Invalid command!")


