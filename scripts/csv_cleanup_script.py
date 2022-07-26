import re

fileOne = "resources/output/raw/lmohada.txt"
fileTwo = "resources/output/raw/yawylno.txt"


def remove_mentions(string):
    string = re.sub('(?:)@[^, ]*', '', string)
    string = string.replace('"', '')

    if string.startswith(' '):
        return remove_mentions(string[1:])

    return string


def remove_urls(string):
    string = re.sub('(?:)https[^, ]*', '', string)

    return string


def isRetweet(string):
    return string.startswith("RT")


def remove_starting_punctuations(s):

    valid_chars = [':(', ':)', ':v', ':s']
    invalid_chars = [':', ',', '.']

    if s[:2] in valid_chars:
        return s

    if s[:1] in invalid_chars:
        return s[1:]

    return s


def clean_tweets(file):
    lines = []

    with open(file, encoding="utf8") as file_in:
        for text_line in file_in:
            string_list = re.split('(\d+)', text_line)

            if len(string_list) > 1:
                sentence = ""
                for s in string_list[2:]:
                    sentence += s

                temp = remove_mentions(sentence)
                cleaned_string = remove_urls(temp)
                if not isRetweet(cleaned_string) and len(cleaned_string) > 1:
                    lines.append(remove_starting_punctuations(cleaned_string))

            elif len(string_list) == 1:
                lines[len(lines) - 1] += remove_mentions(string_list[0])

    return lines


firstList = clean_tweets(fileOne)
secondList = clean_tweets(fileTwo)

joined_list = firstList + secondList

with open('../resources/output/dirty_dataset.txt', 'w', encoding="utf-8") as f:
    for line in joined_list:
        if not line.isspace():
            f.write(line)

