import sys
import string
import re

SUMMARY_FILE = "data/timesummary.dat" # File for counting time totals on each task
TIMELOG_FILE = "data/timelog.dat" # File for all individual log entries

def usage():
    u = """
    Usage: python logger.py [command] [arguments]

    Default command is -s for saving a task time.

    # Commands #
    -s <task> <time>
        where task must have been specified before with -n, e.g. "-n Chinese"
          and time is specified in minutes or hours, e.g. 180, 3h
    -n <task>
        to specify a new task to track time for
    """
    print(u)


### Constructs and related functions ###

TASK_TIME_SEPARATOR = ":;"
TIME_CHARACTERS = 8

def construct_task(name, time=0):
    return {'name': name, 'time': time}

def task_to_string(task):
    timestr = format_time(task['time'])
    return task['name'] + TASK_TIME_SEPARATOR + timestr

def task_from_string(s):
    return construct_task(*s.split(TASK_TIME_SEPARATOR))


### File operations ###

# File write
def format_time(minutes):
    return str(minutes).zfill(TIME_CHARACTERS)


def create_new_task(taskname):
    if not all(x.isalpha() or x.isspace() for x in taskname):
        return False, "Task name must consists only of alphabetic characters and spaces."
    if task_exists(taskname):
        return False, "Task '" + taskname + "' already exists!"
    
    with open(SUMMARY_FILE, 'a') as f:
        task = construct_task(taskname, 0)
        f.write(task_to_string(task) + '\n')

    return True, ""


def update_task_summary(taskname, minutes_to_add):
    """
    Update total number of minutes spent on task.
    @return True on success, False if task was not found
    """
    char_count = 0
    with open(SUMMARY_FILE, 'r+') as f:
        for line in f:

            if len(line.strip()) > 0: # Ignore empty lines
                task = task_from_string(line.strip())

                if task['name'] == taskname:
                    f.seek(char_count, 0)
                    newtime = int(task['time']) + minutes_to_add
                    pattern = re.compile(r"\d\d\d\d\d\d\d\d") # Ugly! Regex depends on constant value TIME_CHARACTERS == 8
                    updated_line = re.sub(pattern, format_time(newtime), line)
                    f.write(updated_line)
                    return True

            char_count = char_count + len(line)

    return False


def log_entry(taskname, time):
    """
    Create an entry in timelog file.
    """
    with open(TIMELOG_FILE, 'a') as f:
        f.write(taskname + TASK_TIME_SEPARATOR + str(time) + '\n')


# File read

def task_exists(taskname):
    with open(SUMMARY_FILE, 'r') as f:
        for line in f:
            if line.strip()[:line.index(TASK_TIME_SEPARATOR)] == taskname:
                return True

    return False


# Command-line arguments

def parse_args():
    args = sys.argv[1:]
    argc = len(args)
    cmd = args[0]
    success = True

    if cmd == "-s" and argc == 3:
        parse_cmd_save(args)
    elif cmd[0] != "-" and argc == 2:
        parse_cmd_save(args)
    elif cmd == "-n" and argc == 2:
        success, errortxt = create_new_task(args[1])
    else:
        usage()

    if not success:
        print(errortxt)


def parse_cmd_save(args):
    taskname = args[-2]
    minutes = get_minutes(args[-1])
    if update_task_summary(taskname, minutes):
        log_entry(taskname, minutes)


def get_minutes(timestr):
    re_minutes = re.compile(r"^\d+[mM]?$")
    re_hours = re.compile(r"^\d+(\.\d\d?)?[hH]$")
    re_HandM = re.compile(r"^\d+[hH]\d\d?[mM]?$")

    if re_minutes.match(timestr):
        timestr = timestr.lower().split("m")[0]
        return int(timestr)
    elif re_hours.match(timestr):
        timestr = timestr.lower().split("h")[0]
        return int(round(60 * float(timestr)))
    elif re_HandM.match(timestr):
        timestr = timestr.lower().replace("m", "")
        hours, minutes = (int(x) for x in timestr.split("h"))
        return 60 * hours + minutes
    else:
        return 0


def minutes_to_hours_and_minutes(minutes): # TODO make a --list, -l command and use this to make times more human-readable!
    minutes = int(minutes)
    hours, minutes = minutes // 60, minutes % 60
    if hours == 0:
        return str(minutes)
    else:
        return str(hours) + "h" + str(minutes)
        

### Main ###
parse_args()
############

