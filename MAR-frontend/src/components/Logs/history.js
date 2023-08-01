import { useEffect, useState } from "react";
import axios from "axios";
import { getHeader } from "../Login/auth";
import { toast } from "react-toastify";

import { Link } from 'react-router-dom'

export default function Ophistory() {

    const [operations, setOperations] = useState([])
    const [selectedFileContent, setSelectedFileContent] = useState("")
    const [selectedOperationIndex, setSelectedOperationIndex] = useState(null)

    const [criticalCount, setCriticalCount] = useState(0)
    const [warnCount, setWarnCount] = useState(0)

    const getOperations = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/getOperations`, {}, getHeader())
            .then(res => {
                setOperations(res.data.msg)
            })
    }
    const loadFile = (url, index) => {
        const toastId = toast.loading('Loading file...');
        axios.get(url, getHeader())
            .then(res => {
                toast.dismiss(toastId);
                setSelectedFileContent(res.data);
                setSelectedOperationIndex(index);
                setCriticalCount((res.data.match(/CRITICAL/g) || []).length);
                setWarnCount((res.data.match(/WARN/g) || []).length);
            })
    }

    useEffect(() => {
        getOperations()
    }, [])

    return (
        <div className="py-16 max-w-3xl m-auto">


            <div className="max-w-2xl m-auto">
                <p className="font-bold text-2xl">Past operations</p>
                <div className="flex items-center justify-between flex-wrap">
                    <div className="w-0 flex-1 flex items-center">
                        <span className="flex p-2 rounded-lg">
                            ID
                        </span>
                        <p className="ml-3 font-medium truncate px-10">
                            <span >EndDate</span>
                        </p>
                        <p className="ml-3 font-medium truncate px-4">
                            <span >Description(function, block, code)</span>
                        </p>
                    </div>
                </div>
                {operations.map((item, index) => (
                    <div key={index} className="border p-2 my-1 rounded">
                        <div className="flex items-center justify-between flex-wrap">
                            <div className="w-0 flex-1 flex items-center">
                                <span className="flex p-2 rounded-lg">
                                    {item.id}
                                </span>
                                <p className="ml-3 font-medium truncate px-4">
                                    <span>{item.endDate}</span>
                                </p>
                                <p className="ml-3 font-medium truncate px-4">
                                    <span>{item.block}</span>
                                </p>

                                <p className="ml-3 font-medium truncate px-6">
                                    <span>{item.operation}</span>
                                </p>
                            </div>
                            <div className="order-2 flex-shrink-0 sm:order-3 sm:ml-2">
                                <button type="button" onClick={() => loadFile(`${process.env.REACT_APP_SERVER_IP.replace('8002', '3001')}/media/${item.logPath}`, index)} className="-mr-1 flex p-2 rounded-md hover:bg-indigo-300 focus:outline-none focus:ring-2 focus:ring-white">
                                    <span className="">View</span>
                                </button>
                                <button type="button" className="-mr-1 flex p-2 rounded-md hover:bg-indigo-300 focus:outline-none focus:ring-2 focus:ring-white">
                                    <a className="text-blue-600" href={`${process.env.REACT_APP_SERVER_IP}/media/${item.logPath}`} target="_blank" download>Download</a>
                                </button>
                            </div>
                            {index === selectedOperationIndex &&
                                <div style={{ maxHeight: '400px', overflowY: 'scroll' }}>
                                    {selectedFileContent.split('\n').map((line, lineIndex) => {
                                        let color;
                                        if (line.includes('CRITICAL')) {
                                            color = 'red';
                                        } else if (line.includes('WARN')) {
                                            color = 'orange';
                                        }
                                        return <pre className="text-[9px]" key={lineIndex} style={{ color: color }}>{line}</pre>
                                    })}
                                </div>
                            }
                            {index === selectedOperationIndex &&
                                <div>
                                    <p className="flex" style={{ color: 'red' }}><span role="img" aria-label="Critical Icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                                    </svg>
                                    </span>: {criticalCount}</p>
                                    <p className="flex" style={{ color: 'orange' }}><span role="img" aria-label="Warning Icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                                    </svg>
                                    </span>: {warnCount}</p>
                                </div>
                            }

                        </div>
                    </div>
                ))}
                <div className="bg-gray-300 rounded">
                    <p className="font-bold p-4">{(operations.length < 1) && 'No operations done'}</p>
                    <pre>{selectedFileContent}</pre>
                </div>

            </div>
        </div>
    )
}
