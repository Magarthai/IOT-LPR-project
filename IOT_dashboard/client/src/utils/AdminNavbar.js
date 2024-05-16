import React from 'react';
import '../css/component_css/adminnavbar.css';
import axios from 'axios';
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom"
import { useUserAuth } from '../context/UserAuthContext';
const AdminNavbar = ({ userData,clicked }) => {
  const normal_profile = "https://cdn.discordapp.com/attachments/445928139021877259/1226572102023249981/Profile_1.png?ex=66254149&is=6612cc49&hm=9011b51c7fbd8cdc9261af8451eecd56f74e1133f18788965b0c229d276d7d95&";
  const navigate = useNavigate()
  const { logout_global } = useUserAuth();
  const hoverHandle = (e) => {
    const x = document.getElementsByClassName('hover-list')[0]; // Select the first element with class 'hover-list'
    console.log(e)
    if (e === "nav-1") {
      x.classList.add('hover1');
    } else if (e === "nav-12") {
      x.classList.remove('hover1');
    } else if (e === "nav-2") {
      x.classList.add('hover2');
    } else if (e === "nav-22") {
      x.classList.remove('hover2');
    } else if (e === "nav-3") {
      x.classList.add('hover3');
    } else if (e === "nav-32") {
      x.classList.remove('hover3');
    }
  };
  const API = process.env.REACT_APP_API;
  const logout = async() => {
    try{
      const logout = await axios.get(`${API}/user/logout`, {
        withCredentials: true 
    });
    logout_global();

    if(logout.data == "success") {
      Swal.fire({
        icon: "success",
        title: "ล็อคเอ้าสําเร็จ",
        confirmButtonText: "ตกลง",
        confirmButtonColor: '#263A50',
      }).then((result) => {
        if (result.isConfirmed) {
            navigate('/');
        } else {
          navigate('/');
        }
      });
    } else if (logout.data == "not found token") {
      Swal.fire({
        icon: "error",
        title: "ไม่พบ Token",
        confirmButtonText: "ตกลง",
        confirmButtonColor: '#263A50',
      }).then((result) => {
        if (result.isConfirmed) {
            navigate('/');
        } else {
          navigate('/');
        }
      });
    }
    } catch(e){
      console.error(e);
    }
  };

  return (
    <div className={ clicked ? "navbar-container-clicked" :"navbar-container"}>
      <div className="navbar">
        <div className="top">
          <div className='navbar-center'>
          </div>
          <div className="navbar-profile navbar-center">
            <img className='profile-img'  src={require('../img/icon.png')}></img>
            {userData && <p>{userData.fname} {userData.lname}</p>}
          </div>
          <div className="navbar-center">
            <div className="navbar-line"></div>
          </div>
          <div className="navbar-list">
            <div className="hover-list"></div>
            <a href='/homepage' className="light navbar-dashboard" id="nav-1" onMouseEnter={() => hoverHandle("nav-1")} onMouseLeave={() => hoverHandle("nav-12")}>
              <img src={require('../img/3.png')} alt="dashboard" />
              <p>Dashboard</p>
            </a>
            <a href='/ticketHistory' className="light navbar-dashboard" id="nav-3" onMouseEnter={() => hoverHandle("nav-2")} onMouseLeave={() => hoverHandle("nav-22")}>
              <img src={require('../img/4.png')} alt="admin manager" />
              <p>Whitelist</p>
            </a>
          </div>
        </div>
        <div className="bottom">
          <button className='bold logout-button' style={{cursor:"pointer"}} onClick={() => logout()}>LOGOUT</button>
        </div>
      </div>
    </div>
  );
}

export default AdminNavbar;
