import os
import numpy as np

from typing import Counter
from matplotlib import pyplot as plt
from datetime import datetime

from config import *
from initialize_logger import output_logger


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        if print_time_for_main_only and time_decorator_work:
            if func.__name__ == "main":
                output_logger.info(
                    str(datetime.now() - start_time).split(":")[2] + " " + func.__name__
                )
        elif time_decorator_work:
            output_logger.info(
                str(datetime.now() - start_time).split(":")[2] + " " + func.__name__
            )

        return result

    return wrapper


@time_decorator
def open_file():
    input_data = []
    try:
        input_data.append(os.listdir(input_text_path)[0])
        input_text_file = input_data[0]
    except IndexError:
        output_logger.error(f"Put some files in {input_text_path} folder")
    except FileNotFoundError:
        output_logger.error(f"There is not {input_text_path} folder. Create it")
    except:
        output_logger.error("Incorrect input data")

    if input_data:
        splited_input_text_file = input_text_file.split(".")
        if splited_input_text_file[len(splited_input_text_file) - 1] == "txt":
            try:
                input_data.append(
                    open(input_text_path + "/" + input_text_file, "rb").read()
                )
                input_text = input_data[1]
                if len(input_text) > 2:
                    output_logger.info(
                        f"{input_text_path}/{input_text_file} opened successfuly"
                    )
                    return input_data
                else:
                    output_logger.error(
                        "the entered text must be at least 3 characters"
                    )

            except FileNotFoundError:
                output_logger.error("FileNotFoundError")
            except:
                output_logger.error("Incorrect input file")
        else:
            output_logger.error(
                "Incorrect input file format. It must be in .txt format"
            )


@time_decorator
def gen_statistic(input_text):
    statistic = Counter(input_text)
    statistic_sorted = dict(
        sorted(statistic.items(), key=lambda item: item[1], reverse=True)
    )
    statistic_sorted_corrected = {}
    for item in statistic_sorted.items():

        if item[0] == 13:
            title = "enter"
        elif item[0] == 9:
            title = "tab"
        elif item[0] == 32:
            title = "space"
        elif item[0] in black_list_of_characters:
            continue
        else:
            title = chr(item[0])

        if round(item[1] / len(input_text) * 100, 2) > 0.001:
            statistic_sorted_corrected[title] = round(
                item[1] / len(input_text) * 100, 3
            )

    return statistic_sorted_corrected


@time_decorator
def gen_str(dict_input, input_text_len):
    statistic_str = "statistic\n"
    i = 0
    for item in dict_input.items():
        i += 1
        statistic_str += f"{i}) {item[0]}: {item[1]} \n"

    statistic_str += "number of input chars: " + str(input_text_len) + "\n"
    statistic_str += "number of different chars: " + str(len(dict_input)) + "\n"

    return statistic_str


def matplotlib_visualisation(
    result, file_name, num_of_horizontal_divisions, num_of_vertical_divisions
):
    plt.switch_backend("TkAgg")
    plt.style.use("dark_background")
    figure = plt.figure(figsize=(16, 8), dpi=90)
    figure.canvas.manager.set_window_title("char_sense")
    ax = figure.subplots()
    ax.set_title(file_name)
    ax.set_xlabel("character")
    ax.set_ylabel("Percentage of use")

    if len(result) > num_of_horizontal_divisions:
        while len(result) > num_of_horizontal_divisions - 1:
            result.popitem()
        result["other"] = 100 - sum(result.values())

    y_max_val = max(result.values())
    ytick_len = y_max_val // num_of_vertical_divisions + 1
    ax.set_yticks(np.arange(0, y_max_val + 1, ytick_len))

    make_indent = False
    str_data = []
    for item in result.items():
        if len(item[0]) > 1:
            if make_indent == False:
                str_data.append(item[0])
                make_indent = True
            else:
                str_data.append("\n" + item[0])
                make_indent = False
        else:
            str_data.append(item[0])
            make_indent = False

    int_data = [int(item[1]) for item in result.items()]

    ax.bar(str_data, int_data, color="#5e1f82")
    ax.grid(linestyle="dashed", linewidth=1)
    if save_statistic_visualisation:
        os.makedirs("statistic_visualisations", exist_ok=True)
        plt.savefig(f"statistic_visualisations/{file_name}_statistic_visualisation.jpg")
    if show_statistic_visualisation:
        plt.show()


@time_decorator
def main():
    input_data = open_file()
    if input_data:
        result = gen_statistic(input_data[1])
        if print_statistic_to_console:
            output_logger.info(
                gen_str(dict_input=result, input_text_len=len(input_data[1]))
            )
        if calculate_statistic_visualisation:
            matplotlib_visualisation(
                result,
                input_data[0],
                num_of_horizontal_divisions=44,
                num_of_vertical_divisions=40,
            )


main()
