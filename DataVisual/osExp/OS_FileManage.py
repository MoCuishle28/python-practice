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

    def set_date_time(self,date_time):
        self.date_time = date_time

    def add_contain(self,fcb):
        self.contain_dict[fcb.name] = fcb

    def __str__(self):
        return str(self.date_time)+'\t name:'+self.name + '\t type:'+str(self.type) + '\t size:'+str(self.size)

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

def MK(currDir,fcb):
    MD(currDir,fcb)

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
            if file_name[1:-1] in name:
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

def displayDisk(disk):
    for i in range(len(disk)):
        print(disk[i],end=' ')
        if (i+1)%10 == 0:
            print()
    print()

def findNoneDisk(disk):
    for i in range(len(disk)):
        if disk[i] == 0:
            return i
    return -1

def disFAT(fat):
    for i in range(len(fat)):
        print("%X"%fat[i],end=' ')
        if (i+1)%10 == 0:
            print()
    print()

if __name__ == '__main__':
    m = input("Input disk size:")
    FAT = [EMPTY_BLOCK for i in range(int(m))]
    if int(m) < LAST_BLOCK:
        disk = [0 for i in range(int(m))]
    keep = True
    fileNum = 0
    root = FCB('/',0,0,2,datetime.datetime.now(),None)
    num = findNoneDisk(disk)
    disk[num] = 1
    FAT[num] = LAST_BLOCK
    # print(root.date_time)
    currDir = root
    treeDir = []
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
            num = findNoneDisk(disk)
            disk[num] = 1
            FAT[num] = LAST_BLOCK
            new_fcb = FCB(arr_command[1],0,num,2,datetime.datetime.now(),currDir)
            MD(currDir,new_fcb)

        elif command == 'cd' and len(arr_command) == 2:   #切换工作目录
            currDir = CD(root,currDir,arr_command[1])

        elif command == 'rd' and len(arr_command) == 2:   #搜索所要删除的目录是否为空目录，若是则删除
            fileDel = currDir.contain_dict[arr_command[1]]
            disk[fileDel.first_block] = 0
            first = fileDel.first_block
            while FAT[first] != LAST_BLOCK:
                next = FAT[first]
                FAT[first] = EMPTY_BLOCK
                first = next
            FAT[first] = EMPTY_BLOCK
            currDir = RD(currDir,arr_command[1])

        # 创建指定大小的文件(如输入命令“mk test 2000”,表示创建大小为2000字节的test文件),并在父目录中添加文件名称;还应对FAT表进行适当修改
        elif command == 'mk' and len(arr_command) == 3:
            size = int(arr_command[2])
            needBlock = size//1024 + 1
            num = findNoneDisk(disk)
            disk[num] = 1
            FAT[num] = LAST_BLOCK
            needBlock -= 1
            new_fcb = FCB(arr_command[1],size,num,1,datetime.datetime.now(),currDir)
            while needBlock != 0:
                pre = num
                num = findNoneDisk(disk)
                disk[num] = 1
                FAT[pre] = num
                FAT[num] = LAST_BLOCK
                needBlock -= 1
            MK(currDir,new_fcb)

        elif command == 'del' and len(arr_command) == 2:  #删除
            fileDel = currDir.contain_dict[arr_command[1]]
            disk[fileDel.first_block] = 0
            first = fileDel.first_block
            while FAT[first] != LAST_BLOCK:
                next = FAT[first]
                FAT[first] = EMPTY_BLOCK
                disk[first] = 0
                first = next
            FAT[first] = EMPTY_BLOCK
            disk[first] = 0
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
            disFAT(FAT)
            displayDisk(disk)

        elif command == 'edit' and len(arr_command) == 3:
            pass
            #TODO

        else:
            print('$This command is not exist.')
