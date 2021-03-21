from tkinter import *
from functools import partial   # To prevent unwanted windows
import random
import csv

rounds = 0

# Make a list function
def make_list(file_name):
    file_name = file_name+ ".csv"  # add .csv to names to make it easier to call
    list_name = open(file_name).read().splitlines()
    return list_name


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
        self.heading_label = Label(self.game_frame, text="Country - Capital \nGame", font="Arial 24 bold",
                                   padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Instructions Label
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT, text="Guess the country's capital and "
                                                                                      "see how many you can get correct!")
        self.instructions_label.grid(row=1)

        # Country go here (row 2)

        # Set up country frame
        self.country_frame = Frame(self.game_frame)
        self.country_frame.grid(row=2, pady=10)

        # Country question label
        self.country_q_label = Label(self.country_frame, text="What is the capital of: ", font="Arial 10 bold",
                                        wrap=275, justify=LEFT)
        self.country_q_label.grid(row=0, column=0, pady=5)

        # Country display label

        self.country_label = Label(self.country_frame, text="", font="Arial 18 bold",
                                        wrap=275, justify=LEFT)
        self.country_label.grid(row=1, column=1, pady=5)

        # Country flag display - might have to be moved to ccp function and have the display below
        self.country_p_label = Label(self.country_frame, image="",
                                padx=10, pady=10)
        self.country_p_label.grid(row=1, column=0)

        # Capital goes here (row 3)
        self.capital_frame = Frame(self.game_frame)
        self.capital_frame.grid(row=3, pady=10)

        self.capital_entry = Entry(self.capital_frame, font="Arial 16 bold")
        self.capital_entry.grid(row=0, column=0)

        # Check button goes here (row 4)
        self.check_button = Button(self.game_frame, text="Start Game", bg="#adc178", font="Arial 15 bold",
                                  width=20, padx=10, pady=10, command=self.get_ccp)

        # Bind button to <enter> (users can push to reveal the boxes)
        self.check_button.focus()
        self.check_button.bind('<Return>', lambda e: self.get_ccp())
        # grid setup of button
        self.check_button.grid(row=4)

        # Balance label (row 4)
        start_text = "Round: {} ".format(rounds + 1)

        self.balance_label = Label(self.game_frame, font="Arial 12 bold", fg="#80b918",
                                   text=start_text, wrap=300, justify=LEFT)
        self.balance_label.grid(row=5, pady=10)

        # Help and Game stats button (row 5)
        self.help_export_frame = Frame(self.game_frame, bg="#DDF0FF")
        self.help_export_frame.grid(row=6, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules", font="Arial 15 bold",
                                  bg="#f6bd60", fg="white")
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats", font="Arial 15 bold",
                                   bg="#468faf", fg="white")
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#f07167", font="Arial 15 bold",
                                  width=20, command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=7, pady=10)

    # retrieve information from csv file function
    def get_ccp(self):
        self.check_button.config(text="Check Answer")
        with open("00_country_capital.csv") as f:
            reader = csv.reader(f)
            reader = list(reader)
            randomised_reader = random.choice(reader)

            # Split into variables
            country = randomised_reader[0]
            capital_ans = randomised_reader[1]
            image_file = randomised_reader[2]

            # -- Display for game --
            # country label
            self.country_label.config(text=country)
            # display image
            photo = PhotoImage(file=image_file)
            self.country_p_label.config(image=photo)
            self.country_p_label.photo = photo

    # MIGHT NOT NEED THIS FUNCTION -- TBD
    # def check_answer(self):
    #    # retrieve of the rounds from the initial function..
    #    self.rounds.set(+1)
    #    print("in progress")

    def to_quit(self):
        root.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country - Capital Game")
    something = Start(root)
    root.mainloop()
