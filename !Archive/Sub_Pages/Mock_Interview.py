import streamlit as st
import streamlit.components.v1 as components
from Gen_Process.UI_Chats.Assistant_Chat import Help_Chat


def Mock_Interview():
    st.markdown(
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
        <h1 class="mentor-title">✨ Mock Interview</h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
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

    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Mock Interview</title>
        <style>
        /* General Dark Theme Styling */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #181818;
            color: #e0e0e0;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height:100vh;
            overflow: hidden;
        }

        /* Centered container for video and controls */
        #container {
            text-align: center;
            width: 80%;
            max-width: 800px;
            padding: 10px;
        }

        /* Style for select dropdowns */
        select {
            margin-bottom: 15px;
            padding: 12px;
            font-size: 16px;
            border-radius: 25px;
            background-color: #282828;
            color: #e0e0e0;
            border: 1px solid #444;
            outline: none;
            width: 80%;
        }

        /* Video container styling */
        #videoContainer {
            width: 100%;
            max-width: 640px;
            height: 360px;
            margin: 0 auto;
            background-color: #202020;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            position: relative;
        }
        #selectContainer {
            display: flex;
            justify-content: center; /* Center horizontally within the container */
            gap: 30px; /* Space between select elements */
            margin-top: 20px; /* Space from other elements */
        }
        select {
            padding: 12px;
            font-size: 12px;
            border-radius: 25px;
            background-color: #282828;
            color: #e0e0e0;
            border: 1px solid #444;
            outline: none;
            width: 300px;
        }
        /* Video styling */
        video {
            width: 100%;
            height: 100%;
            object-fit: cover; /* Ensure video covers the container */
            border-radius: 12px;
        }
        </style>
    </head>
    <body>
        <div id="container">
        <br>
        <div id="videoContainer">
            <video id="video" autoplay muted></video>
        </div>
        <br>
        <div id="selectContainer">
            <select id="audioSource"></select>
            <select id="videoSource"></select>
        </div>
        <p id="status"></p>
        </div>

        <script>
        const video = document.getElementById('video');
        const audioSelect = document.getElementById('audioSource');
        const videoSelect = document.getElementById('videoSource');
        const status = document.getElementById('status');

        navigator.mediaDevices.enumerateDevices()
            .then(deviceInfos => {
            deviceInfos.forEach(deviceInfo => {
                const option = document.createElement('option');
                option.value = deviceInfo.deviceId;
                if (deviceInfo.kind === 'audioinput') {
                option.text = deviceInfo.label || `Microphone ${audioSelect.length + 1}`;
                audioSelect.appendChild(option);
                } else if (deviceInfo.kind === 'videoinput') {
                option.text = deviceInfo.label || `Camera ${videoSelect.length + 1}`;
                videoSelect.appendChild(option);
                }
            });
            })
            .catch(error => {
            console.error('Error listing devices:', error);
            status.textContent = 'Error accessing devices.';
            });

        function getStream() {
            if (window.stream) {
            window.stream.getTracks().forEach(track => track.stop());
            }
            const audioSource = audioSelect.value;
            const videoSource = videoSelect.value;
            const constraints = {
            audio: { deviceId: audioSource ? { exact: audioSource } : undefined },
            video: { deviceId: videoSource ? { exact: videoSource } : undefined }
            };
            navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                window.stream = stream;
                video.srcObject = stream;
            })
            .catch(error => {
                console.error('Error accessing media devices:', error);
                status.textContent = 'Error accessing media devices. Please allow camera and microphone access.';
            });
        }

        audioSelect.onchange = getStream;
        videoSelect.onchange = getStream;

        getStream();
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=600)


Mock_Interview()
