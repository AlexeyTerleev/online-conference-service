import React, { useState, useEffect } from 'react';
import { useLocation } from "react-router-dom";
import './ScheduleCreate.css'


export default function ScheduleCreate({ schedules, setSchedules }) {
    
    const addRow = () => {
        console.log(schedules)
        const newRow = {
            date: '',
            start_time: '',
            end_time: '',
        };
        setSchedules([...schedules, newRow]);
    };

    const deleteRow = (index) => {
        const updatedSchedules = schedules.filter((_, i) => i !== index);
        setSchedules(updatedSchedules);
    };

    return(
        <div className='schedule-create-contanier'>
            <div className='schedule-create-wrapper'>
                <div>Schedule</div>
                <div className='schedule-create-list'>
                    <li className='schedule-create-row'><div>Date</div><div>Start</div><div>End</div></li>
                    {schedules.map((schedule, index) => 
                    <li key={index} className='schedule-create-row'>
                        <input 
                            type="text"
                            value={schedule.start_date_time}
                            onChange={(e) => {
                            const updatedSchedules = [...schedules];
                            updatedSchedules[index].date = e.target.value;
                            setSchedules(updatedSchedules);
                            }}
                        />
                        <input
                            type="text"
                            value={schedule.end_date_time}
                            onChange={(e) => {
                            const updatedSchedules = [...schedules];
                            updatedSchedules[index].start_time = e.target.value;
                            setSchedules(updatedSchedules);
                            }}/>
                        <input
                            type="text"
                            value={schedule.end_date_time}
                            onChange={(e) => {
                            const updatedSchedules = [...schedules];
                            updatedSchedules[index].end_time = e.target.value;
                            setSchedules(updatedSchedules);
                            }}/>
                        <button className="schedule-create-delete" onClick={() => deleteRow(index)}>Delete</button>
                    </li>)}
                </div>
                <div className="schedule-create-buttons">
                    <button className="schedule-create-add" onClick={addRow}>Add</button>
                </div>
            </div>
        </div>
    )
}


  
  