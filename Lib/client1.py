import socket,json,time,re
from TCPpack import recvall,get_block,put_block

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#clientSocket.setblocking(False)
addr=("127.0.0.1",6666)

def main():

    info=[]
    global addr
    while True:
        print('使用默认的本机IP地址：127.0.0.1')
        addr=('127.0.0.1',6666)        # addr=("127.0.0.1",6666)
        print("连接服务器ing...")
        try:
            clientSocket.connect(addr)      #连接服务器
            break
        except:
            print("连接服务器失败，你输入的IP地址为: %s 请重新输入！"%addr[0])

    #打印服务器发来的点数
    while True:
        info.append('Alice')
        put_block(clientSocket,json.dumps(info).encode('utf-8'))      #玩家注册
        time.sleep(1)
        try:
            block=get_block(clientSocket)
            block=json.loads(block.decode('utf-8'))
            if (type(block)==list) and (len(block)==5):
                print('接收到的点数是：',block)

            #竞猜点数
            while True:
                info = []
                info.append('Alice')
                print('请输入竞猜点数,输入open则开奖：')
                guess=input()
                if guess=='open':
                    info.append(guess)
                    put_block(clientSocket,json.dumps(info).encode('utf-8'))

                elif re.findall(r'\A\d\s{1}?\d\Z|\A\d{2}\s{1}?\d\Z',guess):
                    guess = guess.split()
                    if (int(guess[0]) <= 30) and (int(guess[1]) < 7):
                        info.append(int(guess[0]))
                        info.append(int(guess[1]))
                        put_block(clientSocket, json.dumps(info).encode("utf-8"))
                        print('你的点数已提交')

                    else:
                        print('输入不合法，请重新输入')
                        continue
                else:
                    print('输入不合法，请重新输入')
                    continue
                # 查看是否开奖
                block = get_block(clientSocket)
                block = json.loads(block.decode('utf-8'))
                if type(block) == str:
                    print('开奖信息为：', block, '下一局开始......')
                    info=[]
                    break

                else:
                    print(block)
        except EOFError:
            print('socket closed with {} bytes left')

if __name__ == "__main__":
    main()
