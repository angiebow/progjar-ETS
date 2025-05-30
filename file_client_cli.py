import socket
import json
import base64
import logging
import os

server_address = ('127.0.0.1', 6666)

def send_command(command_str="", is_binary=False):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"Connecting to {server_address}")
    try:
        if isinstance(command_str, str):
            command_bytes = command_str.encode()
        else:
            command_bytes = command_str
        logging.warning(f"Sending message")
        sock.sendall(command_bytes)
        data_received = ""
        while True:
            data = sock.recv(4096)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received.strip())
        logging.warning("Data received from server")
        return hasil
    except Exception as e:
        logging.warning(f"Error during data receiving: {e}")
        return False
    finally:
        sock.close()

# LIST
def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("Daftar file:")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal mendapatkan daftar file")
        return False

# GET / Download
def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as fp:
            fp.write(isifile)
        print(f"Berhasil mengunduh file: {namafile}")
        return True
    else:
        print(f"Gagal mengunduh file: {filename}")
        return False

# UPLOAD
def remote_upload(filepath=""):
    if not os.path.exists(filepath):
        print(f"File {filepath} tidak ditemukan.")
        return False
    try:
        filename = os.path.basename(filepath)
        with open(filepath, 'rb') as f:
            filedata = f.read()
        encoded = base64.b64encode(filedata).decode()
        payload = {
            "command": "UPLOAD",
            "filename": filename,
            "filedata": encoded
        }
        payload_str = json.dumps(payload) + "\r\n\r\n"
        hasil = send_command(payload_str)
        if hasil and hasil['status'] == 'OK':
            print(f"File {filename} berhasil diupload.")
            return True
        else:
            print(f"Gagal upload file {filename}")
            return False
    except Exception as e:
        print(f"Error saat upload: {e}")
        return False

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--get', type=str)
    parser.add_argument('--upload', type=str)
    args = parser.parse_args()

    if args.list:
        remote_list()
    if args.get:
        remote_get(args.get)
    if args.upload:
        remote_upload(args.upload)