import React, {useContext, useEffect, useState} from "react";
import axios from 'axios';


import {toast} from "react-toastify";
import { useNavigate } from "react-router-dom";


function Login() {
    const [user, setUser] = useState('')
    const [password, setPassword] = useState('')
    const [logged, setLogged] = useState(false)

    const navigate = useNavigate()

    useEffect(() => {
        if (logged){
            navigate('/')
        }
    }, [logged, navigate])


    const log = () => {
        const data = {username:user, password: password}
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/auth/login`, data)
            .then(res => {
                console.log(res)
                if(res.status === 200){
                    toast.success('Logged In')
                    localStorage.setItem('token', res.data.token)
                    setLogged(true)
                }
            })
            .catch(err => {
                toast.error('Error')
            })
    }

    return(
        <div className="z-10 w-full h-full bg-white grid place-content-center">
                <h1 className="text-center text-2xl p-10">MAR login</h1>

                <span>Username</span>
                <label className="relative block">
                    <input onChange={(e => setUser(e.target.value))} name="user" className="placeholder:text-slate-400 block border border-slate-300 rounded-md py-2 pl-3 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm" />
                </label>

                <span className="mt-5">Password</span>
                <label className="relative block">
                    <input onChange={(e => setPassword(e.target.value))} name="password" type="password" className="placeholder:text-slate-400 block border border-slate-300 rounded-md py-2 pl-3 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm" />
                </label>

                <button onClick={log} className="mt-5 rounded-full p-4 border border-zinc-500 m-3 bg-zinc-300 hover:border-zinc-100 hover:bg-zinc-700 hover:text-white">Login</button>
        </div>
    )

}


export default Login