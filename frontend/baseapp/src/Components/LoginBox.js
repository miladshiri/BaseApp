import { useState, useEffect, useContext } from 'react'
import { useNavigate } from "react-router-dom";
import { UserContext } from "../App"
import { loginAPI } from '../utils/APIs.js'


const LoginBox = () => {
    const {isUserLoggedIn, userAccessToken} = useContext(UserContext)
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    


    const handleSubmit = async (e) => {
        e.preventDefault();
        const res = await loginAPI(username, password)
        console.log(res.status)
        if (res.status == 200) {
            const data = await res.json();
            localStorage.setItem('userAccessToken', data['access'])
            localStorage.setItem('userRefreshToken', data['refresh'])
            navigate("/");
            window.location.reload();
        } else {
            return -1
        }
    };

    
    // if there's a user show the message below
    if (isUserLoggedIn) {
      return <div>You are already loggged in!!</div>;
    }
    
  return (
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-md-6 col-lg-4">
            <div class="card">
                <div class="card-body">
                <h5 class="card-title text-center mb-4">Login</h5>
                <form>
                    <div class="form-group">
                    <label for="inputEmail">Email address</label>
                    <input type="email" class="form-control" id="inputEmail" placeholder="Enter email"/>
                    </div>
                    <div class="form-group">
                    <label for="inputPassword">Password</label>
                    <input type="password" class="form-control" id="inputPassword" placeholder="Password"/>
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Sign in</button>
                </form>
                </div>
            </div>
            </div>
        </div>
    </div>

  );
};

export default LoginBox;