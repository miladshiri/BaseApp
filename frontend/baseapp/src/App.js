import { useState, useEffect, createContext, useContext, useMemo } from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";

import LoginRegisterPage from './Pages/LoginRegisterPage';
import HomePage from './Pages/HomePage';
import { verifyTokenAPI } from './utils/APIs.js'

export const UserContext = createContext()

function App() {
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(0)
  const [userAccessToken, setUserAccessToken] = useState("");
  const providerValue = useMemo(() => ({isUserLoggedIn, userAccessToken}), [isUserLoggedIn, userAccessToken])

  const validateUserLogin = async (token) => {
    const res =  await verifyTokenAPI(token)
    if (res.status == 200){
        setIsUserLoggedIn(1)
    } else {
        localStorage.removeItem("userAccessToken")
        setIsUserLoggedIn(0)
    }
  }

  useEffect(() => {
    const accessToken = localStorage.getItem("userAccessToken")
    if (accessToken) {
        setUserAccessToken(accessToken)
    }
  },[]);

  useEffect(() => {
          console.log('user access token: ', userAccessToken)
          if (userAccessToken) {
              validateUserLogin(userAccessToken)
          }

  }, [userAccessToken])

  return (
    <UserContext.Provider value={providerValue}>
      <Router>
        <Routes>
          <Route exact path='/' element={<HomePage />}></Route>
          <Route exact path='/login' element={<LoginRegisterPage />}></Route>
        </Routes>
      </Router>
    </UserContext.Provider>

  );
}

export default App;