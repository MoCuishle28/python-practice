
glo = 1000

class A(object):
    def __init__(self,i):
        self.i = i
        self.queue = []

    def __str__(self):
        return 'i = '+str(self.i) + ' queue:' + str(self.queue)

def change(a,l):
    a.queue.remove(3)
    a.queue.append(5)
    l.remove(3)

def f():
    global l
    l = [2 for i in range(3)]

l = [1,1,1]
f()
print(l)
