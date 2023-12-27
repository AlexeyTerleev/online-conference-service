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

      const scheduleId = location.state && location.state.schedule_id;
      const url = scheduleId
        ? `http://localhost:8000/schedule/${location.state.schedule_id}/room`
        : `http://localhost:8000/room`;
  
      axios
        .post(url, data, config)
        .then(response => {
          console.log(response.data)
          if (location.state.schedule_id){
            navigate("/schedule")
          }
          else {
            navigate("/main")
          }
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
            <form onSubmit={sendData}> 
            <div className='room-create-row'>
                <p>Private: </p>
                <input type='checkbox' checked={isPrivate} onChange={e => setPrivate(e.target.checked)} />
            </div>
            
            {isPrivate && (
                <div className='room-create-row'>
                    <p>Password: </p>
                    <input type="password" autoComplete="new-password" onChange={e => setPassword(e.target.value)} />
                </div>
            )}
            <button type="submit">Create Room</button>
            </form>
          </div>
        </div>
      </div>
    );
  }


  
  