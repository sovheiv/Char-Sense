import os
from matplotlib import pyplot as plt


def open_file():
    input_text_file = ""
    try:
        input_text_file = os.listdir("input_text")[0]
    except IndexError:
        print("Put some files in input_text folder")
    except FileNotFoundError:
        print("There is not input_text folder. Create it")
    except:
        print("Incorrect input data")

    if input_text_file:
        splited_input_text_file = input_text_file.split(".")
        if splited_input_text_file[len(splited_input_text_file)-1] == "txt":
            try:
                input_text = open("input_text" + "/" + input_text_file, "rb").read()
                return input_text
            except FileNotFoundError:
                print("FileNotFoundError")
            except:
                print("Incorrect input file")
        else:
            print("Incorrect input file format. It must be in .txt format")



def gen_statistic(input_text):
    statistic = {}
    for i in input_text:
        if i in statistic.keys():
            statistic[i] += 1
        else:
            statistic[i] = 0

    statistic_sorted = dict(sorted(statistic.items(), key=lambda item: item[1]))

    for i in statistic_sorted.keys():
        statistic_sorted[i] = round(statistic_sorted[i] / len(input_text) * 100, 2)

    return statistic_sorted


def gen_str(dict_input):
    statistic_str = ""

    for item in dict_input.items():
        statistic_str += chr(item[0]) + ": " + str(item[1]) + "\n"

    return statistic_str

# def matplotlib_visualisation():
#     str_data = [chr(item[0]) for item in result.items()]
#     int_data = [int(item[1]) for item in result.items()]

#     fig = plt.figure(figsize=(21, 9))
#     ax = fig.add_subplot()

#     ax.bar(str_data, int_data)
#     ax.grid()
#     plt.show()

def main():
    input_text = open_file()
    if input_text:
        result = gen_statistic(input_text)
        print(gen_str(result))
        print(len(input_text))

main()