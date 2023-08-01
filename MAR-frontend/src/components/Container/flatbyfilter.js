import {IndividualContainer} from "./individual";
import DataTable from "react-data-table-component";
import Display from "./display";

import Separator from '../Body/separator'

const FlatFContainer = (props) => {

    const columns = [
        {
            name: 'ID',
            selector: row => row.id,
            sortable: true
        },
        {
            name: 'Band',
            selector: row => row.band,
            sortable: true
        },
        {
            name: 'isValid',
            selector: row => row.isvalid.toString(),
            sortable: true
        },
    ];

    const expandRow = ({data}) => {
        const display = new Display('flatf')

        Object.entries(data).map(([item, value]) => (
            (item !== 'flats' ? (
                display.addFragments(item, value)
            ) : (
                display.addAditionals(<IndividualContainer data={value} header="Flats Used" />)
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

export { FlatFContainer }