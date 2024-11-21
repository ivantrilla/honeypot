#!/usr/bin/env python3

import re
import time
from store_db import Database

def grab_user(match, state):

    # create a dictionary that will store the users attempted on the last logging record
    users = {}

    for user in match:
        user  = user.replace("USER '", "")
        if state:
            user = user.replace("' logged in", "")
        else:
            user = user.replace("' failed login.", "")

        if user not in users:
            users[user] = 1
        else:
            users[user] += 1

    return users

def clear_file(file):

    # just empty the file contents
    with open(file, "w") as f:
        blank = ""
        f.write(blank)



def readlog(file):

    with open(file, "r") as f:
        content = f.read()

    # grabbing successful logs
    match = re.findall("USER \'\w+\' logged in", content)
    if match:
        users = grab_user(match, True)
        Database(users, "user")


    # grabbing failed logs
    match = re.findall("USER \'\w+\' failed login.", content)
    if match:
        fail_users = grab_user(match, False)
        Database(fail_users, "fail")
        
    # detect any attempts of downloading the bait file
    # we don't need to keep track of which user downloads the file since only admin will have enough privileges to do so
    # I just want to detect the amount of times someone downloads it.
    amount = len(re.findall("to_do.txt completed=1", content))
    if amount:
        downloads = {"amount": amount}
        Database(downloads, "download")
    

    # clear logs
    clear_file(file)

    # call recursively the readlog function to keep track of any changes, wait 5 seconds between update checks
    # sys.setrecursionlimit(n) can set how many times a function can call itself, the default value is 1000
    time.sleep(5)
    readlog(file)