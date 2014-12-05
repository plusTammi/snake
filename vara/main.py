import numpy as np
import queue
import matplotlib.pylab as plt
import matplotlib.animation as animation
import copy
from time import sleep

##0##
#3#1#
##2##


def unique_columns2(data):
    dt = np.dtype((np.void, data.dtype.itemsize * data.shape[0]))
    dataf = np.asfortranarray(data).view(dt)
    u,uind = np.unique(dataf, return_inverse=True)
    u = u.view(data.dtype).reshape(-1,data.shape[0]).T
    return (u,uind)

class Snake:
    def __init__(s,start_size,field_size,x,y):
        s.place=queue.Queue()
        s.head=(x,y)
        s.size=start_size
        for i in range(0,start_size-1)[::-1]:
            s.place.put((x-1-i,y))
        s.place.put(s.head)
        s.possibles=[]
        for i in range(0,field_size):
            for j in range(0,field_size):
                s.possibles.append((i,j))
        s.possibles=s.possibles
        s.dirs=np.array([[0,-1],[1,0],[-1,0],[0,1]])#1234
        s.path=queue.LifoQueue()
        s.calc=0
                
        
    def ret_place(s):
        return s.place.queue
    
    
    def move_close(s,wh,place,poss,iters):
        #print(iters)
        s.calc+=1
        if iters>s.place.qsize()*2:
            #print("Too many iterations ",place)
            return True
        if s.calc>500:
            return "iterations_limit"
        dirs=(place-s.dirs)
        dirs=dirs[(dirs>=0).all(axis=1)]
        dists=np.abs(dirs-wh).sum(axis=1)
        if 0 in dists:
            s.path.put(dirs[np.where(dists==0)[0][0]])
            return True
        dirs=np.abs(dirs[np.array([(x == poss).all(axis=1).any() for x in dirs]),:])
        dists=np.abs(dirs-wh).sum(axis=1)
        for i in dirs[np.argsort(dists)]:
            ret=s.move_close(wh,i,poss[np.logical_not((i == poss).all(axis=1)),:],iters+1)
            if ret==True:
                s.path.put(i)
                return True
            if ret=="iterations_limit":
                return "iterations_limit"
        return False
        
    def move(s,wh):
        s.calc=0
        place=list(s.place.queue)
        pos=np.array(list(set(s.possibles)-set(place)))
        #print(place)
        #print("Apple ",wh)
        if s.path.empty():
            ret=s.move_close(wh,np.array(s.head),pos,0)
            if ret=="iterations_limit" or ret==False:
                print("asd")
                d=np.array(s.head)-s.dirs
                d=np.abs(d[np.array([(x == pos).all(axis=1).any() for x in d]),:])
                if len(d)==0:
                    print(s.place.qsize())
                    exit()
                s.path.put(d[0])
            
        #print("Place ",a)
        s.head=tuple(s.path.get())
        s.place.put(s.head)
        if s.head==wh:
            return "Apple"
        else:
            s.place.get()
            return False
                

    def move_vara(s,wh):
        try:
            place=list(s.place.queue)
            print(place)
            pos=[(s.head[0]+1,s.head[1]),(s.head[0]-1,s.head[1]),(s.head[0],s.head[1]+1),(s.head[0],s.head[1]-1)]
            pos=np.array(list(set(pos)-set(place)))
            dist=list(np.sum(np.power(pos-wh,2),axis=1))
            s.head=tuple(pos[dist.index(min(dist))])
            s.place.put(s.head)
            if s.head==wh:
                return "Apple"
            else:
                s.place.get()
                return False
        except ValueError:
            sleep(1)
            exit()
        
class Field:
    def __init__(s,size, start_apple):
        s.size=size
        s.apple=start_apple
        s.field=np.zeros((size,size))
        s._apple_places=[]
        for i in range(0,size):
            for j in range(0,size):
                s._apple_places.append((i,j))
        s._apple_places=set(list(map(tuple,s._apple_places)))
        
    def ret_field(s):
        t=copy.copy(s.field)
        t[s.apple]=255
        return t
    
    def apple_loc(s):
        return s.apple
        
    def new_apple(s,sn):
        
        x=list(set(range(0,s.size))-set(sn[0]))
        y=list(set(range(0,s.size))-set(sn[1]))
        possible=list(s._apple_places-set(list(map(tuple,sn.transpose()))))
        indx=range(0,len(possible))
        try:
            s.apple=(possible[np.random.choice(indx)])
        except ValueError:
            print("No possible places to put apple")
            exit()
        
    #def is_game_over(s):
        
        
        
size=200

sn=Snake(3,size,9,7)
f=Field(size,(5,4))

def update(sn,f):
    if sn.move(f.apple_loc())=="Apple":
        f.new_apple(np.array(sn.ret_place()).transpose())
    #f.is_game_over
    to_plot=f.ret_field()[:]
    inds=np.array(sn.ret_place()).transpose()
    to_plot[inds[0],inds[1]]=255
    return to_plot

def updatefig(*args):
    global f
    global sn
    #Field=update_Field(Snake,Field)
    im.set_array(update(sn,f))
    return im,


im=plt.matshow(f.ret_field(),cmap="gray")
fig=im.get_figure()
fig.set_size_inches(5, 5)
plt.axis("off")
ani = animation.FuncAnimation(fig, updatefig, interval=1,blit=True,)
#ani.save("demo.gif",writer='imagemagick', fps=20,bitrate=0)
plt.show()

