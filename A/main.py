
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import socket
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
def server_program():
    k1 = b'`\xb0\x1d\x80\xf9\x90\xb81\x9a\xb7\x10\x15\xd5/\x99\x83'
    k2 = b'\x9b\xba\xc1\x0b\xcd\xf1\xefd\xc3\xd7n&\xc0\x8d\x19l'
    k3 = b'\x14\xf4E\xdfA\xc2\x82\x08d\x14\x96\xfbo\xebn\xe4'
    iv = b'\x14\xf4E\xdfA\xc2\x82\x08d\x14\x96\xfbo\xebn\xe4'
    q=10
    fileObject = open("text.txt", "r")
    dat = fileObject.read()
    stringg=dat
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        stringg = dat
        data = input(' -> ')
        if(data == "CBC"):
            conn.send(data.encode())
            cipher = AES.new(k3, AES.MODE_CBC,IV=iv)
            ciphertext = cipher.encrypt(k1)
            conn.send(ciphertext)
            iv1=iv
            index=0
            while(len(stringg)>16):
                if index==9:
                    index=0
                    conn.send("keyRefreshhhhhhh".encode())
                    k1=get_random_bytes(16)
                    cipher = AES.new(k3, AES.MODE_CBC, IV=iv)
                    ciphertext = cipher.encrypt(k1)
                    conn.send(ciphertext)
                    print(k1)
                cipher = AES.new(k1, AES.MODE_CBC,IV=iv1)
                str1=stringg[0:16]
                stringg=stringg[16:]
                print(str1)
                str1 = bytes(str1, 'utf-8')
                send = byte_xor(str1,iv1)
                ciphertext = cipher.encrypt(send)
                iv1=ciphertext
                conn.send(ciphertext)
                index+=1

            conn.send("Done".encode())

        if (data == "OFB"):
            conn.send(data.encode())
            cipher = AES.new(k3, AES.MODE_CBC, IV=iv)
            ciphertext = cipher.encrypt(k2)
            conn.send(ciphertext)
            iv1 = iv
            index=0

            while (len(stringg) > 16):
                if index==9:
                    index=0
                    conn.send("keyRefreshhhhhhh".encode())
                    k2=get_random_bytes(16)
                    cipher = AES.new(k3, AES.MODE_CBC, IV=iv)
                    ciphertext = cipher.encrypt(k2)
                    conn.send(ciphertext)
                    print(k1)
                cipher = AES.new(k2, AES.MODE_CBC, IV=iv1)
                str1 = stringg[0:16]
                stringg = stringg[16:]
                print(str1)
                ciphertext = cipher.encrypt(iv1)
                iv1 = ciphertext
                str1 = bytes(str1, 'utf-8')
                send = byte_xor(str1, ciphertext)
                conn.send(send)
                index+=1

            conn.send("Done".encode())



       # conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()