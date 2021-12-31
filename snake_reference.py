from tkinter import Tk, Canvas
import random

# Globals Parametrs
_width = 800
_height = 600
segSize = 20
theBigApple = 50
gameStatus = True
counter = 0
if counter > 5:
    counter = 0

# Helper functions
def apple():
    """ Creates an apple to be eaten """
    global appleGlob
    global counter
    posx = segSize * random.randint(1, (_width-segSize) / segSize)
    posy = segSize * random.randint(1, (_height-segSize) / segSize)
    appleGlob = canvas.create_oval(posx, posy,
                          posx+segSize, posy+segSize,
                          fill="red")
    if counter == 5:
        appleGlob = canvas.create_oval(posx, posy,
                          posx+theBigApple, posy+theBigApple,
                          fill="red")    

def main():
    """ Handles game process """
    global gameStatus
    global counter
    if gameStatus:
        current_snake.move()
        head_coords = canvas.coords(current_snake.segments[-1].create)
        x1, y1, x2, y2 = head_coords
        # Check for collision with gamefield edges
        if x2 > _width or x1 < 0 or y1 < 0 or y2 > _height:
            gameStatus = False
        # Eating apples
        elif head_coords == canvas.coords(appleGlob):
            current_snake.add_segment()
            canvas.delete(appleGlob)
            apple()
            counter+=1
            if counter == 5:
                current_snake.add_segment()
                current_snake.add_segment()
        # Self-eating
        else:
            for index in range(len(current_snake.segments)-1):
                if head_coords == canvas.coords(current_snake.segments[index].create):
                    gameStatus = False
        root.after(100, main)
    # Not gameStatus -> stop game and print message
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


class Segment(object):
    """ Single snake segment """
    def __init__(self, x, y):
        self.create = canvas.create_rectangle(x, y,
                                           x+segSize, y+segSize,
                                           fill="white")


class Snake(object):
    """ Simple Snake class """
    def __init__(self, segments):
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = self.mapping["Right"]

    def move(self):
        """ Moves the snake with the specified vector"""
        for index in range(len(self.segments)-1):
            segment = self.segments[index].create
            x1, y1, x2, y2 = canvas.coords(self.segments[index+1].create)
            canvas.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = canvas.coords(self.segments[-2].create)
        canvas.coords(self.segments[-1].create,
                 x1+self.vector[0]*segSize, y1+self.vector[1]*segSize,
                 x2+self.vector[0]*segSize, y2+self.vector[1]*segSize)

    def add_segment(self):
        """ Adds segment to the snake """
        last_seg = canvas.coords(self.segments[0].create)
        x = last_seg[2] - segSize
        y = last_seg[3] - segSize
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ Changes direction of snake """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            canvas.delete(segment.create)


def set_state(item, state):
    canvas.itemconfigure(item, state=state)


def clicked(event):
    global gameStatus
    current_snake.reset_snake()
    gameStatus = True
    canvas.delete(appleGlob)
    canvas.itemconfigure(restart_text, state='hidden')
    canvas.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():
    global current_snake
    apple()
    current_snake = create_snake()
    # Reaction on keypress
    canvas.bind("<KeyPress>", current_snake.change_direction)
    main()


def create_snake():
    # creating segments and snake
    segments = [Segment(segSize, segSize),
                Segment(segSize*2, segSize),
                Segment(segSize*3, segSize),]
    return Snake(segments)


# Setting up window
root = Tk()
root.title("PythonicWay Snake")


canvas = Canvas(root, width=_width, height=_height, bg="#003300")
canvas.grid()
# catch keypressing
canvas.focus_set()
game_over_text = canvas.create_text(_width/2, _height/2, text="GAME OVER!",
                               font='Arial 20', fill='red',
                               state='hidden')
restart_text = canvas.create_text(_width/2, _height-_height/3,
                             font='Arial 30',
                             fill='white',
                             text="Click here to restart",
                             state='hidden')
canvas.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()