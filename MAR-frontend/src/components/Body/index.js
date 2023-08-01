//import { DateContextProvider } from "../Calendar/contexts";
import { DayInfoContextProvider } from "../DayInfo/context";
import PopUpProvider from "../PopUp/context";

export default function Body({children}) {
  return (
    <PopUpProvider>
      <div className='h-screen'>
        {children}
      </div>
    </PopUpProvider>
  )
}