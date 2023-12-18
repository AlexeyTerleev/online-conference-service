import React, { useState} from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";

import './Signup.css'

export default function Signup() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    if (username === '' || password === '') {
      return;
    } else {

      const data = {
        "name": name,
        "login": username,
        "password": password,
        "role": role? "STUDENT": "TEACHER",
        "personal_info": "",
        "img_path": NaN,
      }

      const config = {
        headers: {
          Accept: 'application/json',
        },
      };

      axios
        .post('http://localhost:8000/auth/signup', data, config)
        .then(function (response) {
          if (response.data) {
            console.log('success');
            navigate("/login")
          }
        })
        .catch(function (error) {
          console.log(error, 'error');
        });
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-wrapper">
        <div className="signup-header">Sign Up</div>
        <form onSubmit={handleSubmit}>
          <div class="toggle-button-cover">
            <div class="button-cover">
              <div class="button b2" id="button-10">
                <input type="checkbox" class="checkbox" onChange={e => setRole(e.target.value)} />
                <div class="knobs">
                  <span>Student</span>
                </div>
              </div>
            </div>
          </div>

          <label>
            <p>Name</p>
            <input type="text" onChange={e => setName(e.target.value)} />
          </label>
          <label>
            <p>Username</p>
            <input type="text" onChange={e => setUserName(e.target.value)} />
          </label>

          <label>
            <p>Password</p>
            <input type="password" onChange={e => setPassword(e.target.value)} />
          </label>
          <div className="submit-wrapper">
            <button className="submit-button" type="submit">
              Submit
            </button>
            <div className="login"><Link to="/login">Log in</Link></div>
          </div>
        </form>
      </div>
    </div>
  );
}