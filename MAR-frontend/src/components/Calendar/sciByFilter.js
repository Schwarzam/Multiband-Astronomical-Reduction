import axios from 'axios'
import { toast } from 'react-toastify';
import { getHeader } from "../Login/auth";

class FlatByFilter{
    objects = []


    getObjectById = async (id) => {
        if(!id){id = 1}
        const result = []
        const data = {
            type: 'get',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
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

        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                try{res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null"))}
                catch{}
                
                toast.success("Loaded sci by filter blocks", { autoClose: 1000 });
                this.objects = this.objects.concat(res.data.msg)
                this.setObjects(calendarApi)
            })
            .catch(err => {
                console.log(err)
                toast.error("Error loading sci by filter files");
            })
    }

    setObjects = (calendarApi) => {
        for (const key in this.objects) {
            const e = calendarApi.getEventById(`scif${this.objects[key].id}`)
            if (e !== null){e.remove()}

            calendarApi.addEvent({
                id: `scif${this.objects[key].id}`,
                title: `Sci Filter ${this.objects[key].band} ${this.objects[key].id}${this.objects[key].comments != null ? ` - ${this.objects[key].comments}` : ''}`,
                start: this.objects[key].blockStartDate,
                end: this.objects[key].blockEndDate,
                color: '#C2C2C2',
                textColor: 'black'
            });
        }
    }

    processObjectById = async (id, code) => {
        var data = {
            type: 'process',
            id: id
        }

        if (code.trim() !== ''){
            data['code'] = code
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Processing sci by filter block ${id}`)
            })
            .catch(err => {
                toast.error(`Error processing sci by filter block ${id}`)
            })
    }

    setStatus = async (id, status) => {
        const data = {
            type: 'setstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on scif ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on scif ${id}`)
            })
    }

    setSubStatus = async (id, status) => {
        const data = {
            type: 'setsubstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on linked files on scif ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on scif ${id}`)
            })
    }

    validate = async (id) => {
        const data = {
            type: 'validate',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Changed validity of scibyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on scibyfilter ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Set comment of scibyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on scibyfilter ${id}`)
            })
    }

    add = async (id, targetId) => {
        const data = {
            type: 'add',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Added individual ${targetId} of scibyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error adding individual ${targetId} on scibyfilter ${id}`)
            })
    }

    remove = async (id, targetId) => {
        const data = {
            type: 'remove',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scibyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Removed individual ${targetId} of scibyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error removing individual ${targetId} on scibyfilter ${id}`)
            })
    }

}

export default FlatByFilter