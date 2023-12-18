import React from 'react';
import './App.css';
import { BrowserRouter, Route, Routes, Navigate} from 'react-router-dom';
import MainPage from '../MainPage/MainPage';
import Login from '../Login/Login';
import Signup from '../Signup/Signup';
import UserPage from '../UserPage/UserPage';
import CoursePage from '../CoursePage/CoursePage';
import CourseCreate from '../CourseCreate/CourseCreate';
import Schedule from '../Schedule/Schedule'
import RoomCreate from '../RoomCreate/RoomCreate'
import useToken from './useToken';

function App() {
  const { token, setToken } = useToken();

  const ProtectedRoute = ({ element: Element, ...rest }) => {
    return token ? <Element {...rest} /> : <Navigate to="/login" />;
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/main" element={<ProtectedRoute element={MainPage} />} />
        <Route path="/user/me" element={<ProtectedRoute element={UserPage} />} />
        <Route path="/courses" element={<ProtectedRoute element={CoursePage} />} />
        <Route path="/course/create" element={<ProtectedRoute element={CourseCreate} />} />
        <Route path="/schedule" element={<ProtectedRoute element={Schedule} />} />
        <Route path="/room/create" element={<ProtectedRoute element={RoomCreate} />} />
        <Route path="*" element={<Navigate to="/main" />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;