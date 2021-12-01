from tkinter import *
run_tkinter = Tk()
run_tkinter.title("snake")
width_ = 800
height_ = 800
seg_size = 20
play_status = True
canv = Canvas(
    run_tkinter, 
    width=width_, 
    height=height_, 
    background="green")
canv.grid()
canv.focus_set()    
run_tkinter.mainloop()

class snake_seg(object):
    def __init__(self, x, y):
        self.instance = canv.create_rectangle(
            x,
            y, 
            x+seg_size, 
            y+seg_size, 
            fill="white")
class snake(object):
    def __init__(self, segment):
        self.segment = segment
        self.mapping = {
            "down":(0, 1),
            "up":(0, -1),
            "right":(1, 0), 
            "left":(-1, 0)}
        self.vector = self.mapping["right"]
#класс змейки
    #функция описания движения
    #функция движения
    #функия рисования
    