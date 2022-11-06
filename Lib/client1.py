import socket,json,time
import TCPpack
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
info={}
addr=("127.0.0.1",6666)

def main():
    global addr

    while True:
        addr=('127.0.0.1',6666)        # addr=("127.0.0.1",6666)
        print("连接服务器ing...")
        try:
            clientSocket.connect(addr)      #连接服务器
            break
        except:
            print("连接服务器失败，你输入的IP地址为: %s 请重新输入！"%addr[0])

    global info
    clientSocket.send('Alice')      #玩家注册
    chunk, _ = clientSocket.recv(1024).decode('utf-8')
    while True:
        while True:
            block=get_block(chunk)
            if not block:
                continue
            if type(json.loads(block))==list:
                print(json.loads(block))

        gamble=[]
        guess=input()
        guess=guess.split()
        gamble.append(int(guess[0]))
        gamble.append(int(guess[1]))
        info = json.dumps(gamble).encode("utf-8")
        put_block(clientSocket,json.dumps(dict_info).encode("utf-8"))
        while True:
            block=get_block(chunk)
            if not block:
                continue
            elif type(json.loads(block))==str:
                print(json.loads(block))
                break


if __name__ == "__main__":
    main()
