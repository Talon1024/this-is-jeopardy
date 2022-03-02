import csv  # Input data is in a separate CSV file
from collections import namedtuple
import shlex
from io import StringIO

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
def export_inputs_copypasta(input_data, fname=None):
    copypasta = "[" + ",\n".join([repr(d) for d in input_data]) + "]"
    if isinstance(fname, str):
        with open(fname, "w") as input_pasta_file:
            print(copypasta, file=input_pasta_file)
    else:
        print(copypasta)


# Ditto, but as a CSV file
def export_inputs_csv(input_data, fname=None):
    copypasta = StringIO()
    fieldnames = ["words"]
    for row in input_data:
        for key in row.options:
            if key not in fieldnames:
                fieldnames.append(key)

    writer = csv.DictWriter(copypasta, fieldnames)
    writer.writeheader()

    for row in input_data:
        row_dict = {"words": shlex.join(row.words)}
        for fieldname in fieldnames:
            if fieldname == "words":
                continue
            row_dict[fieldname] = row.options.get(fieldname, None)
        writer.writerow(row_dict)
    copypasta = copypasta.getvalue()

    if isinstance(fname, str):
        with open(fname, "w") as input_csv_file:
            print(copypasta, file=input_csv_file)
    else:
        print(copypasta)
