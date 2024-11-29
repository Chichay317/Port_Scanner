import socket
from queue import Queue
import threading

host = "127.0.0.1"
queue = Queue()
opened_ports = []

def scan_ports(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, port))
        service_banner = get_service_banner(sock)
        return True, service_banner
    except:
        return False, None

def get_service_banner(sock):
    try:
        banner = sock.recv(1024).decode().strip()
        return banner if banner else "No banner"
    except:
        return "No banner"

def fetch_ports(mode):
    if mode == 1:
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2:
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter your ports (separate by space):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        result, banner = scan_ports(port)
        if result:
            print(f"Port {port} is open! Service: {banner}")
            opened_ports.append((port, banner))

def run_scanner(threads, mode):

    fetch_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("\nOpen ports and services:")
    for port, banner in opened_ports:
        print(f"Port {port}: {banner}")

run_scanner(100, 1)

