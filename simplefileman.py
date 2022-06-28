import os
import sys
import ctypes
import shutil
import logging


"""
simplefileman - CLI-Based File Manager by Tyler Lorence
Version Pre-Indev (SNAPSHOT 4.6)

TODO: Add error handling with Try/Except.
TODO: Add error logging with the logging module.
TODO: Add 'appendfile' command
TODO: Other ideas that come to me along the way.
TODO: Add 'filesize' command


"""



logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler("FourthPlayground.log", mode="w")

logger.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(name)s / %(levelname)s]: %(message)s")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.info("Program started!")

try:
    os.chdir("C:\\")
except FileNotFoundError:
    logger.info("Error: The \"C:\\\" directory could not be found. Not changing directory.")

def dfilesize(file):
    if os.stat(file).st_size < 1000:
        return f"{os.stat(file).st_size} B"
    elif os.stat(file).st_size >= 1000 and os.stat(file).st_size < 1000000:
        return f"{round((os.stat(file).st_size / 1000), 2)} KB"
    elif os.stat(file).st_size >= 1000000 and os.stat(file).st_size < 1000000000:
        return f"{round((os.stat(file).st_size / 1000000), 2)} MB"
    elif os.stat(file).st_size >= 1000000000 and os.stat(file).st_size < 1000000000000:
        return f"{round((os.stat(file).st_size / 1000000000), 2)} GB"
    elif os.stat(file).st_size >= 1000000000000:
        return f"{round((os.stat(file).st_size / 1000000000000), 2)} TB"

def list():
    with os.scandir() as dir_iter:
        for element in dir_iter:
            if element.is_file():
                print(f"{element.name}     ({dfilesize(element)})")
            elif element.is_dir():
                print(f"[DIR] {element.name}")
            else:
                logger.error("There was an error ")

def create_file(filename):
    with open(filename, "w") as f:
        pass
    logger.info(f"Created the file {filename} successfully.")

def change_directory(directory):
    try:
        os.chdir(directory)
    except FileNotFoundError as e:
        logger.error(f"Error attempting to change directory: Cannot find the directory {directory}")

def make_directory(directory_name):
    os.mkdir(directory_name)
    logger.info(f"Created the directory {directory_name} successfully.")

def remove_directory(directory_name):
    try:
        os.rmdir(directory_name)
    except FileNotFoundError:
        logger.error(f"Error attempting to remove directory: Cannot find the directory {directory_name}")
    except OSError as e:
        if "The directory is not empty:" not in str(e):
            logger.error(f"An unknown error has occured! Please contact the developer about this issue\nAttempted Action: Removing directory (remove_directory) with parameter {directory_name}\nError Thrown: {e}\nNote: The error does not have the string \"The directory is not empty:\" in it.")
            return
        shutil.rmtree(directory_name)

def read(file):
    try:
        with open(file, "r") as f:
            print(f"""\
                ----- File {file} -----
    {f.read()}
            """)
    except FileNotFoundError:
        logger.error(f"Error attempting to read file: Cannot find the file {file}")

def remove_file(file):
    os.remove(file)

def write_to_file(*contents):
    if os.path.isfile(contents[0][0]):
        with open(contents[0][0], "w+") as f:
            logger.debug(f"\"*contents*\" parameter provided: {contents} / First index (at index 0) of contents parameter: {contents[0]}")
            joined_contents = " ".join(contents[0][1:])
            logger.debug(f"Joined contents via \"joined_contents\". type(joined_contents): {type(joined_contents)} / Joined Contents: {joined_contents}")
            f.write(joined_contents)
    else:
        logger.error(f"Error attempting to write to file: Cannot find the file {contents[0][1]}")


def filesize(file):
    if os.stat(file).st_size < 1000:
        return f"Size of File {file}: {os.stat(file).st_size} Bytes"
    elif os.stat(file).st_size >= 1000 and os.stat(file).st_size < 1000000:
        return f"Size of File {file}: {round((os.stat(file).st_size / 1000), 2)} Kilobytes"
    elif os.stat(file).st_size >= 1000000 and os.stat(file).st_size < 1000000000:
        return f"Size of File {file}: {round((os.stat(file).st_size / 1000000), 2)} Megabytes"
    elif os.stat(file).st_size >= 1000000000 and os.stat(file).st_size < 1000000000000:
        return f"Size of File {file}: {round((os.stat(file).st_size / 1000000000), 2)} Gigabytes"
    elif os.stat(file).st_size >= 1000000000000:
        return f"Size of File {file}: {round((os.stat(file).st_size / 1000000000000), 2)} Terabytes"



command_information = {
    ("help", "?"): "--- Command \"help\" / \"?\" ---\n\nReturns the list of commands, or information about a command\nUsage: help [command name]\nExample: help\nExample: help cd\n",
    ("dir", "ls"): "--- Command \"dir\" / \"ls\" ---\n\nReturns the elements of the directory the program is currently in\nUsage: dir\nExample: 'dir'\n",
    ("cd"): "--- Command \"cd\" ---\n\nChanges the directory of the program\nUsage: cd <new directory>\nExample: 'cd C:\\Users\\admin\\Desktop'\nExample: 'cd Users'\n",
    ("md", "mkdir"): "--- Command \"md\" / \"mkdir\" ---\n\nMakes a new directory\nUsage: 'md <New Folder Name>'\nExample: 'md NewFolder'\n",
    ("rd", "rmdir"): "--- Command \"rd\" / \"rmdir\" ---\n\nRemoves a directory\nUsage: 'rd <Folder to Remove>'\nExample: 'rd NewFolder'\n",
    ("createfile", "makefile"): "--- Command \"createfile\" / \"makefile\" ---\n\nCreates a new file\nUsage: createfile <new file name>\nExample: 'createfile HelloWorld.txt'\n",
    ("read", "more"): "--- Command \"read\" / \"more\" ---\n\nReads the text contents of a file.\nUsage: read <file name>\nExample: 'read HelloWorld.txt'\n",
    ("write", "writeto"): "--- Command \"write\" / \"writeto\" ---\n\nWrites text content to a file, overriding the current file contents\nUsage: write <file name> <new file contents>\nExample: 'write HelloWorld.txt Hello, world!'\n",
    ("append", "appendto"): "--- Command \"append\" / \"appendto\" ---\n\nDEVELOPER NOTE: This command has not been made yet! Appends text content to a file, appending to the current file contents\nUsage: append <file name> <file contents to append>\nExample: 'append HelloWorld.txt Hi!!'\n",
    ("copy", "copyfile"): "--- Command \"copy\" / \"copyfile\" ---\n\nDEVELOPER NOTE: This command has not been made yet! Copies a file.\nUsage: copy <file to copy> <new file>\nExample: 'copy HelloWorld.txt TestFile.txt'\n",
    ("del", "delete"): "--- Command \"del\" / \"delete\" ---\n\nDeletes a file\nUsage: del <file to delete>\nExample: 'del TestFile.txt'\n",
    ("filesize"): "--- Command \"help\" / \"?\" ---\n\nDEVELOPER NOTE: This command has not been made yet! Gets the size of a file.\nUsage: filesize <file name>\nExample: 'filesize HelloWorld.txt'",
    ("exit"): "--- Command \"exit\" ---\n\nExits the program\nUsage: exit\nExample: 'exit'\n"


}




while True:
    user_input = input(f"{os.getcwd()}>").split(" ")
    if user_input[0].casefold() == "ls" or user_input[0].casefold() == "dir":
        list()
    elif user_input[0].casefold() == "cd":
        change_directory(user_input[1])
    elif user_input[0].casefold() == "createfile" or user_input[0] == "makefile":
        try:
            create_file(user_input[1])
        except PermissionError:
            logger.error(f"Error attempting to create file {user_input[1]}: Permission denied")
            logger.debug("Developer Note: Use \"debug_uac\" to open an elevated instance.")
        except IndexError:
            logger.error(f"Error attempting to create file: No file name provided!")
    elif user_input[0].casefold() == "md" or user_input[0].casefold() == "mkdir":
        try:
            make_directory(user_input[1])
        except IndexError:
            logger.error("Error attempting to create directory: No directory name provided!")
        except FileExistsError:
            logger.error(f"Error attempting to make directory: Cannot create a directory when that directory already exists: '{user_input[1]}'")
    elif user_input[0].casefold() == "rd" or user_input[0].casefold() == "rmdir":
        try:
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
        except PermissionError:
            logger.error(f"Error attempting to delete folder '{user_input[1]}': Permission denied")
            logger.debug("Developer Note: Use \"debug_uac\" to open an elevated instance.")
            break
    elif user_input[0].casefold() == "del" or user_input[0].casefold() == "delete":
            while True:
                try:
                    confirmation = input(f"WARNING: Are you sure you want to remove the file \"{user_input[1]}\"? This action is permanent and cannot be undone. (Y/N)\n> ")
                    if confirmation.casefold() == "y":
                        remove_file(user_input[1])
                        break
                    elif confirmation.casefold() == "n":
                        logger.info("Cancelled operation.")
                        break
                    else:
                        print("Invalid option! Please enter \"y\" or \"n\" for this prompt.")
                except PermissionError:
                    logger.error(f"Error attempting to delete file '{user_input[1]}': Permission denied")
                    logger.debug("Developer Note: Use \"debug_uac\" to open an elevated instance.")
                    break
    elif user_input[0].casefold() == "read" or user_input[0].casefold() == "more":
        try:
            read(user_input[1])
        except IndexError:
            logger.error(f"Error attempting to read file: No file name was provided")
    elif user_input[0].casefold() == "write" or user_input[0].casefold() == "writeto":
        try:
            write_to_file(user_input[1:])
        except IndexError:
            logger.error(f"Error attempting to write to file: No filename was provided.")
    elif user_input[0].casefold() == "filesize" or user_input[0].casefold() == "size":
        try:
            print(filesize(user_input[1]))
        except IndexError:
            logger.error(f"Error attempting to fetch file size: No argument provided!")
    elif user_input[0].casefold() == "help" or user_input[0].casefold() == "?":
        if len(user_input) == 1:
            print("""\
                Available Commands:
                help, dir, cd, md, rd, createfile, read, write, append, copy, del, filesize
                Type 'help <command name> to get information about a command.
                """)
        else:
            # print(command_information.get(user_input[1], "Error: Command Not Found!"))
            found = 0
            for key, value in command_information.items():
                if user_input[1].casefold() in key:
                    found = 1
                    print(value)
                    break
                else:
                    pass
            if found == 0:
                logger.error(f"Error attempting to get information about command {user_input[1]}: Command Not Found!")
    elif user_input[0].casefold() == "exit":
        exit(0)
    elif user_input[0].casefold() == "debug_uac":
        # This is a debug command that will be removed in the future. Its purpose is to test opening a new instance of the program with UAC permissions.
        # The documentation is based on the ShellExecuteA function, seen in Microsoft's documentation for the Win32 Shell API.
        # https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutea?redirectedfrom=MSDN
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    elif user_input[0].casefold() == "developer" or user_input[0].casefold() == "dev":
        logger.info("Entering developer mode.")
        while True:
            dev_input = input("Dev >> ")
            if dev_input.casefold() == "exit":
                logger.info("Exiting developer mode.")
                break
            elif dev_input == "eval":
                dev_eval = input("Dev/Eval >> ")
                try:
                    print(eval(dev_eval))
                except Exception as e:
                    print(f"""\
                        An error has occured!
                        Error Type: {type(e)}
                        Error: {e}
                        Error Args: {e.args}
                    """)
            elif dev_input.casefold() == "feval":
                dev_eval = input("Dev/Forced_Eval >> ")
                print(eval(dev_eval))
            else:
                logger.error("Dev Error: Invalid Command Provided!")
    else:
        print("Invalid command!")
