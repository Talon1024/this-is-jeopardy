from search import *
# Data analysis functions

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
