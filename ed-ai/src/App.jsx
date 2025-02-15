import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopNavBar from "./components/topNavBar";
import SideNavBar from "./components/sideNavBar";
import Learn from './components/learn';
import Practice from "./components/practice";
import MockInterview from "./components/mockInterview";
import Chat from "./components/chat";
import ResumeOptimizer from "./components/resumeOptimizer";
import JobTracker from "./components/jobTracker";
import CourseContent from './components/courseContent';
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import InterviewPage from './components/interviewPage'

function App() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Router>
      <div className="container-fluid px-4 py-3">
        <div className="d-flex flex-column">
          <TopNavBar isExpanded={isExpanded} setIsExpanded={setIsExpanded} />
          <div className="d-flex flex-row mt-3">
            <div className="me-3">
              <SideNavBar isExpanded={isExpanded} />
            </div>
            <div className="w-100 main-container p-3">
              <Routes>
                <Route path="/" element={<Learn isExpanded={isExpanded} />} />
                <Route path="/practice" element={<Practice isExpanded={isExpanded}/>} />
                <Route path="/mock-interview" element={<MockInterview />} />
                <Route path="/chat" element={<Chat />} />
                <Route path="/resume-optimizer" element={<ResumeOptimizer />} />
                <Route path="/job-tracker" element={<JobTracker />} />
                <Route path="/course/:courseId" element={<CourseContent />} />
                <Route path="/interview" element={<InterviewPage/>}/>
              </Routes>
            </div>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
