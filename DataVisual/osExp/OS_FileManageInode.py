import datetime
import time
import re

EMPTY_BLOCK = 0x0000
LAST_BLOCK = 0xffff

class FCB(object):
    def __init__(self,name,size,first_block,type,date_time,parent):
        self.name = name
        self.size = size
        self.first_block = first_block
        self.type = type        #1为文件,2为目录,0为已删除目录项
        self.date_time = date_time
        self.parent = parent    #父目录
        self.contain_dict = {}  #子目录或文件
        self.iSet = {}

    def set_date_time(self,date_time):
        self.date_time = date_time

    def add_contain(self,fcb):
        self.contain_dict[fcb.name] = fcb

    def __str__(self):
        return str(self.date_time)+'\t name:'+self.name + '\t type:'+str(self.type) + '\t size:'+str(self.size)

class Inode(object):
    def __init__(self,name):
        self.name = name
        self.blockList = [-1 for i in range(5)]
        self.blockList[-2] = []
        self.blockList[-1] = [[] for i in range(4)]

class Block(object):
    def __init__(self):
        self.cnt = 0
        self.blockList = []

    def addCnt(self):
        self.cnt += 1

def findNullBlock(block):
    if block.cnt > 1:
        res = block.blockList[0]
        block.blockList.remove(block.blockList[0])
        block.cnt -= 1
        return res,block
    res = block.blockList[0]
    block.blockList.remove(block.blockList[0])
    block.cnt -= 1
    block = block.blockList[-1]
    return res,block

def CD(root,currDir,pos):
    if pos == '/':
        currDir = root
        return currDir
    if pos == '..':
        if currDir.parent != None:
            currDir = currDir.parent
        return currDir
    posArr = pos.split('/')
    if pos[0] == '/':
        currDir = root
        posArr.remove(posArr[0])
    for posName in posArr:
        if posName in currDir.contain_dict and currDir.contain_dict[posName].type == 2:
            currDir = currDir.contain_dict[posName]
        else:
            print("$Path is not exist!")
            break
    return currDir

def MD(currDir,md_file):
    if md_file.name in currDir.contain_dict:
        print('$This file have exist.')
        return
    currDir.add_contain(md_file)
    currDir.size += md_file.size


def RD(currDir,del_fileName):
    if del_fileName not in currDir.contain_dict:
        print('$This file is not exist.')
        return currDir
    t = currDir.contain_dict[del_fileName]
    if not t.contain_dict: #如果子目录为空
        currDir.contain_dict.pop(del_fileName)
    return currDir

def MK(currDir,fcb,block):
    if fcb.name in currDir.contain_dict:
        print('$This file have exist.')
        return block
    inode = Inode(fcb.name)
    currDir.iSet[inode.name] = inode
    size = fcb.size
    needBlock = size//1024
    if size % 1024 != 0:
        needBlock += 1
    if needBlock > 15:
        print("Not enough space.")
        return block,iSet

    cnt = 0
    while needBlock != 0 and cnt != 3:
        num,block = findNullBlock(block)
        needBlock -= 1
        inode.blockList[cnt] = num
        cnt += 1
    if needBlock:
        num,block = findNullBlock(block)
        inode.blockList[-2].append(num)            #二级索引的第一位存索引的地址号
    while needBlock != 0 and cnt != 6:   #使用二级索引
        num,block = findNullBlock(block)
        needBlock -= 1
        inode.blockList[-2].append(num)
        cnt += 1
    if needBlock:
        num,block = findNullBlock(block)
        inode.blockList[-1][0] = num             #三级索引的第一位存索引的地址号

    cnt2 = 1
    tt = 0
    while needBlock != 0 and cnt != 15:   #使用三级索引
        if len(inode.blockList[-1][cnt2]) == 0:     #如果此索引还未启用
            num, block = findNullBlock(block)
            inode.blockList[-1][cnt2].append(num)     # 三级索引第二层的第一位存索引的地址号
            continue
        num,block = findNullBlock(block)
        inode.blockList[-1][cnt2].append(num)
        cnt += 1
        needBlock -= 1
        if len(inode.blockList[-1][cnt2]) == 4:
            cnt2 += 1

    if needBlock:
        print('Not enough space.')
        Free(currDir.iSet,block,inode)
        DEL(currDir,fcb.name)
        # TODO 回收外存超级块
    currDir.add_contain(fcb)
    currDir.size += fcb.size
    return block

def DEL(currDir,del_fileName):
    if del_fileName not in currDir.contain_dict:
        print('$This file is not exist.')
        return currDir
    currDir.contain_dict.pop(del_fileName)
    return currDir

def DIR(currDir):
    for name in currDir.contain_dict:
        print(currDir.contain_dict[name])

def Add_Tab(s,num):
    for i in range(num):
        s += '\t'
    return s+'|-'

def TREE(currDir,level):
    s = ''
    s = Add_Tab(s,level)
    level += 1
    print(s+currDir.name)
    for name in currDir.contain_dict:
        TREE(currDir.contain_dict[name],level)

def PWD(currDir):
    temp = currDir
    l = []
    s = ''
    while temp.name != '/':
        l.append(temp.name)
        temp = temp.parent
    if len(l) == 0:
        return '/'
    l.reverse()
    for si in l:
        s += '/' + si
    return s

def FIND(currDir,file_name):
    if file_name[0] == '*' and file_name[-1] == '*': #前后有*,搜索中间字符
        for name in currDir.contain_dict:
            if file_name[1:-1] in name[1:-1]:
                print(currDir.contain_dict[name])
    elif file_name[0] == '*':   #前面有*
        temp_name = file_name[1:]
        pattern = r'' + temp_name + '$'
        for name in currDir.contain_dict:
            match = re.search(pattern, name)
            if match:
                print(currDir.contain_dict[name])
    elif file_name[-1] == '*':  #后面有*
        temp_name = file_name[0:-1]
        pattern = r'^'+temp_name
        for name in currDir.contain_dict:
            match = re.search(pattern,name)
            if match:
                print(currDir.contain_dict[name])
    elif file_name[-1] != '*' and file_name[0] != '*':
        for name in currDir.contain_dict:
            if name == file_name:
                print(currDir.contain_dict[name])

def disDisk(disk):
    for i in range(len(disk)):
        print(disk[i],end=' ')
        if (i+1)%5 == 0:
            print()
    print()

def disBlock(block):
    for i in range(len(block.blockList)):
        if isinstance(block.blockList[i],Block):
            print('next')
            disBlock(block.blockList[i])
            continue
        print(block.blockList[i],end=' ')

def findNullDisk(disk):
    for i in range(len(disk)):
        if disk[i] == 0:
            return i
    return -1

def disInode(inode):
    print('-------1 Level-----------')
    print('File: '+inode.name)
    for i in range(3):
        if inode.blockList[i] == -1:
            break
        print(inode.blockList[i])

    if inode.blockList[-2]:
        print('-------2 Level-----------')
        print(' ',end='')
        print(inode.blockList[-2][0])
        print('   ', end='')
        print(inode.blockList[-2][1:])
    if inode.blockList[-1][0]:
        print('-------3 Level-----------')
        for tlist in inode.blockList[-1]:
            if isinstance(tlist,int):
                print(tlist)
                continue
            for ti in tlist:
                print('  ',end='')
                if tlist.index(ti) != 0:
                    print('  ',end='')
                print(ti)
    #TODO

def dis_iSet(iSet):
    for inode in iSet:
        disInode(iSet[inode])

def addBlock(block,num):
    if block.cnt == 3:
        t = block
        block = Block()
        block.blockList.append(t)
    block.blockList.insert(0,num)
    block.addCnt()
    return block

def Free(iSet,block,inode):
    iSet.pop(inode.name)
    index = 0
    while inode.blockList[index] != -1 and index != 3:
        num = inode.blockList[index]
        inode.blockList[index] = -1
        block = addBlock(block,num)
        index += 1
    while inode.blockList[-2]:         #如果二级目录有占用外存
        block = addBlock(block,inode.blockList[-2].pop())
    cnt2 = 0
    if inode.blockList[-1][cnt2]:      #释放二级索引的外存
        block = addBlock(block, inode.blockList[-1][cnt2])
        inode.blockList[-1].remove(inode.blockList[-1][cnt2])
    while inode.blockList[-1][cnt2]:   #如果三级目录有占用外存
        while inode.blockList[-1][cnt2]:
            block = addBlock(block,inode.blockList[-1][cnt2].pop())
        cnt2 += 1

    return block


if __name__ == '__main__':
    keep = True
    iSet = {}
    m = input("Input disk size:")
    m = int(m)
    disk = [0 for i in range(m)]
    root = FCB('/',0,0,2,datetime.datetime.now(),None)
    inode = Inode(root.name)
    inode.blockList[0] = 0
    root.iSet[inode.name] = inode

    supBlock = Block()
    temp = supBlock
    disk[0] = 1
    for i in range(1,len(disk)):
        temp.blockList.append(i)
        temp.addCnt()
        if i%3 == 0:
            temp.blockList.append(Block())
            temp = temp.blockList[-1]
    #disBlock(supBlock)
    print()
    currDir = root
    while keep:
        command = input(PWD(currDir)+'->'+"$")
        arr_command = command.split(' ')
        # print(arr_command)
        command = arr_command[0]

        if command == 'exit':
            keep = False

        elif command == 'pwd':
            print(PWD(currDir))

        elif command == 'md' and len(arr_command) == 2:   #创建子目录
            # first = findNullDisk(disk)
            first,supBlock = findNullBlock(supBlock)           # 取出超级块
            new_fcb = FCB(arr_command[1],0,first,2,datetime.datetime.now(),currDir)
            inode = Inode(new_fcb.name)
            inode.blockList[0] = first
            currDir.iSet[inode.name] = inode
            MD(currDir,new_fcb)

        elif command == 'cd' and len(arr_command) == 2:   #切换工作目录
            currDir = CD(root,currDir,arr_command[1])

        elif command == 'rd' and len(arr_command) == 2:   #搜索所要删除的目录是否为空目录，若是则删除
            # TODO 回收外存超级块
            supBlock = Free(currDir.iSet, supBlock, currDir.iSet[arr_command[1]])
            currDir = RD(currDir,arr_command[1])

        # 创建指定大小的文件(如输入命令“mk test 2000”,表示创建大小为2000字节的test文件),并在父目录中添加文件名称;还应对FAT表进行适当修改
        elif command == 'mk' and len(arr_command) == 3:
            size = int(arr_command[2])
            needBlock = size//1024 + 1
            new_fcb = FCB(arr_command[1],size,0,1,datetime.datetime.now(),currDir)
            supBlock = MK(currDir,new_fcb,supBlock)

        elif command == 'del' and len(arr_command) == 2:  #删除
            # TODO 回收外存超级块
            supBlock = Free(currDir.iSet, supBlock, currDir.iSet[arr_command[1]])
            currDir = DEL(currDir,arr_command[1])

        elif command == 'dir':
            DIR(currDir)

        elif command == 'tree':
            TREE(currDir,0)

        elif command == 'clear':
            print('\n')
            print('\n')
            print('\n')
            print('\n')
            print('\n')
            print('\n')
            print('\n')
            print('\n')
            print('\n')
            print('\n')

        elif command == 'find' and len(arr_command) == 2:
            FIND(currDir,arr_command[1])

        elif command == 'disk':
            disDisk(disk)

        elif command == 'inode' and len(arr_command) == 1:
            dis_iSet(currDir.iSet)

        elif command == 'inode' and len(arr_command) == 2:
            if arr_command[1] in currDir.iSet:
                disInode(currDir.iSet[arr_command[1]])
            else:
                print('This file is not exist.')

        elif command == 'super':
            disBlock(supBlock)
            print()

        elif command == 'edit' and len(arr_command) == 3:
            pass
            #TODO

        else:
            print('$This command is not exist.')
