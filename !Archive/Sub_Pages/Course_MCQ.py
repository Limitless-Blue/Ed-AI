import json
import streamlit as st
from Gen_Process.UI_Chats.Assistant_Chat import Help_Chat


def Course_MCQ(test_file):
    st.sidebar.markdown(
        """
        <style>
        .mentor-title {
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(90deg, #FFF5EE, #F3CFC6, #f9bec7, #ffafcc, #f72585, #b5179e, #7209b7, #560bad, #480ca8, #3a0ca3, #3f37c9, #4361ee, #4895ef, #4cc9f0, #caf0f8, #FFF5EE, #FFF5EE);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            background-size: 200% 200%;
            animation: gradientFlow 5s ease infinite;
            text-align: center;
            margin-top: 0;
            margin-bottom: 15px;
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        <h1 class="mentor-title">✨ Mentor Chat</h1>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <style>
        .gradient-divider-sidebar {
            height: 5px;
            border-radius: 15px;
            background: linear-gradient(to right, #212529, #343a40, #212529);
            margin: 0px 0;
            border: none;
        }
        </style>
        <div class="gradient-divider-sidebar"></div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        Help_Chat()

    with open(test_file, "r") as f:
        questions_data = json.load(f)

    questions = questions_data["questions"]

    current_question_idx = st.session_state.get("current_question_idx", 0)
    if "selected_answers" not in st.session_state:
        st.session_state["selected_answers"] = [None] * len(questions)
    selected_answers = st.session_state["selected_answers"]

    def navigate(direction):
        if direction == "next" and current_question_idx < len(questions) - 1:
            st.session_state["current_question_idx"] = current_question_idx + 1
        elif direction == "prev" and current_question_idx > 0:
            st.session_state["current_question_idx"] = current_question_idx - 1
        else:
            st.session_state["current_question_idx"] = direction

    st.markdown(
        """
        <style>
        .gradient-divider-sidebar {
            height: 5px;
            border-radius: 15px;
            background: linear-gradient(to right, #212529, #343a40, #212529);
            margin: 30px 0;
            border: none;
        }
        </style>
        <div class="gradient-divider-sidebar"></div>
        """,
        unsafe_allow_html=True,
    )

    colq_1, colq_2 = st.columns([7, 3])
    with colq_1:
        st.markdown(f"### Question {current_question_idx + 1}:", unsafe_allow_html=True)
        st.markdown(
            f"<h4>{questions[current_question_idx]['question']}</h4>",
            unsafe_allow_html=True,
        )

        selected_answer = st.radio(
            "",
            questions[current_question_idx]["options"],
            index=(
                None
                if selected_answers[current_question_idx] is None
                else questions[current_question_idx]["options"].index(
                    selected_answers[current_question_idx]
                )
            ),
            key=f"question_{current_question_idx}",
        )

        if selected_answer:
            selected_answers[current_question_idx] = selected_answer
            if selected_answer == questions[current_question_idx]["answer"]:
                st.success("Correct!")
                st.write(
                    f"Explanation: {questions[current_question_idx]['explanation']}"
                )
            else:
                st.error("Incorrect!")
                selected_option_key = selected_answer[0]
                explanation = questions[current_question_idx][
                    "incorrect_explanation"
                ].get(selected_answer, "No explanation available.")
                st.write(f"Explanation: {explanation}")

    with colq_2:
        st.markdown("<h5>Jump to Question</h5>", unsafe_allow_html=True)
        cols = st.columns(5)
        for idx, question in enumerate(questions):
            with cols[idx % 5]:
                button_label = f"Q{idx + 1}"
                if st.button(button_label, key=f"q_btn_{idx}"):
                    navigate(idx)

    st.markdown(
        """
        <style>
        .gradient-divider-sidebar {
            height: 5px;
            border-radius: 15px;
            background: linear-gradient(to right, #212529, #343a40, #212529);
            margin: 30px 0;
            border: none;
        }
        </style>
        <div class="gradient-divider-sidebar"></div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if current_question_idx > 0:
            st.button(
                "Previous", on_click=navigate, args=("prev",), use_container_width=True
            )

    with col2:
        if current_question_idx < len(questions) - 1:
            st.button(
                "Next", on_click=navigate, args=("next",), use_container_width=True
            )
