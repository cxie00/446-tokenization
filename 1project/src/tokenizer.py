def tokenize_text(file):
    # step 0: read the text word by word or line by line.
    with open(file) as f:
        lines = f.readlines()

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
                if index < len(line) - 2:
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

# step 2: implement stopword removal
def remove_stopwords_stem(tokens):
    # step 0: read the text word by word or line by line.
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    corpus = []
    vocab = {}
    for word in tokens:
        if word not in stopwords:
            temp = word
            if len(word) != 1:
                word = stem(word)
                # print(f'word:{temp} stemmed: {word}')
                corpus.append(word)
                if word in vocab:
                    vocab[word] += 1
                else:
                    vocab[word] = 1
    return (corpus, vocab)

# step 3: Implement the first two steps of Porter stemming, as defined in the text. 
def stem(word):
    vowels = "aeiouy"
    suffix = get_suffix(word)
    if len(word) < 4:
        return word
    if suffix == "sses":
        # print(f'word: {word} suffix: {suffix}')
        word = word.replace(suffix, "ss")
        return word
    elif suffix == "ied" or suffix == "ies":
        # print(f'word: {word} suffix: {"ies"}')
        temp = word.replace(suffix, "")
        if len(temp) > 1:
            word = word.replace(suffix, "i")
        else:
            word = word.replace(suffix, "ie")
        return word
    elif suffix == "s":
        # print(f'word: {word} suffix: {suffix}')
        if word[-2] == 'e' or word[-2] not in vowels:
            word = word[:-1]
        return word
    elif  suffix == "eed" or suffix == "eedly":
        # print(f'word: {word} suffix: {suffix}')
        """
        Iterate through letter for first non vowel after a vowel
        then check for next vowel if = to suffix
            if yes, word = word.replace(suffix, "ee")
            else: break early
        """
        # print(f'{word} {suffix}')
        first_vowel = False
        non_vowel = False
        for index in range(len(word)):
            if word[index] in vowels and not first_vowel:
                first_vowel = True
            elif word[index] not in vowels and first_vowel:
                non_vowel = True
            elif word[index] in vowels and first_vowel and non_vowel:
                # conditional above means: in part of word after first non-vowel following a vowel
                if word[index:] == suffix:
                    word = word.replace(suffix, "ee")
                else:
                    break
        return word
    elif suffix == "ed" or suffix == "edly" or suffix == "ing" or suffix == "ingly":
        # print(f'word: {word} suffix: {suffix}')
        temp = word.replace(suffix, "", 1)
        for letter in reversed(temp):
            if letter in vowels:
                word = word.replace(suffix, "", 1)
                if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
                    word += "e"
                elif word[-1] == word[-2] and (word[-2:] != "ll" and word[-2:] != "ss" and word[-2:] != "zz"):
                    word = word[:-1]
                elif len(word) <= 3 and word[-1] != "y":
                    word += "e"
                return word 
    return word

def get_suffix(word):
    if word.endswith("sses"):
        return "sses"
    elif word.endswith("ss"):
        return ""
    elif word.endswith("us"):
        return ""
    elif word.endswith("s"):
        return "s"
    elif word.endswith("ied"):
        return "ied"
    elif word.endswith("ies"):
        return "ies"
    elif word.endswith("eed"):
        return "eed"
    elif word.endswith("ed"):
        return "ed"
    elif word.endswith("eedly"):
        return "eedly"
    elif word.endswith("edly"):
        return "edly"
    elif word.endswith("ing"):
        return "ing"
    elif word.endswith("ingly"):
        return "ingly"
    return ""

def tokenization(file):
    tokenized = tokenize_text(file)
    corpus, vocab = remove_stopwords_stem(tokenized)
    return corpus, vocab

# testing
# tokenization("tokenization-input-part-A.txt")
# tokenization("test2.txt")

corpus, vocab = tokenization("tokenization-input-part-B.txt")
sort_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
count = 0 
for i in sort_vocab:
    if count > 199:
        break
    count +=1
    print(i[0], i[1])
print(f'num words in corpus: {len(corpus)} | num words in vocab: {len(vocab)}')