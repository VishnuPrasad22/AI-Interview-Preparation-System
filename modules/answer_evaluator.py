import ollama


def evaluate_answer(question, answer):

    if not answer.strip():

        return """
Score: 0/10

Strengths:
- No answer provided

Weaknesses:
- Question was skipped

Recommendation:
- Attempt every question even if unsure.
"""

    prompt = f"""
    You are an expert technical interviewer.

    Question:
    {question}

    Candidate Answer:
    {answer}

    IMPORTANT RULES:

    - If answer is empty, Score = 0/10
    - Score only the candidate answer
    - Do not assume knowledge not written in the answer
    - Be strict

    Return:

    Score: X/10

    Strengths:
    - ...

    Weaknesses:
    - ...

    Recommendation:
    - ...
    """

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]