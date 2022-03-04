from search import *
from display import *

# Play a round of Jeopardy!
def play(jeopardy_data):
    # Makes it easier to change the variables later
    categories_to_show = 7
    min_questions = 5

    # Ensure each category has 5 or more questions, and pick 7 random
    # categories out of those available.
    categories = jeopardy_data.category
    categories = categories.value_counts().apply( \
        lambda c: c >= min_questions)
    categories = categories[categories == True]
    categories = categories.sample(categories_to_show)
    categories = categories.index

    # Get 5 questions for the available categories
    questions = jeopardy_data[jeopardy_data.category.apply( \
        lambda c: c in categories)]
    category_question_count = {}
    def incr(key):
        category_question_count.setdefault(key, 0)
        category_question_count[key] += 1
        return category_question_count[key] <= 5

    questions = questions[questions.category.apply(incr)].reset_index(
        drop=True)
    del category_question_count

    # This is easier to manage, and allows game screen to be data driven
    questions = {c: [
        {"value": q.value_float, "question": q.question, "answer": q.answer, \
        "answered": None} for q in \
        questions[questions.category == c].itertuples()] for c in categories}
    # Add question money values if there are none
    for category in questions.values():
        for row, question in enumerate(category):
            if question["value"] is None:
                question["value"] = row * 400

    # Get parameters related to the interface/view of the categories and questions
    # Terminals are typically 80 characters wide
    view_width = 80
    view_parms = get_view_parms(view_width, categories_to_show)

    # Print out the categories and money values for each question in the category
    def print_game_screen(view_parms):
        game_screen = [categories]
        # Print out the money values for each selected question
        for row in range(min_questions):
            game_screen.append([])
            for col in categories:
                answered = questions[col][row]["answered"]
                if answered is None:
                    money_number = questions[col][row]["value"]
                    money_value = "${}".format(money_number)
                else:
                    money_value = "✓" * 4 if answered else "x" * 4
                game_screen[-1].append(money_value)
        print_data_table(view_parms, game_screen)

    # Prompt for category and money value
    wallet = 0
    answers_given = 0
    max_answers = categories_to_show * min_questions
    def play_one_question():
        nonlocal wallet
        nonlocal questions
        nonlocal answers_given
        if answers_given > max_answers:
            return False

        print_game_screen(view_parms)
        print("Your wallet: ${}".format(wallet))

        # Prompt for category
        print("Select category (1-{}, "
            "from left to right, or Q to quit)" \
            .format(categories_to_show),
            sep="", end="\n>>> ")
        category_index_choice = None
        while type(category_index_choice) != int:
            category_index_choice = input()
            if category_index_choice.lower() == "q":
                return False
            try:
                category_index_choice = int(category_index_choice)
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue
            if (category_index_choice > categories_to_show or
                    category_index_choice < 1):
                print("Invalid choice.")
                category_index_choice = None
        category_index_choice -= 1  # 0-based indices

        # Prompt for question
        print("Select question (1-{}, "
            "from top to bottom, or Q to quit)" \
            .format(min_questions),
            sep="", end="\n>>> ")
        question_index_choice = None
        while type(question_index_choice) != int:
            question_index_choice = input()
            if question_index_choice.lower() == "q":
                return False
            try:
                question_index_choice = int(question_index_choice)
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue
            if (question_index_choice > min_questions or
                    question_index_choice < 1):
                print("Invalid choice.")
                question_index_choice = None
        question_index_choice -= 1  # 0-based indices

        selected_category = categories[category_index_choice]
        selected_question = \
            questions[selected_category][question_index_choice]

        if questions[selected_category][question_index_choice]["answered"] is None:
            print("{} for {}: {}" \
            .format(selected_category, selected_question["value"], \
                selected_question["question"]), end="\n>>> Who/What/Where/When is ")
        else:
            print("Question has already been answered.")
            return True

        your_answer = input()
        if your_answer == selected_question["answer"]:
            print("Correct!")
            wallet += selected_question["value"]
            answers_given += 1
            questions[selected_category][question_index_choice]["answered"] = True
        elif your_answer.lower() == "q":
            return False
        else:
            print("Incorrect. The answer is {}".format(selected_question["answer"]))
            questions[selected_category][question_index_choice]["answered"] = False
            answers_given += 1

        return True

    while play_one_question():
        pass
    print("You walk away with ${}".format(wallet))

