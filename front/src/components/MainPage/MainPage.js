import React, { useState } from 'react';
import { Link, useNavigate, Navigate } from 'react-router-dom'; // Assuming you're using React Router
import './MainPage.css';
import useToken from '../App/useToken';


export default function MainPage() {
  const {token, setToken} = useToken();

  if (token) {
    return( 
    <div className="page-container">
      <div className="page-wrapper">
        <div className="header">Online Chat</div>
        <div className="body">
          <div className="main-page-container">
            <div className="main-menu">
              <Link to="/room/enter" className="main-menu-button">Connect</Link>
              <Link to="/room/create" className="main-menu-button">Create</Link>
              <Link to="/schedule" className="main-menu-button">Schedule</Link>
              <Link to="/courses" className="main-menu-button">Courses</Link>
              <Link to="/user/me" className="main-menu-button">Profile</Link>
              <Link to="/login" className="main-menu-button" onClick={() => localStorage.removeItemo('token')}>Sign Out</Link>
            </div>
          </div>
        </div>
      </div>
    </div>)
  }
  else {
    return( <Navigate to="/login" /> )
  }
}