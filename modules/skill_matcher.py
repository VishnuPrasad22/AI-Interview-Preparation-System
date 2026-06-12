import re
 
 
def flatten_skills(skills):
 
    result = []
 
    for item in skills:
 
        if isinstance(item, str):
            result.append(item)
 
        elif isinstance(item, dict):
 
            for value in item.values():
 
                if isinstance(value, list):
                    result.extend(value)
 
                else:
                    result.append(str(value))
 
    return result
 
 
# Common aliases/synonyms so different naming conventions still match.
# Key = canonical form, Value = list of alternate forms.
SKILL_ALIASES = {
    "machine learning": ["ml", "fundamentals of machine learning"],
    "scikit-learn": ["sklearn", "scikit learn"],
    "tensorflow": ["tf"],
    "natural language processing": ["nlp"],
    "deep learning": ["dl"],
    "artificial intelligence": ["ai"],
    "convolutional neural network": ["cnn", "convolutional neural networks"],
    "recurrent neural network": ["rnn", "recurrent neural networks"],
    "artificial neural network": ["ann", "artificial neural networks"],
    "computer vision": ["cv", "opencv"],
    "structured query language": ["sql"],
    "python": ["python3", "python 3"],
    "probability and statistics": ["statistics", "probability"],
    "linear algebra": ["linear-algebra"],
}
 
 
def normalize(text):
    text = text.strip().lower()
    # remove punctuation like parentheses, hyphens normalized to space
    text = re.sub(r"[()/]", " ", text)
    text = re.sub(r"[-_]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
 
 
def expand_with_aliases(skill_set):
    """For each skill, add any known aliases/canonical forms to the set."""
    expanded = set(skill_set)
 
    for canonical, aliases in SKILL_ALIASES.items():
        canonical_norm = normalize(canonical)
        alias_norms = [normalize(a) for a in aliases]
 
        all_forms = [canonical_norm] + alias_norms
 
        # If any form is present in the set, add all forms
        if any(form in expanded for form in all_forms):
            expanded.update(all_forms)
 
    return expanded
 
 
def skills_match(skill_a, skill_b):
    """True if two normalized skill strings should be considered the same skill."""
 
    if skill_a == skill_b:
        return True
 
    # Substring match (covers "python" in "python programming", etc.)
    if skill_a in skill_b or skill_b in skill_a:
        return True
 
    return False
 
 
def match_skills(resume_data, jd_data):
 
    resume_skills_raw = {
        normalize(skill)
        for skill in flatten_skills(resume_data.get("skills", []))
        if str(skill).strip()
    }
 
    jd_skills_raw = {
        normalize(str(skill))
        for skill in jd_data.get("required_skills", [])
        if str(skill).strip()
    }
 
    resume_skills = expand_with_aliases(resume_skills_raw)
 
    matched_skills = []
    missing_skills = []
 
    for jd_skill in sorted(jd_skills_raw):
 
        jd_forms = expand_with_aliases({jd_skill})
 
        found = False
        for jd_form in jd_forms:
            for resume_skill in resume_skills:
                if skills_match(jd_form, resume_skill):
                    found = True
                    break
            if found:
                break
 
        if found:
            matched_skills.append(jd_skill)
        else:
            missing_skills.append(jd_skill)
 
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }