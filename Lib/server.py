import socket,json,random,gevent
from gevent import monkey

serverDice={1:0,2:0,3:0,4:0,5:0,6:0}   #初始化服务器实际发送给客户端的所有点数对应的数目的键值对
clientDice={1:0,2:0,3:0,4:0,5:0,6:0}   #初始化玩家竞猜报给服务器的点数对应的数目的键值对
clientSquence=[]                       #利用循环的数组来实现对玩家的排序
allplayer=4                            #所有玩家人数

def serviceClient(newSocket):
    global allplayer
    global clientSquence
    global serverDice
    def sendToclient(dict_info):
        newSocket.send(json.dumps(dict_info).encode("utf-8"))

    # 接收请求
    while True:
        while True:
            block=get_block(newSocket)
            if not block:
                continue
            if type(json.loads(block))==str:
                print(json.loads(block))

        for i in range(5):
            dice=[]
            singleDice=random.randint(1,6)
            serverDice[singleDice]=serverDice[singleDice]+1    # 记录发送给客户端的所有数字分别有多少个
            dice.append(singleDice)

        put_block(newSocket,dice)
        recvdata=newSocket.recv(1024).decode("utf-8")
        data=json.loads(recvdata)
        clientSquence[]=''
        if data[1]!='open':
            global clientDice
            print(data)
            clientDice[data[2]]=clientDice[data[2]]+data[1]     #记录玩家上报的点数的数目
        else:
             data[0]       #判断胜负



def main():
    "服务器基本功能"
    monkey.patch_all()
    # 创建套接字
    severSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口
    severSock.bind(("", 6666))
    # 准备监听
    severSock.listen(4)

    while True:
        # 等待客户端链接
        clientSocket, client_addr=severSock.accept()
        # 为客户端服务
        gevent.spawn(serviceClient, clientSocket)


if __name__ == "__main__":
    main()
