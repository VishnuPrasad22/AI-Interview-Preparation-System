import json
import re
import ollama


def extract_jd_details(jd_text):

    prompt = f"""
You are an expert Job Description parser.

Analyze the job description and return ONLY valid JSON.

Rules:
- Extract the job role.
- Extract INDIVIDUAL technical skills only.
- Do NOT return complete sentences as skills.
- Split skills separately.

Example:

If JD contains:

"Knowledge of Python, Pandas, NumPy, TensorFlow and Keras"

Return:

[
    "Python",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "Keras"
]

Output format:

{{
    "job_role": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_required": ""
}}

Job Description:

{jd_text}
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

    result = response["message"]["content"]

    print("\n====== JD RAW OUTPUT ======")
    print(result)
    print("===========================\n")

    cleaned_text = (
        result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        json_match = re.search(
            r"\{.*\}",
            cleaned_text,
            re.DOTALL
        )

        if json_match:
            cleaned_text = json_match.group()

        data = json.loads(cleaned_text)

        print("\n====== JD PARSED DATA ======")
        print(data)
        print("============================\n")

        return data

    except Exception as e:

        print("\n====== JD JSON ERROR ======")
        print(e)
        print(cleaned_text)
        print("===========================\n")

        return {
            "job_role": "",
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "experience_required": ""
        }