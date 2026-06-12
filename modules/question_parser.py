import re

def extract_questions(question_text):

    questions = []

    for line in question_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Match numbered questions
        if line[0].isdigit():
            questions.append(line)

    return questions