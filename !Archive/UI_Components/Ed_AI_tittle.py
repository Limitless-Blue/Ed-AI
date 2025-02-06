import streamlit as st


def Ed_AI_tittle():
    css = """
  <style>
  @keyframes fadeIn {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
  }

  @keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
  }

  @keyframes rotate3D {
    0% { transform: rotateX(0) rotateY(0); }
    100% { transform: rotateX(360deg) rotateY(360deg); }
  }

  .fancy-text {
    font-size: 72px;
    font-weight: bold;
    color: transparent;
    background: linear-gradient(90deg, #FFF5EE, #F3CFC6, #f9bec7, #ffafcc, #f72585, #b5179e, #7209b7, #560bad, #480ca8, #3a0ca3, #3f37c9, #4361ee, #4895ef, #4cc9f0, #caf0f8, #FFF5EE, #FFF5EE, #caf0f8, #4cc9f0, #4895ef, #4361ee, #3f37c9, #3a0ca3, #480ca8, #560bad, #7209b7, #b5179e, #f72585, #ffafcc, #f9bec7, #F3CFC6, #FFF5EE);
    background-clip: text;
    -webkit-background-clip: text;
    animation: fadeIn 2s ease-out, gradientFlow 5s linear infinite;
    background-size: 400% 400%;
    text-shadow: none; /* Remove text shadow for flat appearance */
    position: relative;
    z-index: 1;
  }

  .ring-container {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 300px;
    height: 300px;
    transform-style: preserve-3d;
    animation: rotate3D 10s linear infinite;
    z-index: 0;
    margin-left: -150px; /* Center the container horizontally */
    margin-top: -150px; /* Center the container vertically */
  }

  .ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
    transform-origin: center;
  }

  .ring:nth-child(1) { transform: rotateX(0deg) translateZ(150px); }
  .ring:nth-child(2) { transform: rotateX(120deg) translateZ(150px); }
  .ring:nth-child(3) { transform: rotateX(240deg) translateZ(150px); }
  </style>
  """

    st.markdown(css, unsafe_allow_html=True)

    st.markdown(
        """
  <div style="position: relative; width: 100%; height: 60vh; display: flex; align-items: center; justify-content: center;">
      <div class="ring-container">
          <div class="ring"></div>
          <div class="ring"></div>
          <div class="ring"></div>
      </div>
      <div class="fancy-text">✨ Ed AI</div>
  </div>
  """,
        unsafe_allow_html=True,
    )
