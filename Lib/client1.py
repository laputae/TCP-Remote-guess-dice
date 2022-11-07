import socket,json,time
import TCPpack

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    put_block(clientSocket,json.dumps(info).encode('utf-8'))      #玩家注册
    #打印服务器发来的点数
    while True:

        while True:
            block=get_block(clientSocket)
            block=json.loads(block.decode('utf-8'))
            if not block:
                continue
            if type(block)==list:
                print(block)
                break
        #竞猜点数
        info=[]
        while True:
            #查看是否开奖
            block=get_block(chunk)
            block = json.loads(block.decode('utf-8'))
            if not block:
                print("")
            elif type(block)==str:
                print(block)
                break
            #输入点数
            guess=input()
            if guess=='open':
                info[1]=guess
                put_block(clientSocket,json.dumps(info).encode('utf-8'))
                break
            else:
                guess=guess.split()
                info[1]=(int(guess[0]))
                info[2]=(int(guess[1]))
                put_block(clientSocket,json.dumps(info).encode("utf-8"))


if __name__ == "__main__":
    main()
