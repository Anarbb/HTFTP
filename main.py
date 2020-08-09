import http.server
import socketserver
import os
import sys
import socket
import logging
import threading
import platform
from time import sleep
from datetime import datetime
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import WindowsAuthorizer



def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def run_web_server(ADDR, PORT, DIRE):
    web_dir = DIRE
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer((ADDR, PORT), Handler) as httpd:
            print(f"[-] Serving at http://{ADDR}:{PORT}/")
            print(f"[-] Web local directory: {web_dir}")
            httpd.serve_forever()
    except OSError:
        print('HTTP port already in use')


def run_ftp_server(ADDR, PORT):
    logging_path = os.path.join(os.path.dirname(__file__), 'ftp_logs')
    now = datetime.now()
    current_time_file = now.strftime("%Y%m%d%H%M%S")
    current_time_logging = now.strftime("%Y-%m-%d-%H-%M-%S")
    handler = FTPHandler
    authorizer = WindowsAuthorizer()
    handler.authorizer = authorizer
    handler.log_prefix = f'[{current_time_logging}] %(username)s - %(remote_ip)s'
    if os.path.exists(logging_path):
        logging.basicConfig(
            filename=logging_path + f"/log{current_time_file}.txt", level=logging.INFO)
    else:
        os.makedirs(logging_path)
        logging.basicConfig(
            filename=logging_path + f"/log{current_time_file}.txt", level=logging.INFO)
    sleep(8)
    print(f'[-] Serving FTP server at {ADDR}:{PORT}')
    server = FTPServer((ADDR, PORT), handler)
    server.serve_forever()


def http_only(ADDR):
    try:
        HTTP_PORT = int(input('HTTP port > '))
        if HTTP_PORT > 65535:
            print("Invalid port number.")
            HTTP_PORT = None
            quit()
        else:
            pass
    except ValueError:
        print("Invalid port number.")
        quit()
    HTTP_DIRE = input('HTTP working directory > ')
    HTTP_DIRE = os.path.join(os.path.dirname(__file__), HTTP_DIRE)
    if os.path.exists(HTTP_DIRE):
        os.chdir(HTTP_DIRE)
        pass
    else:
        try:
            os.makedirs(HTTP_DIRE)
            os.chdir(HTTP_DIRE)
        except OSError:
            print("Invalid folder name")
            quit()
    http_thread = threading.Thread(
        target=run_web_server, args=(ADDR, HTTP_PORT, HTTP_DIRE))
    http_thread.start()


def ftp_only(ADDR):
    try:
        FTP_PORT = int(input('FTP port > '))
        if FTP_PORT > 65535:
            print("Invalid port number.")
            quit()
        else:
            pass
    except ValueError:
        print("Invalid port number.")
        quit()
    ftp_thread = threading.Thread(target=run_ftp_server, args=(ADDR, FTP_PORT))
    ftp_thread.start()


def guid():
    print('''
Pretty meh web server mostly made for home use like a local webserver on an old machine to host movies and such
it pretty simple to use only enter your http working directory, and the FTP is global as in will show all the files on that user's personal folder
your FTP login credentials are the same as your Windows login credentials (for security reasons)
if you have no password set there won't be a password on the FTP so it's reccomended to have one.

- Unix and Linux systems FTP support is in the works
- PHP support is in the works\n
    ''')
    run()


def run():
    ADDR = get_ip()
    print("Type 'help' for info\n")
    print('1) HTTP Only\n2) FTP Only\n3) HTTP and FTP')
    user_in = input('> ').lower()
    if user_in == '1':
        http_only(ADDR)
    elif user_in == '2':
        ftp_only(ADDR)
    elif user_in == '3':
        ftp_only(ADDR)
        http_only(ADDR)
    else:
        guid()


if __name__ == '__main__':
    run()
