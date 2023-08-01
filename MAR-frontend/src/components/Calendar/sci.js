import axios from 'axios'
import { toast } from 'react-toastify';
import { getHeader } from "../Login/auth";

class SciBlock{
    objects = []

    getObjectById = async (id) => {
        console.log("teiii")
        if(!id){id = 1}
        const result = []
        const data = {
            type: 'get',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                try{res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null"))}
                catch{}
                result.push(res.data.msg[0])
            })

        return result
    }

    async getObjectByDateCalendar(startDate, endDate, calendarApi) {
        const data = {
            type: 'get',
            startDate: startDate,
            endDate: endDate
        }

        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                try{res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null"))}
                catch{}
                toast.success("Loaded sci blocks", { autoClose: 1000 });
                this.objects = this.objects.concat(res.data.msg)
                this.setObjects(calendarApi)
            })
            .catch(err => {
                toast.error("Error loading sci files");
            })
    }

    setObjects = (calendarApi) => {
        for (const key in this.objects) {
            const e = calendarApi.getEventById(`sci${this.objects[key].id}`)
            if (e !== null){e.remove()}

            calendarApi.addEvent({
                id: `sci${this.objects[key].id}`,
                title: `SCIES ${this.objects[key].id}${this.objects[key].comments != null ? ` - ${this.objects[key].comments}` : ''}`,
                start: this.objects[key].blockStartDate,
                end: this.objects[key].blockEndDate,
                color: '#D7E2C6',
                textColor: 'black'
            });
        }
    }

    processObjectById = async (id, code) => {
        const data = {
            type: 'process',
            id: id
        }

        if (code.trim() !== ''){
            data['code'] = code
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Processing sci block ${id}`)
            })
            .catch(err => {
                toast.error(`Error processing sci block ${id}`)
            })
    }

    setStatus = async (id, status) => {
        const data = {
            type: 'setstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on scibl ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on scibl ${id}`)
            })
    }

    setSubStatus = async (id, status) => {
        const data = {
            type: 'setsubstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on linked files on sci ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on sci ${id}`)
            })
    }

    validate = async (id) => {
        const data = {
            type: 'validate',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Changed validity of sciblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on sciblock ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set comment of sciblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on sciblock ${id}`)
            })
    }

    add = async (id, targetId) => {
        const data = {
            type: 'add',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Added scif ${targetId} of sciblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error adding scif ${targetId} on sciblock ${id}`)
            })
    }

    remove = async (id, targetId) => {
        const data = {
            type: 'remove',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/sciblock`, data, getHeader())
            .then(res=>{
                toast.success(`Removed scif ${targetId} of sciblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error removing scif ${targetId} on sciblock ${id}`)
            })
    }

}

export default SciBlock