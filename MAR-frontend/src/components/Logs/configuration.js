
import {useEffect, useState} from "react";
import axios from "axios";
import {getHeader} from "../Login/auth";

import { toast } from 'react-toastify'

export default function Config(){

    const [config, setConfig] = useState({})

    const getConfig = () => {
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/getConf`, null, getHeader())
            .then(res => {
                setConfig(res.data.msg)
            })
            .catch(err => {
                toast.error('Error getting config.')
            })
    }

    useEffect(() => {
        getConfig()
    }, [])

    const changeConf = (section, item, value) => {
        
        var tmp = JSON.parse(JSON.stringify(config))
        tmp[section][item] = value
        setConfig(tmp)

    }

    const handleKeyDown = (e, section, item) => {
        if (e.key === 'Enter'){
            console.log(e.target.value, section, item)
            const data = {section: section, item: item, value: e.target.value}
            axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/setItemConf`, data, getHeader())
                .then(res => {
                    toast(res.data.msg)
                })
                .catch(err => {
                    toast.error('Error changing value.')
                })
        }
    } 

    

    return(
        <div className="m-auto max-w-xl mt-8">
            <p>Press "Enter" to change value.</p>
            <small>Change MAR library configs in real time.</small>
            <div>
                {Object.keys(config).map(key => (
                    <div key={key} className="py-4">
                        <p className="font-bold text-xl">{key}</p>
                        {Object.keys(config[key]).map(subkey => (
                            <div key={subkey} className="flex">
                                <p className="ml-8">{subkey}</p>
                                <input className="text-rose-700 mx-4 border-b outline-none border-black" onKeyDown={(e) => handleKeyDown(e, key, subkey)} onChange={(e) => changeConf(key, subkey, e.target.value)} value={config[key][subkey]}></input>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    )
}