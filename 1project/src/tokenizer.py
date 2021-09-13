def tokenize_text(file):
    # step 0: read the text word by word or line by line.
    with open(file) as f:
        lines = f.readlines()
        print(lines)
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
def remove_stopwords(tokenized_text):
    # step 0: read the text word by word or line by line.
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    text_no_sw = []
    for word in tokenized_text:
        if word not in stopwords:
            text_no_sw.append(word)
    return text_no_sw
# step 3: Implement the first two steps of Porter stemming, as defined in the text. 


def tokenization(file):
    tokenized = tokenize_text(file)
    print(f'tokenized: {tokenized}')
    no_stopwords = remove_stopwords(tokenized)
    print(f'no stopwords: {no_stopwords}')
    return no_stopwords
tokenization("tokenization-input-part-A.txt")
# testing
# print(tokenize_text("tokenization-input-part-A.txt"))
# print(remove_stopwords())

