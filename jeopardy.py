#!/usr/bin/env python3
import argparse
import pandas as pd
from sys import exit, stdin
from display import *
from import_export import *
from processing import *
from analysis import *
from search import *
import play
import shlex

pd.set_option('display.max_colwidth', None)


# =============================================================================
# Internal functions
# =============================================================================

def apply_inputs(data, frame, function, self=None):
    if not callable(function):
        function_name = function
        function = globals()[function_name]

    def convert_value(value, self):
        bool_values = {"True": True, "False": False}
        if value in bool_values:
            return bool_values[value]
        elif value.find("-") == 0 and all(map(str.isdigit, value[1:])):
            return int(value, 10)
        elif all(map(str.isdigit, value)):
            return int(value, 10)
                                    # str.maketrans(".-e", "012")
        elif all(map(str.isdigit, value.translate({46: 48, 45: 49, 101: 50}))):
            return float(value)
        return value

    def resolve_function(name, self):
        if self is not None:
            if isinstance(self, dict):
                f = self.get(name)
            else:
                f = vars(self).get(name)
            if f is not None: return f
        return vars().get(name, globals().get(name, None))

    resolver_callbacks = {
        "filter_function": resolve_function,
    }
    results = []
    for datum in data:
        my_opts = datum.options.copy()
        for key, val in my_opts.items():
            resolve = resolver_callbacks.get(key, convert_value)
            my_opts[key] = resolve(val, self)
        results.append(function(frame, *datum.words, **my_opts))
    return results

# Testing
# print(remove_text_garbage("Kevin's behaviour (bare-bones in the catacombs) would've been too overwhelming (why?) had he not..."))

# 3.1/3.2: See search.py
# 5.2 and 6: See analysis.py

def run_analysis():
    # 3.3
    # resser means "Result series"
    resser = df_word_search(jeopardy, "King", "England", exact=False, case_sensitive=True)
    print(jeopardy[resser].question.count())
    # Part of 5.2
    apply_inputs(input_data, jeopardy, average_value_for)
    # Part of 6
    apply_inputs(input_data, jeopardy, unique_answers)
    # After 7.1
    resser = df_word_search(jeopardy, "Computer")
    results = (*jeopardy[resser].groupby("air_year").count()["question"].items(),)
    print(results)

def play_jeopardy():
    return play.play(jeopardy)

def interactive_word_search():
    choice = shlex.split(input("Search for: "))
    print("Available columns:", *jeopardy.columns, sep=", ")
    col_choice = input("In column (default=question):") or "question"
    resser = df_word_search(jeopardy, *choice, col=col_choice)
    data = jeopardy[resser]

    output_cols = ["question", "answer"]
    # Prompt for sorting
    print("Sort by one or more columns? Available columns:")
    print(*data.columns, sep=", ")
    print(
        "NOTE:\n- shlex module is used to separate column names"
        "\n- Enter \"asc\" as a column name to sort in ascending order")
    sort_by = shlex.split(input("Sort by: "))
    if sort_by:
        ascending = False
        if "asc" in sort_by:
            ascending = True
        sort_by = list(filter(lambda el: el in data.columns, sort_by))
        if len(sort_by) != 0:
            # sort_key = None
            # if len(sort_by) == 1 and (data[sort_by[0]].dtype == "int64" or
            #         data[sort_by[0]].dtype == "float64"):
            #     sort_key = lt
            data = data.sort_values(by=sort_by, axis=0, ascending=ascending)
            output_cols.extend(sort_by)

    # Format for printing out
    formatted_data = [output_cols]
    for row in data.iterrows():
        formatted_data.append([])
        for col in output_cols:
            formatted_data[-1].append(row[1][col])

    # Display the data
    view_parms = get_view_parms(80, len(output_cols))
    print_data_table(view_parms, formatted_data)
    # Display the value counts
    for sort_col in sort_by:
        print("{}:".format(sort_col))
        print(data[sort_col].value_counts().sort_index(
            ascending=ascending
        ))

def interactive_average():
    choice = shlex.split(input("Search for: "))
    resser = average_value_for(jeopardy, *choice)

def interactive_unique_answers():
    choice = shlex.split(input("Search for: "))
    resser = unique_answers(jeopardy, *choice)

def interactive_export_inputs():
    choice = input("Filename: ")
    if choice == "":
        choice = None
    export_inputs_copypasta(input_data, choice)

def interactive_export_csv():
    choice = input("Filename: ")
    if choice == "":
        choice = None
    export_inputs_csv(input_data, choice)

if __name__ == "__main__":
    print("Loading. Please wait...")
    input_data = get_inputs()
    # 2
    try:
        jeopardy = pd.read_csv("jeopardy.csv", memory_map=True)
    except Exception:
        print("jeopardy.csv not found! Get it from Codecademy (Data Analyst "
              "course)")
        exit(1)
    preprocess(jeopardy)
    if stdin.isatty():
        main_menu = True
        while main_menu != False:
            funcs = {
                "1": interactive_word_search,
                "2": interactive_average,
                "3": interactive_unique_answers,
                "4": run_analysis,
                "5": interactive_export_inputs,
                "6": interactive_export_csv,
                "7": play_jeopardy,
            }
            print(
                "========== Welcome to ==========\n"
                " (This is)    J E O P A R D Y !\n"
                "(Talon1024's project for the Codecademy Data Analyst "
                "course)\n"
                "1. Word search\n"
                "2. Calculate average value for questions containing the "
                "given words\n"
                "3. Get number of unique answers for questions containing "
                "the given words\n"
                "4. Run the built-in scripts\n"
                "5. Export input data to Python list\n"
                "6. Export input data to CSV\n"
                "7. PLAY\n"
                "Anything else will quit.\n")
            choice = input(">>> ")
            to_run = funcs.get(choice)
            if to_run: to_run()
            else: main_menu = False
    else:
        run_analysis()
