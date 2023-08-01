import {toast} from "react-toastify";
import axios from 'axios';

const login = (username, password, that) => {
    const data = {username: username, password: password}

    axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/auth/login`, data)
        .then(res => {
            console.log(res)
            if(res.status === 200){
                toast.success('Logged In')
                localStorage.setItem('token', res.data.token)
                that.setState({loggedIn: true})
            }

            else{
                toast.error('Error')
            }
        })

        .catch(err => {
            console.log(err)
            toast.error('Error')
        })
}


export { login }