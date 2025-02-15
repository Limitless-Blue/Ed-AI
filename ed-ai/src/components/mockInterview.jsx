import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Modal, Button, Form } from "react-bootstrap";
import "../assets/style/mockInterview.css";
import { IoCloudUploadOutline } from "react-icons/io5";
import API_BASE_URL from "../config.js";

function MockInterview() {
  const [filters, setFilters] = useState({ interviewType: [], level: [], topic: [] });
  const [selected, setSelected] = useState({ 
    interviewType: "", 
    level: "", 
    topic: "", 
    jobDescription: "", 
    mention: "", 
    resume: null 
  });
  const [showResults, setShowResults] = useState(false);
  const [results, setResults] = useState([]);
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API_BASE_URL}/interview/filters`)
      .then((response) => response.json())
      .then((data) => setFilters(data))
      .catch((error) => console.error("Error fetching filters:", error));
  }, []);

  const handleChange = (e) => {
    setSelected({ ...selected, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelected({ ...selected, resume: file });
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelected({ ...selected, resume: file });
    }
  };

  const startInterview = () => {
    const newErrors = {};

    if (!selected.interviewType) newErrors.interviewType = "Interview Type is required.";
    if (!selected.level) newErrors.level = "Level is required.";
    if (!selected.topic) newErrors.topic = "Topic is required.";
    if (!selected.jobDescription) newErrors.jobDescription = "Job Description is required.";
    if (!selected.resume) newErrors.resume = "Resume is required.";

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});

    const interviewData = {
      resumeFile: selected.resume ? selected.resume.name : null,
      InterviewType: selected.interviewType,
      Level: selected.level,
      JobDescriptions: selected.jobDescription,
      Topics: selected.topic ? [selected.topic] : [],
      OthersData: selected.mention || "",
    };

    fetch(`${API_BASE_URL}/interview/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(interviewData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.acknowledgement) {
          navigate("/interview");
        } else {
          setErrors({ general: "Interview could not be started. Please try again." });
        }
      })
      .catch((error) => {
        console.error("Error starting interview:", error);
        setErrors({ general: "Something went wrong. Please try again." });
      });
  };

  return (
    <div className="mock-interview-container p-3">
      <Form className="mock-interview-form">
        <div className="d-flex w-100 justify-content-between gap-4 mb-3">
          <Form.Group className="w-100">
            <Form.Select className="custom-dropdown" name="interviewType" onChange={handleChange}>
              <option value="">Interview Type</option>
              {filters.interviewType.map((type) => (
                <option key={type}>{type}</option>
              ))}
            </Form.Select>
            {errors.interviewType && <p className="error-text">{errors.interviewType}</p>}
          </Form.Group>

          <Form.Group className="w-100">
            <Form.Select className="custom-dropdown" name="level" onChange={handleChange}>
              <option value="">Level</option>
              {filters.level.map((level) => (
                <option key={level}>{level}</option>
              ))}
            </Form.Select>
            {errors.level && <p className="error-text">{errors.level}</p>}
          </Form.Group>
        </div>

        <div className="d-flex w-100 justify-content-between gap-4 mb-3">
          <Form.Group className="w-100">
            <Form.Control
              className="custom-textarea"
              as="textarea"
              name="jobDescription"
              rows={3}
              onChange={handleChange}
              placeholder="Job description..."
            />
            {errors.jobDescription && <p className="error-text">{errors.jobDescription}</p>}
          </Form.Group>

          <div className="d-flex flex-column w-100 gap-2">
            <Form.Group className="w-100 mb-2">
              <Form.Select className="custom-dropdown" name="topic" onChange={handleChange}>
                <option value="">Topic</option>
                {filters.topic.map((topic) => (
                  <option key={topic}>{topic}</option>
                ))}
              </Form.Select>
              {errors.topic && <p className="error-text">{errors.topic}</p>}
            </Form.Group>

            <Form.Group className="w-100">
              <div 
                className="file-drop" 
                onDragOver={handleDragOver} 
                onDrop={handleDrop}
              >
                <IoCloudUploadOutline className="cloud-icon" />
                <span className="mt-3">
                  {selected.resume ? selected.resume.name : "Drag and Drop your Resume"}
                </span>
                <input 
                  type="file" 
                  onChange={handleFileChange} 
                  className="file-input"
                />
                <Button className="upload-btn mt-2" onClick={() => document.querySelector(".file-input").click()}>
                  Upload
                </Button>
              </div>
              {errors.resume && <p className="error-text">{errors.resume}</p>}
            </Form.Group>
          </div>
        </div>

        <Form.Group>
          <Form.Control
            className="custom-textarea"
            as="textarea"
            name="mention"
            rows={6}
            onChange={handleChange}
            placeholder="Anything You Want to Mention? (Optional)"
          />
        </Form.Group>
      </Form>

      <hr className="text-white mt-5 mb-5 opacity-100" />

      <div className="d-flex flex-column gap-4">
        <Button className="start-btn" onClick={startInterview}>
          Let's Start The Interview
        </Button>
        <Button className="results-btn">
          View Previous Results
        </Button>
      </div>

      {errors.general && <p className="error-text">{errors.general}</p>}
    </div>
  );
}

export default MockInterview;