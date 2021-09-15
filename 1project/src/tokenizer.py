def tokenize_text(file):
    # step 0: read the text word by word or line by line.
    with open(file) as f:
        lines = f.readlines()
        # print(lines)
    tokenized = []
    for line in lines:
        # step 1.1: all non-period punctuation is a word separator. remove punctuation
        # initializing punctuations string
        punc = '''!()-[]\{\};:'"\,<>/?@#$%^&*_~'''
        # removing punctuations in string
        for elem in line:
            if elem in punc:
                line = line.replace(elem, " ")
        # step 1.2: period and abbrev. checking
        length = len(line)
        temp = ""
        for index in range(length):
            if line[index] == '.':
                # check for single letter acronyms and replace . with ""
                if line[index + 1] != " " and line[index + 2] == ".":
                    temp += ""
                    length -= 1
                else: 
                    temp += " "
            else:
                temp += line[index]
        line = temp
        #  step 1.3 lowercase all
        line = line.lower()
        for word in line.split():
            tokenized.append(word)
    return tokenized

# UPDATE 9/12/21: my tokenizer will separate urls and will keep single letter abbreviations together. f Ph.ds they can suffer.
# should i remove one-letter words? i think they are important sometimes... .... ... 


# step 2: implement stopword removal
def remove_stopwords(tokens):
    # step 0: read the text word by word or line by line.
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    vocab = []
    for word in tokens:
        if word not in stopwords:
            temp = word
            word = stem(word)
            # print(f'word:{temp} stemmed: {word}')
            vocab.append(word)
    return vocab
# step 3: Implement the first two steps of Porter stemming, as defined in the text. 
"""
step 1a
    - sses -> ss
    - delete s if preceding word part contains a vowel not immediately beore the s
    - replace ied or ies by i if preceded by more than one letter otherwise by ie
    if suffix is us or ss do nothing
step 1b
    - replace eed, eedly by ee if it is in the part of the word after the non vowel
        following a vowel
    - delete ed, edly, ing, ingly if the preceding word part contains a vowel, 
        and them if the word ends in at, bl, or iz add e, or if the word ends
        with a double letter that is not ll, ss, or zz (Falling > fall, 
        dripping > drip), remove the last letter,
        or if the word is short, add e (hoping -> hope)
"""
def stem(word):
    vowels = "aeiouy"
    suffixSet1 = set(["sses", "s", "ied", "ies", "ies" "eed", "eedly", "ed", "edly", "ing"])
    suffixSet2 = set(["at", "bl", "iz" ])
    if len(word) == 1:
        return word
    for suffix in suffixSet1:
        if word.endswith(suffix):
            if suffix == "sses":
                word = word.replace(suffix, "ss")
            elif suffix == "ied" or suffix == "ies":
                temp = word.replace(suffix, "")
                if len(temp) > 1:
                    word = word.replace(suffix, "i")
                else:
                    word = word.replace(suffix, "ie")
            elif suffix == "s":
                if word[-2] == 'e' or word[-2] not in vowels:
                    word = word.replace(word[-1], "")
            elif suffix == "eed" or suffix == "eedly":
                # TODO: how to find FIRST non-vowel following a vowel
                """
                Iterate through letter for first non vowel after a vowel
                then check for next vowel if = to suffix
                    if yes, word = word.replace(suffix, "ee")
                    else: break early
                """
            elif suffix == "ed" or suffix == "edly" or suffix == "ing" or suffix == "ingly":
                # TODO:
                temp = word.replace(suffix, "")
                for letter in reversed(temp):
                    # print(f'letter: {letter} temp: {temp}')
                    if letter in vowels:
                        word = word.replace(suffix, "")
                        # print(f'word: {word}')
                        if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
                            # unit tested for pirated, pirating
                            word += "e"
                        elif word[-1] == word[-2] and (word[-2:] != "ll" and word[-2:] != "ss" and word[-2:] != "zz"):
                            # print(f'word: {word}, word[-1]:{word[-1]}')
                            # unit tested for
                            word = word[:-1]
                            # print(word)
                        elif len(word) <= 3:
                            # unit tested for hoping
                            word += "e"
                        # print("Break")
                        break
    return word


def tokenization(file):
    tokenized = tokenize_text(file)
    # print(f'tokenized: {tokenized}')
    no_stopwords = remove_stopwords(tokenized)
    print(f'no stopwords: {no_stopwords}')
    return no_stopwords

# testing
# tokenization("tokenization-input-part-A.txt")
tokenization("test.txt")
# word = "word"
# print(word[-2:])
# vowels = "aeiou"
# if word[-2] not in vowels:
#     word = word.replace(word[-1], "")
# print(word)
