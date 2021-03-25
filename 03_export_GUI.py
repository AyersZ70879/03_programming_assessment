from tkinter import *
from functools import partial   # To prevent unwanted windows
import random
import csv


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
        global how_many_r
        how_many_r = starting_rounds

        # initialise variables
        self.rounds = IntVar()

        # List for holding stats
        self.game_stats_list = []
        self.rounds_stats = []


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
                                   bg="#468faf", fg="white", command=self.to_stats(self.rounds_stats, self.game_stats_list))
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#f07167", font="Arial 15 bold",
                                  width=20, command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=8, pady=10)

    # Help section
    def help(self):
        get_help = Help(self)
        get_help.help_text.configure(text="There will be a country and its flag shown and all you need to do it figure out "
                                          "that country's capital! If you don't know take a guess.")

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)

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
        # get rounds for stats
        self.rounds_stats.append(get_rounds)
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
        capital_guess = self.capital_entry.get().lower()   # ***for error testing this code works***


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
            # disable check button
            self.check_button.config(state=DISABLED)
            # change entry background
            self.capital_entry.config(bg=error_back)

            # if there are rounds left
            if get_rounds != how_many_r:
                # enable next button
                self.next_button.config(state=NORMAL)
                # user answer feedback
                self.capital_answer.config(text="Incorrect! The capital is {}".format(capital_ans))
            else:
                # user answer feedback
                self.capital_answer.config(text="Incorrect! The capital is {}.\n\n"
                                                "Game Over! Click Game Stats to view your game "
                                                "statistics".format(capital_ans))

        # if guess is correct
        else:
            # disable check button
            self.check_button.config(state=DISABLED)
            # change bg to green in entry box
            self.capital_entry.config(bg="#CAFFBF")

            # if rounds are left
            if get_rounds != how_many_r:
                # enable next button
                self.next_button.config(state=NORMAL)
                # user answer feedback
                self.capital_answer.config(text="Correct!")

            else:
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


# Game Stats
class GameStats:
    def __init__(self, partner, game_history, game_stats):

        all_game_stats = [
            "Rounds Played: {}".format(game_history),
            #"Number of Correct Answers: ${}".format(game_stats[0]),
            #"Number of Incorrect Answers: ${}".format(game_stats[1])
        ]

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        # Sets up child windows (ie: help box)
        self.stats_box = Toplevel()

        # If users press cross at top, closes help and 'releases' button

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # Set up GUI Frame
        self.stats_frame = Frame(self.stats_box, bg="#DDF0FF")
        self.stats_frame.grid()

        # Set up a Help heading (row 0)
        self.stats_heading_label = Label(self.stats_frame, text="Game Stats",
                                         font="arial 19 bold", bg="#DDF0FF")
        self.stats_heading_label.grid(row=0)

        # To export <instructions> (row 1)
        self.export_instructions = Label(self.stats_frame,
                                         text="Here are your Game Stats. "
                                              "Please use the Export Button to "
                                              "access the results of each round "
                                              "that you played.", wrap=250, font="arial 10 italic",
                                         justify=LEFT, fg="green", padx=10, pady=10, bg="#DDF0FF")
        self.export_instructions.grid(row=1)

        # Stats Frame (row 2)
        self.details_frame = Frame(self.stats_frame, bg="#DDF0FF")
        self.details_frame.grid(row=2)

        # Rounds played(row 2.0)

        self.rounds_played_label = Label(self.details_frame, text="Rounds Played",
                                         font=heading, anchor="e", bg="#DDF0FF")
        self.rounds_played_label.grid(row=0, column=0, padx=0)

        self.start_rounds_played_label = Label(self.details_frame, font=content,
                                               text="{}".format(get_rounds),
                                               anchor="w", bg="#DDF0FF")
        self.start_rounds_played_label.grid(row=0, column=1, padx=0)

        # Current Balance (row 2.2)
        self.current_balance_label = Label(self.details_frame, text="Number of Answers Correct: ",
                                           font=heading, anchor="e", bg="#DDF0FF")
        self.current_balance_label.grid(row=1, column=0, padx=0)

        self.current_balance_value_label = Label(self.details_frame, font=content,
                                                 text="{}".format(game_stats[1]), bg="#DDF0FF")
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        # Export Button
        self.export_button = Button(self.details_frame, text="Export", font="Arial 10 bold",
                                    bg="orange")
        self.export_button.grid(row=5, column=0, padx=2)

        # Dismiss button (row 3)
        self.dismiss_btn = Button(self.details_frame, text="Dismiss", width=10, bg="orange",
                                  font="arial 10 bold", command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=5, column=1, pady=10)

    def export(self, game_history, all_game_stats):
        Export(self, game_history, all_game_stats)

    def close_stats(self, partner):
        # Put stats button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()

# Export section
class Export:
    def __init__(self, partner, game_history, all_game_stats):

        # Disable export button
        partner.export_button.config(state=DISABLED)

        # Sets up child window (ie: export box)
        self.export_box = Toplevel()

        # If users press cross at top, closes export and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        # Set up GUI frame
        self.export_frame = Frame(self.export_box, width=300)
        self.export_frame.grid()

        # Set up export heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions", font="arial 14 bold")
        self.how_heading.grid(row=0)

        # Export Instructions (label, row 1)
        self.export_text = Label(self.export_frame, text="Enter a filename in the box below and press the "
                                                         "Save button to save your calculation history to "
                                                         "text file.", justify=LEFT, width=40, wrap=250)
        self.export_text.grid(row=1)

        # Warning text (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, "
                                                         "its contents will be replaced with your calculation "
                                                         "history", justify=LEFT, bg="#ffafaf", fg="maroon",
                                 font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # Filename Entry Box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20, font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # Error Message Labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)

        # Save / Cancel Frame (row 5)
        self.save_frame = Frame(self.export_box)
        self.save_frame.grid(row=5, pady=10)

        # Save and Cancel Buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_frame, text="Save", font="Arial 15 bold", bg="#003366",
                                  fg="white",
                                  command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=1)

    def save_history(self, partner, game_history, game_stats):

        # Regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        filename = self.filename_entry.get()

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "(No spaces allowed)"

            else:
                problem = ("(No {}'s allowed)".format(letter))
            has_error = "yes"
            break

        if filename == "":
            problem = "File name can't be blank"
            has_error = "yes"

        if has_error == "yes":
            self.filename_entry.config(bg="#ffafaf")
            self.save_error_label.config(text="Invalid Name: {}".format(problem))

        else:
            # If there are no errors, generate text filename and then close dialogue
            # add .txt suffix
            filename = filename + ".txt"

            # Create file to hold data
            f = open(filename, "w+")

            # Heading for stats
            f.write("**Game Statistics**\n\n")

            # Game stats
            for round in game_stats:
                f.write(round + "\n")

            # Heading for Rounds
            f.write("\nRound Details\n\n")

            # Add new line at end of each item
            for item in game_history:
                f.write(item + "\n")

            # close file
            f.close()

            # close dialogue
            self.close_export(partner)

    def close_export(self, partner):
        # Put export button back to normal...
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Country - Capital Game")
    something = Start(root)
    root.mainloop()
