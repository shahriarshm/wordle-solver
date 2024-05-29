from collections import defaultdict

import pandas as pd

dataset_path = "datasets/english_unigram_freq.csv"
word_length = 5
output_path = "datasets/5_letter_scored_english_words.csv"

words = pd.read_csv(dataset_path)  # Dataset should have at least 'word' column.
words["word"] = words["word"].str.lower()

# Count common letters in all words.
letters = defaultdict(int)
for word in words["word"]:
    for letter in str(word):
        letters[letter] += 1

words["score"] = words["word"].map(lambda w: sum(letters[l] for l in set(str(w))))

words = words[words["word"].str.len() == word_length]

words.to_csv(output_path, index=False)
