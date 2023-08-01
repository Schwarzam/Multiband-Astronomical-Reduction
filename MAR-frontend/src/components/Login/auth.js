import axios from 'axios'
import {useContext} from "react";
import {useNavigate} from "react-router-dom";

function getHeader() {
    var token = localStorage.getItem('token')

    const config = {
        headers:{
            'Content-Type': 'application/json'
        }
    };

    config.headers['Authorization'] = `Token ${token}`;
    return config
}


async function validateToken() {
    const header = getHeader()

    await axios.get(`${process.env.REACT_APP_SERVER_IP}/reduction/auth/user`, header)
        .then(res =>{

        })
        .catch(err => {
            //localStorage.removeItem('token')
        })
}

const useValidadeLogin = (backlink = '/') => {
    const header = getHeader()
    const navigate = useNavigate()

    axios.get(`${process.env.REACT_APP_SERVER_IP}/reduction/auth/user`, header)
        .then(res =>{

        })
        .catch(err => {
            console.log(err)
            if (backlink !== 'login'){
                navigate('/login')
            }
        })
}



export { getHeader, validateToken, useValidadeLogin }