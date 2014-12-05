import numpy as np
import random

apple_color=127

class Field:
    def __init__(s,size, start_apple):
        global apple_color
        s.size=size
        s.apple=start_apple[0]+start_apple[1]*1j
        s.field_cord=[]
        s.field_vals=np.zeros(size*size)
        s._apple_places=[]
        for i in range(0,size):
            for j in range(0,size):
                s._apple_places.append(complex(i,j))
                s.field_cord.append(complex(i,j))
        s.field_cord=np.array(s.field_cord)
        s._apple_places=set(s._apple_places)
        s.field_vals[s.field_cord==4+3j]=1
        s._apple_places=set(s._apple_places)
        
    def ret_field(s,snake):
        t=np.copy(s.field_vals)
        t[s.field_cord==s.apple]=apple_color
        p=snake.ret_place()
        t=t.reshape(s.size,s.size)
        t[(p.real).astype(int),(p.imag).astype(int)]=255
        return t.reshape(s.size,s.size)
    
    def apple_loc(s):
        return s.apple
        
    def new_apple(s,sn):
        possible=s._apple_places-set(sn)
        try:
            s.apple=random.sample(possible,1)
        except ValueError:
            print("No possible places to put apple")
            exit()
