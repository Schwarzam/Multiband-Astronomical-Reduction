import Icon from "../Icons";
import React, {useEffect, useState} from "react";
import axios from "axios";
import {getHeader} from "../Login/auth";
import {toast} from "react-toastify";

const useCreateBlock = (popUp) => {

    const [disable, setDisable] = useState(false)
    const [selected, setSelected] = useState('bias')

    const [startDate, setStartDate] = useState('')
    const [endDate, setEndDate] = useState('')
    const [band, setBand] = useState('')

    const [nameContains, setNameContains] = useState('')

    const onSelect = (e) => {
        setSelected(e.target.value)
    }

    function showBand() {
        if (selected === 'scif' || selected === 'flatf'){
            return (
                <div>
                    <span>Band: </span>
                    <input value={band} onChange={(e) => setBand(e.target.value.toUpperCase())} className="p-2 rounded bg-gray-300 mt-2 w-24" placeholder="F..." />
                </div>
            )
        }
    }

    const create = () =>{
        setDisable(true)
        const data = {
            type: 'create',
            startDate: startDate,
            endDate: endDate,
            band: band
        }

        if (nameContains.trim() !== ''){
            data['nameContains'] = nameContains
        }

        let link;
        if(selected === 'bias'){ link = 'reduction/biasblock'}
        if(selected === 'flatf'){ link = 'reduction/flatbyfilter'}
        if(selected === 'flat'){ link = 'reduction/flatblock'}
        if(selected === 'scif'){ link = 'reduction/scibyfilter'}
        if(selected === 'sci'){ link = 'reduction/sciblock'}

        const loa = toast.loading('Creating block, this might take a while...')
        axios.post(`${process.env.REACT_APP_SERVER_IP}/${link}`, data, getHeader())
            .then(res=>{
                setDisable(false)
                toast(res.data.msg)
                toast.dismiss(loa)
            })
            .catch(err => {
                setDisable(false)
                console.log(err)
                toast.error('Error creating block')
                toast.dismiss(loa)
            })
    }

    useEffect(() => {
        setSelected('bias')
    }, [popUp])

    return (
        <div>
            <h1>Create a block</h1>

            <select onChange={(e) => onSelect(e)} className="p-2 rounded bg-gray-200 mt-4">
                <option value="bias">Bias Block</option>
                <option value="flatf">Flat Block By Filter</option>
                <option value="flat">Flat Block (all filters)</option>
                <option value="scif">Sci Block By Filter</option>
                <option value="sci">Sci Block (all filters)</option>
            </select>

            <br/>

            <span>Start date: </span>
            <input onChange={(e) => setStartDate(e.target.value)} className="p-2 rounded bg-gray-300 mt-8" placeholder="YYYY-MM-DD" />
            <br/>
            <span>End date: </span>
            <input onChange={(e) => setEndDate(e.target.value)} className="p-2 rounded bg-gray-300 mt-2" placeholder="YYYY-MM-DD" />

            {showBand()}

            <br/>
            <span>Contains in object name: </span>
            <input onChange={(e) => setNameContains(e.target.value)} className="p-2 rounded bg-gray-300 mt-2" placeholder="Search for objects that contains" />


            <br/>
            <button onClick={() => create()} disabled={disable} className="p-4 bg-slate-300 mt-8 rounded">Create Block</button>
        </div>
    )
}

export default useCreateBlock