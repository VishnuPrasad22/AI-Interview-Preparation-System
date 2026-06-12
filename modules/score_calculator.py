import re


def calculate_interview_score(answer_evaluations):

    total_score = 0
    total_questions = len(answer_evaluations)

    answered_questions = 0
    skipped_questions = 0

    for item in answer_evaluations:

        evaluation = item["evaluation"]

        match = re.search(
            r"Score:\s*(\d+)/10",
            evaluation
        )

        if match:

            score = int(match.group(1))

            total_score += score

            if score == 0:
                skipped_questions += 1
            else:
                answered_questions += 1

    max_score = total_questions * 10

    percentage = 0

    if max_score > 0:
        percentage = round(
            (total_score / max_score) * 100,
            2
        )

    return {
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "answered_questions": answered_questions,
        "skipped_questions": skipped_questions
    }