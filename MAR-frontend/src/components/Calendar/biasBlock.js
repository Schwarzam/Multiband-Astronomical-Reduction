import axios from 'axios'
import { toast } from 'react-toastify';
import { getHeader } from "../Login/auth";

class BiasBlock{
    objects = []


    getObjectById = async (id) => {
        if(!id){id = 1}
        const result = []
        const data = {
            type: 'get',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                result.push(res.data.msg[0])
            })

        return result
    }

    async getObjectByDateCalendar(startDate, endDate, calendarApi) {
        const data = {
          type: "get",
          startDate: startDate,
          endDate: endDate,
        };
      
        try {
          const res = await axios.post(
            `${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`,
            data,
            getHeader()
          );
          toast.success("Loaded bias blocks", { autoClose: 1000 });
          this.objects = this.objects.concat(res.data.msg);
          this.setObjects(calendarApi);
        } catch (err) {
          toast.error("Error loading bias files");
        }
    }

    setObjects = (calendarApi) => {
        for (const key in this.objects) {
            const e = calendarApi.getEventById(`bias${this.objects[key].id}`)
            if (e !== null){e.remove()}
            
            calendarApi.addEvent({
                id: `bias${this.objects[key].id}`,
                title: `BIAS ${this.objects[key].id}${this.objects[key].comments != null ? ` - ${this.objects[key].comments}` : ''}`,
                start: this.objects[key].blockStartDate,
                end: this.objects[key].blockEndDate,
                color: '#FFB6C1',
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

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Processing bias block ${id}`)
            })
            .catch(err => {
                toast.error(`Error processing bias block ${id}`)
            })
    }

    setStatus = async (id, status) => {
        const data = {
            type: 'setstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on bias ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on bias ${id}`)
            })
    }

    setSubStatus = async (id, status) => {
        const data = {
            type: 'setsubstatus',
            id: id,
            status: status
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set status on linked files on bias ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting status on bias ${id}`)
            })
    }

    validate = async (id) => {
        const data = {
            type: 'validate',
            id: id
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Changed validity of bias ${id}`)
            })
            .catch(err => {
                toast.error(`Error changing validity on bias ${id}`)
            })
    }

    setComment = async (id, comment) => {
        const data = {
            type: 'setcomment',
            id: id,
            comment: comment
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Set comment of bias ${id}`)
            })
            .catch(err => {
                toast.error(`Error setting comment on bias ${id}`)
            })
    }

    add = async (id, targetId) => {
        const data = {
            type: 'add',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Added individual ${targetId} of bias ${id}`)
            })
            .catch(err => {
                toast.error(`Error adding individual ${targetId} on bias ${id}`)
            })
    }

    remove = async (id, targetId) => {
        const data = {
            type: 'remove',
            id: id,
            objid: targetId
        }

        await axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/biasblock`, data, getHeader())
            .then(res=>{
                toast.success(`Removed individual ${targetId} of bias ${id}`)
            })
            .catch(err => {
                toast.error(`Error removing individual ${targetId} on bias ${id}`)
            })
    }

}

export default BiasBlock