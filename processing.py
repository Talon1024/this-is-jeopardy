import datetime
import re

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

# 7.1
def to_date(date):
    date_things = date.split("-")
    #if len(date_things) < 3:
        #print("Date:", date)
    #date_things += ["1"] * (3 - len(date_things))
    return datetime.date(*map(int, date_things))

# Helper - set up Jeopardy DataFrame for analysis
def preprocess(jeopardy):
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
