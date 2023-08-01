import React, {useContext, useEffect, useState} from 'react'
import FullCalendar from '@fullcalendar/react' // must go before plugins
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'


import IndividualObjects from "./IndividualObjects"; // a plugin!
import BiasBlock from "./biasBlock";


import dayjs from 'dayjs'
import {useValidadeLogin} from "../Login/auth";
import { PopUpContext } from '../PopUp/context';
import DayInfoContext from '../DayInfo/context';
import PopUp from '../PopUp';
import useDayInfo from "../DayInfo";
import FlatByFilter from "./flatByFilter";
import SciByFilter from "./sciByFilter";
import FinalTiles from "./finalTiles";
import Icon from "../Icons";
import CreateBlock from "./createBlock";
import useCreateBlock from "./createBlock";
import FlatBlock from "./flat";
import SciBlock from "./sci";

export default function CalendarComponent() {

    const calendarRef = React.createRef()

    const { openPopUp, setOpenPopUp } = useContext(PopUpContext)
    const { dayInfo, setDayInfo } = useContext(DayInfoContext)
    const [ type, setType ] = useState(null)
    const [ targetId, setTargetId ] = useState(null)
    const [ calendar, setCalendar ] = useState(null)
    const [ popUp, setPopUp ] = useState(false)

    const [loadUpdate, setLoadUpdate] = useState(false)

    const [ sciC, setSciC ] = useState(false)
    const [ scifC, setScifC ] = useState(false)
    const [ flatC, setFlatC ] = useState(false)
    const [ flatfC, setFlatfC ] = useState(false)
    const [ biasC, setBiasC ] = useState(false)
    const [ indC, setIndC ] = useState(false)
    const [ finalC, setFinalC ] = useState(false)

    useValidadeLogin()
    let individuals = new IndividualObjects()
    let biasbl = new BiasBlock()
    let flatbyf = new FlatByFilter()
    let scibyf = new SciByFilter()
    let final = new FinalTiles()
    let scibl = new SciBlock()

    let flatbl = new FlatBlock()

    useEffect(() => {
        setCalendar(calendarRef.current.getApi())
    }, [])

    const load = async () => {
        if (calendar){
            var start = dayjs(calendar.getDate()).subtract(1, 'month')
            var end = dayjs(calendar.getDate()).add(1, 'month')
            start = start.toISOString().substring(0, 10)
            end = end.toISOString().substring(0, 10)

            if (indC){
                await individuals.getObjectByDateCalendar(start, end, calendar)
            }
            if (biasC){
                await biasbl.getObjectByDateCalendar(start, end, calendar)
            }
            if (flatfC){
                await flatbyf.getObjectByDateCalendar(start, end, calendar)
            }
            if (scifC){
                await scibyf.getObjectByDateCalendar(start, end, calendar)
            }
            if (finalC){
                await final.getObjectByDateCalendar(start, end, calendar)
            }
            if (flatC) {
                await flatbl.getObjectByDateCalendar(start, end, calendar)
            }
            if (sciC) {
                await scibl.getObjectByDateCalendar(start, end, calendar)
            }
            
            setLoadUpdate(!loadUpdate)
        }
    }

    //calendar.gotoDate( date ) -> Para ir ate uma data
    const handleEventClick = (e) => {
        if (e.event.title.includes('Individual')){
            setType('individual')
            setOpenPopUp(true)
            setDayInfo(dayjs(e.event.startStr, "YYYY-MM-DD"))
        }
        if (e.event.title.includes('Coadded')){
            setType('fin')
            setOpenPopUp(true)
            setDayInfo(dayjs(e.event.startStr, "YYYY-MM-DD"))
        }
        if (e.event.title.includes('BIAS')){
            setType('bias')
            setOpenPopUp(true)
            setTargetId(e.event.id.replace('bias', ''))
        }
        if (e.event.title.includes('Flat')){
            setType('flatf')
            setOpenPopUp(true)
            setTargetId(e.event.id.replace('flatf', ''))
        }
        if (e.event.title.includes('FLAT')){
            setType('flat')
            setOpenPopUp(true)
            setTargetId(e.event.id.replace('flat', ''))
        }
        if (e.event.title.includes('Sci')){
            setType('scif')
            setOpenPopUp(true)
            setTargetId(e.event.id.replace('scif', ''))
        }
        if (e.event.title.includes('SCIES')){
            setType('sci')
            setOpenPopUp(true)
            setTargetId(e.event.id.replace('sci', ''))
        }
    }

    const openDayPopUp = (date) => {
        setType(null)
        setOpenPopUp(true)
        setDayInfo(date)
    }

    const dayInfoComp = useDayInfo({ dayInfo, setDayInfo, type, targetId, loadUpdate })
    const createBlock = useCreateBlock(popUp)

    return (
        <div className='mt-0 h-auto'>
            
            <div className='rounded px-8 py-16 bg-gray-100 m-auto mb-6 grid-cols-2 grid'>
              <div>
                <p>Objects to be loaded in calendar: </p>
                <p className='text-sm'>Use this to optimize the time loading objects.</p>
              </div>
              
              <div>
              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {biasC}
                    onChange={(e) => setBiasC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    BiasBlock
                  </label>
                </div>
              </div>

              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {flatC}
                    onChange={(e) => setFlatC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    FlatBlock
                  </label>
                </div>
              </div>

              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {flatfC}
                    onChange={(e) => setFlatfC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    FlatBlocksByFilter
                  </label>
                </div>
              </div>

              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {sciC}
                    onChange={(e) => setSciC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    SciBlock
                  </label>
                </div>
              </div>

              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {scifC}
                    onChange={(e) => setScifC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    SciBlocksByFilter
                  </label>
                </div>
              </div>

              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {indC}
                    onChange={(e) => setIndC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    IndividualFiles
                  </label>
                </div>
              </div>

              <div className="relative flex items-start">
                <div className="flex items-center h-5">
                  <input
                    type="checkbox"
                    checked = {finalC}
                    onChange={(e) => setFinalC(e.target.checked)}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="comments" className="font-medium text-gray-700">
                    Coadded
                  </label>
                </div>
              </div>
              </div>
            </div>

            <FullCalendar
                ref={calendarRef}
                plugins={[dayGridPlugin, interactionPlugin]}

                dateClick={function(info) {
                    openDayPopUp(dayjs(info.dateStr, "YYYY-MM-DD"))
                }}
                eventClick = {(e) =>  handleEventClick(e)}
                headerToolbar={{
                        start: 'title', // will normally be on the left. if RTL, will be on the right
                        center: 'refresh removeAll newBlock',
                        end: 'prev,next prevYear,nextYear' // will normally be on the right. if RTL, will be on the left
                }}
                customButtons={{
                    refresh: {
                        text: "Fetch",
                        click: () => {load()}
                    },
                    removeAll: {
                      text: "Clear",
                      click: () => {calendar.removeAllEvents()}
                    },
                    newBlock: {
                        text: "New Block",
                        click: () => setPopUp(true)
                    }
                }}
            />
            {openPopUp && (
                <PopUp>
                    {dayInfoComp}
                </PopUp>
            )}
            {popUp && (
                <div className='fixed h-full w-full top-0 left-0 z-10 bg-black bg-opacity-60'>
                    <div className='flex h-screen items-center justify-center'>
                        <div className='relative rounded h-[600px] w-[900px] z-10 bg-white p-4 my-auto'>
                            <button className='absolute top-4 right-4' onClick={() => setPopUp(false)}>
                                <Icon name='x' className='h-5 text-gray-700' />
                            </button>
                            {createBlock}
                        </div>
                    </div>
                </div>
            )}
        </div>

    );
}

