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
from modules.resume_improver import generate_resume_suggestions
from modules.custom_style import (
    inject_custom_css,
    render_hero,
    render_skill_badges,
    render_empty_state,
    render_footer,
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


# =====================================================
# Helper: safe call wrapper
# =====================================================

def safe_call(fn, *args, error_label="this step", **kwargs):
    """Run a module function, surfacing a friendly error instead of crashing."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:
        st.error(f"Something went wrong while running {error_label}. Details: {exc}")
        return None


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:
    st.markdown("### 📌 Workflow")
    st.markdown(
        """
        1. Upload your resume (PDF)
        2. Paste the job description
        3. Click **Analyze**
        4. Review your ATS score & tips
        5. Generate interview questions
        6. Take the mock interview
        7. Get your study plan & roadmap
        """
    )

    st.markdown("---")

    if "ats_score" in st.session_state:
        st.markdown("### 📊 Current ATS Score")
        st.metric("Score", f"{st.session_state.ats_score}%")
    else:
        st.markdown("### 📊 ATS Score")
        st.caption("Run an analysis to see your score here.")

    if st.session_state.get("score_history"):
        st.markdown("### 📈 Mock Interview History")
        for i, s in enumerate(st.session_state.score_history, start=1):
            st.caption(f"Attempt {i}: {s}%")

    st.markdown("---")
    if st.button("🔄 Reset Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# =====================================================
# Resume + JD Input
# =====================================================

col_left, col_right = st.columns(2)

with col_left:
    section_card_start()
    st.subheader("📄 Upload Resume")
    resume = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )
    if resume is None:
        st.caption("Accepted format: PDF")
    section_card_end()

with col_right:
    section_card_start()
    st.subheader("💼 Paste Job Description")
    job_description = st.text_area(
        "Enter Job Description Here",
        height=150,
        label_visibility="collapsed",
        placeholder="Paste the full job description here..."
    )
    section_card_end()

analyze_clicked = st.button("🔍 Analyze", use_container_width=True)

if analyze_clicked:

    if resume is None:
        st.error("Please upload a resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        with st.spinner("Reading your resume..."):
            resume_text = safe_call(extract_resume_text, resume, error_label="resume parsing")

        if resume_text:

            with st.spinner("Analyzing your resume and matching it to the job..."):
                resume_data = safe_call(extract_resume_details, resume_text, error_label="resume analysis")
                jd_data = safe_call(extract_jd_details, job_description, error_label="job description analysis")

                skill_match_result = None
                ats_score = None

                if resume_data is not None and jd_data is not None:
                    skill_match_result = safe_call(match_skills, resume_data, jd_data, error_label="skill matching")

                if skill_match_result is not None and jd_data is not None:
                    ats_score = safe_call(calculate_ats_score, skill_match_result, jd_data, error_label="ATS scoring")

            if resume_data is not None and jd_data is not None and skill_match_result is not None and ats_score is not None:
                st.session_state.resume_text = resume_text
                st.session_state.resume_data = resume_data
                st.session_state.jd_data = jd_data
                st.session_state.skill_match_result = skill_match_result
                st.session_state.ats_score = ats_score

                # Reset downstream state on a fresh analysis
                for key in [
                    "questions", "parsed_questions", "current_question_index",
                    "interview_started", "answer_evaluations", "user_answers",
                    "interview_report", "study_plan", "resources", "roadmap",
                ]:
                    st.session_state.pop(key, None)

                st.success("✅ Resume analyzed successfully!")
            else:
                st.error("Analysis could not be completed. Please check the inputs and try again.")


# =====================================================
# Main tabs
# =====================================================

tab_resume, tab_questions, tab_interview, tab_growth, tab_coach = st.tabs(
    ["📄 Resume & ATS", "📝 Interview Questions", "🎤 Mock Interview", "📈 Growth Plan", "🤖 Ask Coach"]
)


# -----------------------------------------------------
# TAB 1: Resume & ATS
# -----------------------------------------------------
with tab_resume:

    if "resume_data" not in st.session_state:
        render_empty_state(
            "No analysis yet",
            "Upload your resume and paste a job description above, then click Analyze."
        )
    else:

        if "resume_text" in st.session_state:
            with st.expander("📄 View Extracted Resume Text"):
                st.text_area(
                    "Extracted Resume",
                    st.session_state.resume_text,
                    height=250,
                    label_visibility="collapsed"
                )

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
                st.caption("Not Found")
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
                st.caption("Not Found")
            section_card_end()

        # Skill Match
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

        # ATS Score
        section_card_start()
        st.subheader("📊 ATS Match Score")

        score_col, bar_col = st.columns([1, 3])
        with score_col:
            st.metric(label="ATS Score", value=f"{st.session_state.ats_score}%")
        with bar_col:
            st.progress(min(int(st.session_state.ats_score), 100) / 100)
        section_card_end()

        # Resume Improvement Suggestions
        section_card_start()
        st.subheader("📈 Resume Improvement Suggestions")

        if "resume_suggestions" not in st.session_state:
            with st.spinner("Generating suggestions..."):
                st.session_state.resume_suggestions = safe_call(
                    generate_resume_suggestions,
                    st.session_state.resume_data,
                    st.session_state.jd_data,
                    st.session_state.skill_match_result,
                    error_label="resume suggestions"
                )

        if st.session_state.get("resume_suggestions"):
            st.markdown(st.session_state.resume_suggestions)

            st.download_button(
                "⬇️ Download Suggestions",
                data=st.session_state.resume_suggestions,
                file_name="resume_suggestions.txt",
                mime="text/plain"
            )
        section_card_end()


# -----------------------------------------------------
# TAB 2: Interview Questions
# -----------------------------------------------------
with tab_questions:

    if "resume_data" not in st.session_state:
        render_empty_state(
            "Analyze your resume first",
            "Interview questions are tailored to your resume and the job description."
        )
    else:

        section_card_start()
        st.subheader("📝 Interview Question Generator")
        st.caption("Generates a fresh set of role-specific questions based on your skill gaps.")

        if st.button("✨ Generate Interview Questions"):

            with st.spinner("Generating tailored interview questions..."):
                questions = safe_call(
                    generate_questions,
                    st.session_state.resume_data,
                    st.session_state.jd_data,
                    st.session_state.skill_match_result,
                    error_label="question generation"
                )

            if questions:
                parsed_questions = safe_call(extract_questions, questions, error_label="question parsing") or []
                parsed_questions = [q.strip() for q in parsed_questions if q.strip()]

                if len(parsed_questions) == 0:
                    st.error("No interview questions were generated. Please try again.")
                else:
                    st.session_state.questions = questions
                    st.session_state.parsed_questions = parsed_questions

                    # Reset mock interview state
                    st.session_state.current_question_index = 0
                    st.session_state.interview_started = False
                    st.session_state.answer_evaluations = []
                    st.session_state.user_answers = []
                    st.session_state.pop("interview_report", None)
                    st.session_state.pop("study_plan", None)
                    st.session_state.pop("resources", None)

                    st.success(f"Generated {len(parsed_questions)} questions. Head to the Mock Interview tab to begin.")

        if "questions" in st.session_state:
            with st.expander("📋 Generated Interview Questions", expanded=True):
                st.markdown(st.session_state.questions)

            st.download_button(
                "⬇️ Download Questions",
                data=st.session_state.questions,
                file_name="interview_questions.txt",
                mime="text/plain"
            )
        else:
            st.caption("No questions generated yet.")

        section_card_end()


# -----------------------------------------------------
# TAB 3: Mock Interview
# -----------------------------------------------------
with tab_interview:

    if not st.session_state.get("parsed_questions"):
        render_empty_state(
            "No questions ready",
            "Generate interview questions in the previous tab to start a mock interview."
        )
    else:

        section_card_start()
        st.subheader("🎤 Mock Interview")

        if "current_question_index" not in st.session_state:
            st.session_state.current_question_index = 0

        if "interview_started" not in st.session_state:
            st.session_state.interview_started = False

        if "answer_evaluations" not in st.session_state:
            st.session_state.answer_evaluations = []

        if not st.session_state.interview_started:
            st.caption(f"{len(st.session_state.parsed_questions)} questions ready.")
            if st.button("▶️ Start Mock Interview"):
                st.session_state.current_question_index = 0
                st.session_state.interview_started = True
                st.session_state.answer_evaluations = []
                st.rerun()

        if st.session_state.interview_started:

            current_question = get_current_question(
                st.session_state.parsed_questions,
                st.session_state.current_question_index
            )

            if current_question:

                total_questions = len(st.session_state.parsed_questions)
                current_index = st.session_state.current_question_index
                progress = current_index / total_questions

                st.progress(progress)
                st.write(f"**Question {current_index + 1} of {total_questions}**")
                st.info(current_question)

                answer = st.text_area(
                    "Your Answer",
                    key=f"answer_{current_index}",
                    height=120
                )

                col1, col2 = st.columns(2)

                with col1:
                    submit_btn = st.button("✅ Submit Answer", use_container_width=True)

                with col2:
                    skip_btn = st.button("⏭️ Skip Question", use_container_width=True)

                if submit_btn:

                    if not answer.strip():
                        st.warning("Please enter an answer.")
                        st.stop()

                    st.session_state.setdefault("user_answers", []).append(
                        {"question": current_question, "answer": answer}
                    )

                    with st.spinner("Evaluating your answer..."):
                        evaluation = safe_call(
                            evaluate_answer, current_question, answer,
                            error_label="answer evaluation"
                        )

                    st.session_state.answer_evaluations.append(
                        {
                            "question": current_question,
                            "answer": answer,
                            "evaluation": evaluation or "Score: 0/10"
                        }
                    )

                    st.session_state.current_question_index += 1
                    st.rerun()

                if skip_btn:

                    st.session_state.setdefault("user_answers", []).append(
                        {"question": current_question, "answer": "Skipped"}
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

                st.success("🎉 Mock Interview Completed!")

                score_data = safe_call(
                    calculate_interview_score,
                    st.session_state.answer_evaluations,
                    error_label="score calculation"
                )

                if score_data:

                    if "score_history" not in st.session_state:
                        st.session_state.score_history = []

                    if not st.session_state.get("score_recorded", False):
                        st.session_state.score_history.append(score_data["percentage"])
                        st.session_state.score_recorded = True

                    st.subheader("📊 Interview Summary")

                    m1, m2, m3 = st.columns(3)

                    with m1:
                        st.metric("Percentage", f"{score_data['percentage']}%")

                    with m2:
                        st.metric("Answered Questions", score_data["answered_questions"])

                    with m3:
                        st.metric("Skipped Questions", score_data["skipped_questions"])

                    st.write(
                        f"**Total Score:** {score_data['total_score']} / {score_data['max_score']}"
                    )

                    if st.button("📑 Generate Interview Report"):

                        with st.spinner("Generating your feedback report..."):
                            report = safe_call(
                                generate_interview_report,
                                st.session_state.answer_evaluations,
                                error_label="report generation"
                            )

                        if report:
                            st.session_state.interview_report = report

                    if st.session_state.get("interview_report"):
                        st.subheader("📊 AI Feedback Report")
                        st.markdown(st.session_state.interview_report)

                        st.download_button(
                            "⬇️ Download Report",
                            data=st.session_state.interview_report,
                            file_name="interview_report.txt",
                            mime="text/plain"
                        )

                if st.button("🔁 Retake Mock Interview"):
                    st.session_state.current_question_index = 0
                    st.session_state.interview_started = True
                    st.session_state.answer_evaluations = []
                    st.session_state.score_recorded = False
                    st.session_state.pop("interview_report", None)
                    st.rerun()

        section_card_end()


# -----------------------------------------------------
# TAB 4: Growth Plan (Study Plan, Resources, Roadmap)
# -----------------------------------------------------
with tab_growth:

    if "skill_match_result" not in st.session_state:
        render_empty_state(
            "Analyze your resume first",
            "Your study plan and career roadmap are based on your skill gaps."
        )
    else:

        missing_skills = st.session_state.skill_match_result.get("missing_skills", [])

        # Study Plan + Resources (requires interview report)
        section_card_start()
        st.subheader("📚 Personalized Study Plan")

        if not st.session_state.get("interview_report"):
            st.caption(
                "Complete a mock interview and generate the AI feedback report "
                "to unlock a personalized study plan."
            )
        else:

            if "study_plan" not in st.session_state:
                with st.spinner("Building your study plan..."):
                    st.session_state.study_plan = safe_call(
                        generate_study_plan,
                        missing_skills,
                        st.session_state.interview_report,
                        error_label="study plan generation"
                    )

            if st.session_state.get("study_plan"):
                st.markdown(st.session_state.study_plan)

                st.download_button(
                    "⬇️ Download Study Plan",
                    data=st.session_state.study_plan,
                    file_name="study_plan.txt",
                    mime="text/plain"
                )

            st.markdown("#### 📖 Recommended Resources")

            if missing_skills:
                render_skill_badges(missing_skills, kind="missing")

                if "resources" not in st.session_state:
                    with st.spinner("Finding resources..."):
                        st.session_state.resources = safe_call(
                            recommend_resources, missing_skills,
                            error_label="resource recommendations"
                        )

                resources = st.session_state.get("resources") or {}
                for skill, links in resources.items():
                    st.markdown(f"**{skill}**")
                    for link in links:
                        st.markdown(f"- {link}")
            else:
                st.caption("No missing skills identified — nice work!")

        section_card_end()

        # Career Roadmap
        section_card_start()
        st.subheader("🗺 Career Roadmap")
        st.caption("A longer-term plan to close skill gaps and grow toward this role.")

        if st.button("🚀 Generate Career Roadmap"):
            with st.spinner("Charting your career roadmap..."):
                roadmap = safe_call(
                    generate_career_roadmap,
                    st.session_state.resume_data,
                    st.session_state.jd_data,
                    missing_skills,
                    error_label="career roadmap generation"
                )
            if roadmap:
                st.session_state.roadmap = roadmap

        if st.session_state.get("roadmap"):
            st.markdown(st.session_state.roadmap)

            st.download_button(
                "⬇️ Download Roadmap",
                data=st.session_state.roadmap,
                file_name="career_roadmap.txt",
                mime="text/plain"
            )

        section_card_end()


# -----------------------------------------------------
# TAB 5: Ask Interview Coach (RAG)
# -----------------------------------------------------
with tab_coach:

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    section_card_start()
    st.subheader("🤖 Ask Interview Coach")
    st.caption("Ask anything about interview prep, behavioral questions, or this role.")

    col_clear, _ = st.columns([1, 4])
    with col_clear:
        if st.button("🗑 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    user_question = st.text_input(
        "Ask any interview question",
        placeholder="e.g. How should I answer 'Tell me about yourself'?",
        label_visibility="collapsed"
    )

    if st.button("💬 Ask Coach"):

        if not user_question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer = safe_call(ask_interview_coach, user_question, error_label="coach response")

            if answer:
                st.session_state.chat_history.append(
                    {"question": user_question, "answer": answer}
                )

    if st.session_state.chat_history:
        st.markdown("#### 💬 Conversation")

        for chat in reversed(st.session_state.chat_history):
            st.markdown(
                f'<div class="chat-user">🧑 <strong>You:</strong> {chat["question"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="chat-coach">🤖 <strong>Coach:</strong> {chat["answer"]}</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("No conversation yet. Ask your first question above.")

    section_card_end()


render_footer()
