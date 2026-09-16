import socket
import threading
from protocol import send_message, recv_message


clients = {}
clients_lock = threading.Lock()


def handle_client(client_sock):
    username = 'Неизвестно'
    try:
        while True:
            result = recv_message(client_sock)
            
            if result is None:
                break
            
            command, payload = result
            text_payload = payload.decode('utf-8')
            
            if command == 'JOIN':
                with clients_lock:
                    clients[client_sock] = text_payload
                    username = text_payload
                    
            elif command == 'TEXT':
                with clients_lock:
                    sender = clients.get(client_sock, 'Неизвестно')
                    msg_to_send = f'{sender}: {text_payload}'
                    
                    for other_sock in clients:
                        if other_sock != client_sock:
                            try:
                                send_message(other_sock, 'TEXT', msg_to_send.encode('utf-8'))
                            except (ConnectionResetError, BrokenPipeError):
                                pass
                                
            elif command == 'LIST':
                with clients_lock:
                    current_users = ','.join(clients.values())
                send_message(client_sock, "LIST", f"Users online: {current_users}".encode('utf-8'))
            
            elif command == 'QUIT':
                break
            
            else:
                send_message(client_sock, 'ERROR', b'Unknown command')
                
    except (ConnectionResetError, BrokenPipeError):
        print(f"[СЕРВЕР] Клиент {username} отключился аварийно.")
        
    finally:
        with clients_lock:
            if client_sock in clients:
                username = clients[client_sock]
                del clients[client_sock]
                

        quit_msg = f"Пользователь {username} покинул чат"
        with clients_lock:
            for other_sock in clients:
                try:
                    send_message(other_sock, 'TEXT', quit_msg.encode('utf-8'))
                except (ConnectionResetError, BrokenPipeError):
                    pass
                    

        client_sock.close()
        
        
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 5000))
    server_socket.listen()
    print("[СЕРВЕР] Запущен...")
    
    while True:
        client_sock, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_sock,))
        client_thread.start()      