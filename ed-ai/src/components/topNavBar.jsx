import React, { useState, useRef, useEffect } from 'react';
import { Search, Flame } from "lucide-react";

function TopNavBar({ isExpanded, setIsExpanded }) {
    const [showStreak, setShowStreak] = useState(false);
    const streakRef = useRef(null);

    const currentDate = new Date();
    const totalDays = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
    const streakCount = 14; 

    useEffect(() => {
        function handleClickOutside(event) {
            if (streakRef.current && !streakRef.current.contains(event.target)) {
                setShowStreak(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);
    return (
        <div className='d-flex align-items-center rounded-4'>
            <div>
                <div className="expand me-3" onClick={() => setIsExpanded(!isExpanded)}>
                    <img src="../src/assets/images/Expand_left.svg" alt="expand" />
                </div>
            </div>
            <div className="topNav rounded-sm w-100">
                <div>
                    <img
                        src="../src/assets/images/ED AI.png"
                        alt="Logo"
                        className="logo"
                    />
                </div>
                <div className="search w-50 max-w-2xl">
                    <input
                        type="text"
                        placeholder="search"
                        className="w-100 pl-5 pr-12 bg-gray-200 text-gray-700 border border-gray-300 outline-none text-center p-2"
                    />
                    <Search className="search-icon" />
                </div>
                <div className='bg-black rounded-4'>
                    <Flame className="ms-4 me-4 mt-3 text-white" onClick={() => setShowStreak(!showStreak)} style={{ cursor: 'pointer' }} />
                </div>
            </div>

            {showStreak && (
                <div ref={streakRef} className="streak-tracker position-absolute">
                    <p className="streak-text">
                        Streak: <span className="text-success">{streakCount}</span>
                    </p>
                    <div className="streak-grid">
                        {Array.from({ length: totalDays }).map((_, index) => (
                            <div key={index} className={`streak-circle ${index < streakCount ? "active" : ""}`}>
                                <Flame size={16} />
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default TopNavBar
