import React, { useState, useEffect } from 'react';
import '../css/page_css/landingpage.css';
import Swal from "sweetalert2";
import LoginPopup from '../utils/LoginPopup'
import { useCookies } from 'react-cookie';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useUserAuth } from '../context/UserAuthContext';
import { auth, db, storage, ref, uploadBytes, getDownloadURL } from '../config/firebase';
function LandingPage() {
  const { checkToken, userData } = useUserAuth();
  const [selectTopic, setSelectTopic] = useState("");

  const [openPopup, setOpenPopup] = useState(false);

  const navigate = useNavigate();


  useEffect(() => {
    if (userData) {
      navigate("/homepage")
    }
    console.log(selectTopic);
  }, [selectTopic, userData]);



  const login = () => {
    setOpenPopup(true)
    console.log(login)
  }
 

  const slide = () => {
    const element = document.getElementById('2');
    element?.scrollIntoView({
      behavior: 'smooth'
    });
  }



  return (
    <div className='container'>

      <LoginPopup open={openPopup} onClose={() => setOpenPopup(false)}></LoginPopup>
      <section className='first-section' style={{ filter: openPopup ? 'blur(2px)' : 'none' }}>
        <header className='landingpage-header'>
        <img className='disable-select header-img' src='https://i.imgur.com/1jSDKVN.png' alt='NIPA CLOUD ICON'></img>
          <a className='disable-select button-color medium font-white-color login-button' onClick={() => login()}>ลงชื่อเข้าใช้งาน</a>
        </header>

        <div className='landing-page-1 font-primary'>
          <div className='landing-text'>
            <h1>LPR MANAGER</h1>
            <p>ระบบการตรวจจับป้ายทะเบียนเพื่อเปิดไม้กั้นรถ คุณสามารถตั้งค่า หรือดูรายละเอียดต่างๆได้ผ่านปุ่มนี้</p>
            <a className='pick-button medium button-color' onClick={() => slide()}>คลิกปุ่มนี้</a>

          </div>
          <img className='extralight landing-img' src='https://i.imgur.com/TqMUiiB.png' alt='cloud server'></img>
        </div>
      </section>



    </div>
  )
}

export default LandingPage