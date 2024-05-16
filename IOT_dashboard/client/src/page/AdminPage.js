import React, { useEffect, useState } from 'react';
import AdminNavbar from '../utils/AdminNavbar.js';
import { useUserAuth } from '../context/UserAuthContext';
import axios from 'axios'
import '../css/page_css/adminpage.css';
import GraphSkeleton from '../utils/graphSkeleton.js';
import CountSkeleton from '../utils/CountSkeleton.js';
import HambergerBar from '../utils/HambergerBar.js';
import { AreaChart, Area, Tooltip, ResponsiveContainer, Cell, XAxis, YAxis, CartesianGrid, Legend, BarChart, Bar } from 'recharts'
import { useNavigate } from "react-router-dom"
function AdminPage() {
  const [isLoading, setIsLoading] = useState(true);
  const { userData,logout_global } = useUserAuth();
  const [data, setData] = useState([]);
  const [dataa, setDataa] = useState([]);
  const [data2, setData2] = useState([]);
  const [statusInfo, setStatusInfo] = useState({});
  const [clicked, setClicked] = useState(false); 
  const API = process.env.REACT_APP_API
  const navigate = useNavigate()
  useEffect(() => {
    if(userData) {
    fetchStatusInfo();
    }
  }, [userData]); 

  const fetchStatusInfo = async () => {
    try {
      const response = await axios.get(`${API}/dashboard/getStatusCount`, {
        headers: {
            Authorization: `Bearer ${userData.refreshToken}`,
            role: userData.role
            
        }
        });
      if (response.data) {
        setStatusInfo(response.data);
      }
      const response2 = await axios.get(`${API}/dashboard/getMonthTicket`, {
        headers: {
            Authorization: `Bearer ${userData.refreshToken}`,
            role: userData.role
            
        }
        });
      if (response2.data) {
        setData(response2.data);
      }
      
      const response3 = await axios.get(`${API}/dashboard/getSuccessErrorCount`, {
        headers: {
            Authorization: `Bearer ${userData.refreshToken}`,
            role: userData.role
            
        }
        });
        
      if (response3.data) {
        console.log("data2",response3.data)
        setData2(response3.data);
      }
      setTimeout(() => {
        setIsLoading(false)
      }, 1000);
    } catch (err) {
      if(err.response.status === 401) {
        navigate('/')
        logout_global();
        console.log("You are not admin")
        
      } else {
      console.error(err)
      }
    }
  };

  const toggleClicked = () => {
    setClicked(!clicked);
  };

  return (
    <div className="admin-container">
      <HambergerBar clicked={clicked} toggleClicked={toggleClicked} />
      <AdminNavbar clicked={clicked} userData={userData} />
      <div className='adminpage-header button-color'></div>
      <div className="leftside">
        {isLoading ? <CountSkeleton></CountSkeleton> : (
          <div className="summary-status-container">


            <div className="summary-status-card">
              <div className="info">
                <h1 className='light'>Entry</h1>
                {statusInfo && <span className='extralight'>{statusInfo.entry}&nbsp;รายการ</span>}
              </div>
              <div className="status-img success">
                <img src={require('../img/Ok.png')} alt="success" />
              </div>
            </div>
            <div className="summary-status-card">
              <div className="info">
                <h1 className='light'>Out</h1>
                {statusInfo && <span className='extralight'>{statusInfo.exit}&nbsp;รายการ</span>}
              </div>
              <div className="status-img reject">
                <img src={require('../img/Cancel.png')} alt="reject" />
              </div>
            </div>
          </div>
        )}
        {isLoading ? <GraphSkeleton></GraphSkeleton> : (
        <div>
          <div className="dashboard-container">
            <div className="line-graph">
              <h1 className='light'>กราฟจํานวน คนเข้า - ออก ลานจอดรถในเดือนนี้</h1>
              <ResponsiveContainer width="100%" height={300} style={{ padding: "0 1%" }}>
                <AreaChart width={500} height={300} data={data}>
                  <defs>
                    <CartesianGrid strokeDasharray="3 3" />
                    <linearGradient id="colorview" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="30%" stopColor='#0d78b6' stopOpacity={0.4}></stop>
                      <stop offset="85%" stopColor='#8ed2e7' stopOpacity={0}></stop>
                    </linearGradient>
                  </defs>

                  <Tooltip />
                  <Area type="monotone" dataKey="value" fill='url(#colorview)' />
                  <YAxis type="number" tick={{ fontSize: 10 }} />
                  <XAxis type="category" dataKey="date" tick={{ fontSize: 10 }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="bar-chart">
              <ResponsiveContainer width="100%" height="100%" style={{ padding: "15px" }}>
                <BarChart
                  width={500}
                  height={300}
                  data={data2}

                  layout="vertical"
                >
                  <defs>
                    <linearGradient id="successGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#1D976C" stopOpacity={1} />
                      <stop offset="100%" stopColor="#93F9B9" stopOpacity={1} />
                    </linearGradient>
                    <linearGradient id="rejectGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#b31217" stopOpacity={1} />
                      <stop offset="100%" stopColor="#e52d27" stopOpacity={1} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" tick={{ fontSize: 10 }} />
                  <YAxis type="category" dataKey="name" tick={{ fontSize: 10 }} domain={[1, 5]} />
                  <Tooltip />
                  <Bar dataKey="value">
                    {
                      data2.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.name === 'entry' ? 'url(#successGradient)' : 'url(#rejectGradient)'} />
                      ))
                    }
                  </Bar>
                </BarChart>


              </ResponsiveContainer>
            </div>
          </div>
        </div>
        )}
      </div>

    </div>
  )
}

export default AdminPage