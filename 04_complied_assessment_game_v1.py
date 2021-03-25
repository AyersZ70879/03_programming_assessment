from tkinter import *
from functools import partial   # To prevent unwanted windows
import random
import csv

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

        self.play_button = Button(self.play_frame, text="Play", command=self.to_game,
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

        Game(self, starting_rounds_set)

        # hide start up window
        root.withdraw()


class Game:
    def __init__(self, partner, starting_rounds):
        global how_many_r
        how_many_r = starting_rounds

        # initialise variables
        self.rounds = IntVar()

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
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT,
                                        text="Guess the country's capital and "
                                             "see how many you can get "
                                             "correct!"
                                             " Punctuation does matter.")
        self.instructions_label.grid(row=1)

        # Country go here (row 2)

        # Set up country frame
        self.country_frame = Frame(self.game_frame)
        self.country_frame.grid(row=2, pady=10, padx=10)

        # Country question label
        self.country_q_label = Label(self.country_frame, text="Press Start to play", font="Arial 10 bold",
                                     wrap=275, justify=LEFT)
        self.country_q_label.grid(row=0, column=0, pady=5)

        # Country display label

        self.country_label = Label(self.country_frame, text="", font="Arial 18 bold",
                                   wrap=275, justify=LEFT)
        self.country_label.grid(row=2, pady=5)

        # Country flag display - might have to be moved to ccp function and have the display below
        self.country_p_label = Label(self.country_frame, image="",
                                     padx=10, pady=10)
        self.country_p_label.grid(row=1, column=0)

        # Capital goes here (row 3)
        self.capital_frame = Frame(self.game_frame)
        self.capital_frame.grid(row=3, pady=10, padx=10)

        self.capital_entry = Entry(self.capital_frame, font="Arial 15 bold")
        self.capital_entry.grid(row=0, column=0, ipady=10)

        # Check button goes here (row 3)
        self.check_button = Button(self.capital_frame, text="Check", bg="#8ecae6", font="Arial 15 bold",
                                   padx=5, pady=5, command=self.check)
        self.check_button.grid(row=0, column=1)
        # Disable check button before user starts game
        self.check_button.config(state=DISABLED)

        # Capital answer display (row 3)
        self.capital_answer = Label(self.game_frame, text="", font="Arial 10 bold",
                                    wrap=275, justify=LEFT)
        self.capital_answer.grid(row=4, pady=10)

        # Next button goes here (row 5)
        self.next_button = Button(self.game_frame, text="Start Game", bg="#adc178", font="Arial 15 bold",
                                  width=20, padx=10, pady=10, command=self.get_ccp)
        # grid setup of button
        self.next_button.grid(row=5)

        # Balance label (row 6)
        self.rounds_frame = Frame(self.game_frame)
        self.rounds_frame.grid(row=6, pady=10, padx=10)

        start_text = "Round: "

        self.rounds_label = Label(self.rounds_frame, font="Arial 12 bold", fg="#80b918",
                                  text=start_text)
        self.rounds_label.grid(row=0, column=0, pady=10)

        self.rounds1_label = Label(self.rounds_frame, font="Arial 12 bold", fg="#80b918", text="0")
        self.rounds1_label.grid(row=0, column=1, pady=10)

        # Help and Game stats button (row 7)
        self.help_export_frame = Frame(self.game_frame, bg="#DDF0FF")
        self.help_export_frame.grid(row=7, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules", font="Arial 15 bold",
                                  bg="#f6bd60", fg="white", command=self.help)
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats", font="Arial 15 bold",
                                   bg="#468faf", fg="white")
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#f07167", font="Arial 15 bold",
                                  width=20, command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=8, pady=10)

    # Help section
    def help(self):
        get_help = Help(self)
        get_help.help_text.configure(
            text="There will be a country and its flag shown and all you need to do it figure out "
                 "that country's capital! If you don't know take a guess.")

    # retrieve information from csv file function
    def get_ccp(self):

        # --- Configure display (below) ---

        # When user plays game, change label
        self.next_button.config(text="Next")
        # Disable next button
        self.next_button.config(state=DISABLED)
        # enable check button
        self.check_button.config(state=ACTIVE)
        # Change background to white
        self.capital_entry.config(bg="white")
        # clear capital answer
        self.capital_answer.config(text="")
        # clear entry box field
        self.capital_entry.delete(0, 'end')
        # change question label
        self.country_q_label.config(text="What is the capital of: ")
        # add rounds when next button is clicked
        global get_rounds
        get_rounds = self.rounds.get()
        get_rounds += 1
        self.rounds.set(get_rounds)
        self.rounds1_label.config(text=get_rounds)
        # for testing
        print(get_rounds)

        # Open csv file and get provided information
        with open("00_country_capital.csv") as f:
            reader = csv.reader(f)
            reader = list(reader)

            # deletes first row in csv file
            del reader[0]

            # get randomised country, capital and image
            randomised_reader = random.choice(reader)

            # Split into variables
            country = randomised_reader[0]
            global capital_ans
            capital_ans = randomised_reader[1]
            image_file = randomised_reader[2]

            # -- Display for game --

            # Country label
            self.country_label.config(text=country)

            # Display image
            photo = PhotoImage(file=image_file)
            self.country_p_label.config(image=photo)
            self.country_p_label.photo = photo

        # *** For testing Purposes ***
        print(capital_ans)

    # Check user input function
    def check(self):
        # Get capital from above function
        get_capital_answer_lo = capital_ans.lower()

        # get user input
        capital_guess = self.capital_entry.get().lower()  # ***for error testing this code works***

        # error setup
        error_back = "#ffafaf"
        has_errors = "no"

        # -- Error types below --

        capital_guess = str(capital_guess)
        # if left blank
        if capital_guess == "":
            has_errors = "yes"
            error_feedback = "Please do not leave this field blank.\nHINT: The capital starts with the " \
                             "letter '{}'".format(capital_ans[0])

        # if guess is incorrect
        elif capital_guess != get_capital_answer_lo:
            if get_rounds != how_many_r:
                # disable check button
                self.check_button.config(state=DISABLED)
                # change entry background
                self.capital_entry.config(bg=error_back)
                # enable next button
                self.next_button.config(state=NORMAL)
                # user answer feedback
                self.capital_answer.config(text="Incorrect! The capital is {}".format(capital_ans))
            else:
                # disable check button
                self.check_button.config(state=DISABLED)
                # change entry background
                self.capital_entry.config(bg=error_back)
                # user answer feedback
                self.capital_answer.config(text="Incorrect! The capital is {}.\n\n"
                                                "Game Over! Click Game Stats to view your game "
                                                "statistics".format(capital_ans))

        # if guess is correct
        else:
            if get_rounds != how_many_r:
                # enable next button
                self.next_button.config(state=NORMAL)
                # change bg to green in entry box
                self.capital_entry.config(bg="#CAFFBF")
                # disable check button
                self.check_button.config(state=DISABLED)
                # user answer feedback
                self.capital_answer.config(text="Correct!")
            else:
                # disable check button
                self.check_button.config(state=DISABLED)
                # change bg to green in entry box
                self.capital_entry.config(bg="#CAFFBF")
                # user answer feedback
                self.capital_answer.config(text="Correct!\n\n"
                                                "Game Over! Click Game Stats to view your game "
                                                "statistics")

        # if user enters an invalid string
        if has_errors == "yes":
            self.capital_entry.config(bg=error_back)
            self.capital_answer.config(text=error_feedback)

    def to_quit(self):
        root.destroy()


# Help GUI
class Help:
    def __init__(self, partner):
        background = "#fbc4ab"

        # disable help button
        partner.help_button.config(state=DISABLED)

        # Sets up child window (ie: help box)
        self.help_box = Toplevel()

        # If users press the cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Set up GUI Frame

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        # Set up Help Heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions", font="arial 14 bold",
                                 bg=background)
        self.how_heading.grid(row=0)

        # Help text (label, row 1)
        self.help_text = Label(self.help_frame, text="", justify=LEFT, width=40, bg=background,
                               wrap=250)
        self.help_text.grid(column=0, row=1)

        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="#f4978e",
                                  font="arial 10 bold", command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        # Put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country - Capital Game")
    something = Start(root)
    root.mainloop()
