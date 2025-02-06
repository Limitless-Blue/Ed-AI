import streamlit as st
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from UI_Components.Ed_AI_tittle import Ed_AI_tittle

load_dotenv()
client_secrets_file = "Login_Secret.json"


def SignUp():
    flow = Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
        redirect_uri="http://localhost:8501",
    )

    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: #e0e0e0;
        }
        .stButton button {
            background-color: #333;
            color: #fff;
            border: 1px solid #141414;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .stButton button:hover {
            background-color: #050505;
            transform: scale(1.05);
        }
        .stTextInput input {
            background-color: #141414;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 10px;
        }
        .stTextInput input:focus {
            border-color: #777;
        }
        .stMarkdown {
            text-align: center;
        }
        .SignUp-container {
            max-width: 500px;
            margin: 0 auto;
        }

        </style>
    """,
        unsafe_allow_html=True,
    )

    if "SignUp_status" not in st.session_state:
        st.session_state["SignUp_status"] = False

    if not st.session_state["SignUp_status"]:
        col1, col2 = st.columns([1, 1])
        with col1:
            auth_url, _ = flow.authorization_url()

            st.markdown("<div class='SignUp-container'>", unsafe_allow_html=True)

            username = st.text_input("Username", key="signup_username")
            password = st.text_input("Password", type="password", key="signup_password")
            re_password = st.text_input(
                "Confirm Password", type="password", key="signup_re_password"
            )

            if st.button("SignUp", use_container_width=True):
                if (password == re_password) and (username == "1" and password == "1"):
                    st.success("SignUp successful!")
                    st.session_state["SignUp_status"] = True
                    st.rerun()
                else:
                    st.error("Enter Proper Username / Password.")

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="button-container">
                    <a href="{auth_url}" style="
                        display: inline-block;
                        background-color: red;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        font-size: 16px;
                        cursor: pointer;
                        border-radius: 50px;
                        width: 100%; /* Adjust to full width of the column */
                        max-width: 100%; /* Ensure it doesn't overflow */
                        box-sizing: border-box; /* Include padding in width calculation */
                    ">Continue with Google</a>
                    <br><br>
                </div>
            """,
                unsafe_allow_html=True,
            )

            query_params = st.query_params
            if "code" in query_params:
                code = query_params["code"]
                try:
                    flow.fetch_token(code=code)
                    credentials = flow.credentials
                    request = google.auth.transport.requests.Request()
                    id_info = credentials.id_token

                    if id_info:
                        st.session_state["SignUp_status"] = True
                        st.rerun()
                except Exception as e:
                    st.error(f"Error during SignUp: {e}")
                    st.write(
                        "Ensure that the redirect URI matches the one configured in Google Cloud Console and that the authorization code is valid."
                    )

            if st.button(
                "Already Have an Account?",
                key="signup_create_account",
                use_container_width=True,
                help="Click to create a new account",
            ):
                st.write("Login now")
        with col2:
            Ed_AI_tittle()
    else:
        st.title("Its time for test")
