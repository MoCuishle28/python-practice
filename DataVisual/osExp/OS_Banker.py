
class PCB(object):
    def __init__(self,name,max,allocation):
        self.name = name
        self.max = [x for x in max]
        self.allocation = [x for x in allocation]
        self.need = []
        for i in range(len(self.max)):
            self.need.append(self.max[i] - self.allocation[i])

    def __str__(self):
        return 'name:'+str(self.name) + ' max:' + str(self.max)+' allocation:'+str(self.allocation)+' need:'+str(self.need)

def disQueue(queue):
    for p in queue:
        print(p)

def canAssign(pcb,resourceList):
    can = True
    for i in range(len(resourceList)):
        if pcb.need[i] > resourceList[i]:
            can = False
            break
    return can

def banker(resourceList,tempQueue):
    dis = lambda p:'name:'+str(p.name)+' work:'+str(p.work)+' need:'+str(p.need)+' allocation'+str(p.allocation)+ ' W+A:'+str(p.currReso)
    tempResoList = [x for x in resourceList]
    sumPCB = len(tempQueue)
    savePCB = [p for p in tempQueue]
    saveReso = [x for x in tempResoList]
    safetyList = []
    work = []
    cnt = 0
    find = True

    while cnt != sumPCB and find:
        find = False
        for p in tempQueue:
            if canAssign(p,tempResoList):
                work = [x for x in tempResoList]
                p.work = work
                p.currReso = [p.work[i] + p.allocation[i] for i in range(len(p.work))]
                tempResoList = [p.work[i] + p.allocation[i] for i in range(len(tempResoList))]
                safetyList.append(p)
                tempQueue.remove(p)
                find = True
                break
        cnt += 1

    print('---------------------------------Safety List--------------------------------------')
    if not tempQueue:
        global queue
        queue = [p for p in savePCB]
        for p in safetyList:
            print(dis(p))
        return saveReso
    else:
        print('Do not safe.')
        return None

queue = []
keep = True
while keep:
    command = input('>>>')
    command = command.split(' ')

    if command[0] == 'exit':
        keep = False

    elif command[0] == 'bank':
        queue.clear()
        resNumbers = input('Input resources:')
        resNumbers = resNumbers.split(' ')
        resourceList = [int(x) for x in resNumbers]
        print('Available:',resourceList)
        n = int(input('Input PCB\'s numbers:'))
        resoNum = len(resourceList)
        for i in range(n):
            pcbStr = input()
            pcbStr = pcbStr.split(' ')
            maxReso = pcbStr[1:1+resoNum]
            maxReso = [int(x) for x in maxReso]
            allocation = pcbStr[1+resoNum:1+resoNum+resoNum]
            allocation = [int(x) for x in allocation]
            pcb = PCB(pcbStr[0],maxReso,allocation)
            queue.append(pcb)
        disQueue(queue)
        tempQueue = []
        for p in queue:
            newP = PCB(p.name, p.max, p.allocation)
            tempQueue.append(newP)
        banker(resourceList,tempQueue)

    elif command[0] == 'jud':
        tempQueue = []
        for p in queue:
            newP = PCB(p.name, p.max, p.allocation)
            tempQueue.append(newP)

        name = input('PCB\'s name:')
        pcb = None
        for p in tempQueue:
            if p.name == name:
                pcb = p
                break
        if not pcb:
            print('PCB do not exist.')
        else:
            newAllocation = input('Allocation:')
            newAllocation = newAllocation.split(' ')
            newAllocation = [int(x) for x in newAllocation]
            resoSub = [pcb.allocation[i] - newAllocation[i] for i in range(len(newAllocation))]
            pcb.allocation = [x for x in newAllocation]
            pcb.need = [p.max[i] - p.allocation[i] for i in range(len(pcb.allocation))]
            tempResoList = [resoSub[i] + resourceList[i] for i in range(len(resourceList))]
            disQueue(tempQueue)
            temp = banker(tempResoList,tempQueue)
            if temp:
                resourceList = temp

    elif command[0] == 'req':
        tempQueue = []
        for p in queue:
            newP = PCB(p.name, p.max, p.allocation)
            tempQueue.append(newP)
        name = input('PCB\'s name:')
        pcb = None
        for p in tempQueue:
            if p.name == name:
                pcb = p
                break
        if not pcb:
            print('PCB do not exist.')
        else:
            req = input('Request:')
            req = req.split(' ')
            req = [int(x) for x in req]
            can = True
            for i in range(len(req)):
                if req[i] > pcb.need[i] or req[i] > resourceList[i]:
                    can = False
                    break

            if can:
                pcb.allocation = [pcb.allocation[i] + req[i] for i in range(len(req))]
                pcb.need = [pcb.need[i] - req[i] for i in range(len(req))]
                tempResoList = [resourceList[i] - req[i] for i in range(len(req))]
                print('resourceList:',tempResoList)
                disQueue(tempQueue)
                temp = banker(tempResoList,tempQueue)
                if temp != None:
                    resourceList = temp
            else:
                print('Do not safe.')
