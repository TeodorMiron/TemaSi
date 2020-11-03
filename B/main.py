import socket
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
def client_program():
    k3 = b'\x14\xf4E\xdfA\xc2\x82\x08d\x14\x96\xfbo\xebn\xe4'
    iv = b'\x14\xf4E\xdfA\xc2\x82\x08d\x14\x96\xfbo\xebn\xe4'
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
      # take input
    ok=1
    while ok!=0:
        data=client_socket.recv(1024)
        if(data.decode()=="CBC"):
            data = client_socket.recv(16)

            cipher = AES.new(k3, AES.MODE_CBC,IV=iv)
            plaintext = cipher.decrypt(data)
            k1=plaintext
            iv1=iv
            ok1=True
            while(ok1):
                data = client_socket.recv(16)
                if(data=="keyRefreshhhhhhh".encode()):
                    data = client_socket.recv(16)
                    cipherr = AES.new(k3, AES.MODE_CBC, IV=iv)
                    plaintext = cipherr.decrypt(data)
                    k1=plaintext
                elif(data!=b"Done"):
                    cipher = AES.new(k1, AES.MODE_CBC, IV=iv1)
                    plaintext = cipher.decrypt(data)
                    recive=byte_xor(plaintext,iv1)
                    iv1=data
                    print(recive.decode())
                else:
                    ok1=False

        if (data.decode() == "OFB"):
            data = client_socket.recv(16)

            cipher = AES.new(k3, AES.MODE_CBC, IV=iv)
            plaintext = cipher.decrypt(data)
            k2 = plaintext
            iv1 = iv
            ok1 = True
            while (ok1):

                data = client_socket.recv(16)
                if (data == "keyRefreshhhhhhh".encode()):
                    data = client_socket.recv(16)
                    cipherr = AES.new(k3, AES.MODE_CBC, IV=iv)
                    plaintext = cipherr.decrypt(data)
                    k2 = plaintext
                elif (data != b"Done"):
                    cipher = AES.new(k2, AES.MODE_CBC, IV=iv1)
                    plaintext = cipher.encrypt(iv1)
                    recive = byte_xor(plaintext, data)
                    iv1 = plaintext
                    print(recive.decode())
                else:
                    ok1 = False

       # message = input(" -> ") # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()