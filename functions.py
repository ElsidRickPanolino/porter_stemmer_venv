import re
import string

# for testing
import random

# converts word to cv pattern
def wordTocv(word):
    cons = "bcdfghjklmnpqrstvwxz"
    vowels = "aeiouy"
    
    cv_pattern = ""
    
    if len(word)>0:

        for i in range(len(word)):
            if i==len(word)-1:
                cons = "bcdfghjklmnpqrstvwxyz"
                vowels = "aeiou"
                
            for c in cons:
                if word[i] == c:
                    cv_pattern += "c"
            for v in vowels:
                if word[i] == v:
                    cv_pattern += "v"
                    
    return cv_pattern

# group the c's and v's and returns CV patterns
def cvToCV(cv):
    CV = ""
    previous = ""
    for i in cv:
        if previous == "":
            if i == "c":
                CV += "C"
            
            if i == "v":
                CV += "V"
            previous = i
            continue
        
        if i == "c" and previous != "c":
            CV += "C"
            
        if i == "v" and previous != "v":
            CV += "V"
            
        previous = i
        
    return CV
        
# count the number of CV
def countM(CV):
    # while CV !="" and CV[-1]=='C':
    #     CV = CV[:-1]
    m = CV.count('VC')
    return m

# combine functions to count the value of M given the word
def wordToM(word):
    cv = wordTocv(word)
    CV = cvToCV(cv)
    m = countM(CV)
    return m

# porter stemer algorithm notation *s
# determine if the word ends with s or other letter
def endsWith(word, letter): 
    if word.endswith(letter):
        return True
    else:
        return False
    
# porter stemer algorithm notation *v*
# determine if the word ends contains vowel
def haveVowel(word): 
    pattern = r'^.*[aeiouAEIOU].*$'
    return re.match(pattern, word) is not None
    
# porter stemer algorithm notation *d
# determine if the word ends with double consonant
def doubleConsonant(word): 
    cv = wordTocv(word)
    if(len(word)>=2):
        if endsWith(cv, "cc") and word[-1] == word[-2]:
            return True
    else:
        return False
    
# porter stemer algorithm notation *o
# determine if the word ends with double consonant
def iscvc(word): 
    cv = wordTocv(word)
    if len(cv) >= 3:
        if endsWith(cv, "cvc"):
            if word[-1] != 'w' or word[-1] != 'x' or word[-1] != 'y':
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def replace_end(word, old, new):
    trim_size = len(old)*-1
    word = word [:trim_size]
    word += new
    return word

def changeWord(word, old, new):
        if endsWith(word, old):
            word = replace_end(word, old, new)
        return word

    
# to get the base word from the plural form
def step1a(word):
    suffix_list = [["sses", "ss"], ["ies", "i"], ["ss", "ss"], ["s", ""]]
    for i in suffix_list:
        if endsWith(word, i[0]):
            word = replace_end(word, i[0], i[1])
            break
    return word


def step1b(word):
    sec_and_third = False
    if wordToM(word) > 0:
        word = changeWord(word, "eed","ee")
        if haveVowel(word):            
            if endsWith(word, "ed"):
                word = replace_end(word, "ed","")
                sec_and_third = True

            elif endsWith(word, "ing"):
                word = replace_end(word, "ing","")
                sec_and_third = True

            if sec_and_third:
                if endsWith(word, "at"):
                    word = replace_end(word, "at","ate")
                elif endsWith(word, "bl"):
                    word = replace_end(word, "bl","ble")
                elif endsWith(word, "iz"):
                    word = replace_end(word, "iz","ize")
                if doubleConsonant(word) and not endsWith(word, "l") and not endsWith(word, "s") and not endsWith(word, "z"):
                    word = word[:-1]
                if wordToM(word) == 1 and iscvc(word):
                    word += "e"
                    
                    
    return word
      
def step1c(word):
    
    if endsWith(word, "y"):
        if haveVowel(word):
            word = replace_end(word, "y","i")
    return word

def step2(word):
    suffix_list = [["ational", "ate"], 
                   ["tional", "tion"], 
                   ["enci", "ence"], 
                   ["anci", "ance"], 
                   ["izer", "ize"], 
                   ["abli", "able"], 
                   ["alli", "al"], 
                   ["entli", "ent"], 
                   ["eli", "e"],
                   ["ousli", "ous"],
                   ["ization", "ize"],
                   ["ation", "ate"],
                   ["ator", "ate"],
                   ["alism", "al"],
                   ["iveness", "ive"],
                   ["fulness", "ful"],
                   ["ousness", "ous"],
                   ["aliti", "al"],
                   ["iviti", "ive"],
                   ["bility", "ble"]]

    if wordToM(word)>0:
        for i in suffix_list:
            if endsWith(word, i[0]):
                word = replace_end(word, i[0], i[1])
                break
    return word
    
def step3(word):
    suffix_list = [["icate", "ic"], 
                   ["ative", ""], 
                   ["alize", "al"], 
                   ["iciti", "ic"], 
                   ["ical", "ic"], 
                   ["full", ""], 
                   ["ness", ""]]
    if wordToM(word)>0:
        for i in suffix_list:
            if endsWith(word, i[0]):
                word = replace_end(word, i[0], i[1])
                break
    return word
    
def step4(word):
    suffix_list = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment", "ent", "ion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"]

    if wordToM(word)>1:
        for i in suffix_list:
            if i == "ion":
                if endsWith(word, "sion"):
                    word = replace_end(word, i, "")

                if endsWith(word, "tion"):
                    word = replace_end(word, i, "")
                
            if endsWith(word, i):
                word = replace_end(word, i, "")
                break
    return word



def step5a(word):
    if wordToM(word) > 1:
        word = changeWord(word, "e", "")
    elif wordToM(word) == 1 and not endsWith(word, "o"):
        word = changeWord(word, "e", "")
        
    return word


def step5b(word):
    if wordToM(word)>1 and doubleConsonant(word) and endsWith(word,"l"):
        word = changeWord(word, "ll", "l")
        
    return word
        
def stem(word):
    word = word.lower()
    
    rnd = random.randint(0,10)
    if(rnd == 5):
        print(word, " - ", end="")
    
    punctuation_chars = set(string.punctuation)
    
    word = word.rstrip(''.join(punctuation_chars))

    word = step1a(word)
    # print(word, "1a")
    word = step1b(word)
    # print(word, "1b")
    word = step1c(word)
    # print(word, "1c")
    word = step2(word)
    # print(word, "2")
    word = step3(word)
    # print(word, "3")
    word = step4(word)
    # print(word, "4")
    word = step5a(word)
    # print(word, "5a")
    word = step5b(word)
    # print(word, "5b")
    
    if(rnd == 5):
        print(word)

    return word


def stemPhrase(phrase):
    
    if not isinstance(phrase, str):
        phrase = str(phrase)

    words = phrase.split()

    stemmed_tokens = []

    for word in words:

        word_without_punctuation = ''.join([char for char in word if char not in string.punctuation])

        stemmed_word = stem(word_without_punctuation)
        stemmed_word_with_punctuation = ''.join([char if char in string.punctuation else '' for char in word]) + stemmed_word

        stemmed_tokens.append(stemmed_word_with_punctuation)
    stemmed_phrase = ' '.join(stemmed_tokens)

    return stemmed_phrase


