from tkinter import *
import time
import serial
from PIL import ImageTk,Image
from PIL.ImageTk import PhotoImage

   
class air_glove:
    def __init__(self):
        self.port=''
        self.x=0
        self.y=0
        self.z=0
        self.paired=False
    

    #step1
    def pair_glove(self):
        self.port= serial.Serial('/dev/cu.wchusbserial1410', 9600)
        #self.port= serial.Serial('/dev/cu.wchusbserial1410', 9600)
        print('connected via USB')
        self.paired=True

        
    def read_position(self):
        if self.paired==True:
            try:
                coordinates=self.port.readline().decode('utf-8')
                x=int(re.search('x:[+,-]*(\d)*',coordinates).group(0).strip('x:'))
                y=int(re.search('y:[+,-]*(\d)*',coordinates).group(0).strip('y:'))
                z=int(re.search('z:[+,-]*(\d)*',coordinates).group(0).strip('z:'))
                coordinates=[x,y,z]
                return coordinates
            except :
                print("crash")
                #return self.lastCoordinates
                return [0,0,0]
        else:
            return [0,0,0]

        
           
        

        
class air_mouse:
    def __init__(self):
        self.glove=air_glove()
        self.root=Tk()
        self.canvas=Canvas(master=self.root, width=1200,height=750, background='white')
        self.canvas.grid(row=0,column=0)
        self.x=500
        self.y=500
        self.z=500
        self.canvas.bind('<Button-1>',self.coordinates)
        self.hand = PhotoImage(file="hand.gif")
 

    def coordinates(self,event):
        coord='x:{} y:{}'.format(event.x,event.y)
        print(coord)
        
    def can_interact(self):
        if self.x>100 and self.x<200 and self.y>100 and self.y<200:
            self.glove.port.write(str.encode('1'))
        else:
            pass
        
    def draw_circle(self,x,y,tag=''):
        radius=10
        self.point=self.canvas.create_oval(x,y,x+radius,y+radius,fill='black', tags=tag)
    
            
    def  update_c(self):
        self.canvas.delete(ALL)
        #air_mouse.draw_circle(self,self.x,self.y)
        self.canvas.create_image(self.x,self.y, anchor=NW, image=self.hand)
        
    
    #with real mouse
    def move(self,event):
        self.x=event.x5
        self.y=event.y
        air_mouse.update_c(self)


    def bounding_box(self,x,y):
         if x<=0:
             x=0
         if x>=1200-50:
             x=1200-50
         if y<=0:
            y=0
         if y>=750-50:
             y=750-50
         return (x,y)

    def glove_control(self):
        coord=self.glove.read_position()
        x=coord[0]+ self.x
        y=coord[1]+ self.y
        x_y_=air_mouse.bounding_box(self,x,y)
        self.x=x_y_[0]
        self.y=x_y_[1]
        self.z=coord[2]
    

    def game_stats(self):
        score_display='Shots: {}'.format(0)
        self.canvas.create_text(31,100,text=score_display,tags='score')
        attempts_display='Attempts: {}'.format(0)
        self.canvas.create_text(40,118,text=attempts_display,tags='attempts')
        
    def next(self):
        air_mouse.glove_control(self)
        air_mouse.update_c(self)
        self.root.after(1,air_mouse.next,self )
        
test=air_mouse()
test.glove.pair_glove()
test.next()
test.root.mainloop()

