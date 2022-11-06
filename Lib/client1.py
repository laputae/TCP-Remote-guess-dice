import socket,json,time
import TCPpack

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr=("127.0.0.1",6666)
info=[]

def main():
    global addr
    global info
    while True:
        addr=('127.0.0.1',6666)        # addr=("127.0.0.1",6666)
        print("连接服务器ing...")
        try:
            clientSocket.connect(addr)      #连接服务器
            break
        except:
            print("连接服务器失败，你输入的IP地址为: %s 请重新输入！"%addr[0])
    info[0]='Alice'
    clientSocket.send(json.dumps(info).encode('utf-8'))      #玩家注册
    chunk, _ = clientSocket.recv().decode('utf-8')
    #打印服务器发来的点数
    while True:
        while True:
            block=get_block(chunk)
            if not block:
                continue
            if type(json.loads(block))==list:
                print(json.loads(block))
                break
        #竞猜点数
        info=[]
        while True:
            guess=input()
            if guess=='open':
                info
                put_block(clientSocket,guess)
                break
            else:
                guess=guess.split()
                info.append(int(guess[0]))
                info.append(int(guess[1]))
            info = json.dumps(info).encode("utf-8")
            put_block(clientSocket,info)
        #打印输赢消息
        while True:
            block=get_block(chunk)
            if not block:
                continue
            elif type(json.loads(block))==str:
                print(json.loads(block))
                break


if __name__ == "__main__":
    main()
