import axios from 'axios'
import { toast } from 'react-toastify';
import { getHeader } from "../Login/auth";

class IndividualObjects {
    objects = []
    schedules = {}

    getObjectById = async (id) => {
        const result = []
        const data = {
            type: 'get',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/individualfile`, data, getHeader())
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

        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/individualfile`, data, getHeader())
            .then(res => {
                try { res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null")) }
                catch { }
                toast.success("Loaded individual files", { autoClose: 1000 });
                if (res.status) {
                    this.objects = []
                    this.schedules = {}
                    this.objects = this.objects.concat(res.data.msg)
                    let date, dateIso;
                    let updated = false;
                    this.objects.forEach(obj => (
                        date = new Date(obj.obsDate),
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
                toast.error("Error loading individual files");
            })
    }

    setObjects = (calendarApi) => {
        for (const [key, value] of Object.entries(this.schedules)) {
            const e = calendarApi.getEventById(`ind${new Date(key).toISOString()}`)
            if (e !== null) { e.remove() }

            calendarApi.addEvent({
                id: `ind${new Date(key).toISOString()}`,
                title: `${value} Individuals`,
                date: key,
                color: '#C2B280',
                textColor: 'black',
                allDay: true
            });
        }
    }

    getFromDate = async (dateReq) => {
        var date = new Date(dateReq);

        const startDate = date.toISOString().substring(0, 10)
        date.setDate(date.getDate() + 1);
        const endDate = date.toISOString().substring(0, 10)

        const result = []
        const data = {
            type: 'get',
            startDate: startDate,
            endDate: endDate
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/individualfile`, data, getHeader())
            .then(res => {
                var date
                try { res.data = JSON.parse(res.data.replace(/\bNaN\b/g, "null")) }
                catch { }
                if (!res.data.msg) { return }
                res.data.msg.forEach(obj => (
                    date = new Date(obj.obsDate),
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

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/individualfile`, data, getHeader())
            .then(res => {
                toast.success(`Changed validity of individualfile ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on individualfile ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/individualfile`, data, getHeader())
            .then(res => {
                toast.success(`Set comment of individualfile ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on individualfile ${id}`)
            })
    }
}

export default IndividualObjects
