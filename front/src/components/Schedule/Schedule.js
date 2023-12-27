import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import useToken from '../App/useToken';
import './Schedule.css'



export default function Schedule() {
    const { token, setToken } = useToken();

    const location = useLocation();
    const navigate = useNavigate();
    const [schedules, setSchedule] = useState(null);
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

    const fetchData = () => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        
        axios
        .get("http://localhost:8000/user/me/schedule", config)
        .then(response => {
            var schedules = response.data;
            var schedulesByDate = {};

            var dates = schedules.map(schedule => schedule.start_date_time.split("T")[0]);
            schedulesByDate = dates.reduce((acc, date) => {
                const schedulesOnDate = schedules.filter(schedule => schedule.start_date_time.startsWith(date));
                return { ...acc, [date]: schedulesOnDate };
            }, {});
            var sortedSchedulesByDate = Object.entries(schedulesByDate)
                .sort((a, b) => new Date(a[0]) - new Date(b[0]))
                .reduce((acc, [date, schedulesOnDate]) => ({ ...acc, [date]: schedulesOnDate }), {});
            setSchedule(sortedSchedulesByDate);
        })
        .catch(error => {
            console.error(error);
        });
    }

    const handleRoomCreateClick = (schedule_id) => {
        navigate('/room/create', { state: { schedule_id } });
    };

    const handleRoomJoinClick = (schedule_id) => {
        console.log(schedule_id);
        navigate('/room/enter', { state: { schedule_id } });
    };

    useEffect(fetchData, [location]);

    if (!schedules) {
        return <div>Loading...</div>;
    }

    return(
        <div className="page-container">
            <div className="page-wrapper">
                <div className='header'>Schedule</div>
                <div className='body'>
                    <div className='schedule-container'>
                        {
                            Object.keys(schedules).map(
                                date =>
                                <li key={date} className='schedule-day'>
                                    <div className='schedule-day-date'>{date}</div>
                                    <ul className='schedule-day-list'>
                                        {
                                            schedules[date].map(
                                                schedule => <li key={schedule.id} className='schedule-day-row'>
                                                    <div className='schedule-day-row-time'>{schedule.start_date_time.split("T")[1]} - {schedule.end_date_time.split("T")[1]}</div>
                                                    <div className='schedule-day-row-name'>{schedule.course.name}</div>
                                                    <div className='schedule-day-row-button'>
                                                    {!schedule.room_id && userRole === "TEACHER" && <button onClick={() => handleRoomCreateClick(schedule.id)} className='create'>Create</button>}
                                                    {schedule.room_id && <button className='join' onClick={() => handleRoomJoinClick(schedule.room_id)}>Join</button>}
                                                    </div>
                                                </li>
                                            )
                                        }
                                    </ul>
                                </li>
                            )
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}


  
  