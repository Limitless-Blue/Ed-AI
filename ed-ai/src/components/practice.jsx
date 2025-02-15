import React, { useEffect, useState } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import { FaFilter } from 'react-icons/fa';
import '../assets/style/coursePages.css';
import API_BASE_URL from "../config.js";
import { FiCheckCircle } from "react-icons/fi";

function Practice({ isExpanded }) {
  const [recommendations, setRecommendations] = useState([]);
  const [filters, setFilters] = useState({ level: [], topic: [], status: [] });
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFilters, setSelectedFilters] = useState({
    type: 'MCQs', 
    level: '',
    topic: '',
    status: '',
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const recRes = await fetch(`${API_BASE_URL}/practice/recommendations`);
        const recData = await recRes.json();
        
        if (selectedFilters.type === 'MCQs') {
          setRecommendations(recData.mcqRecommendations || []);
          setFilters(recData.filters.mcqs || {});
        } else {
          setRecommendations(recData.codingRecommendations || []);
          setFilters(recData.filters.codingQuestions || {});
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
      query.append("type", selectedFilters.type);
      if (selectedFilters.level) query.append("level", selectedFilters.level);
      if (selectedFilters.topic) query.append("topic", selectedFilters.topic);
      if (selectedFilters.status) query.append("status", selectedFilters.status);

      const coursesRes = await fetch(`${API_BASE_URL}/practice/items?${query.toString()}`);
      const coursesData = await coursesRes.json();
      
      setCourses(Array.isArray(coursesData) ? coursesData : []);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  }

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
          className="recommendations-carousel"
        >
          {recommendations.map((rec) => (
            <SwiperSlide key={rec.id} className="recommendation-slide">
              <div className="recommendation-card">
                <img
                  src={`../src/assets/images/ED AI Static Image Data/THumbnail of materials/Practice Page/${selectedFilters.type}/Recommendations/${rec.id}.png`}
                  alt={rec.practiceName}
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
            value={selectedFilters.type}
            onChange={(e) => setSelectedFilters({ ...selectedFilters, type: e.target.value })}
          >
            <option value="MCQs">MCQs</option>
            <option value="Coding problems">Coding Problems</option>
          </select>
        </div>

        <div className="filter-item w-25">
          <select
            value={selectedFilters.level}
            onChange={(e) => setSelectedFilters({ ...selectedFilters, level: e.target.value })}
          >
            <option value="">Level</option>
            {filters.level?.map((lvl) => (
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
            {filters.topic?.map((top) => (
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

      {selectedFilters.type === 'MCQs' ? (
        <div className="courses-container mt-2">
          {courses.length === 0 ? <p>No courses found</p> : courses.map((course) => (
            <div key={course.id} className="course-card">
              <img
                src={`../src/assets/images/ED AI Static Image Data/THumbnail of materials/Practice Page/${selectedFilters.type}/All Display/${course.id}.png`}
                alt={course.practiceName}
              />
            </div>
          ))}
        </div>
      ) : (
        <div className="coding-container mt-2">
      {courses.length === 0 ? (
        <p>No coding exercises found</p>
      ) : (
        <table className="coding-table">
          <thead>
            <tr>
              <th>Status</th>
              <th>S. No</th>
              <th>Title</th>
              <th>Difficulty</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((course, index) => (
              <tr key={course.id}>
                <td className="status-icon">
                  {course.status ? (
                    <FiCheckCircle className="completed" />
                  ) : (
                    <FiCheckCircle className="not-completed" />
                  )}
                </td>

                <td>{index + 1}</td>
                <td>{course.practiceName}</td>
                <td>
                  <span className={`difficulty ${course.difficulty.toLowerCase()}`}>
                    {course.difficulty}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
      )}
    </div>
  );
}

export default Practice;