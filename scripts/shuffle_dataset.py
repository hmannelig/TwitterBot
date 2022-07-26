import random
data = []

with open("../resources/output/cleaned_dataset.txt", encoding="utf8") as file_in:
    data = file_in.read()

randomized = random.sample(data, len(data))

with open("../resources/shuffled/randomized_data.txt", "w", encoding="utf-8") as f:
    f.writelines(randomized)