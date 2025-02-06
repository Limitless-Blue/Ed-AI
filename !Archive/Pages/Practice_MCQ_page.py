import os
import json
import base64
import mimetypes
import streamlit as st
from urllib.parse import urlencode
from Sub_Pages.Practice_MCQ import Practice_MCQ
from Gen_Process.UI_Chats.Assistant_Chat import Help_Chat


def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def show_details(selected_image):
    Tests_Question_json_file_path = (
        r"Static_Files\Practice_Page\Redirecting_MCQ_test.json"
    )
    with open(Tests_Question_json_file_path, "r") as file:
        data = json.load(file)

    MCQ_test_file_value = data[selected_image]["Test_file"]
    Practice_MCQ(rf"{MCQ_test_file_value}", selected_image)
    return


def Practice_MCQ_page():
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
    directory_Featured = r"Static_Files\Practice_Page\Featured"
    directory_All_Courses = r"Static_Files\Practice_Page\All_Courses"
    directory_Recommendation = (
        r"dynamic files\Main_pages\Recommendations\Practice_MCQ_page_recommendation"
    )

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
                    f"margin-right: {margin_right}px;" if i < len(filenames) - 1 else ""
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
            width: {2 * total_width}px;
            animation: scroll 50s linear infinite;
            transition: transform 0.5s ease;
        }}

        .scroll-content img {{
            width: {image_width}px;
            height: {image_height}px;
            object-fit: cover;
            border-radius: 3px;
            flex-shrink: 0;
            transition: transform 0.4s ease, border-radius 1s ease;
        }}

        .scroll-container:hover .scroll-content {{
            animation-play-state: paused;
        }}

        .scroll-content img:hover {{
            transform: scale(0.9);
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
                    f"margin-right: {margin_right}px;" if i < len(filenames) - 1 else ""
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

        .scroll-container-static::-webkit-scrollbar {{
            height: 8px;
        }}

        .scroll-container-static::-webkit-scrollbar-track {{
            background: #333;
            border-radius: 20px;
        }}

        .scroll-container-static::-webkit-scrollbar-thumb {{
            background: #555;
            border-radius: 10px;
            border: 2px solid #333;
        }}

        .scroll-container-static::-webkit-scrollbar-thumb:hover {{
            background: #888; 
        }}

        .scroll-container-static {{
            scrollbar-width: thin;
            scrollbar-color: #555 #333;
            border-radius: 10px;
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

    st.title("All Courses")

    if os.path.exists(directory_All_Courses):
        image_width = 480
        image_height = 230
        margin_right = 10

        image_tags = ""
        filenames = sorted(os.listdir(directory_All_Courses))
        for i, filename in enumerate(filenames):
            file_path = os.path.join(directory_All_Courses, filename)
            if os.path.isfile(file_path):
                encoded_image = load_image_as_base64(file_path)
                mime_type = get_mime_type(filename)
                margin_style = (
                    f"margin-right: {margin_right}px;" if i < len(filenames) - 1 else ""
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
            transition: transform 0.4s ease, box-shadow 0.4s ease, filter 0.4s ease, border-radius 1s ease;
        }}

        .scroll-content-static img:hover {{
            transform: scale(0.93);
            box-shadow: 0px 8px 30px rgba(255, 255, 255, 0.2),
                        0px 4px 15px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(10px);
            filter: brightness(1.1);
            border-radius: 12px;
        }}

        .scroll-container-static::-webkit-scrollbar {{
            height: 8px;
        }}

        .scroll-container-static::-webkit-scrollbar-track {{
            background: #333;
            border-radius: 20px;
        }}

        .scroll-container-static::-webkit-scrollbar-thumb {{
            background: #555;
            border-radius: 10px;
            border: 2px solid #333;
        }}

        .scroll-container-static::-webkit-scrollbar-thumb:hover {{
            background: #888;
        }}

        .scroll-container-static {{
            scrollbar-width: thin;
            scrollbar-color: #555 #333;
            border-radius: 10px;
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
        st.error(f"Directory not found: {directory_All_Courses}")
