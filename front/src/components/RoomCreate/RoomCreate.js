import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate} from "react-router-dom";
import axios from "axios";
import useToken from '../App/useToken';
import './RoomCreate.css'



export default function RoomCreate({ schedule_id }) {
    const { token, setToken } = useToken();
    const navigate = useNavigate();
    const location = useLocation()
    const [isPrivate, setPrivate] = useState(false);
    const [password, setPassword] = useState(null);

  
    const sendData = () => {
      const config = {
        headers: {
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + token,
        },
      };
      const data = {
        "private": isPrivate,
        "password": password,
      };
  
      axios
        .post(`http://localhost:8000/schedule/${location.state.schedule_id}/room`, data, config)
        .then(response => {
          navigate("/schedule");
        })
        .catch(error => {
          console.error(error);
        });
    };
  
    useEffect(() => {
      setPrivate(false);
    }, []);
  
    return (
      <div className="page-container">
        <div className="page-wrapper">
          <div className='header'>Create Room</div>
          <div className='room-create-container'>
            <div className='room-create-row'>
                <p>Private: </p>
                <input type='checkbox' checked={isPrivate} onChange={e => setPrivate(e.target.checked)} />
            </div>
            
            {isPrivate && (
                <div className='room-create-row'>
                    <p>Password: </p>
                    <input type="password" onChange={e => setPassword(e.target.value)} />
                </div>
            )}
            <button onClick={sendData}>Create Room</button>
          </div>
        </div>
      </div>
    );
  }


  
  