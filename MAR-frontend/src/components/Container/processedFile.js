import DataTable from "react-data-table-component";
import {BiasContainer} from "./bias";
import {FlatFContainer} from "./flatbyfilter";
import Display from "./display";

import Separator from '../Body/separator'

const ProcessedFile = (props) => {
    const columns = [
        {
            name: 'Type',
            selector: row => row.file_type,
            sortable: true
        },
        {
            name: 'ID',
            selector: row => row.id,
            sortable: true
        },
    ];

    const dataToTable = []
    props.data.map(obj => (
        dataToTable.push(obj)
    ))

    const expandRow = ({data}) => {
        const display = new Display('individual')
        Object.entries(data).map(([item, value]) => {
            if(item){
                display.addFragments(item, value)
            }
            // }else if(item === 'masterFlatUsed'){
            //     display.addAditionals(<FlatFContainer data={value} header={"MasterFlat linked"} />)
            // }else if(item === 'masterBiasUsed'){
            //     display.addAditionals(<BiasContainer data={value} header={"MasterBias linked"} />)
            // }
        })
        return (display.getFinal())
    }

    return(
        <div className="h-full mb-24">
            {props.header && (
                    <div className="p-6 text-2xl">
                         <h1>{props.header}</h1>
                    </div>
                )}

            <DataTable
                columns={columns}
                data={dataToTable}
                expandableRows
                expandableRowsComponent={expandRow}
            />

            <Separator />
        </div>
    )
}

export { ProcessedFile }