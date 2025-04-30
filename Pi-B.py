import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from rpi_rf import RFDevice
import time
import serial

BAUD_RATE = 9600
SERIAL_PORT = "/dev/ttyUSB0"

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Serial error: {e}")

tx = RFDevice(17)
tx.enable_tx()
tx.tx_repeat = 15
protocol = 1
pulselength = 350
syn = 1001

# ----------------------- GUI SETUP -------------------------
root = tk.Tk()
root.title("RF Receiver")
root.geometry("800x480")
root.configure(bg="#ADD8E6")  # Light blue background

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#ADD8E6", font=("Arial", 20), padding=10)
style.configure("TButton", font=("Arial", 16), padding=6)

receivingState = False
handshakeState = False

# Sensor Labels Block
sensor_frame = ttk.Frame(root)
sensor_frame.pack(pady=20)

temp_label = ttk.Label(sensor_frame, text="Temperature: --.-F")
temp_label.grid(row=0, column=0, padx=27, pady=10)

humi_label = ttk.Label(sensor_frame, text="Humidity: --.-%")
humi_label.grid(row=0, column=1, padx=30, pady=10)

press_label = ttk.Label(sensor_frame, text="Pressure: ---- hPa")
press_label.grid(row=0, column=2, padx=27, pady=10)

time_label = ttk.Label(root, text="Last Update: --/--/---- --:--:--", font=("Arial", 14))
time_label.pack(pady=5)

# Buttons
handshakeStart = ttk.Button(root, text="Start Handshake", command=lambda: start_handshake())
handshakeStart.pack(pady=15)

shakeLabel = ttk.Label(root, text="----------[SESSION DISCONNECTED]----------", font=("Arial", 12))
shakeLabel.pack(pady=5)

toggleReceive = ttk.Button(root, text="Toggle Receiving", command=lambda: toggle_receiving())
toggleReceive.pack(pady=10)
toggleReceive.config(state="disabled")

receiveLabel = ttk.Label(root, text="RECEIVING: OFF", font=("Arial", 12))
receiveLabel.pack(pady=5)

# -------------------- FUNCTIONAL CODE ----------------------

def send_code(code):
    print(f"TX: {code}")
    tx.tx_code(code, protocol, pulselength)

def wait_for_code(timeout=None):
    start = time.time()
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            try:
                value = int(line)
                print(f"RX: {value}")

                if 990 <= value < 1010 and handshakeState:
                    press = value
                    press_label.config(text=f"Pressure: {press} hPa")
                    time_label.config(text=f"Last Update: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    return value

                elif 600 <= value < 900:
                    temp = value / 10.0
                    temp_label.config(text=f"Temperature: {temp:.1f}F")
                    time_label.config(text=f"Last Update: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    return value

                elif 40 <= value < 80:
                    humi = value
                    humi_label.config(text=f"Humidity: {humi:.1f}%")
                    time_label.config(text=f"Last Update: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    return value

                elif value == syn + 1:
                    print(f"RX: {value}")
                    return value

            except ValueError:
                continue

        if timeout is not None and timeout > 0 and (time.time() - start) >= timeout:
            print("Timeout waiting for response.")
            return None
        time.sleep(0.1)

def start_handshake():
    global handshakeState
    if not handshakeState:
        print("Starting handshake...")
        handshakeStart.config(state="disabled")
        send_code(syn)
        print(f"Sent: {syn}")
        if wait_for_code() == (syn + 1):
            time.sleep(2)
            print(f"Got: {syn + 1}")
            send_code(syn + 2)
            print(f"Sent: {syn + 2}")
            time.sleep(7)
            shakeLabel.config(text="----------[SESSION CONNECTED]----------")
            toggleReceive.config(state="enabled")
            handshakeState = True
        else:
            print("No ACK received. Handshake failed.")
            handshakeStart.config(state="enabled")

def toggle_receiving():
    global receivingState
    if not receivingState and handshakeState:
        receivingState = True
        receiveLabel.config(text="RECEIVING: ON")
        receive()
    else:
        receivingState = False
        receiveLabel.config(text="RECEIVING: OFF")

def receive():
    global receivingState
    if not receivingState:
        return
    wait_for_code(timeout=None)
    root.after(100, receive)

def on_close():
    tx.cleanup()
    GPIO.cleanup()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()


