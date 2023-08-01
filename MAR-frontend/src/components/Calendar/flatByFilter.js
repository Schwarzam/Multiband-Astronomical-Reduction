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

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
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

        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                this.objects = []
                toast.success("Loaded flat by filter blocks", { autoClose: 1000 });
                this.objects = this.objects.concat(res.data.msg)
                this.setObjects(calendarApi)
            })
            .catch(err => {
                toast.error("Error loading bias files");
            })
    }

    setObjects = (calendarApi) => {
        for (const key in this.objects) {
            const e = calendarApi.getEventById(`flatf${this.objects[key].id}`)
            if (e){e.remove()}

            calendarApi.addEvent({
                id: `flatf${this.objects[key].id}`,
                title: `Flat Filter ${this.objects[key].band} ${this.objects[key].id}${this.objects[key].comments != null ? ` - ${this.objects[key].comments}` : ''}`,
                start: this.objects[key].blockStartDate,
                end: this.objects[key].blockEndDate,
                color: '#ECEFF1',
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

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Processing flat by filter block ${id}`)
            })
            .catch(err => {
                toast.error(`Error processing flat by filter block ${id}`)
            })
    }

    setStatus = async (id, status) => {
        const data = {
            type: 'setstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
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

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on linked files on flatf ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on flatf ${id}`)
            })
    }

    validate = async (id) => {
        const data = {
            type: 'validate',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Changed validity of flatbyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on flatbyfilter ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Set comment of flatbyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on flatbyfilter ${id}`)
            })
    }

    add = async (id, targetId) => {
        const data = {
            type: 'add',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Added individual ${targetId} of flatbyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error adding individual ${targetId} on flatbyfilter ${id}`)
            })
    }

    remove = async (id, targetId) => {
        const data = {
            type: 'remove',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/flatbyfilter`, data, getHeader())
            .then(res=>{
                toast.success(`Removed individual ${targetId} of flatbyfilter ${id}`)
            })
            .catch(err => {
                toast.error(`Error removing individual ${targetId} on flatbyfilter ${id}`)
            })
    }

}

export default FlatByFilter