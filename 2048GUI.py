from tkinter import * 
from game import *
from random import *
from copy import deepcopy
import math

class TwentyFortyEight_GUI():

    def __init__(self, twentyfortyeight):
        self.TFE = twentyfortyeight
        self.window = Tk()
        self.window.title("2048 Game")
        self.window.bind_all("<Key>", self.key_pressed)
        self.canvas1 = Canvas(self.window, bg = "peach puff", width = 500, height = 100)
        self.canvas2 = Canvas(self.window, bg = "lemon chiffon", width = 500, height = 500)
        self.button1 = Button(self.canvas2, text="Best Scores", anchor=NW, bg="gold", font=("Times", 18, "bold"), bd = 3, command=self.display_best_scores)
        self.button2 = Button(self.canvas2, text="New Game", anchor=NE, bg="SpringGreen2", font=("Times", 18, "bold"), bd = 3, command=self.reset)
        self.draw_game_init()
        self.update_tiles()
        

    def draw_game_init(self):
        """
        Create items on the two canvases.
        """
        self.canvas1.pack()
        self.canvas2.pack()
        
        #coordinates
        x1,y1,x2,y2 = 50,50,450,50
        
        #Canvas1
        #"score" text
        self.canvas1.create_text(360, 26, text="SCORE", font=("Times", 25, "bold"))
        #actual score
        self.canvas1.create_text(360, 50, text="0", font=("Times", 22, "bold"), tag="score")


        #Canvas2
        #"best scores" button
        self.canvas2.create_window(90,23, window=self.button1)
        #"new game" button
        self.canvas2.create_window(410,23, window=self.button2)
        #background of canvas2
        self.canvas2.create_rectangle(50, 50, 450, 450, fill = "bisque2", outline = "lavender blush")
		
		#coordinates for reference
        #x1,y1,x2,y2 = 50,50,550,50
		
        #lines to create the boxes for game
        for i in range(5):
            #horizontal lines
            self.canvas2.create_line(x1-2, y1+i*100, x2+2, y2+i*100, fill="NavajoWhite4", width=7, smooth=1)
            #vertical lines
            self.canvas2.create_line(x1+i*100, y1, x1+i*100, 450, fill="NavajoWhite4", width=7, smooth=1)


    def update_tiles(self):
        """
        Update and display the tiles after each move.
        """

        #clear the original tiles
        self.canvas2.delete("rect")
        self.canvas2.delete("text")

        #color of tiles with different numbers
        color_dic = {
            2:"light salmon",
            4:"orange",
            8:"tomato",
            16:"red",
            32:"yellow2",
            64:"dark slate gray",
            128:"medium orchid",
            256:"lawn green",
            512:"spring green",
            1024:"thistle1",
            2048:"gold",
            4096:"lavender",
            8192:"cyan"
            }

        #coordinates of the tile at row 0, col 0
        x, y, z, w = 53, 53, 153, 153
		
        #create all the tiles based on the coordinates above
        for i in range(self.TFE.numRow):
            for j in range(self.TFE.numCol):
                value = self.TFE.grid[i][j]
                if value != 0:
                    self.canvas2.create_rectangle(x+j*100, (y+i*100), (z+j*100)-5, (w+i*100)-7, fill = color_dic[value], outline = color_dic[value], tag="rect")
                    self.canvas2.create_text((x+z+j*200)/2, (y+w+i*200)/2, fill = "white", text = str(value), font=("Impact", 18), tag="text")


    def update_score(self):
        """
        Update and display the score after each move.
        """
        self.canvas1.delete("score")
        self.canvas1.create_text(360, 50, text=str(self.TFE.actualScore), font=("Times", 22, "bold"), tag="score")


    def reset(self):
        """
        Reset the game board to start a new game.
        """
        self.TFE.reset()
        self.update_score()
        self.update_tiles()


    def key_pressed(self, event):
        """
        Method to act upon the keyboard actions with the update of the game state.
        """
        key = event.keysym
        #each arrow kwy corresponds to a direction
        if key in ["Up", "Down", "Left", "Right"]:
            try:
                direction = key.upper()
                self.TFE.move(direction)
                self.update_score()
                self.update_tiles()
                #display "Game Over" and the score when the game board reaches the final state.
                #record the score each time and update the list of the best five scores
                if self.TFE.game_over():
                    if len(self.TFE.bestScores) < 5:
                        self.TFE.bestScores.append(self.TFE.actualScore)
                    else:
                        mins = min(self.TFE.bestScores)
                        if self.TFE.actualScore > mins:
                            self.TFE.bestScores[self.TFE.bestScores.index(mins)] = self.TFE.actualScore
                    tv = "Your score is %d"%(self.TFE.actualScore)
                    self.window.update()
                    d = game_over_box(self.canvas2, self, tv)
                    self.window.wait_window(d.top)
            except:
                pass
            

    def display_best_scores(self):
        """
        display the top five scores.
        """
        self.window.update()
        d = best_score_box(self.canvas2, self, self.TFE.bestScores)
        self.window.wait_window(d.top)
        

    def run2048(self):
        """
        Rules to be maintained in the game.
        """
        self.reset()
        while not self.TFE.game_over():
            for dir in ['DOWN', 'LEFT', 'DOWN', 'RIGHT']:
                try:
                    self.TFE.move(dir)
                    self.update_score()
                    self.update_tiles()
                except:
                    pass
        
        
        tv = "Your score is %d"%(self.TFE.actualScore)
        self.window.update()
        d = game_over_box(self.canvas2, self, tv)
        self.window.wait_window(d.top)

    def exit_game(self):
        self.window.destroy()

class game_over_box():
    """
    when the game is over.
    """
    def __init__(self, parent, GUI, tv):
        self.top = Toplevel(master=parent, bg = "red", bd = 1)
        self.GUI = GUI
        Label(self.top, text = "GAME OVER!", bg = "red", font = ("Times", 30, "bold"), anchor=S).pack()
        Label(self.top, text = tv, bg = "red", font = ("Times", 25, "bold"), anchor = N, height = 2).pack()
        
        button1 = Button(self.top, text = "Play Again", width = 15, height = 2, bg = "SpringGreen2", font = ("Times", 20, "bold"), command = self.reset_and_exit)
        button1.pack(side=LEFT)
        button2 = Button(self.top, text = "Exit 2048", width = 15, height = 2, bg = "lavender", font = ("Times", 20, "bold"), command = self.GUI.window.destroy)
        button2.pack(side=RIGHT)
        
    def reset_and_exit(self):
        self.GUI.reset()
        self.top.destroy()
                    
class best_score_box():
    """
	kalra you need to implement a class to display the top 5
    scores when the "Best Scores" button is clicked.
    """
    def __init__(self, parent, GUI, scorelist):
        self.GUI = GUI
        self.bestScores = sorted(scorelist, reverse = True)
        self.top = Toplevel(master=parent, bg = "light blue", bd = 1)
        
        Label(self.top, text = "Top Five Scores", bg = "light blue", font = ("Times", 25, "bold"), anchor=S).pack()

        #iterate over the list of five scores and display each score
        for score in self.bestScores:
            Label(self.top, text = score, fg = "black", bg = "light blue", font = ("Times", 22, "bold"), anchor=S).pack()
            
        button1 = Button(self.top, text = "Back to the Game", width = 20, height = 2, bg = "lavender", font = ("Times", 20, "bold"), command = self.top.destroy)
        button1.pack()

        
if __name__ == "__main__":

	twentyfortyeight = TwentyFortyEight(4, 4)
	my2048GUI = TwentyFortyEight_GUI(twentyfortyeight)
	mainloop()
