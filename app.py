from matplotlib import pyplot as plt

text_input = open("text_input.txt", "rb").read()
text_char_array = list(text_input)


def gen_statistic(array):
    statistic = {}
    for i in array:
        if i in statistic.keys():
            statistic[i] += 1
        else:
            statistic[i] = 0

    statistic_sorted = dict(sorted(statistic.items(), key=lambda item: item[1]))

    for i in statistic_sorted.keys():
        statistic_sorted[i] = round(statistic_sorted[i] / len(text_char_array) * 100, 2)

    return statistic_sorted


def gen_str(dict_input):
    statistic_str = ""

    for item in dict_input.items():
        statistic_str += chr(item[0]) + ": " + str(item[1]) + "\n"

    return statistic_str


result = gen_statistic(text_char_array)
print(gen_str(result))
print(len(text_char_array))

str_data = [chr(item[0]) for item in result.items()]
int_data = [int(item[1]) for item in result.items()]

fig = plt.figure(figsize=(21, 9))
ax = fig.add_subplot()

ax.bar(str_data, int_data)
ax.grid()
plt.show()
