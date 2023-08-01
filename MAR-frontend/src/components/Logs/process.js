import {useEffect, useState} from "react";
import axios from "axios";
import {getHeader} from "../Login/auth";
import {toast} from "react-toastify";


export default function Process(){
    const [logs, setLogs] = useState(null)
    const [logsC, setLogsC] = useState('indigo')
    const [status, setStatus] = useState(null)
    const [statusC, setStatusC] = useState('indigo')

    const getProcess = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/get_process`, null, getHeader())
            .then(res => {
                setLogs(res.data.msg)
                if (res.data.msg !== 'Available'){
                    setLogsC('green')
                }else{
                    setLogsC('indigo')
                }
                setStatus('online')
                setStatusC('#D7E2C6')
            })
            .catch(err => {
                setLogs('offline')
                setLogsC('#FFE5D9')
                setStatus('offline')
                setStatusC('#FFE5D9')
            })
    }

    const resetT = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/reset_threads`, null, getHeader())
            .then(res => {
                toast.success(res.data.msg)
            })
            .catch(err => {
                toast.error(`error reseting threads`)
            })
    }



    useEffect(() => {
        getProcess()
        const interval = setInterval(() => {
            getProcess()
          }, 100000);
          return () => clearInterval(interval);
    }, [])

    return (
        <div className="m-auto mb-6">

            <div>
                <div className="bg-[#FFE5D9] bg-[#D7E2C6] bg-orange-600 bg-green-300 bg-indigo-300 bg-orange-300"></div>
                
                <div className="mt-6 grid grid-cols-2 gap-0.5 lg:mt-8 m-auto">
                    <div className={`rounded col-span-1 bg-[${statusC}] flex justify-center py-8 px-8 bg-gray-50`}>
                        Server Status: {status}
                    </div>
                    <div className={`rounded col-span-1 bg-[${statusC}] flex justify-center py-8 px-8 bg-gray-50`}>
                        Server Process: {logs}
                    </div>
                </div>
                
                <div className="grid grid-cols-2 gap-0.5 lg:mt-8 m-auto">
                    <button onClick={() => getProcess()} className={`items-center px-2 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gray-400`}>
                        Refresh
                    </button>

                    <button onClick={() => (window.confirm(`All processes will be lost, proceed?`) && resetT())} className={`items-center px-2 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-[#282828]`}>
                        Reset Threads
                    </button>
                </div>
            </div>

        </div>
    )
}