import json
import re
import ollama


def normalize_skills(skills):

    flat_skills = []

    for item in skills:

        if isinstance(item, str):
            flat_skills.append(item)

        elif isinstance(item, dict):

            for value in item.values():

                if isinstance(value, list):
                    flat_skills.extend(value)

                else:
                    flat_skills.append(str(value))

    return list(set(flat_skills))


def extract_resume_details(resume_text):

    prompt = f"""
You are an expert ATS resume parser.

Extract information from the resume.

Return ONLY valid JSON.

Rules:
- Extract the candidate name.
- Extract ALL technical skills.
- Include Programming Languages.
- Include Frameworks.
- Include Libraries.
- Include Tools.
- Include Databases.
- Include AI/ML skills.
- Include Generative AI skills.
- Include Cloud skills if available.
- Extract project names.
- Extract education details.
- Extract work experience.

Do NOT:
- Explain anything.
- Add markdown.
- Add headings.
- Add notes.
- Add any text outside JSON.

Required JSON Keys:

name
skills
projects
education
experience

Important:
- skills must be a flat list of strings.
- Do NOT group skills.
- Do NOT create dictionaries.
- Do NOT create categories.
- Return only skill names.

Resume:

{resume_text}
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

    print("\n====== RAW MODEL OUTPUT ======")
    print(result)
    print("==============================\n")

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

        print("\n====== CLEANED JSON ======")
        print(cleaned_text)
        print("==========================\n")

        data = json.loads(cleaned_text)

        if "skills" in data:
            data["skills"] = normalize_skills(
                data["skills"]
            )

        print("\n====== PARSED DATA ======")
        print(data)
        print("=========================\n")

        return data

    except Exception as e:

        print("\n========== JSON ERROR ==========")
        print(str(e))

        print("\nReturned Text:\n")
        print(cleaned_text)

        print("\n===============================\n")

        return {
            "name": "",
            "skills": [],
            "projects": [],
            "education": [],
            "experience": []
        }