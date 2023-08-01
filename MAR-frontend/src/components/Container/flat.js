import {IndividualContainer} from "./individual";
import DataTable from "react-data-table-component";
import {FlatFContainer} from "./flatbyfilter";
import Display from "./display";

import Separator from '../Body/separator'

const FlatContainer = (props) => {

    const columns = [
        {
            name: 'ID',
            selector: row => row.id,
            sortable: true
        },
        {
            name: 'blockStartDate',
            selector: row => row.blockStartDate,
            sortable: true
        },
        {
            name: 'blockEndDate',
            selector: row => row.blockEndDate,
            sortable: true
        },
    ];

    const expandRow = ({data}) => {
        const display = new Display('flat')

        Object.entries(data).map(([item, value]) => (
            (item !== 'flatsByFilter' ? (
                display.addFragments(item, value)
            ) : (
                display.addAditionals(<FlatFContainer data={value} header={"FlatBlocksByFilter linked"} />)
            ))
        ))

        return (display.getFinal())
    }

    const dataToTable = []
    props.data.map(obj => (
        dataToTable.push(obj)
    ))

    if (props.data){
        return(
            <div className="">
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
            </div>
        )
    }

    return(<></>)

}

export { FlatContainer }