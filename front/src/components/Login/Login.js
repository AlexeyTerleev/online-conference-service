import React, { useState} from 'react';
import { Link,useNavigate } from 'react-router-dom';
import axios from "axios";
import PropTypes from 'prop-types';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './Login.css'

export default function Login({ setToken }) {
  const navigate = useNavigate();
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [isUsernameError, setIsUsernameError] = useState(false); 
  const [isPasswordError, setIsPasswordError] = useState(false);

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
            if (error.response) {
              console.log(error.response.data)
              const responseData = error.response.data;
              const errorDetail = responseData && responseData.detail;
              const wrongUsernamePattern = /^User with login \[.*\] not found$/;

              if (wrongUsernamePattern.test(errorDetail)) {
                setIsUsernameError(true); 
              }
              else if (errorDetail === "Incorrect password") {
                setIsPasswordError(true);
              }
              toast.error(errorDetail, 
                {
                  position: "top-center",
                  autoClose: 2000,
                  hideProgressBar: false,
                  closeOnClick: true,
                  pauseOnHover: true,
                  draggable: true,
                  progress: undefined,
                  theme: "dark",
                }
              );
            } else {
              console.log("An error occurred. Please try again.");
            }
          });
      }
    };

  return(
    <div className="page-container">
      <div className="page-wrapper">
        <div className="header">Please Log In</div>
        <div className="body">
          <form className="sign-in-form" onSubmit={handleSubmit}>
            <label>
                <p>Username</p>
                <input 
                  type="text" 
                  autoComplete="username" 
                  className={isUsernameError ? "error-input" : ""} 
                  onChange={
                    e => {setUserName(e.target.value); setIsUsernameError(false);}
                  } 
                />
            </label>
            <label>
                <p>Password</p>
                <input 
                  type="password" 
                  autoComplete="current-password" 
                  className={isPasswordError ? "error-input" : ""} 
                  onChange={
                    e => {setPassword(e.target.value); setIsPasswordError(false);}
                  } 
                />
            </label>
            <div className="submit-wrapper">
                <button className="submit-button" type="submit">Submit</button>
                <div className="sign-up"><Link to="/signup">Sign up</Link></div>
            </div>
          </form>
        </div>
      </div>
      <ToastContainer position="top-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
      />
    </div>
  )
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
};

