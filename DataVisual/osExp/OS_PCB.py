class PCB(object):

    def __init__(self,name,arrival_time,burst_time,priority = 0):
        self.name = name
        self.arrival_time = arrival_time    #到达时间
        self.burst_time = burst_time        #服务时间
        self.priority = priority

        self.start_time = None              #开始时间
        self.runned_time = 0                #已运行时间
        self.finished_time = None           #结束时间

    def __str__(self):
        if self.runned_time != None and self.finished_time != None and self.start_time != None:
            return 'name:'+self.name + ' arrival:' + str(self.arrival_time) + ' burst:' + str(self.burst_time) +' start:' + str(self.start_time) + ' finish:' + str(self.finished_time) + ' runnned:' + str(self.runned_time) + ' priority:' + str(self.priority)+' T:'+str(self.T)+' W:'+str(self.W)
        else:
            return 'name:'+self.name + ' arrival:' + str(self.arrival_time) + ' burst:' + str(self.burst_time) + ' priority:' + str(self.priority)

    def initPCB(self):
        self.runned_time = 0
        self.finished_time = None
        self.start_time = None

class MultiQueue(object):

    def __init__(self,level):
        self.level = level
        self.queue = []
        self.nextQueue = None

    def __str__(self):
        return  'level:' + str(self.level)+' '+str(self.queue)+' '+str(self.nextQueue)

ready = []
block = []
running = None
finished = []
MAX_TIME = 100000
dis = lambda p: 'name:' + str(p.name) + ' arrival:' + str(p.arrival_time) + ' burst:' + str(p.burst_time) + ' runned:' + str(p.runned_time)
def disMultiQueue(queue):
    t = queue
    while t:
        print('Level: '+str(t.level))
        print(end='    ')
        for p in t.queue:
            print(dis(p),end='\n    ')
        t = t.nextQueue
        print()

def disList(l):
    for p in l:
        print(p)

def W_and_T(finished):
    sumT = 0
    sumW = 0
    for p in finished:
        sumT += p.T
        sumW += p.W
    print('平均周转时间'+str(sumT/len(finished)),'平均带权周转时间'+str(sumW/len(finished)))

def Priority():
    temp_ready = sorted(ready,key= lambda  p:p.priority, reverse=True)
    currTime = MAX_TIME
    for p in ready:
        if p.arrival_time < currTime:
            currTime = int(p.arrival_time)
    while temp_ready:
        for p in temp_ready:
            if p.arrival_time <= currTime:
                p.start_time = currTime
                p.finished_time = currTime + p.burst_time
                p.runned_time = p.finished_time - p.start_time
                p.T = p.finished_time - p.arrival_time
                p.W = p.T / p.runned_time
                print(p)
                currTime += p.burst_time
                temp_ready.remove(p)
                finished.append(p)
                break
    print('-------------------------END----------------------------')
    disList(finished)
    W_and_T(finished)
    finished.clear()

def FCFS():
    temp_ready = sorted(ready,key=lambda p:p.arrival_time,reverse=True)
    currTime = temp_ready[-1].arrival_time
    while temp_ready:
        pcb = temp_ready.pop()
        pcb.start_time = currTime
        pcb.finished_time = currTime + pcb.burst_time
        pcb.runned_time = pcb.finished_time - pcb.start_time
        pcb.T = pcb.finished_time - pcb.arrival_time
        pcb.W = pcb.T/pcb.runned_time
        currTime = currTime + pcb.burst_time
        finished.append(pcb)
    disList(finished)
    W_and_T(finished)
    finished.clear()
    for pcb in ready:
        pcb.initPCB()

def SJF():
    temp_ready = sorted(ready, key=lambda p:p.burst_time) #按服务时间从小到大排序
    currTime = MAX_TIME
    for pcb in temp_ready:
        if currTime > int(pcb.arrival_time):
            currTime = int(pcb.arrival_time)
    while temp_ready:
        for pcb in temp_ready:
            if pcb.arrival_time <= currTime:
                print(dis(pcb))
                pcb.start_time = currTime
                currTime = currTime + int(pcb.burst_time)
                pcb.finished_time = currTime
                pcb.runned_time = pcb.finished_time - pcb.start_time
                pcb.T = pcb.finished_time - pcb.arrival_time
                pcb.W = pcb.T/pcb.runned_time
                temp_ready.remove(pcb)
                finished.append(pcb)
                break
    print('----------------------------END--------------------------------------')
    disList(finished)
    W_and_T(finished)
    finished.clear()
    for p in ready:
        p.initPCB()

def TIME():
    temp_ready = sorted(ready,key=lambda p:p.arrival_time)
    do = 1
    currTime = MAX_TIME
    finished = []
    for pcb in temp_ready:
        if currTime > int(pcb.arrival_time):
            currTime = int(pcb.arrival_time)
    dis = lambda p:'name:'+str(p.name)+' arrival:'+str(p.arrival_time)+' burst:'+str(p.burst_time)+' runned:'+str(p.runned_time)

    while len(temp_ready) != len(finished):
        for p in temp_ready:
            if p.arrival_time <= currTime and (p not in finished):
                p.runned_time += do

                if p.start_time == None:
                    p.start_time = currTime
                if p.runned_time == p.burst_time:
                    p.finished_time = currTime
                    p.T = p.finished_time - p.arrival_time
                    p.W = p.T/p.runned_time
                    # 共享资源问题
                    finished.append(p)
                    # temp_ready.remove(p)
                print('- Current time:%s'%currTime,dis(p))
                currTime += do
    print('------------------------------END------------------------------')
    disList(finished)
    W_and_T(finished)
    finished.clear()
    for p in ready:
        p.initPCB()

def addPCB(currTime,temp_ready,head):
    for p in temp_ready:
        if p.arrival_time <= currTime:
            head.queue.append(p)
    for p in head.queue:
        if p in temp_ready:
            temp_ready.remove(p)

def doQueue(head,queue,finished,currTime,temp_ready):
    """
    :param queue: 当前队列
    :param finished: 完成队列
    :param currTime: 当前时刻
    :param temp_ready: 就绪队列
    :return: queue,finished,currTime,temp_ready
    """
    # print('curr time:',currTime)
    addPCB(currTime,temp_ready,head)    # 如果是当前时刻到达的进程,则加入第一级队列
    disMultiQueue(head)                 # 显示当前多级队列情况
    print('-----------------------------------------------------------------')
    if head.queue != [] and queue != head:
        return currTime
    for p in queue.queue:
        if not p.start_time:
            p.start_time = currTime
        if p.runned_time + 2**queue.level <= p.burst_time:
            p.runned_time += 2**queue.level
            currTime += 2**queue.level
        else:
            currTime += p.burst_time - p.runned_time
            p.runned_time = p.burst_time
        if p.runned_time == p.burst_time:           # 如果进程完成
            p.finished_time = currTime
            p.T = p.finished_time - p.arrival_time
            p.W = p.T/p.runned_time
            finished.append(p)
        elif queue.nextQueue != None:
            t = queue.nextQueue
            t.queue.append(p)
        addPCB(currTime,temp_ready,head)            # 如果是当前时刻到达的进程,则加入第一级队列
        if head.queue != [] and queue != head:      # 如果有新进程加入,则回到第一级队列
            break

    for p in finished:  # 清理完成的进程
        if p in queue.queue:
            queue.queue.remove(p)

    if queue.nextQueue != None:
        for p in queue.nextQueue.queue: # 清理放入下一级队列的进程
            if p in queue.queue:
                queue.queue.remove(p)

    if head.queue == [] and queue.nextQueue:        # 如果没有新进程加入并且有下一级队列,进入下一级队列
        currTime = doQueue(head,queue.nextQueue,finished,currTime,temp_ready)

    return currTime

def multi_LevelQueue():
    temp_ready = sorted(ready, key=lambda p: p.arrival_time)
    currTime = temp_ready[0].arrival_time
    multiQueue = MultiQueue(0)
    tempQueue = multiQueue
    for i in range(3): # 建立多级队列
        tempQueue.nextQueue = MultiQueue(i+1)
        tempQueue = tempQueue.nextQueue

    finished = []
    readyLen = len(temp_ready)
    while len(finished) != readyLen:
        currTime = doQueue(multiQueue,multiQueue,finished,currTime,temp_ready)
        # disMultiQueue(multiQueue) # 显示当前多级队列情况
        # print('-----------------------------------------------------------------')
    print('-------------------------------END----------------------------------------')
    disList(finished)
    W_and_T(finished)
    finished.clear()
    for p in ready:
        p.initPCB()

keep = True
while keep:
    command = input('>>>')
    command = command.split(' ')

    if command[0] == 'c' and len(command) == 2:
        ready.clear()
        n = int(command[1])
        for i in range(n):
            pcb_str = input()
            pcb_str = pcb_str.split(' ')
            if len(pcb_str) < 3:
                print('No.%d input error'%(i+1))
                continue
            if len(pcb_str) == 4:
                pcb = PCB(pcb_str[0], int(pcb_str[1]), int(pcb_str[2]), int(pcb_str[3]))
            elif len(pcb_str) == 3:
                pcb = PCB(pcb_str[0], int(pcb_str[1]), int(pcb_str[2]))
            ready.append(pcb)

    elif command[0] == 'fcfs':
        FCFS()

    elif command[0] == 'sjf':
        SJF()
    elif command[0] == 'time':
        TIME()

    elif command[0] == 'pri':
        Priority()
    elif command[0] == 'mul':
        multi_LevelQueue()

    elif command[0] == 'exit':
        keep = False