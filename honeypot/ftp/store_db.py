#!/usr/bin/env python3
import mariadb
import datetime
import sys

class Database:
    # data will store only one user, and the amount of times that has been logged within that period of ~5s
    # the action variable can hold 3 different values: user, fail, download
    def __init__(self, data, action):

    
        try: 

            conn = mariadb.connect(
                    user="user1",
                    password="password1",
                    host="127.0.0.1",  
                    port=3306,
                    database="Logs"
                    )
            
            cur = conn.cursor()

            # depending on the action it'll have to save different stuff

            if action == "user":
                for user, amount in data.items():
                    self.user = user
                    self.amount = amount
                self.successful_login(cur)

            elif action == "download":
                self.amount = data["amount"]
                self.download(cur)

            conn.commit()


        # print and log any kind of error message pops up 

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

            with open("mysql_error.log", "a") as f:
                f.write(f"Error connecting to MariaDB Platform: {e}\n")
            sys.exit(1)

        # Ensure the connection is closed
        finally:
            if conn:
                cur.close()
                conn.close()

    def successful_login(self, cur):

        # just grab a dateframe of last login

        dateframe =  str(datetime.datetime.now())
  
        # I previosuly need to fetch amount of previous logins to add the new ones    
        # admin will have ID 1
        if self.user == "admin":

            cur.execute("SELECT amount FROM FTPSuccess WHERE ID=1")
            for elem in cur:
                amount = elem[0]

            self.amount+=amount
            cur.execute("update FTPSuccess set amount = ?, last_time = ? where Id = 1", (self.amount, dateframe)) 
                    
        #anonymous user will have ID 2
        else:
            cur.execute("SELECT amount FROM FTPSuccess WHERE ID=2")
            for elem in cur:
                amount = elem[0]

            self.amount+=amount
            cur.execute("update FTPSuccess set amount = ?, last_time = ? where Id = 2", (self.amount, dateframe)) 
                    

    def download(self, cur):
  
        dateframe =  str(datetime.datetime.now())

        cur.execute("SELECT amount FROM BaitDownload")
        for elem in cur:
            amount = elem[0]

        self.amount+=amount
        cur.execute("update BaitDownload set last_time = ?, amount = ?", (dateframe, self.amount))


"""
This is how the mariadb database was created, it's left here as comment to have an idea of its schema and use:

create database Logs;
use Logs;

CREATE USER 'user1'@localhost IDENTIFIED BY 'password1';
GRANT ALL PRIVILEGES ON Logs.* TO 'user1'@localhost IDENTIFIED BY 'password1';


insert into FTPSuccess (ID, username, amount, last_time) values (1, "anonymous", 0, "random");
insert into FTPSuccess (ID, username, amount, last_time) values (2, "anonymous", 0, "random");


"""

