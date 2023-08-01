import React, {useContext, useEffect, useState} from 'react'
import Icon from '../Icons'
import dayjs from 'dayjs'
import IndividualObjects from "../Calendar/IndividualObjects";
import { toast } from 'react-toastify';

import DataTable from 'react-data-table-component';
import BiasBlock from "../Calendar/biasBlock";
import FlatByFilter from "../Calendar/flatByFilter";
import SciByFilter from "../Calendar/sciByFilter";
import FinalTiles from "../Calendar/finalTiles";
import {IndividualContainer} from "../Container/individual";
import {BiasContainer} from "../Container/bias";
import {FlatFContainer} from "../Container/flatbyfilter";
import {SciFContainer} from "../Container/scibyfilter";
import FlatBlock from "../Calendar/flat";
import {FlatContainer} from "../Container/flat";
import SciBlock from "../Calendar/sci";
import {SciContainer} from "../Container/sci";
import {FinalContainer} from "../Container/finaltile";

// Using https://react-data-table-component.netlify.app/?path=/docs/performance-examples-hook-component--hook-component
// table


export default function useDayInfo(props) {

  const dateFormat = 'dddd[, ]D[ de ]MMMM[ de ]YYYY'

  function handleNextDate() {
    let date = props.dayInfo['$d']
    date.setDate(date.getDate()+1)
    props.setDayInfo(dayjs(date))
  }

  function handlePrevDate() {
    let date = props.dayInfo['$d']
    date.setDate(date.getDate()-1)
    props.setDayInfo(dayjs(date))
  }

  function handleResetDate() {
    props.setDayInfo(dayjs())
  }

  const [displaying, setDisplaying] = useState([])

  useEffect( () => {
    

    if (props.type in ['fin', 'bias', 'flatf', 'scif', 'flat', 'sci'] && props.targetId === null){
      return
    }
    
    async function fetchData(){
      toast.success(`Loaded files for ${props.dayInfo.format("YYYY-MM-DD")}`)
      setDisplaying([])

      console.log(props.dayInfo, props.type, props.targetId)
      if(props.type === 'individual'){
        let individuals = new IndividualObjects()
        const res = await individuals.getFromDate(props.dayInfo.format("YYYY-MM-DD"))
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === 'fin'){
        let final = new FinalTiles()
        const res = await final.getFromDate(props.dayInfo.format("YYYY-MM-DD"))
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === 'bias'){
        let biasbl = new BiasBlock()
        const res = await biasbl.getObjectById(props.targetId)
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === 'flatf'){
        let flatf = new FlatByFilter()
        const res = await flatf.getObjectById(props.targetId)
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === 'scif'){
        let scif = new SciByFilter()
        const res = await scif.getObjectById(props.targetId)
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === 'flat'){
        let flat = new FlatBlock()
        const res = await flat.getObjectById(props.targetId)
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === 'sci'){
        let sci = new SciBlock()
        const res = await sci.getObjectById(props.targetId)
        if(res[0]){setDisplaying(res)}
      }

      if(props.type === null){
        let individuals = new IndividualObjects()
        const res = await individuals.getFromDate(props.dayInfo.format("YYYY-MM-DD"))
        if(res[0]){setDisplaying(res)}
      }


    }
    fetchData()
  }, [props.dayInfo, props.type, props.targetId])


  const data = []
  displaying.map(obj => (
      data.push(obj)
  ))

  return (
    <>

      {props.type === 'individual' && (
        <header className='flex items-center px-2 h-10'>
          <button
            onClick={handlePrevDate}
            className='flex mr-2 p-2 rounded-md border border-gray-200
            text-gray-500 hover:text-gray-900 hover:bg-gray-50'>
            <Icon name='left' className='m-auto h-4' />
          </button>
          <button
            onClick={handleNextDate}
            className='flex mr-5 p-2 rounded-md border border-gray-200
            text-gray-500 hover:text-gray-900 hover:bg-gray-50'>
            <Icon name='right' className='m-auto h-4' />
          </button>
          <button
            onClick={handleResetDate}
            className='flex mr-5 px-3 py-1 rounded-md border border-gray-200
            text-gray-500 hover:text-gray-900 hover:bg-gray-50'>
            Hoje
          </button>
          <h1 className='font-bold text-2xl text-gray-600'>
            {props.dayInfo.format(dateFormat)}
          </h1>
        </header>
      
      )}
      

      {props.type === 'individual' && (
          <div style={{'height': '90%'}} className="overflow-auto">
            <IndividualContainer data={data} />
          </div>
      )}
      {props.type === 'bias' && (
          <div style={{'height': '98%'}} className="overflow-auto">
            <BiasContainer data={data} />
          </div>
      )}
      {props.type === 'flatf' && (
          <div style={{'height': '98%'}} className="overflow-auto">
            <FlatFContainer data={data} />
          </div>
      )}
      {props.type === 'flat' && (
          <div style={{'height': '98%'}} className="overflow-auto">
            <FlatContainer data={data} />
          </div>
      )}
      {props.type === 'scif' && (
          <div style={{'height': '98%'}} className="overflow-auto">
            <SciFContainer data={data} />
          </div>
      )}
      {props.type === 'sci' && (
          <div style={{'height': '98%'}} className="overflow-auto">
            <SciContainer data={data} />
          </div>
      )}
      {props.type === 'fin' && (
          <div style={{'height': '98%'}} className="overflow-auto">
            <FinalContainer data={data} />
          </div>
      )}

    </>
  )
}
