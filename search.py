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
