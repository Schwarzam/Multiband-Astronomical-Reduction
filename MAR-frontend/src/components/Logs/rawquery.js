import {useEffect, useState} from "react";
import axios from "axios";
import {getHeader} from "../Login/auth";

import {toast} from 'react-toastify'
import QueryMaker from "./query";

export default function RawQuery(){
    const [query, setQuery] = useState('')
    const [res, setRes] = useState('')
    const [resQuery, setResQuery] = useState('')

    const execute = () => {
        const data = {query}

        const toastId = toast.loading('Executing query...');
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/rawQuery`, data, getHeader())
            .then(res => {
                toast.dismiss(toastId);
                if (res.data.error){
                    toast.error("Error with query!")
                    return
                }
                setRes(res.data.msg)
                setResQuery(res.data.query)
            })

            .catch(err => {
                toast.dismiss(toastId);
                toast.error('Error executing query')
            })
    }

    return(
        <div>
            <QueryMaker setQuery={setQuery} />


            <div className="max-w-2xl m-auto py-16">   
                <p>Perform query</p>
                <textarea 
                    className="border-2 w-full rounded p-1 h-32"
                    rows={4}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button className="p-2 bg-neutral-400 rounded" onClick={() => execute()}>Submit</button>

            </div>

            {res !== '' && (
                <div className="max-w-2xl m-auto py-16">   
                    
                    <p>Response to query:</p>
                    <p>{resQuery}</p>
                    <button className="bg-neutral-200 p-3 rounded">
                        <a href={`${process.env.REACT_APP_SERVER_IP}/media/${res}`} download>Download</a>
                    </button>
                </div>
            )}

            
            
        </div>
    )
}