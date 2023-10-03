import socket
import concurrent.futures
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def scan_port(ip, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except Exception as e:
        pass

def scan_ip(ip, ports, timeout):
    global open_ports
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_port = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            future.result()

def scan_button_clicked():
    target_ip = target_ip_entry.get()
    port_range = port_range_entry.get()
    timeout = float(timeout_entry.get())
    
    try:
        target_ip = socket.gethostbyname(target_ip)
    except socket.gaierror:
        messagebox.showerror("Error", "Invalid target IP address")
        return

    start_port, end_port = map(int, port_range.split('-'))
    ports_to_scan = range(start_port, end_port + 1)

    scan_ip(target_ip, ports_to_scan, timeout)
    
    if open_ports:
        result_window = tk.Toplevel(root)
        result_window.title("Scan Results")
        
        # Increase result label font size and add padding
        result_label = ttk.Label(result_window, text="Open ports:", font=("Arial", 14), foreground="green")
        result_label.pack(padx=10, pady=5)
        
        result_text = ', '.join(map(str, open_ports))
        result_text_label = ttk.Label(result_window, text=result_text, font=("Arial", 12))
        result_text_label.pack(padx=10, pady=5)
        
        copy_button = ttk.Button(result_window, text="Copy", command=lambda: root.clipboard_append(result_text))
        copy_button.pack(pady=10)
        
        copyright_label = ttk.Label(result_window, text="© 2023 Pooyan Azadparvar", font=("Arial", 10), foreground="gray")
        copyright_label.pack(pady=5)
    else:
        messagebox.showinfo("Result", "No open ports found")

# Create the main window
root = tk.Tk()
root.title("Port Scanner")

# Set fixed size for the main window
root.geometry("500x200")

# Create and configure input fields and labels
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), foreground="red", background="blue")

app_frame = ttk.Frame(root, padding=10)
app_frame.pack(fill="both", expand=True)

target_ip_label = ttk.Label(app_frame, text="Enter the target IP address or hostname:")
target_ip_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
target_ip_entry = ttk.Entry(app_frame)
target_ip_entry.grid(row=0, column=1, padx=10, pady=5)

port_range_label = ttk.Label(app_frame, text="Enter port range (e.g., 1-1000):")
port_range_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
port_range_entry = ttk.Entry(app_frame)
port_range_entry.grid(row=1, column=1, padx=10, pady=5)

timeout_label = ttk.Label(app_frame, text="Enter timeout for each port scan (in seconds):")
timeout_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
timeout_entry = ttk.Entry(app_frame)
timeout_entry.grid(row=2, column=1, padx=10, pady=5)

scan_button = ttk.Button(app_frame, text="Scan Ports", command=scan_button_clicked)
scan_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter main loop
root.mainloop()
