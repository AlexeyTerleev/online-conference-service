import React, { useState, useEffect } from 'react';
import { useLocation } from "react-router-dom";
import axios from "axios";
import './UserPage.css';
import useToken from '../App/useToken';



export default function UserPage() {
    const { token, setToken } = useToken();
    const location = useLocation();
    const [user, setUser] = useState(null);

    useEffect(() => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        if (location.pathname === '/user/me') {
          axios
            .get("http://localhost:8000/user/me", config)
            .then(response => {
              setUser(response.data);
            })
            .catch(error => {
              console.error(error);
            });
        }
    }, [location]);

    if (!user) {
        return <div>Loading...</div>;
    }

    return(
        <div className="page-container">
            <div className="page-wrapper">
                <div className="header">Role: {user.role}</div>
                <div className="body">
                    <div className="image-wrapper">
                        <img src="https://static.vecteezy.com/system/resources/previews/020/765/399/non_2x/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg" alter = "Img" />
                    </div>
                    <div className="info-wrapper">
                        <div>Name: {user.name}</div>
                        <div>Personal info: {user.personal_info}</div>
                    </div>
                </div>
            </div>
        </div>
    )
}


  
  