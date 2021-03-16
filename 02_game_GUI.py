from tkinter import *
from functools import partial   # To prevent unwanted windows
import random

rounds = 0

class Start:
    def __init__(self, parent):

        # GUI to get starting balances and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Play Button
        self.push_me_button = Button(self.start_frame, text="Push Me", command=self.to_game)
        self.push_me_button.grid(row=0, pady=10)

    def to_game(self):
        # retrieve starting rounds
        starting_rounds = 3

        Game(self, starting_rounds)

        # hide start up window
        self.start_frame.destroy()


class Game:
    def __init__(self, partner, starting_rounds):
        print(starting_rounds)

        # initialise variables
        self.rounds = IntVar()

        # Set starting balance to amount entered by the user at the start if the game
        self.rounds.set(starting_rounds)

        # List for holding stats
        self.round_stats_list = []

        # GUI Setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # If user press cross at top, game quits
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # Heading Row
        self.heading_label = Label(self.game_frame, text="Play...", font="Arial 24 bold",
                                   padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Instructions Label
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT, text="Guess the country's capital and "
                                                                                      "see how many you can get correct!")
        self.instructions_label.grid(row=1)

        # Capital go here (row 2)

        self.country_frame = Frame(self.game_frame)
        self.country_frame.grid(row=2, pady=10)

        # photo = PhotoImage(file="question.gif")

        # Check button goes here (row 3)
        self.check_button = Button(self.game_frame, text="Check Answer", bg="#FDEA9B", font="Arial 15 bold",
                                  width=20, padx=10, pady=10, command=self.check_answer)

        # bind button to <enter> (users can push to reveal the boxes)
        self.check_button.focus()
        self.check_button.bind('<Return>', lambda e: self.check_answer())
        self.check_button.grid(row=3)

        # Balance label (row 4)

        start_text = "Round: {} ".format(rounds + 1)

        self.balance_label = Label(self.game_frame, font="Arial 12 bold", fg="green",
                                   text=start_text, wrap=300, justify=LEFT)
        self.balance_label.grid(row=4, pady=10)

        # Help and Game stats button (row 5)
        self.help_export_frame = Frame(self.game_frame, bg="#DDF0FF")
        self.help_export_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules", font="Arial 15 bold",
                                  bg="#808080", fg="white")
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats", font="Arial 15 bold",
                                   bg="#003366", fg="white")
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#660000", font="Arial 15 bold",
                                  width=20, command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    def check_answer(self):
        # retrieve of the balance from the initial function..
        print("in progress")


    def to_quit(self):
        root.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
