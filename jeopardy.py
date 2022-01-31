#!/usr/bin/env python3
import argparse
import pandas as pd
# from sys import exit
from sys import stdin
from import_export import get_inputs
from processing import *
from analysis import *

pd.set_option('display.max_colwidth', -1)


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

if __name__ == "__main__":
    print("Loading. Please wait...")
    input_data = get_inputs()
    # 2
    jeopardy = pd.read_csv("jeopardy.csv")
    jeopardy.rename(columns={
    "Show Number": "show_number",
    " Air Date": "air_date",
    " Round": "round",
    " Category": "category",
    " Value": "value",
    " Question": "question",
    " Answer": "answer"
    }, inplace=True)
    jeopardy["value_float"] = jeopardy.value.apply(money_to_float)
    jeopardy.air_date = jeopardy.air_date.apply(to_date)
    jeopardy["air_year"] = jeopardy.air_date.apply(lambda d: d.year)
    if stdin.isatty():
        funcs = {"4": run_analysis}
        print(
            "= Welcome to =\n"
            "J E O P A R D Y\n"
            "(Talon1024's Data Analyst project)\n"
            "1. Word search\n"
            "2. Calculate average value for questions containing the given words\n"
            "3. Get number of unique answers for questions containing the given words\n"
            "4. Run the built-in scripts and quit\n"
            "5. Export input data to Python list\n"
            "6. PLAY\n"
            "7. Quit\n")
        choice = input(">>> ")
        to_run = funcs.get(choice)
        if to_run: to_run()
    else:
        run_analysis()
