# 🐍 Python Trojan Simulation (Educational Project)

## 📌 Overview
This project is an **educational trojan simulation** developed in Python as part of an academic programming module.  
It demonstrates how real-world malware operates at a **behavioral and architectural level**, with the goal of improving understanding of malware analysis, detection, and defensive cybersecurity techniques.

The project includes a **simple game application** that acts as a launcher while the simulated trojan executes silently in the background.

---

## ⚠️ Disclaimer
> **This project is strictly for educational and academic purposes only.**

- Not intended for real-world deployment or malicious use  
- Must only be executed in **isolated environments** (VMs / sandboxes)  
- The author assumes **no responsibility** for misuse  
- Created to study malware behavior for **defensive security learning**

---

## 🎯 Project Objectives
- Understand trojan-based malware architecture  
- Study Command & Control (C2) communication  
- Explore anonymized networking techniques  
- Learn encryption, payload protection, and execution flow  
- Simulate common malware capabilities for **analysis and detection**

---

## 🧠 Key Concepts Demonstrated
- Client–server (C2) architecture  
- Encrypted communication channels  
- TOR-based anonymized networking  
- Executable payload encryption and runtime decryption  
- Background execution via a legitimate application  
- Multi-client management and lifecycle control  

---

## 🧩 Features & Capabilities

### 🔗 Networking & Communication
- Remote **Command & Control (C2)** communication
- Operates across different networks using an **anonymizing network (TOR)**
- Encrypted data transmission between client and server
- **Multi-client support** (simultaneous infected clients)
- Centralized command dispatching

---

### 🧠 C2 Server Capabilities
- Handles **multiple connected clients concurrently**
- Maintains a registry of active clients
- Automatically detects disconnected or inactive clients
- **Cleans up dead clients** to maintain server stability and accuracy
- Thread-safe client management

---

### 📁 File Management
- **File upload** from server to client
- **File download / exfiltration** from client to server
- Controlled file transfer mechanisms
- Demonstrates data exfiltration concepts used in malware analysis

---

### 🖥️ System Interaction
- Remote command execution (predefined and controlled)
- System information gathering (OS, user, environment details)
- Screenshot capturing

---

### 🎥 Surveillance Simulation
- **Keylogging** (keyboard input capture simulation)
- **Webcam capture**
- **Microphone / voice recording**
- Input and media monitoring for analysis purposes

> These features are included strictly to study how such behavior is detected and prevented in real systems.

---

### 🔐 Payload Protection
- The trojan client (`trojan.py`) is converted into a **standalone executable**
- The executable is encrypted using a custom `encrypte` function
- Demonstrates payload obfuscation and protected storage concepts

---

### 🎮 Game-Based Execution Trigger
- A **simple game** is included in the project
- When the game is launched:
  - The encrypted executable is decrypted at runtime
  - The trojan executes silently in the background
- Simulates malware hidden within legitimate-looking applications

---

### 🧹 Execution Control & Cleanup
- Controlled execution lifecycle
- Graceful shutdown handling
- Optional self-removal / cleanup mechanisms for lab safety

---

## 🗂️ Project Structure (Example)
```
project/
│── server.py        # C2 server (multi-client management)
│── trojan.py        # Trojan client logic
│── game/            # Simple game launcher
│── utils/           # Encryption & helpers
│── README.md
```

---

## ⚙️ Technologies Used
- Python 3
- `socket`
- `threading`
- `cryptography`
- TOR networking (educational usage)
- OS, audio, and video handling libraries

---

## ▶️ Execution Environment
⚠️ **Important**:
- Run only in **virtual machines or sandboxed environments**
- Do NOT deploy on real systems or public networks
- Intended solely for controlled academic demonstrations

---

## 👤 Author
Developed as part of a **Python Programming / Cybersecurity academic module**.
