import React, { useState } from "react";
import { Form, Button, Modal, Spinner } from "react-bootstrap";
import API_BASE_URL from "../config.js";
import { useNavigate } from "react-router-dom";
import "../assets/style/resumeOptimizer.css";
import { FaRedo } from "react-icons/fa";
import { IoSendSharp } from "react-icons/io5";
import { FiCopy } from "react-icons/fi";

function ResumeOptimizer() {
  const navigate = useNavigate();
  const [jobDescription, setJobDescription] = useState("");
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);
  const [showGenerationModal, setShowGenerationModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [coverLetter, setCoverLetter] = useState(null);
  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [updating, setUpdating] = useState(false);

  const analyzeJobMatch = async () => {
    if (!jobDescription.trim()) return alert("Please enter a job description.");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/resume/analysis`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobDescription }),
      });
      const data = await response.json();
      setAnalysisData(data);
      setShowAnalysisModal(true);
    } catch (error) {
      alert("Error fetching analysis. Please try again.");
      console.error(error);
    }

    setLoading(false);
  };

  const getMatchColor = (match) => {
    switch (match.toLowerCase()) {
      case "good":
        return "#0ec10e";
      case "average":
        return "orange";
      case "medium":
        return "red";
      default:
        return "gray";
    }
  };

  const generateCoverLetter = async () => {
    if (!jobDescription.trim()) return alert("Please enter a job description.");
  
    setLoading(true);
    setCoverLetter(null);
    setShowGenerationModal(true);
  
    try {
      const response = await fetch(`${API_BASE_URL}/resume/generate-cover-letter`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobDescription }),
      });
      const data = await response.json();
      setCoverLetter(data.coverLetter);
      setChatHistory([{ sender: "bot", message: data.coverLetter }]);
  
    } catch (error) {
      alert("Error generating cover letter. Please try again.");
      console.error(error);
    }
  
    setLoading(false);
  };

  const handleChatSubmit = async () => {
    if (!chatMessage.trim()) return;
    setUpdating(true);

    const newChatEntry = { sender: "user", message: chatMessage };
    setChatHistory((prevHistory) => [...prevHistory, newChatEntry]);

    try {
      const response = await fetch(`${API_BASE_URL}/resume/cover-letter-chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          jobDescription,
          coverLetter: "cover_letter.txt",
          userMessage: chatMessage,
        }),
      });

      const data = await response.json();
      setCoverLetter(data.coverLetter);
      const botReply = { sender: "bot", message: data.coverLetter };
      setChatHistory((prevHistory) => [...prevHistory, botReply]);

      setChatMessage("");
    } catch (error) {
      alert("Error updating cover letter.");
      console.error(error);
    }

    setUpdating(false);
  };

  return (
    <div>
      <div className="p-4">
        <Form.Control
          as="textarea"
          rows={16}
          placeholder="Enter Job Description you are interested in here..."
          className="job-textarea rounded-4"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />
      </div>

      <div className="buttons-container d-flex flex-column align-items-center gap-3 ps-4 pe-4">
        <Button className="btn-lg btn-custom w-100" onClick={analyzeJobMatch} disabled={loading}>
          {loading ? <Spinner animation="border" size="sm" /> : "Analyze the Job Match"}
        </Button>
        <Button className="btn-lg btn-custom w-100" onClick={generateCoverLetter}>
          Generate Cover Letter
        </Button>
      </div>

      <Modal show={showAnalysisModal} onHide={() => setShowAnalysisModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Job Match Analysis</Modal.Title>
        </Modal.Header>
        <Modal.Body className="bg-dark text-white">
          {analysisData ? (
            <div className="d-flex flex-column">
              <div className="d-flex justify-content-between gap-3">
                <div className="text-center w-50">
                  <div className="match-circle" style={{ backgroundColor: getMatchColor(analysisData.match) }}>{analysisData.match}</div>
                  <Button className="mt-3 w-100 mockInterview-btn" onClick={() => navigate("/mock-interview")}>
                    Mock Interview
                  </Button>
                </div>
                <div className="w-100">
                  <h5 className="heading-text">Skill Gap Analysis</h5>
                  <div className="analysis-box">{analysisData.skillGapAnalysis}</div>
                </div>
              </div>
              <div className="mt-3 w-100">
                <h5 className="heading-text">Salary Insights</h5>
                <div className="analysis-box">{analysisData.salaryInsights}</div>
              </div>
            </div>
          ) : (
            <Spinner animation="border" />
          )}
        </Modal.Body>
      </Modal>

      <Modal show={showGenerationModal} onHide={() => setShowGenerationModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Cover Letter Chat</Modal.Title>
        </Modal.Header>
        <Modal.Body className="bg-dark text-white position-relative">
          <div className="chat-history-container">
            {chatHistory.map((chat, index) => (
              chat.sender === "user" ? (
                <div key={index} className="chat-message user">{chat.message}</div>
              ) : (
                <div key={index} className="cover-letter-container">
                  <pre className="cover-letter-text">{chat.message}</pre>
                  <button
                    className="copy-btn"
                    onClick={() => navigator.clipboard.writeText(chat.message)}
                    title="Copy to Clipboard"
                  >
                    <FiCopy />
                  </button>
                </div>
              )
            ))}
          </div>
          <div className="d-flex">
            <div className="chat-box">
              <input
                type="text"
                placeholder="Chat here about modifications in Cover Letter..."
                className="chat-input"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleChatSubmit()}
              />
              <IoSendSharp className="send-btn" onClick={handleChatSubmit} disabled={updating} />
            </div>
            <button
              className="regenerate-btn pt-4 m-3"
              onClick={generateCoverLetter}
              title="Re-generate Cover Letter"
              disabled={updating}
            >
              {updating ? <Spinner animation="border" size="sm" /> : <FaRedo />}
            </button>
          </div>
        </Modal.Body>
      </Modal>
    </div>
  );
}

export default ResumeOptimizer;