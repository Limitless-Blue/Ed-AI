import streamlit as st
from Sub_Pages.Mock_Interview import Mock_Interview


def Mock_Assessment():
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        col1, col2 = st.columns([5, 4])

        with col1:
            hardness = st.selectbox(
                "Select the hardness level:", ["😉 Easy", "👍 Medium", "💪 Hard"]
            )
            comments = st.text_area("Anything you'd like to say? (Optional)")

        with col2:
            topics = st.multiselect(
                "Select the topics you are interested in:",
                ["Trees", "Graphs", "Arrays", "Linked Lists", "Stacks", "Queue"],
            )
            uploaded_file = st.file_uploader("Upload your resume", type="pdf")

        st.markdown("---")

        if st.button("Let's Start the Assessment"):
            st.session_state.submitted = True
            st.session_state.hardness = hardness
            st.session_state.comments = comments
            st.session_state.topics = topics
            st.session_state.uploaded_file = uploaded_file
            st.rerun()

    if st.session_state.submitted:
        st.write("### Assessment Summary")
        st.write("Hardness:", st.session_state.hardness)
        st.write(
            "Topics selected:",
            ", ".join(st.session_state.topics) if st.session_state.topics else "None",
        )
        st.write(
            "Additional comments:",
            st.session_state.comments if st.session_state.comments else "None",
        )

        if st.session_state.uploaded_file is not None:
            st.write("Resume uploaded successfully!")
        else:
            st.write("No resume uploaded.")
        Mock_Interview()
