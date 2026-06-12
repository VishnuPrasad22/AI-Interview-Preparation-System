import streamlit as st

from modules.resume_parser import extract_resume_text
from modules.llm_parser import extract_resume_details
from modules.jd_parser import extract_jd_details
from modules.skill_matcher import match_skills
from modules.ats_score import calculate_ats_score
from modules.question_generator import generate_questions
from modules.question_parser import extract_questions
from modules.mock_interview import get_current_question
from modules.interview_report import generate_interview_report
from modules.answer_evaluator import evaluate_answer
from modules.score_calculator import calculate_interview_score
from modules.study_plan_generator import generate_study_plan
from modules.resource_recommender import recommend_resources
from modules.rag_engine import ask_interview_coach
from modules.career_roadmap import generate_career_roadmap
from modules.resume_improver import (
    generate_resume_suggestions
)

st.set_page_config(
    page_title="AI Interview Coach",
    layout="wide"
)

st.title(" AI Interview Preparation Coach")

# -------------------------
# Resume Upload
# -------------------------

st.subheader("Upload Resume")

resume = st.file_uploader(
    "Choose Resume PDF",
    type=["pdf"]
)

# -------------------------
# JD Input
# -------------------------

st.subheader("Paste Job Description")

job_description = st.text_area(
    "Enter Job Description Here",
    height=200
)

# -------------------------
# Analyze Button
# -------------------------

if st.button("Analyze"):

    if resume is None:
        st.error("Please upload a resume")

    elif not job_description.strip():
        st.error("Please enter a job description")

    else:

        # Resume Parsing
        resume_text = extract_resume_text(resume)

        st.success("Resume Parsed Successfully")

        st.subheader("Resume Text")

        st.text_area(
            "Extracted Resume",
            resume_text,
            height=300
        )

        # Resume Analysis
        resume_data = extract_resume_details(
            resume_text
        )

        # JD Analysis
        jd_data = extract_jd_details(
            job_description
        )

        # Skill Matching
        skill_match_result = match_skills(
            resume_data,
            jd_data
        )

        # ATS Score
        ats_score = calculate_ats_score(
            skill_match_result,
            jd_data
        )

        # Store in Session State
        st.session_state.resume_data = resume_data
        st.session_state.jd_data = jd_data
        st.session_state.skill_match_result = skill_match_result
        st.session_state.ats_score = ats_score

# -------------------------
# Display Results
# -------------------------

if "resume_data" in st.session_state:
    
    st.subheader("📄 Resume Summary")

    st.write(
        f"**Name:** {st.session_state.resume_data.get('name', 'Not Found')}"
    )

    skills = st.session_state.resume_data.get(
        "skills",
        []
    )


    skill_names = []

    for skill in skills:

        if isinstance(skill, str):
            skill_names.append(skill)

        elif isinstance(skill, dict):
            skill_names.append(str(skill))

    st.write(
        f"**Skills:** {', '.join(skill_names) if skill_names else 'Not Found'}"
    )

    st.subheader("💼 Job Requirements")

    st.write(
        f"**Role:** {st.session_state.jd_data.get('job_role', 'N/A')}"
    )

    required_skills = st.session_state.jd_data.get(
        "required_skills",
        []
    )

    st.write(
        f"**Required Skills:** {', '.join(required_skills) if required_skills else 'Not Found'}"
    )

    st.subheader("🎯 Skill Match")

    matched = st.session_state.skill_match_result.get(
        "matched_skills",
        []
    )

    missing = st.session_state.skill_match_result.get(
        "missing_skills",
        []
    )

    with st.expander(
        f"✅ Matched Skills ({len(matched)})",
        expanded=True
    ):
        if matched:
            for skill in matched:
                st.write(f"• {skill}")
        else:
            st.write("No matched skills found.")

    with st.expander(
        f"❌ Missing Skills ({len(missing)})",
        expanded=True
    ):
        if missing:
            for skill in missing:
                st.write(f"• {skill}")
        else:
            st.write("No missing skills found.")

    st.subheader("📊 ATS Match Score")

    st.metric(
        label="ATS Score",
        value=f"{st.session_state.ats_score}%"
    )

    st.subheader("📈 Resume Improvement Suggestions")

    suggestions = generate_resume_suggestions(
        st.session_state.resume_data,
        st.session_state.jd_data,
        st.session_state.skill_match_result
        )

    st.markdown(suggestions)

# -------------------------
# Question Generator
# -------------------------

if "resume_data" in st.session_state:

    st.subheader("Interview Question Generator")

    if st.button("Generate Interview Questions"):

        questions = generate_questions(
            st.session_state.resume_data,
            st.session_state.jd_data,
            st.session_state.skill_match_result
            )
        

        # Store Questions
        st.session_state.questions = questions

        # Parse Questions
        parsed_questions = extract_questions(
            questions
        )

        # Remove empty questions
        parsed_questions = [
            q.strip()
            for q in parsed_questions
            if q.strip()
        ]

# Check if questions exist
        if len(parsed_questions) == 0:

            st.error(
                "No interview questions were generated. Please regenerate questions."
            )

            st.stop()

        st.session_state.parsed_questions = parsed_questions

        # Reset Mock Interview
        st.session_state.current_question_index = 0
        st.session_state.interview_started = False
        st.session_state.answer_evaluations = []
        st.session_state.user_answers = []

        if "user_answers" in st.session_state:
            del st.session_state.user_answers

    # Show Questions if Available
    if "questions" in st.session_state:

        st.subheader("Generated Interview Questions")

        st.markdown(
            st.session_state.questions
        )

        
# -------------------------
# Mock Interview
# -------------------------

if (
    "parsed_questions" in st.session_state
    and len(st.session_state.parsed_questions) > 0
):

    st.subheader("🎤 Mock Interview")

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False

    if "answer_evaluations" not in st.session_state:
        st.session_state.answer_evaluations = []

    if st.button("Start Mock Interview"):

        st.session_state.current_question_index = 0
        st.session_state.interview_started = True
        st.session_state.answer_evaluations = []

    if st.session_state.interview_started:

        current_question = get_current_question(
            st.session_state.parsed_questions,
            st.session_state.current_question_index
        )

        if current_question:

            total_questions = len(
                st.session_state.parsed_questions
            )

            current_index = (
                st.session_state.current_question_index
            )

            progress = (
                current_index / total_questions
            )

            st.progress(progress)

            st.write(
                f"Question {current_index + 1} of {total_questions}"
            )

            st.info(current_question)

            answer = st.text_area(
                "Your Answer",
                key=f"answer_{current_index}"
            )

            col1, col2 = st.columns(2)

            with col1:
                submit_btn = st.button(
                    "Submit Answer"
                )

            with col2:
                skip_btn = st.button(
                    "Skip Question"
                )

            if submit_btn:

                if not answer.strip():
                    st.warning(
                        "Please enter an answer."
                    )
                    st.stop()

                if "user_answers" not in st.session_state:
                    st.session_state.user_answers = []

                st.session_state.user_answers.append(
                    {
                        "question": current_question,
                        "answer": answer
                    }
                )

                evaluation = evaluate_answer(
                    current_question,
                    answer
                )

                st.session_state.answer_evaluations.append(
                    {
                        "question": current_question,
                        "answer": answer,
                        "evaluation": evaluation
                    }
                )

                st.session_state.current_question_index += 1

                st.rerun()

            if skip_btn:

                if "user_answers" not in st.session_state:
                    st.session_state.user_answers = []

                st.session_state.user_answers.append(
                    {
                        "question": current_question,
                        "answer": "Skipped"
                    }
                )

                st.session_state.answer_evaluations.append(
                    {
                        "question": current_question,
                        "answer": "Skipped",
                        "evaluation": "Score: 0/10"
                    }
                )

                st.session_state.current_question_index += 1

                st.rerun()

        else:

            st.success(
                "🎉 Mock Interview Completed!"
            )

            score_data = calculate_interview_score(
                st.session_state.answer_evaluations
            )

            st.subheader(
                "📊 Interview Summary"
            )

            st.metric(
                "Percentage",
                f"{score_data['percentage']}%"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Answered Questions",
                    score_data["answered_questions"]
                )

            with col2:
                st.metric(
                    "Skipped Questions",
                    score_data["skipped_questions"]
                )

            st.write(
                f"Total Score: {score_data['total_score']} / {score_data['max_score']}"
            )

            if st.button(
                "Generate Interview Report"
            ):

                report = generate_interview_report(
                    st.session_state.answer_evaluations
                )

                st.subheader(
                    "📊 AI Feedback Report"
                )

                st.markdown(report)

    # -------------------------
    # Study Plan
    # -------------------------

                st.subheader("📚 Personalized Study Plan")

                missing_skills = st.session_state.skill_match_result.get(
                    "missing_skills", []
                )

                study_plan = generate_study_plan(
                    missing_skills,
                    report)

                st.markdown(study_plan)


                st.subheader("📖 Recommended Resources")

                st.write("Missing Skills:", missing_skills)

                resources = recommend_resources(
                    missing_skills
                )

                for skill, links in resources.items():
                    
                    st.markdown(f"### {skill}")
                    
                    for link in links:
                        
                        st.markdown(f"- {link}")

# -------------------------
# Career Roadmap
# -------------------------

st.markdown("---")

st.header("🗺 Career Roadmap")

if st.button("Generate Career Roadmap"):

    missing_skills = st.session_state.skill_match_result.get(
        "missing_skills",
        []
    )

    roadmap = generate_career_roadmap(
        st.session_state.resume_data,
        st.session_state.jd_data,
        missing_skills
    )

    st.markdown(roadmap)


# -------------------------
# Ask Interview Coach (RAG)
# -------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("---")

st.header("🤖 Ask Interview Coach")

if st.button("🗑 Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

user_question = st.text_input(
    "Ask any interview question"
)

if st.button("Ask Coach"):

    if not user_question.strip():
        st.warning("Please enter a question.")

    else:

        answer = ask_interview_coach(
            user_question
        )

        st.session_state.chat_history.append(
            {
                "question": user_question,
                "answer": answer
            }
        )

        st.subheader("Answer")
        st.write(answer)

# Chat History
if st.session_state.chat_history:

    st.subheader("💬 Chat History")

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f"**🧑 You:** {chat['question']}"
        )

        st.markdown(
            f"**🤖 Coach:** {chat['answer']}"
        )

        st.markdown("---")