import React, { useState, useEffect, useRef } from 'react';
import { NavLink } from 'react-router-dom';
function SideNavBar({ isExpanded }) {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const userMenuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className='position-relative'>
      <div className={`nav-links ${isExpanded ? 'expanded' : ''}`}>
        <NavLink to="/" className="nav-item">
          <img src="../src/assets/images/learn-icon.svg" alt="Learn" />
          {isExpanded && <span>Learn</span>}
        </NavLink>
        <NavLink to="/practice" className="nav-item">
          <img src="../src/assets/images/book.svg" alt="Practice" />
          {isExpanded && <span>Practice</span>}
        </NavLink>
        <hr className="text-white custom-hr" />
        <NavLink to="/mock-interview" className="nav-item">
          <img src="../src/assets/images/interview-icon.svg" alt="Interview" />
          {isExpanded && <span>Mock Interview</span>}
        </NavLink>
        <NavLink to="/chat" className="nav-item">
          <img src="../src/assets/images/chat-icon.svg" alt="Chat" />
          {isExpanded && <span>Chat</span>}
        </NavLink>
        <hr className="text-white custom-hr" />
        <NavLink to="/resume-optimizer" className="nav-item">
          <img src="../src/assets/images/file-icon.svg" alt="Resume Optimizer" />
          {isExpanded && <span>Resume Optimizer</span>}
        </NavLink>
        <NavLink to="job-tracker" className="nav-item">
          <img src="../src/assets/images/job-tracker.svg" alt="Job Tracker" />
          {isExpanded && <span>Job Tracker</span>}
        </NavLink>
        <div className='bg-black rounded-4 user-profile p-2' onClick={() => setShowUserMenu(!showUserMenu)}>
          <img className={`rounded-1 ${isExpanded ? 'w-25' : 'w-100'}`} src="../src/assets/images/user.png" alt="user" />
          {isExpanded && <span>Name Name</span>}
        </div>
      </div>
      {showUserMenu && (
        <div className="user-menu" ref={userMenuRef}>
          <div className="d-flex align-items-center bg-secondary p-3">
            <img className="user-img" src="../src/assets/images/user.png" alt="User" />
            <span className="user-name">Name Name</span>
          </div>
          <div className="utility-menu">
            <div className='utility-item'>
              <img src="../src/assets/images/bookmark-icon.svg" alt="Saved List" />
            </div>
           <div className='utility-item'>
              <img src="../src/assets/images/settings-icon.svg" alt="Setiings" />
           </div>
          </div>
          <div>
            <div className="menu-item mx-3 my-2 rounded">
              <span>Contact/Bug Report</span>
              <img src="../src/assets/images/bug-icon.svg" alt="Job Tracker" />
            </div>
            <div className="menu-item mx-3 my-2 rounded">
              <span>Donate</span>
              <img src="../src/assets/images/heart-icon.svg" alt="Job Tracker" />
            </div>
            <div className="menu-item mx-3 my-2 rounded">
              <span>Log out</span>
              <img src="../src/assets/images/logout-icon.svg" alt="Job Tracker" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SideNavBar;