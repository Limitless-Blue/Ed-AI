import { useParams, useLocation } from "react-router-dom";
import { FaBookmark, FaRegBookmark, FaRedoAlt } from "react-icons/fa";
import { IoIosArrowBack } from "react-icons/io";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import Chat from "../components/chat";
import API_BASE_URL from "../config.js";
import { FiCheckCircle } from "react-icons/fi";
import { GrNext  } from "react-icons/gr";
import "../assets/style/courseContent.css";

function CourseContent() {
  const { courseId } = useParams();
  const location = useLocation();
  const courseName = location.state?.courseName || "Unknown Course";
  const [selectedTab, setSelectedTab] = useState("material");
  const [markdownContent, setMarkdownContent] = useState("## Course Content Loading...");
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    async function fetchCourseContent() {
      try {
        const response = await fetch(`${API_BASE_URL}/learn/course/${courseId}`);
        const data = await response.json();

        if (data) {
          setMarkdownContent(data.content || "## No Content Available");
          setIsBookmarked(data.bookmark || false);
          setIsCompleted(data.completed || false);
        }
      } catch (error) {
        console.error("Error fetching course content:", error);
      }
    }

    fetchCourseContent();
  }, []);

  const handleBookmarkClick = async () => {
    try {
      const newBookmarkState = !isBookmarked;
      const response = await fetch(`${API_BASE_URL}/common/save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: courseId, value: newBookmarkState }),
      });

      if (response.ok) {
        setIsBookmarked(newBookmarkState);
      } else {
        console.error("Failed to update bookmark");
      }
    } catch (error) {
      console.error("Error updating bookmark:", error);
    }
  };

  return (
    <div className="course-content">
      <div className="course-header">
        <div className="d-flex gap-4">
          <IoIosArrowBack className="back-icon" />
          <h1>{`${courseName}`}</h1>
        </div>
        <div className="header-icons">
          {isBookmarked ? (
            <FaBookmark className="icon" onClick={handleBookmarkClick} />
          ) : (
            <FaRegBookmark className="icon" onClick={handleBookmarkClick} />
          )}
          {isCompleted ? (
            <FiCheckCircle className="completed" />
          ) : (
            <FiCheckCircle className="not-completed" />
          )}
          <button className="next-btn">
            <span className="me-3">Next</span>
            <span className="icon-container">
              <GrNext className="mt-2" />
            </span>
          </button>
        </div>
      </div>
      <div className="tabs">
        <button className={selectedTab === "material" ? "active" : ""} onClick={() => setSelectedTab("material")}>
          Material
        </button>
        <button className={selectedTab === "mentor" ? "active" : ""} onClick={() => setSelectedTab("mentor")}>
          Mentor Help
        </button>
      </div>
      <div className="content-area">
        {selectedTab === "material" ? (
          <div className="markdown-viewer">
            <ReactMarkdown>{markdownContent}</ReactMarkdown>
          </div>
        ) : (
          <div className="chat-wrapper">
            <Chat />
          </div>

        )}
      </div>
    </div>
  );
}

export default CourseContent;