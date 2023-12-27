import React from 'react';
import useToken from '../App/useToken';
import './Room.css'

export default function Room() {
    const { token, setToken } = useToken();

    return(
        <div className="page-container">
            <div className="page-wrapper">
                <div className='header'>Room</div>
                <div className='room-body'>

                </div>
            </div>
        </div>
    )
}


  
  