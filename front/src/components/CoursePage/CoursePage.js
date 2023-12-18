import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate} from "react-router-dom";
import axios from "axios";
import { UserCourseList, TeacherCourseList } from './CourseList/CourseList';
import useToken from '../App/useToken';
import './CoursePage.css'

function UserCoursePage({ location }){
    const { token, setToken } = useToken();
    const [rerender, setRerender] = useState(false);
    const [allCourses, setAllCourses] = useState(null);
    const [myCourses, setMyCourses] = useState(null);

    const fetchData = () => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        
        axios
        .get("http://localhost:8000/courses", config)
        .then(response => {
            setAllCourses(response.data);
        })
        .catch(error => {
            console.error(error);
        });

        axios
        .get("http://localhost:8000/user/me", config)
        .then(response => {
            setMyCourses(response.data.courses);
        })
        .catch(error => {
            console.error(error);
        });
    }

    const handleJoin = (courseId) => {
        const config = {
            headers: {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
        };
    
        axios
            .post('http://localhost:8000/course/' + courseId + "/join", {}, config)
            .then(function (response) {
            if (response) {
                setRerender(!rerender)
            }})
            .catch(function (error) {
            console.log(error, 'error');
            });
    }

    const handleLeave = (courseId) => {
        const config = {
            headers: {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
        };
    
        axios
            .delete('http://localhost:8000/course/' + courseId + "/leave", config)
            .then(function (response) {
            if (response) {
                setRerender(!rerender)
            }})
            .catch(function (error) {
            console.log(error, 'error');
            });
    }

    useEffect(fetchData, [location]);
    useEffect(fetchData, [rerender]);

    if (!myCourses || !allCourses) {
        return <div>Loading...</div>;
    }

    return(
        <div className='courses-wrapper'>
            <div className='all-courses'>
                <UserCourseList title={"All courses"} courses={allCourses} handleButtonClick={handleJoin} buttonTitle={"Join"} />
            </div>
            <div className='vertical-line'></div>
            <div className='my-courses'>
                <UserCourseList title={"My courses"} courses={myCourses} handleButtonClick={handleLeave} buttonTitle={"Leave"}/>
            </div>
        </div>
    )
}

function TeacherCoursePage({ location }){
    const { token, setToken } = useToken();
    const [rerender, setRerender] = useState(false);
    const [myCourses, setMyCourses] = useState(null);
    const navigate = useNavigate();

    const fetchData = () => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        axios
        .get("http://localhost:8000/user/me/courses", config)
        .then(response => {
            setMyCourses(response.data);
        })
        .catch(error => {
            console.error(error);
        });
    }

    const handleDelete = (course_id) => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        axios
        .delete("http://localhost:8000/course/" + course_id, config)
        .then(response => {
            setMyCourses(response.data);
        })
        .catch(error => {
            console.error(error);
        });
    };

    const handleCreateClick = () => {
        navigate('/course/create', { state: { token } });
    };

    useEffect(fetchData, [location]);
    useEffect(fetchData, [rerender]);

    if (!myCourses ) {
        return <div>Loading...</div>;
    }

    return(
        <div className='courses-wrapper'>
            <div className='my-courses'>
                <TeacherCourseList title={"My courses"} courses={myCourses}  onDelete={handleDelete} onCreate={handleCreateClick} />
            </div>
        </div>
    )
}

export default function CoursePage() {
    const { token, setToken } = useToken();
    const location = useLocation();
    const [userRole, setUserRole] = useState('');

    useEffect(() => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        axios
        .get("http://localhost:8000/user/me", config)
        .then(response => {
            setUserRole(response.data.role);
        })
        .catch(error => {
            console.error(error);
        });
    }, []);

    return(
        <div className="page-container">
            <div className="page-wrapper">
                <div className='header'>Courses</div>
                {userRole === "STUDENT"? <UserCoursePage location={location} /> : <TeacherCoursePage location={location} />}
            </div>
        </div>
    )
}


  
  