import axios from 'axios'
import { toast } from 'react-toastify';
import { getHeader } from "../Login/auth";

class FlatBlock{
    objects = []

    getObjectById = async (id) => {
        if(!id){id = 1}
        const result = []
        const data = {
            type: 'get',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
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

        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success("Loaded flat blocks", { autoClose: 1000 });
                this.objects = this.objects.concat(res.data.msg)
                this.setObjects(calendarApi)
            })
            .catch(err => {
                toast.error("Error loading flat files");
            })
    }

    setObjects = (calendarApi) => {
        for (const key in this.objects) {
            const e = calendarApi.getEventById(`flat${this.objects[key].id}`)
            if (e !== null){e.remove()}

            calendarApi.addEvent({
                id: `flat${this.objects[key].id}`,
                title: `FLATS ${this.objects[key].id}${this.objects[key].comments != null ? ` - ${this.objects[key].comments}` : ''}`,
                start: this.objects[key].blockStartDate,
                end: this.objects[key].blockEndDate,
                color: '#FFE5D9',
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

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Processing flat block ${id}`)
            })
            .catch(err => {
                toast.error(`Error processing flat block ${id}`)
            })
    }

    setStatus = async (id, status) => {
        const data = {
            type: 'setstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on flatbl ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on flatbl ${id}`)
            })
    }

    setSubStatus = async (id, status) => {
        const data = {
            type: 'setsubstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on linked files on flat ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on flat ${id}`)
            })
    }

    validate = async (id) => {
        const data = {
            type: 'validate',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Changed validity of flatblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on flatblock ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set comment of flatblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on flatblock ${id}`)
            })
    }

    add = async (id, targetId) => {
        const data = {
            type: 'add',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Added flatf ${targetId} of flatblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error adding flatf ${targetId} on flatblock ${id}`)
            })
    }

    remove = async (id, targetId) => {
        const data = {
            type: 'remove',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatblock`, data, getHeader())
            .then(res=>{
                toast.success(`Removed flatf ${targetId} of flatblock ${id}`)
            })
            .catch(err => {
                toast.error(`Error removing flatf ${targetId} on flatblock ${id}`)
            })
    }

}

export default FlatBlock