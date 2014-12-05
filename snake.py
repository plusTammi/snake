import numpy as np
import queue
import time
import copy
import collections
import heapq

class Snake:
    def __init__(s,start_size,field_size,x,y):
        s.place=queue.Queue()
        s.head=x+y*1j
        s.size=start_size
        for i in range(0,start_size-1)[::-1]:
            s.place.put((x+1+i+y*1j))
        s.place.put(s.head)
        s.possibles=[]
        s.field_size=field_size
        for i in range(0,field_size):
            for j in range(0,field_size):
                s.possibles.append(i +j*1j)
        s.possibles=s.possibles
        s.neighbors=np.array([0-1j,1+0j,-1+0j,0+1j])#1234
        s.path=queue.LifoQueue()
        s.calc=0
        #print(np.array(s.place.queue))
        
    def ret_place(s):
        return np.array(s.place.queue)
    
    
    def a_star(s,start,apple,place):
        neibs=np.array([0-1j,1+0j,-1+0j,0+1j])
        close_set=set()
        parents={}
        gscores={start:0}
        fscores={start:(abs(start-apple))}
        open_list=[]
        
        heapq.heappush(open_list,(fscores[start],start))
        while open_list:
            s.calc+=1
            current=heapq.heappop(open_list)[1]
            if current == apple:
                while current in parents:
                    s.path.put(current)
                    current=parents[current]
                return True
            neighbors=np.array(list(set(current-neibs) - place))
            neighbors=neighbors[np.logical_and(neighbors>0,neighbors.imag>0)]
            #print(neighbors)
            for i in neighbors:
                h_current=gscores[current]+abs(i)
                if i in [x[1] for x in open_list] and h_current > gscores[i]:
                    continue
                if i in close_set and h_current > gscores[i]:
                    continue
                parents[i]=current
                gscores[i]=h_current
                fscores[i]=h_current+abs(i)
                heapq.heappush(open_list,(fscores[i],i))
            close_set.add(current)
        return False
                
    def move_close(s,wh,head,poss,place,iters):
        s.calc+=1
        if iters>s.place.qsize()*20:
            return True
        dirs=(head-s.neighbors)
        if 0 in dirs-wh:
            s.path.put(dirs[((dirs-wh)==0)][0])
            return True
        dirs=np.array(list(set(dirs)&poss))
        #dists=abs(dirs-wh)                                 #Diagonal distance
        temp=dirs-wh                                        #Straight
        dists=abs(temp.real)+abs(temp.imag)
        tail=place.popleft()
        for i in dirs[np.argsort(dists)]:
            place.append(i)
            ret=s.move_close(wh,i,(poss-set([i])|set([tail])),place,iters+1)
            if ret==True:
                s.path.put(i)
                return True
            if ret=="iterations_limit":
                return "iterations_limit"
            place.pop()
        place.appendleft(tail)
        return False
        
    def move(s,wh):
        s.calc=0
        place=collections.deque(s.place.queue)
        pos=set(s.possibles)-set(place)
        if s.path.empty():
            #ret=s.move_close(wh,s.head,pos,place,0)
            ret=s.a_star(s.head,wh,set(place))
            if ret=="iterations_limit" or ret==False:
                print(s.place.qsize())
                exit()
                print("asd")
                d=np.array(s.head)-s.neighbors
                d=np.abs(d[np.array([(x == pos).all(axis=1).any() for x in d]),:])
                if len(d)==0:
                    print(s.place.qsize())
                    exit()
                s.path.put(d[0])
        s.head=s.path.get()
        s.place.put(s.head)
        if s.head==wh:
            return "Apple"
        else:
            s.place.get()
            return False
                
