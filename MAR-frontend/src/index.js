import './output.css'
import { render } from "react-dom"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import CalendarPage from './pages/Calendar'

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import * as ReactDOM from "react-dom";
import {useState} from "react";
import dayjs from "dayjs";

import Login from "./components/Login";
import DayInfoContext from "./components/DayInfo/context";

import Navbar from "./components/Navbar"

import Ophistory  from './components/Logs/history';
import Config from './components/Logs/configuration'
import RawQuery from './components/Logs/rawquery'
import Search from './components/Logs/search';

import Documentation from './components/Documentation'

const App = () => {
	const [ dayInfo, setDayInfo ] = useState(dayjs())


	return(
		<DayInfoContext.Provider value={{ dayInfo, setDayInfo }}>
			
			
			<BrowserRouter>
				<ToastContainer
					position="bottom-left"
					autoClose={2000}
				/>
				<Navbar />
				<Routes>
					<Route path='/login' element={<Login />}/>

					<Route path='/' element={<CalendarPage />}/>
					<Route path='/docs' element={<Documentation />}/>
					<Route path='/operations' element={<Ophistory/>}/>
					<Route path='/config' element={<Config />}/>
					<Route path='/query' element={<RawQuery />}/>

					<Route path='/search' element={<Search />}/>
				</Routes>

			</BrowserRouter>
		</DayInfoContext.Provider>
	)
}


ReactDOM.render(<App />, document.getElementById("root"))