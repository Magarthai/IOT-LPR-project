import React from 'react'
import ReactDOM from 'react-dom/client'
import Landingpage from "./page/LandingPage.js";
import TicketInfo from "./page/TicketInfo.js";
import AdminPage from "./page/AdminPage.js";
import TicketPage from "./page/TicketPage.js";
import Whitelist from "./page/Whitelist.js";
import { UserAuthContextProvider } from "./context/UserAuthContext.jsx"
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import ProtectRoute from './context/protectRoute.jsx';
import './css/component_css/component.css';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Landingpage />
  },
  {
    path: "/homepage",
    element: <ProtectRoute><AdminPage /></ProtectRoute>
  },
  {
    path: "/Whitelist",
    element: <ProtectRoute><Whitelist /></ProtectRoute>
  },

])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
   
    <UserAuthContextProvider>
      <RouterProvider router={router} />
      </UserAuthContextProvider>
      
  </React.StrictMode>
)