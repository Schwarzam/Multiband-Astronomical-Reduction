import React, {useState} from "react"
import Icon from "../Icons"

export default function usePopUp(state) {
    const [openPopUp, setOpenPopUp] = useState(state)

    function open(){

    }

    if (openPopUp){
        return (
            <></>
        )
    }

}