import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate} from "react-router-dom";
import axios from "axios";
import useToken from '../App/useToken';
import './RoomEnter.css'

export default function RoomEnter() {
    const { token, setToken } = useToken();
    const location = useLocation();
    const navigate = useNavigate();
    const [roomExist, setRoomExist] = useState(false);
    const [roomKey, setRoomKey] = useState('');
    const [isPrivate, setIsPrivate] = useState(false);
    const [roomPassword, setRoomPassword] = useState('');

    const fetchData = (value) => {
        const config = {
            headers: {
              'Accept': 'application/json',
              'Authorization': 'Bearer ' + token,
            },
          };
        
        axios
        .get(`http://localhost:8000/room/${value}`, config)
        .then(response => {
            setIsPrivate(response.data.private);
            setRoomExist(true);
        })
        .catch(error => {
            console.error(error);
            setRoomExist(false);
        });
    }

    const isRoomKeyValid = (value) => {
        const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
        return uuidRegex.test(value);
    };

    const handleRoomKeyChange = (e) => {
        const value = e.target.value;
        
        setRoomKey(value);
        if (isRoomKeyValid(value)) {
            fetchData(value)
        }
        else if(isPrivate) {
            setIsPrivate(!isPrivate);
            setRoomExist(false);
        }
        else {
            setRoomExist(false);
        }
    };

    useEffect(() => {
        if (location.state) {
            setRoomKey(location.state.schedule_id || '');
            if (isRoomKeyValid(location.state.schedule_id)) {
                fetchData(location.state.schedule_id)
            }
        }
    }, [location.state]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!isRoomKeyValid(roomKey) || isPrivate && roomPassword === "") {
            console.log("wrong creds")
            return;
        } 
        else {
            const data = {
                "key": roomKey,
                "password": isPrivate ? roomPassword : null,
            }
            const config = {
                headers: {
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
            };
    
            axios
            .post('http://localhost:8000/room/join', data, config)
            .then(function (response) {
                if (response.data) {
                    if (response.data.access) {
                        navigate('/room', { state: { roomKey } });
                    }
                    else {
                        console.log("bad")
                    }
                }
            })
            .catch(function (error) {
                console.log(error, 'error');
            });
      }
    };

    return(
        <div className="page-container">
            <div className="page-wrapper">
                <div className='header'>Room Enter</div>
                <div className='room-body'>
                <form onSubmit={handleSubmit}>
                <label className='row'>
                    <p>Room key:</p>
                    <input type="text" className={roomExist ? "correct-input" : ""} value={roomKey} onChange={handleRoomKeyChange} />
                </label>
                { isPrivate &&
                <label className='row'>
                    <p>Room password:</p>
                    <input type="password" value={roomPassword} onChange={e => setRoomPassword(e.target.value)} />
                </label>
                }
                <div className="submit-wrapper">
                    <button className="submit-button" type="submit">Join</button>
                </div>
                </form>
                </div>
            </div>
        </div>
    )
}


  
  