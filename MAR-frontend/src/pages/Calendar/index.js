import React, {useEffect} from "react"
import CalendarComponent from "../../components/Calendar"
import Navbar from "../../components/Navbar"
import Body from '../../components/Body'
import Container from '../../components/Container'
import {useValidadeLogin} from "../../components/Login/auth";
import Process from "../../components/Logs/process";
import Logs from "../../components/Logs/logs";
import ScanFolder from "../../components/Body/scanfolder";

import Queue from "../../components/Logs/queue";
import Progress from "../../components/Logs/progress"

export default function CalendarPage() {

    useValidadeLogin()

    return (
        <>
            <Body>
                
                <Container>

                    <Process />

                    <Progress />

                    <CalendarComponent />

                    <Logs />

                    <Queue />

                    <ScanFolder />
                </Container>
            </Body>
        </>
    )
}
