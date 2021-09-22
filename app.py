import os

from matplotlib import pyplot as plt
from datetime import datetime
from config import *


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        if print_time_for_main_only and time_decorator_work:
            if func.__name__ == "main":
                print(
                    str(datetime.now() - start_time).split(":")[2] + " " + func.__name__
                )
        elif time_decorator_work:
            print(str(datetime.now() - start_time).split(":")[2] + " " + func.__name__)

        return result

    return wrapper


@time_decorator
def open_file():
    input_text_file = ""
    try:
        input_text_file = os.listdir(input_text_path)[0]
    except IndexError:
        print(f"Put some files in {input_text_path} folder")
    except FileNotFoundError:
        print(f"There is not {input_text_path} folder. Create it")
    except:
        print("Incorrect input data")

    if input_text_file:
        splited_input_text_file = input_text_file.split(".")
        if splited_input_text_file[len(splited_input_text_file) - 1] == "txt":
            try:
                input_text = open(input_text_path + "/" + input_text_file, "rb").read()
                # input_text = [i for i in input_text_bit]

                print(f"{input_text_path}/{input_text_file} opened successfuly")
                return input_text
            except FileNotFoundError:
                print("FileNotFoundError")
            except:
                print("Incorrect input file")
        else:
            print("Incorrect input file format. It must be in .txt format")


@time_decorator
def gen_statistic(input_text):
    print(len(input_text))
    statistic = {}
    for i in input_text:
        if i in statistic.keys():
            statistic[i] += 1
        else:
            statistic[i] = 1
    # print(statistic)
    statistic_sorted = dict(sorted(statistic.items(), key=lambda item: item[1]))
    # print(statistic_sorted["g"])
    for item in statistic_sorted.items():

        if round(item[1] / len(input_text) * 100, 2) > 0.001:
            statistic_sorted[item[0]] = round(item[1] / len(input_text) * 100, 5)

    return statistic_sorted


@time_decorator
def gen_str(dict_input):
    statistic_str = ""

    for item in dict_input.items():
        if item[0] == 13:
            title = "enter"
        elif item[0] == 9:
            title = "tab"
        elif (
            item[0] == 10
            or item[0] == 128
            or item[0] == 147
            or item[0] == 90
            or item[0] == 194
        ):
            continue
        else:
            title = chr(item[0])

        statistic_str += title + ": " + str(item[1]) + "\n"

    statistic_str += str(len(dict_input))
    return statistic_str


def matplotlib_visualisation(result):
    str_data = [chr(item[0]) for item in result.items()]
    int_data = [int(item[1]) for item in result.items()]

    fig = plt.figure(figsize=(21, 9))
    ax = fig.add_subplot()

    ax.bar(str_data, int_data)
    ax.grid()
    plt.show()


@time_decorator
def main():
    input_text = open_file()
    if input_text:
        result = gen_statistic(input_text)
        if print_statistic_to_console:
            print(gen_str(result))
        if show_matplotlib_visualisation:
            matplotlib_visualisation(result)


main()
