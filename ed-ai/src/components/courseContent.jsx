import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import API_BASE_URL from "../config.js";

function CourseContent() {
  const { courseId } = useParams();
  const [courseData, setCourseData] = useState(null);
  const [selectedTab, setSelectedTab] = useState('material');
  const [markdownContent, setMarkdownContent] = useState('');

  useEffect(() => {
    async function fetchCourseDetails() {
      try {
        const response = await fetch(`${API_BASE_URL}/learn/course/${courseId}`);
        const data = await response.json();
        setCourseData(data);

        if (data.course.length > 0) {
          fetchMarkdown(data.course[0]);
        }
      } catch (error) {
        console.error('Error fetching course details:', error);
      }
    }

    fetchCourseDetails();
  }, [courseId]);

  async function fetchMarkdown(filePath) {
    try {
      const response = await fetch(`${API_BASE_URL}/${filePath}`);
      const text = await response.text();
      setMarkdownContent(text);
    } catch (error) {
      console.error('Error fetching markdown:', error);
    }
  }

  if (!courseData) return <p>Loading course details...</p>;

  return (
    <div className="course-content">
      <h1>{`Course ${courseId}`}</h1>

      <div className="course-status">
        <span>{courseData.bookmark ? '🔖 Bookmarked' : '📌 Not Bookmarked'}</span>
        <span>{courseData.completed ? '✅ Completed' : '⏳ In Progress'}</span>
      </div>

      <div className="tabs">
        <button className={selectedTab === 'material' ? 'active' : ''} onClick={() => setSelectedTab('material')}>
          Material
        </button>
        <button className={selectedTab === 'test' ? 'active' : ''} onClick={() => setSelectedTab('test')}>
          Test
        </button>
      </div>

      {selectedTab === 'material' && (
        <div className="material-content">
          <h2>Course Material</h2>
          <select onChange={(e) => fetchMarkdown(e.target.value)}>
            {courseData.course.map((file, index) => (
              <option key={index} value={file}>{`Material ${index + 1}`}</option>
            ))}
          </select>
          <div className="markdown-viewer">
            <ReactMarkdown>{markdownContent}</ReactMarkdown>
          </div>
        </div>
      )}

      {selectedTab === 'test' && (
        <div className="test-content">
          <h2>Test Section</h2>
          <ul>
            {courseData.test.map((testFile, index) => (
              <li key={index}>{testFile}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default CourseContent;