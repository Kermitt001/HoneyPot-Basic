import socket
import threading
import time
import uuid
import paramiko
from config.settings import settings
from storage.logger import event_logger
from storage.database import insert_session
from honeypot.shell import HoneypotShell

# Generate host key if not exists
HOST_KEY = paramiko.RSAKey.generate(2048)

class ServerInterface(paramiko.ServerInterface):
    def __init__(self, client_ip, client_port):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.client_port = client_port
        self.session_id = str(uuid.uuid4())
        self.username = None
        self.password = None

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        self.username = username
        self.password = password
        
        # Log attempt
        event_logger.log_event("auth_attempt", {
            "session_id": self.session_id,
            "ip": self.client_ip,
            "username": username,
            "password": password
        })

        # Allow specific credentials or random chance ? 
        # For this honeypot, we accept anything to log commands, 
        # or we could simulate failed login. 
        # Let's simple accept "root/root" or "admin/admin" for easy testing, 
        # or just ACCEPT ALL to get max interaction.
        # User requested "Capturar user/pass", let's accept everything to see what they do.
        
        # Record session start
        insert_session({
            "session_id": self.session_id,
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
            "src_ip": self.client_ip,
            "src_port": self.client_port,
            "client_version": "Unknown",
            "username": username,
            "password": password,
            "success": True
        })
        
        return paramiko.AUTH_SUCCESS

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

def handle_connection(client, addr):
    client_ip = addr[0]
    client_port = addr[1]
    print(f"Connection from {client_ip}:{client_port}")

    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    transport.local_version = settings.BANNER_TEXT
    
    server = ServerInterface(client_ip, client_port)
    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        return

    channel = transport.accept(20)
    if channel is None:
        return

    server.event.wait(10)
    if not server.event.is_set():
        channel.close()
        return

    channel.send("Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-150-generic x86_64)\r\n\r\n")
    
    # Start Shell interaction
    shell = HoneypotShell(server.session_id)
    
    try:
        while True:
            channel.send(shell.prompt)
            command = ""
            while True:
                # Basic char-by-char reading (simplified)
                char = channel.recv(1)
                if not char:
                    raise Exception("Disconnect")
                
                char = char.decode('utf-8', errors='ignore')
                
                if char == '\r': # Enter
                    channel.send('\r\n')
                    break
                elif char == '\x03': # Ctrl+C
                    channel.send('^C\r\n')
                    command = ""
                    break
                elif char == '\x7f': # Backspace
                    if len(command) > 0:
                        command = command[:-1]
                        channel.send('\b \b')
                else:
                    channel.send(char) # Echo
                    command += char
            
            output = shell.handle_command(command)
            if output == "EXIT":
                break
            channel.send(output.replace('\n', '\r\n'))

    except Exception:
        pass
    finally:
        channel.close()
        transport.close()

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((settings.BIND_ADDRESS, settings.SSH_PORT))
    sock.listen(100)
    print(f"Listening for connection on {settings.BIND_ADDRESS}:{settings.SSH_PORT}...")

    while True:
        try:
            client, addr = sock.accept()
            t = threading.Thread(target=handle_connection, args=(client, addr))
            t.start()
        except Exception as e:
            print(f"Error handling connection: {e}")

if __name__ == "__main__":
    from storage.database import init_db
    init_db()
    start_server()
