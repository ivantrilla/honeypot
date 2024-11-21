import logging

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

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
logging.basicConfig(filename='./myftp.log', level=logging.INFO)

# start ftp server
server.serve_forever()