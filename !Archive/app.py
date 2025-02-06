import streamlit as st
from dotenv import load_dotenv

# from Pre_Pages.login_page import login
from UI_Components.navbar import navbar

load_dotenv()

st.set_page_config(
    page_title="Ed AI", page_icon="✨", layout="wide", initial_sidebar_state="collapsed"
)


def main():
    navbar()


if __name__ == "__main__":
    main()
