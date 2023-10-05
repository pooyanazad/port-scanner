#port-scanner-without-gui-v2
import socket
import concurrent.futures

def scan_port(ip, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} on {ip} is open")
        sock.close()
    except Exception as e:
        pass

def scan_ip(ip, ports, timeout):
    print(f"Scanning {ip}...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use ThreadPoolExecutor to scan ports concurrently
        future_to_port = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            future.result()  # Get the result or handle exceptions here

def get_user_input():
    target_ip = input("Enter the target IP address or hostname: ")
    port_range = input("Enter port range (e.g., 1-1000): ")
    timeout = float(input("Enter timeout for each port scan (in seconds): "))
    return target_ip, port_range, timeout

if __name__ == "__main__":
    target_ip, port_range, timeout = get_user_input()

    try:
        target_ip = socket.gethostbyname(target_ip)
    except socket.gaierror:
        print("Invalid target IP address.")
        sys.exit(1)

    start_port, end_port = map(int, port_range.split('-'))
    ports_to_scan = range(start_port, end_port + 1)

    scan_ip(target_ip, ports_to_scan, timeout)
