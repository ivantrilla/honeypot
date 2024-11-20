import socket

class Ftp:

    def __init__(self):
        
        port = 21
        ip = "localhost"
        self.user = ""
        self.password = ""
        self.domain = "ainslove.es"
        self.banner = f"""Connected to {self.domain}.
220 ProFTPD Server (Debian) [{ip}]
Name ({self.domain}): """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(1)
    
        print(f"Started listener on {ip}:{port}")
        
        self.conn, self.addr = s.accept()

    def listener(self):

        self.conn.recv(2048)

        self.conn.sendall(self.banner.encode()) 
        
        self.user = self.conn.recv(1024).decode()

        self.conn.sendall(f"331 Password required for {self.user}Password: ".encode())

        self.password = self.conn.recv(1024).decode()

        status = self.check_login(self.user, self.password)

        if status:
            self.conn.sendall("230 Login successful.\nftp: Remote system type is UNIX.\nUsing binary mode to transfer files.\nftp> ".encode())

            while True:
                self.conn.recv(1024)
                self.conn.send("ftp> ".encode())

        else:
            self.conn.sendall("530 Login incorrect.\nftp: Login failed\nftp>".encode())
            while True:
                self.conn.recv(1024)
                self.conn.sendall("ftp> ".encode())
    


    @staticmethod
    def check_login(user, password):
        
        # check if anonymous login or admin:admin
        if user.strip() == "anonymous":
            return True
        elif user.strip() == "admin" and password.strip() == "admin":
            return True
        else:
            return False





def main():
    poc = Ftp()
    poc.listener()

if __name__ == "__main__":
    main()