import socket,json,random,gevent
import time
from TCPpack import recvall,get_block,put_block
from gevent import monkey
import threading

#初始化数据
gameRound=0
serverDice = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}   #初始化服务器实际发送给客户端的所有点数对应的数目的键值对
clientSequence = {0:'',1:''}                        #利用循环的数组来实现对玩家的排序
saveClientDice={}                                   #保存玩家的名字对应的竞猜骰子号码
loser={}
def serviceClient(newSocket):
    global allplayer
    global gameRound
    global serverDice
    global clientSequence
    global saveClientDice

    # 接收请求
    while True:
        block=get_block(newSocket)
        block=json.loads(block.decode('utf-8'))

        #注册玩家
        if len(block)==1:
            print('注册玩家：',block)
            #发送点数
            dice=[]
            print('发送点数序列','......',end='')
            for i in range(5):
                singleDice=random.randint(1,6)
                serverDice[singleDice]=serverDice[singleDice]+1    # 记录发送给客户端的所有数字分别有多少个
                dice.append(singleDice)
            put_block(newSocket,json.dumps(dice).encode('utf-8'))
            print('发送点数序列成功')
        #记录玩家上报的点数
        elif len(block)==3:
            print('记录',block[0],'上报的点数',end='')
            gameRound=gameRound+1
            clientSequence[gameRound % 2]=block[0]   #记录顺序
            tempList=[]
            tempList.append(block[1])
            tempList.append(block[2])
            saveClientDice[block[0]]=tempList          #记录玩家名和对应的点数,比如报6个5,就把名字,6和5记下来
            print('点数记录成功')
            # 把当前的点数发给每一个客户端
            put_block(newSocket, json.dumps(saveClientDice).encode('utf-8'))

        #开奖
        elif len(block)==2:
            print("开奖")
            #计算实际点数和玩家上报的点数
            lastPlayer=clientSequence[(gameRound - 1) %2]                   #找到上家的名字

            #寻找上家报出的点数
            M2=10*(saveClientDice[lastPlayer])[0]+(saveClientDice[lastPlayer])[1]       #通过名字找到上家的点数
            M1=10*serverDice[(saveClientDice[lastPlayer][1])]+saveClientDice[lastPlayer][1]
            if M1<M2:
                print('输家是：',lastPlayer)
                put_block(newSocket,json.dumps(lastPlayer+'输').encode('utf-8'))
            else:
                print('输家是：', clientSequence[gameRound%2])
                put_block(newSocket, json.dumps(clientSequence[gameRound%2]+'输').encode('utf-8'))

            #此轮游戏结束，初始化数据
            gameRound = 0
            serverDice = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}   #初始化服务器实际发送给客户端的所有点数对应的数目的键值对
            clientSequence = {0: '', 1: '', 2: '', 3: ''}       #利用循环的数组来实现对玩家的排序
            saveClientDice = {}                                 #保存玩家的名字对应的竞猜骰子号码
            print('新的一局')
            continue


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
        print('创建新的套接字')
        gevent.spawn(serviceClient, clientSocket)


if __name__ == "__main__":
    main()
