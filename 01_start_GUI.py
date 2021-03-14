from tkinter import *
from functools import partial   # To prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        # GUI to get number of rounds
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Set initial balance to zero
        self.starting_rounds = IntVar()
        self.starting_rounds.set(0)

        # Quiz Heading (row 0)
        self.quiz_box_label = Label(self.start_frame, text="Country - Capital Game", font="Arial 19 bold")
        self.quiz_box_label.grid(row=0)

        # Quiz Box Description (row 1)
        self.quiz_instructions = Label(self.start_frame, text="Please enter the number of rounds "
                                                              "you would like to play (between 1-10) and "
                                                              "press the 'Start' button to play.", font="Arial 10 italic", wrap=275,
                                          justify=LEFT, padx=10, pady=10)
        self.quiz_instructions.grid(row=1)

        # Entry box and error frame (row 2)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=0, column=0)

        self.add_rounds_button = Button(self.entry_error_frame, font="Arial 14 bold", text="Check",
                                       command=self.check_rounds)
        self.add_rounds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon", text="", font="Arial 10 bold",
                                        wrap=275, justify=LEFT)
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # Play
        self.play_frame = Frame(padx=5, pady=5, width=200)
        self.play_frame.grid(row=3)

        self.play_button = Button(self.play_frame, text="Play", command=lambda: self.to_game,
                                        font="Arial 12 bold", bg="#87986a")
        self.play_button.grid(row=0, column=0, pady=10)

        # Disable play button at start
        self.play_button.config(state=DISABLED)

    # check rounds function
    def check_rounds(self):
        starting_rounds_set = self.start_amount_entry.get()


        # Set error background and colours (and assume no errors at the start
        error_back = "#ffafaf"
        has_errors = "no"

        # Change background to white (fr testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # If error disable button
        self.play_button.config(state=DISABLED)

        try:
            starting_rounds_set = int(starting_rounds_set)

            if starting_rounds_set < 1:
                has_errors = "yes"
                error_feedback = "Sorry, the least amount of rounds you can play is 1"
            elif starting_rounds_set > 10:
                has_errors = "yes"
                error_feedback = "The most amount of rounds you can play is 10"

            else:
                self.play_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter an integer (not text or decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            # set starting balance to amount entered by user
            self.starting_rounds.set(starting_rounds_set)
            self.start_amount_entry.config(bg="#b7e4c7")


    # to_game function
    def to_game(self):
        starting_rounds_set = self.starting_rounds.get()

        Game(self, starting_rounds)

        # hide start up window
        root.withdraw()


class Game:
    def __init__(self, partner, starting_rounds):
        print("Accepted")



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country - Capital Game")
    something = Start(root)
    root.mainloop()
