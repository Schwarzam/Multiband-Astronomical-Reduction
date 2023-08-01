import { useEffect, useState } from "react";
import axios from "axios";
import { getHeader } from "../Login/auth";

import { toast } from 'react-toastify'
import QueryMaker from "./query";

import { FinalContainer } from "../Container/finaltile";
import { IndividualContainer } from "../Container/individual";
import { GenericalContainer } from "../Container/generical";

import Logs from "./logs";
import ArrowButton from "./arrow";

export default function RawQuery() {
    const [query, setQuery] = useState('')
    const [res, setRes] = useState([])
    const [resQuery, setResQuery] = useState('')

    const [pairs, setPairs] = useState([{ key: 'type', value: '' }]);
    const [link, setLink] = useState('');

    const [type, setType] = useState('')
    const links = [
        'finaltiles',
        'individualfile',
        'superflat',
        'fieldimages',
        'biasblock',
        'sciblock',
        'flatblock',
        'scibyfilter',
        'flatbyfilter',
    ]; // replace these with your links

    const [filter, setFilter] = useState('');

    const handleChangeFilter = (e) => {
        setFilter(e.target.value);
    };

    const filteredData = res.filter((item) =>
        JSON.stringify(item).toLowerCase().includes(filter.toLowerCase())
    );

    const handleLinkChange = (event) => {
        setLink(event.target.value);
    };

    const handlePairChange = (index, key, value, ignore) => {
        const newPairs = [...pairs];
        newPairs[index] = { key, value, ignore };
        setPairs(newPairs);
    };

    const handleIgnoreChange = (index, event) => {
        const newPairs = [...pairs];
        newPairs[index].ignore = event.target.checked;
        setPairs(newPairs);
    };

    const handleAddPair = () => {
        setPairs([...pairs, { key: '', value: '' }]);
    };

    const handleRemovePair = (index) => {
        const newPairs = [...pairs];
        newPairs.splice(index, 1);
        setPairs(newPairs);
    };

    const execute = (event) => {
        event.preventDefault();

        const data = pairs.reduce((obj, pair) => {
            if (!pair.ignore) {
                obj[pair.key] = pair.value;
            }
            return obj;
        }, {});

        const toastId = toast.loading('Executing search...');
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/${link}`, data, getHeader())
            .then(res => {
                toast.dismiss(toastId);
                if (res.data.error || res.data.status === false) {
                    toast.error("Error with query!")
                    toast.error(res.data.msg)
                    return
                }
                if (typeof res.data.msg === 'string') {
                    toast.success(res.data.msg)
                } else {
                    setType(link)
                    setRes(res.data.msg)
                    setResQuery(res.data.query)
                }
            })

            .catch(err => {
                toast.dismiss(toastId);
                toast.error('Error executing query')
            })
    }

    // Dropdown options
    const options = {
        type: [
            "get",
            "create",
            "process",
            "processfield",
            "setstatus",
            "setsubstatus",
            "validate",
            "setflag",
            "setsuperflat",
            "register"
        ],
    };

    return (
        <div>
            <ArrowButton>
                <Logs />
            </ArrowButton>


            <div className="flex flex-col items-center space-y-4 py-12">
                <div className="space-y-2">
                    {pairs.map((pair, index) => (
                        <div key={index} className="flex space-x-2 items-center">
                            <input
                                type="checkbox"
                                checked={pair.ignore}
                                onChange={(e) => handleIgnoreChange(index, e)}
                            />
                            <input
                                value={pair.key}
                                onChange={(e) => handlePairChange(index, e.target.value, pair.value, pair.ignore)}
                                placeholder="Key"
                                className="border-2 border-gray-200 rounded px-3 py-2 flex-grow"
                            />
                            {pair.key in options ? (
                                <select
                                    value={pair.value}
                                    onChange={(e) => handlePairChange(index, pair.key, e.target.value, pair.ignore)}
                                    className="w-full h-10 outline shadow-sm border-gray-300 rounded px-3 py-2 flex-grow"
                                >
                                    <option value="">Select a value</option>
                                    {options[pair.key].map((option, i) => (
                                        <option key={i} value={option}>{option}</option>
                                    ))}
                                </select>
                            ) : (
                                <input
                                    value={pair.value}
                                    onChange={(e) => handlePairChange(index, pair.key, e.target.value, pair.ignore)}
                                    placeholder="Value"
                                    className="border-2 border-gray-200 rounded px-3 py-2 flex-grow"
                                />
                            )}
                            <button onClick={() => handleRemovePair(index)} className="px-3 py-2 bg-red-400 text-white rounded">Remove</button>
                        </div>
                    ))}
                    <button onClick={handleAddPair} className="px-3 py-2 bg-blue-400 text-white rounded">Add pair</button>
                </div>
                <select value={link} onChange={handleLinkChange} className="w-full outline w-[200px] h-10 shadow-sm border-gray-300 rounded px-3 py-2">
                    <option value="">Select link</option>
                    {links.map((link, index) => <option key={index} value={link}>{link}</option>)}
                </select>
                <button onClick={(e) => execute(e)} className="px-3 py-2 bg-blue-400 text-white rounded">Send Request</button>

                <input
                    type="text"
                    className="mb-4 px-3 py-2 border border-gray-300 rounded-lg m-auto"
                    placeholder="Filter data..."
                    value={filter}
                    onChange={handleChangeFilter}
                />
            </div>


            <div className="max-w-7xl m-auto">
                {type === 'finaltiles' && <FinalContainer data={filteredData} header={"Search result"} />}


                {type !== 'finaltiles' && <GenericalContainer data={filteredData} header={"Search result"} />}


            </div>
        </div>
    )
}
