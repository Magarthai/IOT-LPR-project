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
import axios from 'axios'
function AdminPage() {
  const { userData } = useUserAuth();
  const navigate = useNavigate();
  const [data, setData] = useState({});
  const [loader, setLoader] = useState(false);
  const API = process.env.REACT_APP_API
  const [statusInfo, setStatusInfo] = useState({});
  const [clicked, setClicked] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const fetchData = async () => {
    try {
      console.log('xd')
      console.log(userData._id, "userData")
      const info = {
        id: userData._id
      };
      const respone = await axios.post(`${API}/ticket/getTicketByAdmin`, info,
        {
          headers: {
            Authorization: `Bearer ${userData.refreshToken}`,
            role: userData.role

          },
        });
      if (respone.data) {
        console.log(respone.data, "XD")
        if (respone.data.message == "Ticket fetch successfully") {
          setData(respone.data.ticket)
        }

      }

      const respone2 = await axios.post(`${API}/dashboard/getStatusAdminCount`, info,
        {
          headers: {
            Authorization: `Bearer ${userData.refreshToken}`,
            role: userData.role

          },
        });
      if (respone2.data) {
        console.log(respone2.data, "XD2")
        setStatusInfo(respone2.data);
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

  const barColors = ["#1f77b4", "#ff7f0e"]
  const img_status = (e) => {
    console.log(e);
    if (e === "pending") {
      return "https://cdn.discordapp.com/attachments/445928139021877259/1226597902596571216/Group.png?ex=66255951&is=6612e451&hm=c9350934360d3a5cb03d5bab5826e5697b132f68d69b682d7b28b1154b18082d&";
    }
    else if (e === "accepted") {
      return "https://cdn.discordapp.com/attachments/445928139021877259/1226597902856749106/Meeting_Time.png?ex=66255951&is=6612e451&hm=0a5b210c2b113d9c2e614aa32283892babf8fc730ffc3be764725f05460410a0&"
    } else if (e === "success") {
      return "https://cdn.discordapp.com/attachments/445928139021877259/1226597903087308842/Ok.png?ex=66255951&is=6612e451&hm=577726e0f2a2f13cee08eb34845a52b1f62bafa7a42e10ff0a4c44f6fa310c73&"
    } else {
      return "https://cdn.discordapp.com/attachments/445928139021877259/1226597902349111336/Cancel.png?ex=66255951&is=6612e451&hm=68b3f78ea5d25528c45496163533d5a1e38537531fc5852fe41ad5cf8af9f178&"
    }
  };

  const handleSubmit = async (ticket) => {
    try {
      const info = {
        name: ticket.name,
        email: ticket.email,
        topic: ticket.selectTopic,
        time: new Date(ticket.createdAt).toLocaleString(),
        recipient: userData.fname + " " + userData.lname,
        status: "รับเรื่องแล้ว",
        recipientId: userData._id,
        updateStatus: "accepted"
      }

      const updateStatus = await axios.put(`${API}/ticket/updateStatusTicket/:${ticket._id}`, {
        headers: {
          Authorization: `Bearer ${userData.refreshToken}`,
          role: userData.role

        },
        info
      });
      if (updateStatus.data) {
        console.log(updateStatus.data.message)
        if (updateStatus.data.message == "Already accepted") {
          Swal.fire({
            icon: "error",
            title: "รับเรื่องไม่สําเร็จ",
            text: "มีคนรับเรื่องนี้แล้ว!",
            confirmButtonText: "ตกลง",
            confirmButtonColor: '#263A50',
          })
          return;
        } else {
          console.log(updateStatus.data.message)
          setLoader(true);
          const respone = await axios.post(`${API}/ticket/sendemail`, info,
            {
              headers: {
                Authorization: `Bearer ${userData.refreshToken}`,
                role: userData.role

              },
            });

          if (respone.data) {
            if (respone.data.RespCode == 200) {
              setLoader(false);
              navigate("/ticketinfo", { state: { data: ticket } });
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
    }
  }


  const fetchDataQuery = async (e) => {
    try {
      setIsLoading(true);
      console.log('xd')
      const info = {
        status: e,
      }
      const respone = await axios.post(`${API}/ticket/getTicketQuery`, info,
        {
          headers: {
            Authorization: `Bearer ${userData.refreshToken}`,
            role: userData.role

          },
        });
      if (respone.data) {
        if (respone.data.message == "Ticket fetch successfully") {
          setData(respone.data.ticket)
          setTimeout(() => {
            setIsLoading(false)
          }, 1000);
        }

      }
    } catch (err) {
      console.error(err)
    }
  };
  useEffect(() => {
    if (userData) {
      fetchData();
    }

  }, [userData]);
  const toggleClicked = () => {
    setClicked(!clicked);
  };
  return (
    <div className="admin-container" >
      {loader ? <BarLoaders></BarLoaders> : <div></div>}
      <HambergerBar clicked={clicked} toggleClicked={toggleClicked} />
      <AdminNavbar clicked={clicked} userData={userData} />
      <div className='adminpage-header button-color'></div>
      <div className="leftside">
        <div className="summary-status-container">
          <div className="whitelist-container">
            <div className="add-whitelist">
              <div className="car-icon">
                <img src={require('../img/1.png')} alt="" />
              </div>
              <div className="add-whitelist-zone">
                <span>ADD WHITELIST!</span>
                <input type="text" name="license" placeholder='Type whitelist here!'/>
                <button>Add whitelist!</button>
              </div>
            </div>
          </div>
        </div>

      </div>


    </div>


  )
}

export default AdminPage