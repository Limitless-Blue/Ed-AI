import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import { FaFilter } from 'react-icons/fa';
import '../assets/style/coursePages.css';
import API_BASE_URL from "../config.js";

function Learn({ isExpanded }) {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);
  const [filters, setFilters] = useState({ level: [], topic: [], status: [] });
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFilters, setSelectedFilters] = useState({
    level: '',
    topic: '',
    status: '',
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const recRes = await fetch(`${API_BASE_URL}/learn/recommendations`);
        const recData = await recRes.json();
        setRecommendations(Array.isArray(recData.recommendations) ? recData.recommendations : []);

        if (recData.filters) {
          setFilters(recData.filters);
        }

        fetchCourses();
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [selectedFilters]);

  async function fetchCourses() {
    try {
      let query = new URLSearchParams();
      if (selectedFilters.level) query.append("level", selectedFilters.level);
      if (selectedFilters.topic) query.append("topic", selectedFilters.topic);
      if (selectedFilters.status) query.append("status", selectedFilters.status);

      const coursesRes = await fetch(`${API_BASE_URL}/learn/courses?${query.toString()}`);
      const coursesData = await coursesRes.json();
      setCourses(Array.isArray(coursesData) ? coursesData : []);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  }

  const handleCourseClick = (courseId, courseName) => {
    navigate(`/course/${courseId}`, { state: { courseName } });
  };

  if (loading) return <p className="loading-text">Loading...</p>;

  return (
    <div>
      <div className={`learn-container ${isExpanded ? "expanded" : "collapsed"}`}>
        <Swiper
          modules={[Pagination]}
          pagination={{ clickable: true }}
          slidesPerView={3}
          spaceBetween={20}
          loop={false}
          centeredSlides={false}
          className="recommendations-carousel"
        >
          {recommendations.map((rec) => (
            <SwiperSlide key={rec.id} className="recommendation-slide">
              <div className="recommendation-card" onClick={() => handleCourseClick(rec.id, rec.courseName)} style={{ cursor: 'pointer' }}>
                <img
                  src={`../src/assets/images/ED AI Static Image Data/THumbnail of materials/Learn Page/Recommendations/${rec.id}.png`}
                  alt={rec.courseName}
                  className="rounded-3"
                />
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>

      <div className="filters-container">
        <div className="filter-item w-25">
          <select
            value={selectedFilters.level}
            onChange={(e) => setSelectedFilters({ ...selectedFilters, level: e.target.value })}
          >
            <option value="">Level</option>
            {filters.level.map((lvl) => (
              <option key={lvl} value={lvl}>{lvl}</option>
            ))}
          </select>
        </div>

        <div className="filter-item w-50">
          <FaFilter className="filter-icon mt-1" />
          <select
            value={selectedFilters.topic}
            onChange={(e) => setSelectedFilters({ ...selectedFilters, topic: e.target.value })}
          >
            <option value="">Topics</option>
            {filters.topic.map((top) => (
              <option key={top} value={top}>{top}</option>
            ))}
          </select>
        </div>

        <div className="filter-item w-25">
          <select
            value={selectedFilters.status}
            onChange={(e) => setSelectedFilters({ ...selectedFilters, status: e.target.value })}
          >
            <option value="">Status</option>
            <option value="true">Completed</option>
            <option value="false">Not Completed</option>
          </select>
        </div>
      </div>

      <div className="courses-container">
        {courses.length === 0 ? <p>No courses found</p> : courses.map((course) => (
          <div key={course.id} className="course-card" onClick={() => handleCourseClick(course.id, course.courseName)} style={{ cursor: 'pointer' }}>
            <img
              src={`../src/assets/images/ED AI Static Image Data/THumbnail of materials/Learn Page/All Display/${course.id}.png`}
              alt={course.courseName}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default Learn;