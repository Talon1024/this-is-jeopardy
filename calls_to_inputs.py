# This is the script I used to convert all the individual function calls to
# a CSV file, so that the input data is more manageable
import ast
import csv

source_file = "codecademy_jeopardy_inputdata.txt"
outdata_file = "codecademy_jeopardy_inputdata.csv"
with open(source_file) as f:
    sources = f.read()
parsed = ast.parse(sources, filename=source_file)

with open(outdata_file, "w") as csvfile:
    fieldnames = ["words", "col", "exact", "case_sensitive", "filter_function"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    row = {}
    for fcall in parsed.body:
        words = []
        for word in fcall.value.args[0].elts:
            #print(repr(word.value), end=",")
            words.append(word.value)
        row["words"] = " ".join(words)
        for kword in fcall.value.keywords:
            key = kword.arg
            val = getattr(kword.value, "value", None)
            if val is None:
                val = getattr(kword.value, "id", None)
            row[key] = val
        writer.writerow(row)
        row.clear()
