import {useEffect, useState} from "react";
import axios from "axios";
import {getHeader} from "../Login/auth";

import {toast} from 'react-toastify'

export default function Queue(){
    const [queue, setQueue] = useState([])

    const getQueue = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/get_queue`, null, getHeader())
            .then(res => {
                setQueue(res.data.msg)
            })
            .catch(err => {

            })
    }

    const removeFromQueue = (id) => {
        const data = {id}
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/removeQueue`, data, getHeader())
            .then(res => {
                toast(res.data.msg)
            })
            .catch(err => {

            })
    }

    useEffect(() => {
        getQueue()
        const interval = setInterval(() => {
            getQueue()
          }, 60000);
          return () => clearInterval(interval);
    }, [])


    return (
        <div className="py-4">
            <div className="max-w-2xl m-auto">
                <p className="font-bold text-2xl">Queue</p>
                <div className="flex items-center justify-between flex-wrap">
                    <div className="w-0 flex-1 flex items-center">
                        <span className="flex p-2 rounded-lg">
                            ID
                        </span>
                        <p className="ml-3 font-medium truncate px-4">
                            <span>Function</span>
                        </p>
                        <p className="ml-3 font-medium truncate px-4">
                            <span>Block</span>
                        </p>

                        <p className="ml-3 font-medium truncate px-4">
                            <span>Code</span>
                        </p>
                    </div>
                </div>
                {queue.map((item, index) => (
                    <div key={index} className="bg-gray-300 grid-col-3 p-2">
                        <div className="flex items-center justify-between flex-wrap">
                            <div className="w-0 flex-1 flex items-center">
                                <span className="flex p-2 rounded-lg">
                                    {item.id}
                                </span>
                                <p className="ml-3 font-medium truncate px-10">
                                    <span>{item.function}</span>
                                </p>
                                <p className="ml-3 font-medium truncate px-4">
                                    <span>{item.block}</span>
                                </p>

                                <p className="ml-3 font-medium truncate px-10">
                                    <span>{item.block}</span>
                                </p>
                            </div>
                            
                            <div className="order-2 flex-shrink-0 sm:order-3 sm:ml-2">
                            <button type="button" onClick={() => removeFromQueue(item.id)} className="-mr-1 flex p-2 rounded-md hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-white">
                                <span className="sr-only">Dismiss</span>
                                    <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                            </button>
                            </div>
                        </div>
                    </div>
                ))}
                <div className="bg-gray-300 rounded">
                    <p className="font-bold p-4">{(queue.length < 1) && 'Queue empty'}</p>
                </div>
                
            </div>
        </div>
    )
}