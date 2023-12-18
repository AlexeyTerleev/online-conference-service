import React, { useState, useEffect } from 'react';
import { useNavigate} from "react-router-dom";
import axios from "axios";
import ScheduleCreate from './ScheduleCreate/ScheduleCreate';
import useToken from '../App/useToken';
import './CourseCreate.css';


export default function CourseCreate() {
    const { token, setToken } = useToken();
    const navigate = useNavigate();
    const [name, setName] = useState(null);
    const [info, setInfo] = useState(null);
    const [schedules, setSchedules] = useState([]);

    const sendData = () => {
        const config = {
            headers: {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
        };

        const data = {
            "name": name,
            "info": info,
            "schedules": schedules.map(schedule => ({
                "start_date_time": schedule["date"] + "T" + schedule["start_time"],
                "end_date_time": schedule["date"] + "T" + schedule["end_time"],
            })),
        }
        
        axios
        .post("http://localhost:8000/course", data, config)
        .then(response => {
            navigate('/courses', { state: { token } });
        })
        .catch(error => {
            console.error(error);
        });
    }

    const handleDenyClick = () => {
        navigate('/courses', { state: { token } });
    };

    return(
        <div className="page-container">
            <div className="page-wrapper">
                <div className='header'>Create Course</div>
                <div className='body'>
                    <div className='course-create-container'>
                        <div className="course-create-name">
                            <p>Name: </p><input type='text' onChange={e => setName(e.target.value)}></input>
                        </div>
                        <div className="course-create-info">
                            <p>Info: </p><input type='text' onChange={e => setInfo(e.target.value)}></input>
                        </div>
                        <div className="course-create-schedule">
                            <ScheduleCreate schedules={schedules} setSchedules={setSchedules}/>
                        </div>
                        <div className="course-create-buttons">
                            <button onClick={sendData}>Create</button>
                            <button onClick={handleDenyClick}>Deny</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}


  
  