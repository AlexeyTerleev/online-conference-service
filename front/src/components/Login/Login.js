import React, { useState} from 'react';
import { Link,useNavigate } from 'react-router-dom';
import axios from "axios";
import PropTypes from 'prop-types';
import './Login.css'

export default function Login({ setToken }) {
  const navigate = useNavigate();
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = (e) => {
      e.preventDefault();
  
      if (username === '' || password === '') {
        return;
      } else {
        const data = new URLSearchParams();
        data.append('grant_type', '');
        data.append('username', username);
        data.append('password', password);
        data.append('scope', '');
        data.append('client_id', '');
        data.append('client_secret', '');
  
        const config = {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
          },
        };
  
        axios
          .post('http://localhost:8000/auth/login', data, config)
          .then(function (response) {
            if (response.data) {
              setToken(response.data);
              navigate("/main");
            }
          })
          .catch(function (error) {
            console.log(error, 'error');
          });
      }
    };

  return(
    <div className="login-container">
        <div className="login-wrapper">
            <div className="login-header">Please Log In</div>
            <form onSubmit={handleSubmit}>
            <label>
                <p>Username</p>
                <input type="text" onChange={e => setUserName(e.target.value)} />
            </label>
            <label>
                <p>Password</p>
                <input type="password" onChange={e => setPassword(e.target.value)} />
            </label>
            <div className="submit-wrapper">
                <button class="submit-button" type="submit">Submit</button>
                <div className="sign-up"><Link to="/signup">Sign up</Link></div>
            </div>
            </form>
        </div>
    </div>
  )
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
};

