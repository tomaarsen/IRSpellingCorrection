import json

#Open the files consting all english words and store it in english_words

# with open('data/raw/english_words/words.txt') as word_file1:
#     all_words = set(word.strip().lower() for word in word_file1)

# with open('data/raw/english_words/words_subset1.txt') as word_file2:
#     all_words_subset1 = set(word.strip().lower() for word in word_file2)

with open('data/raw/english_words/words_subset2.txt') as word_file3:
    all_words_subset2 = set(word.strip().lower() for word in word_file3)

#Store parsed.json in dictionary
with open('data/processed/parsed.json') as parsed_file:
    parsed = json.load(parsed_file)

def is_english_word(word, english_words):
    """
    Changes all letters in word to lower chase and check if it exits in the set english words
    """
    return word.lower() in english_words

def create_filter(path_to_file):
    """
    Creates a file that consist of english words that make sense and are not obscure, those words don't 
    need to be flagged as misspellings
    """
    with open(path_to_file, 'w+') as file:
        for key in parsed:
            if is_english_word(key, all_words_subset2):
                file.write(key + '\n')
    file.close()
        
if __name__ == "__main__":
    create_filter('data/raw/filter.dat')


