import { useState, createContext } from "react";
import dayjs from 'dayjs'

const DayInfoContext = createContext({
  dayInfo: dayjs(),
  setDayInfo: (i) => {}
})

export default DayInfoContext



