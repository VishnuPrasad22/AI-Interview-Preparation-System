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
from modules.custom_style import (
    inject_custom_css,
    render_hero,
    render_skill_badges,
    section_card_start,
    section_card_end,
)

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

inject_custom_css()
render_hero()

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:
    st.markdown("### 📌 Workflow")
    st.markdown(
        """
        1. Upload your resume (PDF)
        2. Paste the job description
        3. Click **Analyze**
        4. Review ATS score & suggestions
        5. Generate interview questions
        6. Take the mock interview
        7. Get your study plan & roadmap
        """
    )
    st.markdown("---")
    if "ats_score" in st.session_state:
        st.markdown("### 📊 Current ATS Score")
        st.metric("Score", f"{st.session_state.ats_score}%")
    if "answer_evaluations" in st.session_state and st.session_state.answer_evaluations:
        st.markdown("### 🎤 Interview Progress")
        st.write(f"{len(st.session_state.answer_evaluations)} answers recorded")

# -------------------------
# Resume + JD Input
# -------------------------

col_left, col_right = st.columns(2)

with col_left:
    section_card_start()
    st.subheader("📄 Upload Resume")
    resume = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"]
    )
    section_card_end()

with col_right:
    section_card_start()
    st.subheader("💼 Paste Job Description")
    job_description = st.text_area(
        "Enter Job Description Here",
        height=200,
        label_visibility="collapsed",
        placeholder="Paste the full job description here..."
    )
    section_card_end()

# -------------------------
# Analyze Button
# -------------------------

analyze_clicked = st.button("🔍 Analyze", use_container_width=True)

if analyze_clicked:

    if resume is None:
        st.error("Please upload a resume")

    elif not job_description.strip():
        st.error("Please enter a job description")

    else:

        with st.spinner("Analyzing your resume against the job description..."):

            # Resume Parsing
            resume_text = extract_resume_text(resume)

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
            st.session_state.resume_text = resume_text
            st.session_state.resume_data = resume_data
            st.session_state.jd_data = jd_data
            st.session_state.skill_match_result = skill_match_result
            st.session_state.ats_score = ats_score

        st.success("✅ Resume analyzed successfully!")

# -------------------------
# Resume Text (collapsible)
# -------------------------

if "resume_text" in st.session_state:
    with st.expander("📄 View Extracted Resume Text"):
        st.text_area(
            "Extracted Resume",
            st.session_state.resume_text,
            height=300,
            label_visibility="collapsed"
        )

# -------------------------
# Display Results
# -------------------------

if "resume_data" in st.session_state:

    col_a, col_b = st.columns(2)

    with col_a:
        section_card_start()
        st.subheader("📄 Resume Summary")

        st.markdown(
            f"**Name:** {st.session_state.resume_data.get('name', 'Not Found')}"
        )

        skills = st.session_state.resume_data.get("skills", [])

        skill_names = []
        for skill in skills:
            if isinstance(skill, str):
                skill_names.append(skill)
            elif isinstance(skill, dict):
                skill_names.append(str(skill))

        st.markdown("**Skills:**")
        if skill_names:
            render_skill_badges(skill_names, kind="match")
        else:
            st.write("Not Found")
        section_card_end()

    with col_b:
        section_card_start()
        st.subheader("💼 Job Requirements")

        st.markdown(
            f"**Role:** {st.session_state.jd_data.get('job_role', 'N/A')}"
        )

        required_skills = st.session_state.jd_data.get("required_skills", [])

        st.markdown("**Required Skills:**")
        if required_skills:
            render_skill_badges(required_skills, kind="match")
        else:
            st.write("Not Found")
        section_card_end()

    # -------------------------
    # Skill Match
    # -------------------------

    section_card_start()
    st.subheader("🎯 Skill Match")

    matched = st.session_state.skill_match_result.get("matched_skills", [])
    missing = st.session_state.skill_match_result.get("missing_skills", [])

    col_m, col_n = st.columns(2)

    with col_m:
        st.markdown(f"**✅ Matched Skills ({len(matched)})**")
        render_skill_badges(matched, kind="match")

    with col_n:
        st.markdown(f"**❌ Missing Skills ({len(missing)})**")
        render_skill_badges(missing, kind="missing")

    section_card_end()

    # -------------------------
    # ATS Score
    # -------------------------

    section_card_start()
    st.subheader("📊 ATS Match Score")

    score_col, bar_col = st.columns([1, 3])
    with score_col:
        st.metric(label="ATS Score", value=f"{st.session_state.ats_score}%")
    with bar_col:
        st.write("")
        st.progress(min(int(st.session_state.ats_score), 100) / 100)
    section_card_end()

    # -------------------------
    # Resume Improvement Suggestions
    # -------------------------

    section_card_start()
    st.subheader("📈 Resume Improvement Suggestions")

    suggestions = generate_resume_suggestions(
        st.session_state.resume_data,
        st.session_state.jd_data,
        st.session_state.skill_match_result
        )

    st.markdown(suggestions)
    section_card_end()

# -------------------------
# Question Generator
# -------------------------

if "resume_data" in st.session_state:

    section_card_start()
    st.subheader("📝 Interview Question Generator")

    if st.button("Generate Interview Questions"):

        with st.spinner("Generating tailored interview questions..."):

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
        with st.expander("📋 Generated Interview Questions", expanded=True):
            st.markdown(
                st.session_state.questions
            )

    section_card_end()


# -------------------------
# Mock Interview
# -------------------------

if (
    "parsed_questions" in st.session_state
    and len(st.session_state.parsed_questions) > 0
):

    section_card_start()
    st.subheader("🎤 Mock Interview")

    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False

    if "answer_evaluations" not in st.session_state:
        st.session_state.answer_evaluations = []

    if st.button("▶️ Start Mock Interview"):

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
                f"**Question {current_index + 1} of {total_questions}**"
            )

            st.info(current_question)

            answer = st.text_area(
                "Your Answer",
                key=f"answer_{current_index}"
            )

            col1, col2 = st.columns(2)

            with col1:
                submit_btn = st.button(
                    "✅ Submit Answer", use_container_width=True
                )

            with col2:
                skip_btn = st.button(
                    "⏭️ Skip Question", use_container_width=True
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

                with st.spinner("Evaluating your answer..."):
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

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Percentage",
                    f"{score_data['percentage']}%"
                )

            with m2:
                st.metric(
                    "Answered Questions",
                    score_data["answered_questions"]
                )

            with m3:
                st.metric(
                    "Skipped Questions",
                    score_data["skipped_questions"]
                )

            st.write(
                f"**Total Score:** {score_data['total_score']} / {score_data['max_score']}"
            )

            if st.button(
                "📑 Generate Interview Report"
            ):

                with st.spinner("Generating your feedback report..."):
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

                with st.spinner("Building your study plan..."):
                    study_plan = generate_study_plan(
                        missing_skills,
                        report)

                st.markdown(study_plan)

                st.subheader("📖 Recommended Resources")

                if missing_skills:
                    render_skill_badges(missing_skills, kind="missing")
                else:
                    st.write("No missing skills identified.")

                resources = recommend_resources(
                    missing_skills
                )

                for skill, links in resources.items():

                    st.markdown(f"#### {skill}")

                    for link in links:

                        st.markdown(f"- {link}")

    section_card_end()

# -------------------------
# Career Roadmap
# -------------------------

st.markdown("---")
st.header("🗺 Career Roadmap")

section_card_start()

if st.button("🚀 Generate Career Roadmap"):

    if "skill_match_result" not in st.session_state:
        st.warning("Please analyze your resume and job description first.")
    else:
        missing_skills = st.session_state.skill_match_result.get(
            "missing_skills",
            []
        )

        with st.spinner("Charting your career roadmap..."):
            roadmap = generate_career_roadmap(
                st.session_state.resume_data,
                st.session_state.jd_data,
                missing_skills
            )

        st.markdown(roadmap)

section_card_end()


# -------------------------
# Ask Interview Coach (RAG)
# -------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("---")
st.header("🤖 Ask Interview Coach")

section_card_start()

col_clear, _ = st.columns([1, 4])
with col_clear:
    if st.button("🗑 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

user_question = st.text_input(
    "Ask any interview question",
    placeholder="e.g. How should I answer 'Tell me about yourself'?"
)

if st.button("💬 Ask Coach"):

    if not user_question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):
            answer = ask_interview_coach(
                user_question
            )

        st.session_state.chat_history.append(
            {
                "question": user_question,
                "answer": answer
            }
        )

# Chat History
if st.session_state.chat_history:

    st.markdown("#### 💬 Conversation")

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f'<div class="chat-user">🧑 <strong>You:</strong> {chat["question"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="chat-coach">🤖 <strong>Coach:</strong> {chat["answer"]}</div>',
            unsafe_allow_html=True
        )

section_card_end()
