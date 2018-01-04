import sys
import string
import re

TASK_TIME_SEPARATOR = ":;"

def usage():
    u = """
    python logger.py [command] [arguments]

    Default command is -s for saving a task time.

    # Commands #
    -s <task> <time>
        where task must have been specified before with -n, e.g. "-n Chinese"
          and time is specified in minutes or hours, e.g. 180, 3h
    -n <task>
        to specify a new task to track time for
    """
    print(u)
#/def

def new_task(task):
    if not all(x.isalpha() or x.isspace() for x in task):
        return false, "Task name must consists only of alphabetic characters and spaces."
    if check_existing_task(task):
        return false, "Task " + task + " already exists!"
    else:
        with open("data/timelog.dat", "a") as f:
            f.write(task + TASK_TIME_SEPARATOR + "0")
    #
#/def

def parse_args():
    args = sys.argv[1:]
    argc = len(args)
    cmd = args[0]
    if (cmd == "-s" and argc == 3):
        parse_cmd_save()
    elif (cmd[0] != "-" and argc == 2):
        parse_cmd_save()


def parse_cmd_save(args):
    task = args[-2]

    

def get_minutes(timestr):
    re_minutes = re.compile("^\d+[mM]?$")
    re_hours = re.compile("^\d+(\.\d\d?)?[hH]$")
    re_HandM = re.compile("^\d+[hH]\d\d?[mM]?$")

    if re_minutes.match(timestr):
        timestr = timestr.lower().split("m")[0]
        return int(timestr)
    elif re_hours.match(timestr):
        timestr = timestr.lower().split("h")[0]
        return int( round( 60 * float(timestr) ) )
    elif re_HandM.match(timestr):
        timestr = timestr.lower().replace("m", "")
        hours, minutes = (int(x) for x in timestr.split("h"))
        return 60 * hours + minutes
    else:
        return 0

