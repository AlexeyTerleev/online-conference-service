import React from 'react';
import './CourseList.css'




export function UserCourseList({ title, courses, handleButtonClick, buttonTitle }) {

    return(
        <div className="list-container">
            <div className="list-wrapper">
                <div className='list-header'>{title}</div>
                <div className='list-body'>
                    <li className='course-record'>
                        <div className='course-name'>Name</div>
                        <div className='course-info'>Info</div>
                        <div className='course-button'></div>
                    </li>
                    {
                        courses.map(
                            course =>
                            <li key={course.id} className='course-record'>
                                <div className='course-name'>{course.name}</div>
                                <div className='course-info'>{course.info}</div>
                                <button className={`course-button ${buttonTitle.toLowerCase()}`} onClick={() => handleButtonClick(course.id)}>{buttonTitle}</button>
                            </li>
                        )
                    }
                </div>
            </div>
        </div>
    )
}


export function TeacherCourseList({ title, courses, onDelete, onCreate}) {

    return(
        <div className="list-container">
            <div className="list-wrapper">
                <div className='list-header'>{title}</div>
                <div className='list-body'>
                    <li className='course-record'>
                        <div className='course-name'>Name</div>
                        <div className='course-info'>Info</div>
                        <div className='course-button'></div>
                    </li>
                    {
                        courses.map(
                            course =>
                            <li key={course.id} className='course-record'>
                                <div className='course-name'>{course.name}</div>
                                <div className='course-info'>{course.info}</div>
                                <button className='course-delete' onClick={() => onDelete(course.id)}>Delete</button>
                            </li>
                        )
                    }
                </div>
            </div>
            <button className='create-course-button' onClick={() => onCreate()}>Create Course</button>
        </div>
    )
}


  
  