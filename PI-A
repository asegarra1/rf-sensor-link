import time
import serial
from rpi_rf import RFDevice
from sense_hat import SenseHat


TX_PIN = 17
SYN = 1001

tx = RFDevice(TX_PIN)
tx.enable_tx()
tx.tx_repeat = 15
protocol = 1
pulselength = 225

sense = SenseHat()
SERIAL_PORT = "/dev/ttyUSB0"  # Adjust as needed
BAUD_RATE = 9600

def send_code(code):
    print(f"TX: {code}")
    tx.tx_code(code, protocol, pulselength)

def wait_for_handshake(ser):
    print("Waiting for handshake from Pi B via Arduino...")
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            try:
                value = int(line)
                print(f"Arduino RF RX: {value}")
                if value == SYN:
                    time.sleep(3)
                    send_code(SYN + 1)  # ACK
                    time.sleep(1)
                    if(wait_for_handshake_two(ser)):
                        print("Handshake complete.")
                        return True
            except ValueError:
                continue

def wait_for_handshake_two(ser):
    print("Waiting for ACK from Pi B via Arduino...")
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            try:
                value = int(line)
                print(f"Arduino RF RX: {value}")
                if value == SYN+2:
                    return True
            except ValueError:
                continue
            
def read_sensor_data():
    #I2C Read each sensor
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    
    #Round and/or convert Values to desired units
    temp_f = int(((temp * 9/5) + 32) * 10)
    humidity_p = int(humidity)
    pressure_hp = int(pressure)
    return [temp_f, humidity_p, pressure_hp]

def configure_code(data):
    tmp_data = ""
    for i in data:
        tmp_data = str(i) + tmp_data
    return tmp_data

def relay_sensor_data():
    print("Sending Sense HAT sensor data to Pi B...")
    while True:
        data = read_sensor_data()
        for i in data:# Match Pi B decoder
            send_code(i)
            time.sleep(0.5)

try:
    print(f"Opening serial connection to Arduino on {SERIAL_PORT}...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    if wait_for_handshake(ser):
        time.sleep(5)
        relay_sensor_data()

except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    tx.cleanup()
