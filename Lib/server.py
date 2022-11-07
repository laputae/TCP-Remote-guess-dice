import socket,json,random,gevent
from gevent import monkey

serverDice={1:0,2:0,3:0,4:0,5:0,6:0}   #初始化服务器实际发送给客户端的所有点数对应的数目的键值对
clientDice={1:0,2:0,3:0,4:0,5:0,6:0}   #初始化玩家竞猜报给服务器的点数对应的数目的键值对
clientSquence=[]                       #利用循环的数组来实现对玩家的排序
allplayer=4                            #所有玩家人数
gameRound=0
def serviceClient(newSocket):
    global allplayer
    global clientSquence
    global serverDice
    global clientDice

    # 接收请求
    while True:
        while True:
            block=get_block(newSocket)
            block=json.loads(block.decode('utf-8'))
            if not block:
                continue
            #注册玩家
            elif len(block)==1:
                print(block)
                clientSquence[1]=block[0]
                #发送点数
                for i in range(5):
                    dice=[]
                    singleDice=random.randint(1,6)
                    serverDice[singleDice]=serverDice[singleDice]+1    # 记录发送给客户端的所有数字分别有多少个
                    dice.append(singleDice)
                    put_block(newSocket,json.dumps(dice).encode('utf-8'))
            #记录玩家上报的点数
            elif len(block)==3:
                clientDice[block[2]]=clientDice[block[2]]+block[1]
                #记录顺序
                #TODO
            #开奖
            elif block[1]=='open':
                print("开奖")
                #计算实际点数和玩家上报的点数
                #TODO
                break

def main():
    "服务器基本功能"
    monkey.patch_all()
    # 创建套接字
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定端口
    serverSock.bind(("", 6666))
    # 准备监听
    serverSock.listen(4)

    while True:
        # 等待客户端链接
        clientSocket, client_addr=serverSock.accept()
        # 为客户端服务
        gevent.spawn(serviceClient, clientSocket)


if __name__ == "__main__":
    main()
