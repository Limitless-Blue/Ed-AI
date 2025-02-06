import os
import json
import streamlit as st
import base64
import mimetypes
import pandas as pd
from urllib.parse import urlencode
from Sub_Pages.Coding_Problems_Page import Coding_Problems_page

memory_of_select_button = r"EXP\memory select problem.txt"


def clear_and_rewrite_memory_of_navbar(file_path, new_content):
    with open(file_path, "w") as file:
        file.write(new_content)


def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def show_details(selected_image):
    Redirecting_json_file_path = (
        r"Static_Files\Practice_Page_Problems\Coding_Problem.json"
    )

    with open(Redirecting_json_file_path, "r") as f:
        data = json.load(f)

    problem_ID = selected_image
    problem_title = data["problems"][selected_image]["title"]
    problem_problem_description = data["problems"][selected_image][
        "Problem_Description"
    ]
    problem_test_cases = data["problems"][selected_image]["Test_Cases"]

    Coding_Problems_page(
        problem_problem_description, problem_title, problem_test_cases, problem_ID
    )
    return


def Practice_Coding_page():
    if "selected_problem" not in st.session_state:
        st.session_state.selected_problem = None

    directory_Featured = r"Static_Files\Practice_Page_Problems\Featured"
    directory_Recommendation = (
        r"Static_Files\Practice_Page_Problems\All_Coding_Problems"
    )
    directory_Recommendation = (
        r"dynamic files\Main_pages\Recommendations\Practice_Coding_page_recommendation"
    )

    if not st.session_state.selected_problem:
        query_params = st.query_params
        if "selected_image" in query_params:
            selected_image = query_params["selected_image"]
            base_name, extension = os.path.splitext(selected_image)
            show_details(base_name)
            return

        if os.path.exists(directory_Featured):
            image_width = 550
            image_height = 350
            margin_right = 3

            image_tags = ""
            filenames = sorted(os.listdir(directory_Featured))
            N = 0
            for i, filename in enumerate(filenames):
                file_path = os.path.join(directory_Featured, filename)
                if os.path.isfile(file_path):
                    N += 1
                    encoded_image = load_image_as_base64(file_path)
                    mime_type = get_mime_type(filename)
                    margin_style = (
                        f"margin-right: {margin_right}px;"
                        if i < len(filenames) - 1
                        else ""
                    )

                    image_url = f"?{urlencode({'selected_image': filename})}"
                    image_tags += f'<a href="{image_url}"><img src="data:{mime_type};base64,{encoded_image}" alt="{filename}" style="{margin_style} cursor: pointer;"></a>'

            total_width = N * image_width + (N - 1) * margin_right

            full_image_tags = image_tags + image_tags

            st.markdown(
                f"""
            <style>
            .scroll-container {{
                overflow: hidden;
                position: relative;
                width: 100%;
            }}

            .scroll-content {{
                display: flex;
                width: {2 * total_width}px; /* Double the total width */
                animation: scroll 60s linear infinite; /* Adjust duration as needed */
                transition: transform 0.5s ease;
            }}

            .scroll-content img {{
                width: {image_width}px;
                height: {image_height}px;
                object-fit: cover;
                border-radius: 3px;
                flex-shrink: 0; /* Prevent images from shrinking */
                transition: transform 0.4s ease, border-radius 1s ease;
            }}

            .scroll-container:hover .scroll-content {{
                animation-play-state: paused; /* Pause animation on hover */
            }}

            .scroll-content img:hover {{
                transform: scale(0.9); /* Magnify the image on hover */
                border-radius: 11px;
            }}

            @keyframes scroll {{
                0% {{
                    transform: translateX(0);
                }}
                100% {{
                    transform: translateX(-{total_width}px);
                }}
            }}
            </style>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
            <div class="scroll-container">
                <div class="scroll-content">
                    {full_image_tags}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Directory not found: {directory_Featured}")

        st.title("Recommendations")

        if os.path.exists(directory_Recommendation):
            image_width = 480
            image_height = 230
            margin_right = 10

            image_tags = ""
            filenames = sorted(os.listdir(directory_Recommendation))
            for i, filename in enumerate(filenames):
                file_path = os.path.join(directory_Recommendation, filename)
                if os.path.isfile(file_path):
                    encoded_image = load_image_as_base64(file_path)
                    mime_type = get_mime_type(filename)
                    margin_style = (
                        f"margin-right: {margin_right}px;"
                        if i < len(filenames) - 1
                        else ""
                    )

                    image_url = f"?{urlencode({'selected_image': filename})}"
                    image_tags += f'<a href="{image_url}"><img src="data:{mime_type};base64,{encoded_image}" alt="{filename}" style="border-radius: 3px; {margin_style} width: {image_width}px; height: {image_height}px; object-fit: cover; vertical-align: middle;"></a>'

            st.markdown(
                f"""
            <style>
            .scroll-container-static {{
                overflow-x: auto;
                white-space: nowrap;
                -webkit-overflow-scrolling: touch;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}

            .scroll-content-static img {{
                display: inline-block;
                width: {image_width}px;
                height: {image_height}px;
                object-fit: cover;
                border-radius: 30px;
                margin-right: {margin_right}px;
                vertical-align: middle;
                transition: transform 0.3s ease, box-shadow 0.3s ease, border-radius 1s ease, filter 0.4s ease, border-radius 1s ease;
            }}

            .scroll-content-static img:hover {{
                transform: scale(0.95);
                box-shadow: 0px 8px 30px rgba(255, 255, 255, 0.2),
                            0px 4px 15px rgba(0, 0, 0, 0.15);
                backdrop-filter: blur(10px);
                filter: brightness(1.1);
            }}

            /* Dark themed scrollbar with rounded corners */
            .scroll-container-static::-webkit-scrollbar {{
                height: 8px;
            }}

            .scroll-container-static::-webkit-scrollbar-track {{
                background: #333;  /* Dark background for the track */
                border-radius: 20px; /* This does not affect the visual on some browsers */
            }}

            .scroll-container-static::-webkit-scrollbar-thumb {{
                background: #555;  /* Darker thumb */
                border-radius: 10px;
                border: 2px solid #333; /* Add a border to the thumb to visually create the effect of rounded corners */
            }}

            .scroll-container-static::-webkit-scrollbar-thumb:hover {{
                background: #888;  /* Slightly lighter on hover */
            }}

            .scroll-container-static {{
                scrollbar-width: thin;  /* Firefox */
                scrollbar-color: #555 #333;  /* Darker colors for Firefox */
                border-radius: 10px; /* This will only affect the container, not the scrollbar itself */
            }}
            </style>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
            <div class="scroll-container-static">
                <div class="scroll-content-static">
                    {image_tags}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Directory not found: {directory_Recommendation}")

        st.title("All Coding Problems")

        if "selected_problem" not in st.session_state:
            st.session_state.selected_problem = None
            clear_and_rewrite_memory_of_navbar(
                memory_of_select_button, str(st.session_state.selected_problem)
            )

        with open(r"Static_Files\Practice_Page_Problems\Coding_Problem.json") as f:
            json_data = json.load(f)

        problems_data = {"S no.": [], "Title": [], "Difficulty": [], "ID": []}

        problems_info = json_data["problems"]

        for idx, (key, problem) in enumerate(problems_info.items(), start=1):
            problems_data["S no."].append(str(idx))
            problems_data["Title"].append(problem["title"])
            problems_data["Difficulty"].append(problem["Difficulty"])
            problems_data["ID"].append(key)

        df = pd.DataFrame(problems_data)

        difficulty_filter = st.selectbox(
            "Filter by Difficulty:", ["All", "Easy", "Medium", "Hard"], index=0
        )

        if difficulty_filter != "All":
            df = df[df["Difficulty"] == difficulty_filter]

        def difficulty_bg_color(difficulty):
            if difficulty == "Easy":
                return "background-color: rgba(0, 200, 0, 0.7); color: white; font-weight: bold; border-radius: 30px; padding: 5px; text-align: center;"
            elif difficulty == "Medium":
                return "background-color: rgba(249, 105, 14, 0.75); color: white; font-weight: bold; border-radius: 30px; padding: 5px; text-align: center;"
            elif difficulty == "Hard":
                return "background-color: rgba(255, 0, 0, 0.7); color: white; font-weight: bold; border-radius: 30px; padding: 5px; text-align: center;"
            return ""

        st.markdown(
            """
            <style>
                .problem-row { margin-bottom: 10px; }
                .solve-button { text-align: center; }
            </style>
            <hr style='border: 2px solid #ccc; border-radius: 5px;'>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns([1, 5, 2, 2])
        with col1:
            st.subheader("S no.")
        with col2:
            st.subheader("Title")
        with col3:
            st.subheader("Difficulty")
        with col4:
            st.subheader("Action")

        st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

        for i, row in df.iterrows():
            col1, col2, col3, col4 = st.columns([1, 5, 2, 2])

            with col1:
                st.markdown(
                    f"<p style='text-align: center;'>{row['S no.']}</p>",
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"<p style='font-size: 16px; text-align: left;'>{row['Title']}</p>",
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"<div style='{difficulty_bg_color(row['Difficulty'])}'>{row['Difficulty']}</div>",
                    unsafe_allow_html=True,
                )

            with col4:
                if st.button(f"Solve 💻", key=f"button_{i}"):
                    st.session_state.selected_problem = row.to_dict()
                    clear_and_rewrite_memory_of_navbar(
                        memory_of_select_button, str(st.session_state.selected_problem)
                    )
                    st.rerun()

    else:
        selected = st.session_state.selected_problem
        Coding_Q_ID = selected["ID"]

        try:
            with open(
                r"Static_Files\Practice_Page_Problems\Coding_Problem.json", "r"
            ) as file:
                data = json.load(file)

            problem_title = data["problems"][Coding_Q_ID]["title"]
            problem_problem_description = data["problems"][Coding_Q_ID][
                "Problem_Description"
            ]
            problem_test_cases = data["problems"][Coding_Q_ID]["Test_Cases"]

            Coding_Problems_page(
                problem_problem_description,
                problem_title,
                problem_test_cases,
                Coding_Q_ID,
            )

        except FileNotFoundError:
            st.error("Problem details file not found.")

        if st.button("Go to 🏡Home Page", use_container_width=True):
            st.session_state.selected_problem = None
            clear_and_rewrite_memory_of_navbar(
                memory_of_select_button, str(st.session_state.selected_problem)
            )
            st.rerun()
