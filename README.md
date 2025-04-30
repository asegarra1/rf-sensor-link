# 📡 Raspberry Pi RF Sensor Network (433 MHz) 🌡️💧📊

## 🔍 Project Overview

This project implements a **low-cost**, **real-time**, wireless sensor data transmission system using:

- 🧠 **Two Raspberry Pi units**  
- 📶 **433 MHz RF modules**  
- 🔌 **Arduino boards as RF decoders**  
- 🟨 **Sense HAT for environmental sensing**

🌐 **Pi A** collects live environmental data using the Sense HAT and transmits it via RF after completing a custom **3-phase handshake protocol** with  
🖥️ **Pi B**, which listens via Arduino, decodes the stream, and visualizes the readings using a Python `tkinter` GUI.

🎯 This project demonstrates practical use of:
- Embedded communication protocols
- Sensor integration and data formatting
- Asynchronous serial communication
- Lightweight real-time GUIs
- RF-based point-to-point IoT messaging

---

## 🛠️ Hardware Configuration

### 🔴 Pi A — *Sensor Transmitter*
- 🧠 Raspberry Pi (with GPIO and USB support)
- 🟨 Sense HAT (I2C interface for Temp, Humidity, Pressure)
- 📶 433 MHz RF Transmitter (connected to GPIO 17)
- 🔌 Arduino (connected via USB for serial decoding)
- 💻 Role:  
  - Waits for RF handshake via Arduino  
  - Collects sensor data  
  - Transmits data in sequence over RF

### 🟢 Pi B — *Receiver & Display Node*
- 🧠 Raspberry Pi
- 📶 433 MHz RF Transmitter (used solely for initiating the handshake)
- 🔌 Arduino (RF receiver wired to digital input, connected to Pi via USB)
- 🖥️ Tkinter GUI (Temperature, Humidity, Pressure, Session Status)
- 💻 Role:  
  - Initiates handshake  
  - Listens for serial input from Arduino  
  - Decodes values and displays in real time

---

## 🔁 Communication Protocol 📡

The project uses a **custom, three-step handshake protocol** before data transmission begins, helping validate device readiness and connection integrity.

### 🤝 Handshake Process:

| Step | Device | Action                      | Code Sent |
|------|--------|-----------------------------|-----------|
| 1️⃣   | Pi B   | Sends handshake request     | `1001`    |
| 2️⃣   | Pi A   | Sends acknowledgment        | `1002`    |
| 3️⃣   | Pi B   | Final confirmation sent     | `1003`    |

### 📊 Sensor Data Encoding & Decoding:

After a successful handshake, Pi A transmits the following:

- 🌡️ **Temperature** (°F × 10): Encoded as an integer (e.g., `728` = 72.8°F)
- 💧 **Humidity** (%): Integer (e.g., `53`)
- 🧭 **Pressure** (hPa): Integer (e.g., `1006`)

Pi B’s decoding logic uses numeric ranges to identify the data type:

| Value Range | Type       |
|-------------|------------|
| 600–900     | Temperature |
| 40–80       | Humidity    |
| 990–1010    | Pressure    |
| 1001–1003   | Handshake codes |

Timestamps are appended to each update in the GUI for traceability 🕒.

---

## 🖼️ GUI Features (Pi B)

The display interface is built using Python’s `tkinter` module and includes:

- ✅ **Real-time updates** on:
  - Temperature
  - Humidity
  - Pressure
- 📆 **Last update timestamp**
- 🔘 **Start Handshake** button to initiate session
- 🔁 **Toggle Receiving** button to start/stop stream
- 🟢🔴 Status labels for session connection and receiving state

---

## 📦 Software Requirements

### Install on **both Pis**:
pip install rpi-rf pyserial


