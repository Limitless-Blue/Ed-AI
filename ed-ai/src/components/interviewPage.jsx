import React, { useEffect, useState, useRef } from "react";
import { Modal, Button } from "react-bootstrap";
import { FaMicrophone } from "react-icons/fa";
import "../assets/style/interviewPage.css";
import API_BASE_URL from "../config.js";
import { useNavigate } from "react-router-dom";
import { CiHome } from "react-icons/ci";

function InterviewPage() {
    const videoRef = useRef(null);
    const chatBoxRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const hasFetchedInitial = useRef(false);
    const [chatMessages, setChatMessages] = useState([]);
    const [recording, setRecording] = useState(false);
    const [error, setError] = useState("");
    const [showResults, setShowResults] = useState(false);
    const [interviewResults, setInterviewResults] = useState(null);
    const [stream, setStream] = useState(null);
    const [aiSpeaking, setAiSpeaking] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        startCamera();
        if (!hasFetchedInitial.current) {
            sendInitialRequest();
            hasFetchedInitial.current = true;
        }
    }, []);

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [chatMessages]);

    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true,
            });
            setStream(mediaStream);
            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream;
            }
        } catch (err) {
            setError("Failed to access camera. Please allow camera permissions.");
            console.error("Camera Error:", err);
        }
    };

    const sendInitialRequest = async () => {
        const requestBody = {
            audioFile: "",
            conversationHistory: [],
        };

        try {
            const response = await fetch(`${API_BASE_URL}/interview/voice-chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestBody),
            });

            const data = await response.json();

            if (data.responseAudio) {
                playAudio(data.responseAudio);
            }

            setChatMessages([
                { speaker: "ai", text: data.AI || data.ai }
            ]);
        } catch (error) {
            console.error("Error starting interview:", error);
        }
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
                const reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = () => {
                    const base64Audio = reader.result.split(",")[1];
                    sendAudioToAPI(base64Audio);
                };
            };

            mediaRecorderRef.current.start();
            setRecording(true);
        } catch (error) {
            console.error("Recording error:", error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            setRecording(false);
        }
    };

    const sendAudioToAPI = async (audioBase64) => {
        const requestBody = {
            audioFile: audioBase64,
            conversationHistory: chatMessages,
        };

        try {
            const response = await fetch(`${API_BASE_URL}/interview/voice-chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestBody),
            });

            const data = await response.json();

            if (data.responseAudio) {
                playAudio(data.responseAudio);
            }

            setChatMessages([...chatMessages, { speaker: "user", text: data.user }, { speaker: "ai", text: data.AI || data.ai }]);
        } catch (error) {
            console.error("Error communicating with AI:", error);
        }
    };

    const playAudio = (base64Audio) => {
        const audio = new Audio(`data:audio/mp3;base64,${base64Audio}`);

        setAiSpeaking(true);

        audio.onended = () => {
            setAiSpeaking(true);
        };

        audio.play();
    };


    const endInterview = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/interview/end`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ conversationHistory: chatMessages }),
            });

            const data = await response.json();
            setInterviewResults(data);
            setShowResults(true);
        } catch (error) {
            console.error("Error ending interview:", error);
        }
    };

    return (
        <div className="interview-container">
            <div className="d-flex gap-4">
                <div className="video-section">
                    {error ? <p className="error-text">{error}</p> : <video ref={videoRef} autoPlay playsInline className="video-feed"></video>}
                    <div className="controls">
                        <select className="dropdown">
                            <option>Microphone</option>
                        </select>
                        <select className="dropdown">
                            <option>Camera</option>
                        </select>
                        <button className={`mic-btn ${recording ? "recording" : ""}`} onClick={recording ? stopRecording : startRecording}>
                            <FaMicrophone />
                        </button>
                    </div>
                </div>
                <div className="chat-section">
                    <div className="chat-window" ref={chatBoxRef}>
                        {chatMessages.map((msg, index) => (
                            <div key={index} className={`message ${msg.speaker === "user" ? "user-msg" : "bot-msg"}`}>
                                {msg.text}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <div className="ai-speaking-animation-container">
                {aiSpeaking && <div className="ai-speaking-animation"></div>}
            </div>
            <button className="end-btn" onClick={endInterview}>End Interview</button>

            <Modal show={showResults} onHide={() => setShowResults(false)} centered>
                <Modal.Header>
                    <Modal.Title>Result of Interview</Modal.Title>
                    <div className="home-btn" onClick={() => navigate("/learn")}>
                        <span className="me-3">Go to Home</span>
                        <div className="home-icon">
                            <CiHome />
                        </div>
                    </div>
                </Modal.Header>
                <Modal.Body>
                    {interviewResults ? (
                        <div className="results-container">
                            <div className="performance-box">
                                <p className="performance-text">{interviewResults.result}</p>
                            </div>
                            <h5 className="review-heading">Review of Performance</h5>
                            <div className="review-box">
                                <p>{interviewResults.review} sssssssssssss sssssssssss ssssssssssss ssssssssssssssssssssssssssssssssssss sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss</p>
                            </div>
                        </div>
                    ) : (
                        <p>Loading results...</p>
                    )}
                </Modal.Body>
            </Modal>
        </div>
    );
}

export default InterviewPage;