import React, { useState, useRef } from "react";
import { IoSendSharp } from "react-icons/io5";
import { FaMicrophone } from "react-icons/fa";
import '../assets/style/chat.css';
import API_BASE_URL from "../config.js";

function Chat() {
  const [socraticMode, setSocraticMode] = useState(false);
  const [userInput, setUserInput] = useState("");
  const [conversation, setConversation] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const handleSendMessage = async () => {
    if (!userInput.trim()) return;

    const newMessage = { speaker: "user", text: userInput };
    const updatedConversation = [...conversation, newMessage];
    setConversation(updatedConversation);

    const requestBody = {
      socraticAI: socraticMode,
      user: userInput,
      conversationHistory: updatedConversation,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/chat/text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      const aiResponse = data.AI || data.ai;

      if (aiResponse) {
        setConversation([...updatedConversation, { speaker: "ai", text: aiResponse }]);
      } else {
        console.error("AI response is missing:", data);
      }
    } catch (error) {
      console.error("Error fetching AI response:", error);
    }

    setUserInput("");
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/mp3" });
        sendVoiceMessage(audioBlob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendVoiceMessage = async (audioBlob) => {
    const convertBlobToBase64 = (blob) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => resolve(reader.result.split(",")[1]);
        reader.onerror = reject;
      });
    };

    try {
      const base64Audio = await convertBlobToBase64(audioBlob);
      const requestBody = {
        socraticAI: socraticMode,
        audioFile: base64Audio,
        conversationHistory: conversation,
      };

      const response = await fetch(`${API_BASE_URL}/chat/voice`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (data.user && data.AI) {
        const newMessages = [
          { speaker: "user", text: data.user },
          { speaker: "ai", text: data.AI }
        ];
        setConversation([...conversation, ...newMessages]);
      } else {
        console.error("Unexpected response format:", data);
      }
    } catch (error) {
      console.error("Error fetching AI voice response:", error);
    }
  };

  return (
    <div className="chat-container">
      <div className="form-check form-switch mb-4">
        <input
          className="form-check-input"
          type="checkbox"
          id="socraticMode"
          checked={socraticMode}
          onChange={() => setSocraticMode(!socraticMode)}
        />
        <label className="form-check-label text-white ms-2" htmlFor="socraticMode">
          Socratic Mode
        </label>
      </div>
      <div className="chat-box">
        {conversation.map((msg, index) => (
          <div key={index} className={`message ${msg.speaker}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input-wrapper mt-4 rounded-3 p-2">
        <div className="input-container">
          <input
            type="text"
            className="chat-input"
            placeholder="Type Here..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
          />
          <IoSendSharp className="send-icon" onClick={handleSendMessage} />
          <div className={`mic-container ${isRecording ? "recording" : ""}`}>
            <FaMicrophone
              className="mic-icon"
              onClick={isRecording ? stopRecording : startRecording}
            />
          </div>
        </div>
      </div>

    </div>
  );
}

export default Chat;