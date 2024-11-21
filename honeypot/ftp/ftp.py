import logging
import time

from parse_logs import readlog
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def ftp_server():

    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define user admin:admin having full r/w permissions
    authorizer.add_user("admin", "admin", "./ftp_directory", perm="lr")

    # add anon user, he will only be able to list the files in the directory, but won't have enough privileges to interact :)
    authorizer.add_anonymous("./ftp_directory", perm="l")

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer


    # Define a customized banner (string returned when client connects)
    # I'm going to setup a banner to emulate a vulnerable version of ProFTPd vulnerable to RCE
    handler.banner =  "ProFTPD 1.3.5 Server (Debian)"



    # Instantiate FTP server class and listen on all interfaces, port 2121
    address = ('', 21)
    server = FTPServer(address, handler)


    # set a limit for connections
    # for now it can handle 10 simultaneous connections and it has been rate limited to 3 connections from a unique ip
    server.max_cons = 10
    server.max_cons_per_ip = 3

    # create a file on pwd to log everything
    logfile = './myftp.log'
    logging.basicConfig(filename=logfile, level=logging.INFO)

    # now we'll have to regularly check the logs to check for any logins or file downloads
    thread = threading.Thread(target=readlog, args=(logfile,))
    thread.daemon = True
    thread.start()

    # start ftp server
    server.serve_forever()

