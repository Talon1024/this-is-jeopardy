from search import *

# Play a round of Jeopardy!
def play(df):
    # Ensure each category has 5 or more questions, and pick 7 random
    # categories out of those available.
    categories = jeopardy_data.category
    categories = categories.value_counts().apply( \
        lambda c: True if c >= 5 else False)
    categories = categories.sample(7)
    categories

    # Get 5 questions for the available categories
    questions = jeopardy_data[jeopardy_data.category.apply( \
    lambda c: categories[c] if c in categories else False)]
    category_question_count = {}
    def incr(key):
        category_question_count.setdefault(key, 0)
        category_question_count[key] += 1
        return category_question_count[key] <= 5
    questions = questions[questions.category.apply(incr)].reset_index(drop=True)

    # Print out the categories and money values for each question in the category
    # Terminals are typically 80 characters wide
    view_width = 80
    cell_width, expanded_cells = divmod(view_width, categories_to_show)
    cell_width -= 1  # Add space for a pipe character

    longest_category = max(categories.keys(), key=len)
    lines, extra_line = divmod(len(longest_category), cell_width)
    if extra_line > 0:
        lines += 1

    for line in range(lines):
        extender = expanded_cells
        for col in categories.keys():
            start = line * cell_width
            end = start + cell_width
            print("{:^10}|".format(col[start:end]), sep="", end="")
            if extender > 0:
                print(" ", end="")
                extender -= 1
        print()
    print("-" * view_width)

