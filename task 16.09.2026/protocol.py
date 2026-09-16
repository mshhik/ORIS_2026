import struct
import socket


MAX_MESSAGE_SIZE = 10 * 1024 * 1024
HEADER_SIZE = 8

def recv_exact(sock, size):
    data_buffer = b''
    while len(data_buffer) < size:
        chunk = sock.recv(size - len(data_buffer))
        
        if not chunk:
            raise ConnectionError('Соединение закрыто')
        
        data_buffer += chunk
    return data_buffer


def send_message(sock, command: str, payload: bytes):
    cmd_bytes = command.encode('ascii')
    len_bytes = struct.pack('!I', len(payload))
    packet = cmd_bytes + len_bytes + payload
    sock.sendall(packet)
    

def recv_message(sock):
    try:
        header = recv_exact(sock, 8)
    except ConnectionError:
        return None
    command = (header[:4]).decode('ascii').strip()
    len_bytes = (header[4:8])
    payload_len = struct.unpack('!I', len_bytes)[0]
    if payload_len > MAX_MESSAGE_SIZE:
        raise ValueError('Ограничение размера')
    
    payload = recv_exact(sock, payload_len)
    
    return command, payload