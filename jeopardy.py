#!/usr/bin/env python3
import argparse
from collections import namedtuple
import csv  # Input data is in a separate CSV file
import datetime
import pandas as pd
import re
import shlex
# from sys import exit
from sys import stdin

InputDatum = namedtuple("InputDatum", "words options")
pd.set_option('display.max_colwidth', -1)


# =============================================================================
# Internal functions
# =============================================================================

# This function gets input data from an external CSV file, which is easier to
# maintain than dozens of calls to average_value_for, unique_answers, etc.
def get_inputs(fname="inputs.csv"):
    inputs = []
    with open(fname) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            options = row.copy()
            fields = row.keys()
            for field in fields:
                if options[field] == "":
                    del options[field]
            del options["words"]
            words = shlex.split(row["words"])
            inputs.append(InputDatum(words, options))
    return inputs


# Write input data to a file, so that it can be copied/pasted into Codecademy
# or when the input data CSV file otherwise isn't available.
def export_inputs_copypasta(input_data, fname="input_pasta.dat"):
    with open(fname, "w") as input_pasta_file:
        print("[", file=input_pasta_file)
        for datum in input_data:
            print(repr(datum), end=",\n", file=input_pasta_file)
        print("]", file=input_pasta_file)


# Ditto, but as a CSV file
def export_inputs_csv(input_data, fname="input_pasta.csv"):
    with open(fname, "w") as csvf:
        writer = csv.DictWriter(csvf)


def apply_inputs(data, frame, function, self=None):
    if not callable(function):
        function_name = function
        function = globals()[function_name]

    def convert_value(value, self):
        bool_values = {"True": True, "False": False}
        if value in bool_values:
            return bool_values[value]
        elif value.lower() != "infinity":
            return float(value)
        elif value.find("-") == 0:
            return int(value, 10)
        elif all(str.isdigit, value):
            return int(value, 10)
        return value

    def resolve_function(name, self):
        if self is not None:
            try:
                return vars(self)[name]
            except KeyError:
                pass
        try:
            return vars()[name]
        except KeyError:
            return globals()[name]

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

# 3.2
def s_word_search(s, words, exact=True, case_sensitive=False, filter_function=None):
    if not case_sensitive:
        words = list(map(str.lower, words))
    if filter_function is not None:
        words = (*map(filter_function, words),)
    # print("s_word_search words {!r}".format(words))
    def search_row(row):
        nonlocal words
        if not case_sensitive:
            row = row.lower()
        if filter_function is not None:
            row = filter_function(row)
        # print("s_word_search row {!r}".format(row))
        if exact:
            words = set(words)
            row_words = set(row.split())
            return words <= row_words
        row_contains = lambda word: word in row
        return all(map(row_contains, words))
    return s.apply(search_row)
# 3.1
def df_word_search(df, *words, col="question", exact=True, case_sensitive=False, filter_function=None):
    "Search the given column of a DataFrame for the given words, and return the series of matches"
    # print("df_word_search words", words)
    return s_word_search(df[col], words, exact, case_sensitive, filter_function)
# 3.3
# resser means "Result series"
# resser = df_word_search(jeopardy, "King", "England", exact=False, case_sensitive=True)
# print(jeopardy[resser].question.count())

# 3.3
def remove_text_garbage(
        text, remove_apos=True, remove_parens=True, remove_punct=True):
    if remove_parens:
        text = re.sub(r"\(([^)]*)\)", r"\1", text)
    if remove_apos:
        text = re.sub(r"([^\s']+)'[\S]+", r"\1", text)
    if remove_punct:
        text = text.replace(",", "")
        text = text.replace(".", "")
        text = text.replace("?", "")
    return text

# 4.1
# When I originally wrote my word search functions, I made them split the
# question sentence into each word, and then turned the set of words into a set.
# Then, I turned the list of words to search for into a set, and checked whether
# the words to search for were a subset of the words in the question sentence
# resser = df_word_search(jeopardy, "way", "hell", exact=False)
# print(jeopardy[resser].question.count())
# resser = df_word_search(jeopardy, "blue"] exact=False)
# print(jeopardy[resser].question.count())
# resser = df_word_search(jeopardy, "poo", "pool", exact=False)
# print(jeopardy[resser].question.count())
# resser = df_word_search(jeopardy, "they", "there", exact=False)
# print(jeopardy[resser].question.count())
# resser = df_word_search(jeopardy, "'s", exact=False)
# print(jeopardy[resser].question.count())
# resser = df_word_search(jeopardy, "'re", exact=False)
# print(jeopardy[resser].question.count())
# resser = df_word_search(jeopardy, "'ve", exact=False)
# print(jeopardy[resser].question.count())

# 5.1
def money_to_float(money):
    if money is None or money == "None":
        return 0.0
    if money.startswith("$"):
        money = money[1:]
    if money.find(",") >= 0:
        monies = money.split(",")
        money = "".join(monies)
    return float(money)

# 5.2
def average_value_for(df, *words, printout=True, **kwargs):
    resser = df_word_search(df, *words, **kwargs)
    result = df[resser].value_float.mean()
    result_count = df[resser].value_float.count()
    if printout:
        word_string = '"' + " ".join(words) + '"'
        print("Average value for", result_count, "questions containing",
              word_string, kwargs, ':', result)
    return result

# apply_inputs(input_data, jeopardy, average_value_for)

# 6
def unique_answers(df, *words, **search_args):
    resser = df_word_search(df, *words, **search_args)
    answer_count = len(df[resser].groupby("answer").groups)
    question_count = df[resser].question.count()
    get_words = lambda words: '"' + " ".join(words) + '":'
    print("Number of unique answers for", question_count,
          "questions matching", get_words(words), answer_count)
    return answer_count

# apply_inputs(input_data, jeopardy, unique_answers)

# 7.1
def to_date(date):
    date_things = date.split("-")
    #if len(date_things) < 3:
        #print("Date:", date)
    #date_things += ["1"] * (3 - len(date_things))
    return datetime.date(*map(int, date_things))

# resser = df_word_search(jeopardy, "Computer")
# results = (*jeopardy[resser].groupby("air_year").count()["question"].items(),)
# print(results)

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
