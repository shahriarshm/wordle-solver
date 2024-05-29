import re
import sys
from collections import defaultdict


import tkinter as tk
import pandas as pd


class WordleSolverApp:
    def __init__(self, root, words_dataset_path):
        self.root = root
        self.root.title("Wordle Solver")
        
        self.colors = ['#3a3a3c', '#b59f3b', '#538d4e']  # gray, yellow, green
        self.current_colors = [0, 0, 0, 0, 0]  # To keep track of the current color index for each letter box

        self.letter_boxes = []
        for i in range(5):
            canvas = tk.Canvas(root, width=40, height=40, bg=self.colors[0], highlightthickness=1, highlightbackground="black")
            canvas.grid(row=0, column=i, padx=5, pady=5)
            canvas.bind("<Button-1>", lambda e, i=i: self.toggle_color(i))
            canvas.create_text(20, 20, text='', tags=f"text_{i}")
            self.letter_boxes.append(canvas)

        self.guess_button = tk.Button(root, text="Guess", command=self.guess)
        self.guess_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.grid(row=1, column=3, columnspan=2, pady=10)

        self.words_list = tk.Listbox(root, width=30, height=5)
        self.words_list.grid(row=2, column=0, columnspan=5, pady=10)

        self.words_list.bind('<<ListboxSelect>>', self.on_word_select)

        self.words_df = pd.read_csv(words_dataset_path, index_col="word")

        self.initiate_game_state()

    def initiate_game_state(self):
        self.is_first_guess = True
        self.candidate_words = []
        self.incorrect_positions = defaultdict(set)
        self.correct_letters = set()
        self.incorrect_letters = set()
        self.word_pattern = ["\w", "\w", "\w", "\w", "\w"]

    def toggle_color(self, index):
        self.current_colors[index] = (self.current_colors[index] + 1) % len(self.colors)
        new_color = self.colors[self.current_colors[index]]
        self.letter_boxes[index].configure(bg=new_color)

    def guess(self):
        if self.is_first_guess:
            self.candidate_words = ["apple"] * 5
            self.is_first_guess = False
        else:
            for index in range(5):
                color = self.current_colors[index]
                letter = self.letter_boxes[index].itemcget(f"text_{index}", 'text').lower()

                if color == 0:  # gray
                    self.incorrect_letters.add(letter)
                elif color == 1:  # yellow
                    self.correct_letters.add(letter)
                    self.incorrect_positions[letter].add(index)
                else:  # green
                    self.correct_letters.add(letter)
                    self.word_pattern[index] = letter

            pattern = re.compile("".join(self.word_pattern))

            filter_func = lambda w: all(l in w for l in self.correct_letters) \
                and not any(l in w for l in self.incorrect_letters) \
                and not any(w.index(l) in self.incorrect_positions[l] for l in w)
        
            candidates = self.words_df[self.words_df.index.str.match(pattern) & self.words_df.index.map(filter_func)]
            self.candidate_words = candidates.sort_values("count", ascending=False).head(5) \
                .sort_values("score", ascending=False).index.to_list()

        self.update_word_list()

    def reset(self):
        for i in range(5):
            self.current_colors[i] = 0
            self.letter_boxes[i].configure(bg=self.colors[0])
            self.letter_boxes[i].itemconfig(f"text_{i}", text='')
        
        self.initiate_game_state()
        self.update_word_list()

    def update_word_list(self):
        self.words_list.delete(0, tk.END)
        for word in self.candidate_words:
            self.words_list.insert(tk.END, word.upper())

    def on_word_select(self, event):
        selected_index = self.words_list.curselection()
        if selected_index:
            selected_word = self.words_list.get(selected_index)
            self.update_letter_boxes(selected_word)

    def update_letter_boxes(self, word):
        for i in range(5):
            self.current_colors[i] = 0
            self.letter_boxes[i].configure(bg=self.colors[0])
            if i < len(word):
                self.letter_boxes[i].itemconfig(f"text_{i}", text=word[i].upper())
            else:
                self.letter_boxes[i].itemconfig(f"text_{i}", text='')


if __name__ == "__main__":
    path_dataset = sys.argv[1]

    root = tk.Tk()
    app = WordleSolverApp(root, path_dataset)
    root.mainloop()
