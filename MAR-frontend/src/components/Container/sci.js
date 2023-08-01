import {IndividualContainer} from "./individual";
import DataTable from "react-data-table-component";
import { SciFContainer } from "./scibyfilter";
import Display from "./display";


const SciContainer = (props) => {

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
        {
            name: 'isValid',
            selector: row => row.isvalid.toString(),
            sortable: true
        },
    ];

    const expandRow = ({data}) => {
        const display = new Display('sci')

        Object.entries(data).map(([item, value]) => (
            (item !== 'sciByFilter' ? (
                display.addFragments(item, value)
            ) : (
                display.addAditionals(<SciFContainer data={value} />)
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
            <div className="h-full mb-24">

                <div className="p-6 text-2xl">
                    {props.header && <h1>{props.header}</h1>}
                </div>

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

export { SciContainer }