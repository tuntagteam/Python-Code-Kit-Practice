sentence = input("Enter a sentence")
cleansentence = sentence.replace("," , "").replace(".","")
longestWord = ""
word = cleansentence.split()
for word in cleansentence:
    if len(word) > len(longestWord):
        longestWord = word
print(longestWord)


sentence = set(input("Enter a sentence: ").lower().replace(" ", ""))
sentence.remove(",")
sentence.remove(".")
print(len(sentence))

sentence = input("Enter a sentence: ").lower().replace(" ", "")
vowels = ["a", "e", "i", "o", "u"]
existing = []
for letter in sentence:
    if letter in vowels:
        existing.append(letter)
print(len(existing))

sentence = set(input("Enter a sentence: ").replace(" ", ""))
existing = []
for letter in sentence:
    if letter.isupper():
        existing.append(letter)
print(len(existing))

sentence = input("Enter a sentence: ").lower().replace(" ", "")
print(max(sentence.count(char) for char in sentence))

sentence = input("Enter a sentence: ").split()
for word in sentence:
    sWord = list(word)
    sWord.remove(',') if ("," in sWord) else print("L")
    sWord.remove('.') if ("." in sWord) else print("L")
    word = str(sWord)
longestWord = ""
for word in sentence:
    if len(word) > len(longestWord):
        longestWord = word
print(longestWord)