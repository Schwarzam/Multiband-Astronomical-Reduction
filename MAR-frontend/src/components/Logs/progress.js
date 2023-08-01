import {useEffect, useState} from "react";
import axios from "axios";
import {getHeader} from "../Login/auth";


export default function Progress(){

    const [progress, setProgress] = useState({})

    const getProgress = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/getOperationsStats`, null, getHeader())
            .then(res => {
                setProgress(res.data.msg)
                console.log(res.data.msg)
            })
            .catch(err => {
                console.log(err)
            })
    }


    useEffect(() => {
        getProgress()
    }, [])

    return (
        <div className="sm:flex m-auto">
            {Object.keys(progress).map((key, index) => {
    return (
        <div key={key} className="bg-gray-200 rounded-md p-2 m-2 ">
            <p className="font-medium">{key}:</p>
            <p className="font-bold">{progress[key]}</p>
        </div>
    )
})}
            
        </div>
    )
}