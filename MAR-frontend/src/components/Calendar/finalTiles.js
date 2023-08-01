import axios from 'axios'
import { toast } from 'react-toastify';
import { getHeader } from "../Login/auth";

class FinalTiles {
    objects = []
    schedules = {}

    getObjectById = async (id) => {
        const result = []
        const data = {
            type: 'get',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                try { res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null")) }
                catch { }
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

        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                try { res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null")) }
                catch { }
                toast.success("Loaded coadded files", { autoClose: 1000 });
                if (res.status) {
                    this.objects = []
                    this.schedules = {}
                    this.objects = this.objects.concat(res.data.msg)
                    let date, dateIso;
                    let updated = false;
                    this.objects.forEach(obj => (
                        date = new Date(obj.date),
                        (!isNaN(date.getTime())
                            ?
                            (dateIso = date.toISOString().substring(0, 10),
                                (!this.schedules[dateIso] ? this.schedules[dateIso] = 1
                                    :
                                    this.schedules[dateIso] = this.schedules[dateIso] + 1),
                                updated = true)
                            :
                            console.log('detected invalid date'))
                    ))
                    if (updated) {
                        this.setObjects(calendarApi)
                    }
                }
            })
            .catch(err => {
                toast.error("Error loading coadded files");
            })
    }

    processObjectById = async (id) => {
        const data = {
            type: 'process',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                toast.success(`Processing finaltile ${id}`)
            })
            .catch(err => {
                toast.error(`Error processing finaltile ${id}`)
            })
    }

    setSubStatus = async (id, status) => {
        const data = {
            type: 'setsubstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                toast.success(`Set status on linked files on finaltile ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on finaltile ${id}`)
            })
    }

    setObjects = (calendarApi) => {
        for (const [key, value] of Object.entries(this.schedules)) {
            const e = calendarApi.getEventById(`fin${new Date(key).toISOString()}`)
            if (e !== null) { e.remove() }

            calendarApi.addEvent({
                id: `fin${new Date(key).toISOString()}`,
                title: `${value} Coadded`,
                date: key,
                color: '#A7D3E8',
                textColor: 'black',
                allDay: true
            });
        }
    }

    getFromDate = async (dateReq) => {
        var date = new Date(dateReq);

        const startDate = date.toISOString().substring(0, 10)
        const endDate = date.toISOString().substring(0, 10)

        const result = []
        const data = {
            type: 'get',
            startDate: startDate,
            endDate: endDate
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                var date
                try { res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null")) }
                catch { }
                res.data.msg.forEach(obj => (
                    date = new Date(obj.date),
                    (!isNaN(date.getTime()) ? result.push(obj) : null)
                ))
            })
        return result
    }

    validate = async (id) => {
        const data = {
            type: 'validate',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                toast.success(`Changed validity of finaltile ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on finaltile ${id}`)
            })
    }

    flag = async (id, flag) => {
        const data = {
            type: 'setflag',
            id: id,
            flag: flag
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                toast.success(`Changed flag of finaltile ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing flag on finaltile ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/finaltiles`, data, getHeader())
            .then(res => {
                toast.success(`Set comment of finaltile ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on finaltile ${id}`)
            })
    }
}

export default FinalTiles
