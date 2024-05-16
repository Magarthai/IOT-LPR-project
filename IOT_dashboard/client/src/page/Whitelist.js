import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom"
import AdminNavbar from '../utils/AdminNavbar.js';
import { useUserAuth } from '../context/UserAuthContext.jsx';
import Card from '../utils/cardSkeleton.js';
import BarLoaders from '../utils/BarLoader.js';
import '../css/page_css/ticketpage.css';
import Swal from 'sweetalert2';
import CountSkeleton from '../utils/CountSkeleton.js';
import HambergerBar from '../utils/HambergerBar.js';
import DataTable from 'react-data-table-component';

import axios from 'axios'
function AdminPage() {
  const { userData } = useUserAuth();
  const navigate = useNavigate();
  const [data, setData] = useState([]);
  const [usersData, setUsersData] = useState([]);
  const [loader, setLoader] = useState(false);
  const API = process.env.REACT_APP_API
  const [statusInfo, setStatusInfo] = useState({});
  const [clicked, setClicked] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [whitelist, setWhitelist] = useState("");
  const [name, setName] = useState("")
  const fetchData = async () => {
    try {
      console.log('xd')
      console.log(userData._id, "userData")
      const respone = await axios.get(`${API}/whitelist/getWhitelist`)
        
      if (respone.data != undefined) {
        setData(respone.data)

      }


      setTimeout(() => {
        setIsLoading(false)
      }, 1000);
    } catch (err) {
      console.log(err);
    }
  };

  const fetchUserData = async () => {
    try {
      console.log('xd')
      console.log(userData._id, "userData")
      const respone = await axios.get(`${API}/user/all-users`)
      console.log("adminlist",respone.data)
      if (respone.data != undefined) {
        setUsersData(respone.data)

      }


      setTimeout(() => {
        setIsLoading(false)
      }, 1000);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    console.log(data.lenght, "data")
  }, [data])

  const handleSubmit = async () => {
    try {
      const info = {
        name: name,
        license: whitelist,
      }
      const respone = await axios.post(`${API}/whitelist/createWhitelist`,info);
      console.log(respone.data)
      if(respone.data = "success") {
        Swal.fire({
          icon: "success",
          title: "สําเร็จ!",
          text: "สร้าง White ลงในระบบแล้ว!",
          confirmButtonText: "ตกลง",
          confirmButtonColor: '#263A50',
        })
      } else {
        Swal.fire({
          icon: "error",
          title: "ไม่สําเร็จ!",
          text: "เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง!",
          confirmButtonText: "ตกลง",
          confirmButtonColor: '#263A50',
        })
      }
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (userData) {
      fetchData();
      fetchUserData();
    }

  }, [userData]);
  const toggleClicked = () => {
    setClicked(!clicked);
  };

  const columns = [
    {
      name: "Name",
      selector: row => row.name
    },
    {
      name: "License",
      selector: row => row.license
    },
  ];

  const column2 = [
    {
      name: "Firstname",
      selector: row => row.fname
    },
    {
      name: "Lastname",
      selector: row => row.lname
    },
    {
      name: "Email",
      selector: row => row.email
    },
  ];
  return (
    <div className="admin-container" >
      {loader ? <BarLoaders></BarLoaders> : <div></div>}
      <HambergerBar clicked={clicked} toggleClicked={toggleClicked} />
      <AdminNavbar clicked={clicked} userData={userData} />
      <div className='adminpage-header button-color'></div>
      <div className="leftside">
        <div className="whitelist-container">
          <div className="whitelist-container">
            <div className="add-whitelist">
              <div className="car-icon">
                <img src={require('../img/1.png')} alt="" />
              </div>
              <div className="add-whitelist-zone">
                <span>ADD WHITELIST!</span>
                < input style={{marginBottom:10}} type="text" name="license" placeholder='Username!' onChange={(event)=> setName(event.target.value)}/>
                <input type="text" name="license" placeholder='Type whitelist here!' onChange={(event)=> setWhitelist(event.target.value)}/>
                <button onClick={() => handleSubmit()}>Add whitelist!</button>
              </div>
            </div>
          </div>
          <div className="bottom-side">
          <div className="whitelist-list">
            <span>WHITELIST</span>
            <DataTable
            style={{overflowY:'scroll'}}
              columns={columns}
              data={data}>
            </DataTable>
          </div>
          <div className="admin-list">
            <span>Admin</span>
            <DataTable
            style={{overflowY:'scroll'}}
              columns={column2}
              data={usersData}>
            </DataTable>
          </div>
          </div>
          
          
        </div>
      </div>


    </div>


  )
}

export default AdminPage