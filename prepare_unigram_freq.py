import pandas as pd

wikipedia = pd.read_csv("datasets/en-wikipedia.csv")  # should include content of each page
words = pd.read_csv("datasets/en-words.csv")  # should include unique meaningful words

words_count = {w: 0 for w in words["word"]}

for content in wikipedia["content"]:
    for word in content.split():
        if (w := word.strip()) in words_count:
            words_count[w] += 1

df = pd.DataFrame({"word": words_count.keys(), "count": words_count.values()})
df.to_csv("english_unigram_freq.csv", index=False)
