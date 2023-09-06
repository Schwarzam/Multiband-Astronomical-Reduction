import { useEffect, useState } from "react";
import axios from "axios";
import { getHeader } from "../Login/auth";


export default function Logs() {
    const [logs, setLogs] = useState({})

    const getLogs = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/get_logs`, null, getHeader())
            .then(res => {
                if (!res.data.msg) { return }
                setLogs(res.data.msg)
            })
            .catch(err => {

            })
    }

    useEffect(() => {
        getLogs()
        const interval = setInterval(() => {
            getLogs()
        }, 30000);
        return () => clearInterval(interval);
    }, [])

    const clearLogs = () => {
        if (window.confirm('Clear Logs? ')) {

        }
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/clear_logs`, null, getHeader())
            .then(res => {
                getLogs()
            })
            .catch(err => {

            })
    }

    return (
        <div className="mt-6">
            <div className="bg-white">
                <div className="max-w-2xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:max-w-7xl lg:px-8">
                    <h2 className="text-2xl font-extrabold tracking-tight text-gray-900">Logs</h2>

                    <div className="flex pt-4">
                        <button onClick={() => clearLogs()} type="button" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[#242F40] hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Clear logs
                        </button>
                        <button onClick={() => getLogs()} type="button" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[#242F40] hover:bg-[#789fd9] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Refresh
                        </button>
                    </div>

                    <div className="mt-6 ">
                        {Object.entries(logs).map(([item, value]) => (
                            <div key={item} className="group relative">
                                <div className="w-full bg-gray-200 max-h-80 h-80 rounded-md overflow-hidden group-hover:opacity-75 lg:aspect-none overflow-scroll">
                                    <p>Thread {item}</p>
                                    {value.map((obj, index) => (
                                        <div key={index}>
                                            <small className={obj.toString().includes('CRITICAL') ? 'text-rose-500' : (obj.toString().includes('WARN') ? 'text-orange-500' : (obj.toString().includes("TIME")) ? 'text-sky-600 font-extrabold' : null)}>
                                                {obj.toString()}
                                            </small>
                                            <br />
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

        </div>
    )
}
