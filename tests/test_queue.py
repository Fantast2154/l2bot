from queue import Queue

q = Queue()

def pump(s):
    print('pump', s)

def reel():
    print('reel')

def fish():
    print('fish')

def mouse_move_print(pos):
    print('Moved to', pos)

#pump()
#reel()
#fish()

q.put(pump('123'))
q.put(reel())
q.put(fish())
q.put(mouse_move_print(1))
q.put(mouse_move_print(2))
q.put(mouse_move_print(3))
q.put(mouse_move_print(4))

q.get()

#while q.not_empty:
    # print('do')