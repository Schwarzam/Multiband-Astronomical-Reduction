import axios from "axios";
import {getHeader} from "../Login/auth";
import {toast} from "react-toastify";
import {useState} from "react";

export default function ScanFolder() {

    const [path, setPath] = useState('')
    const [contains, setContains] = useState('')

    const scan = () => {
        var data = null
        if (contains.length > 1){
            data = {path, contains}
        }else{
            data = {path}
        }
            
        axios.post(`${process.env.REACT_APP_SERVER_IP}/reduction/scan_folder`, data, getHeader())
            .then(res=>{
                toast.success(`Scanning files!`)
            })
            .catch(err => {
                toast.error(`Error scanning files!`)
            })
    }

    return (
        <div className="m-auto py-16">
            <p className="font-bold text-2xl">Scan folder</p>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Path to folder in server
            </label>
            <div className="flex">
                <div className="mt-1 border-b w-96 border-gray-300 focus-within:border-indigo-600">
                    <input
                        type="text"
                        name="name"
                        id="name"
                        onChange={(e) => setPath(e.target.value)}
                        className="block p-4 w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                        placeholder="/path/to/folder/in/server"
                    />
                    <input
                        type="text"
                        onChange={(e) => setContains(e.target.value)}
                        className="block p-4 mt-2 w-full border-0 border-b border-transparent bg-gray-50 focus:border-indigo-600 focus:ring-0 sm:text-sm"
                        placeholder="contains pattern"
                    />


                </div>
                <button onClick={() => scan()} type="button" className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-[#242F40] bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#242F40]">
                    Scan
                </button>
            </div>
        </div>
    )
}