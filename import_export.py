import csv  # Input data is in a separate CSV file
from collections import namedtuple
import shlex

InputDatum = namedtuple("InputDatum", "words options")

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
