import DataTable from "react-data-table-component";
import Display from "./display";
import { IndividualContainer } from "./individual";

import Separator from '../Body/separator'

const FinalContainer = (props) => {

    const columns = [
        {
            name: 'ID',
            selector: row => row.id,
            sortable: true
        },
        {
            name: 'Date',
            selector: row => row.date,
            sortable: true
        },
        {
            name: 'flag',
            selector: row => row.flag,
            sortable: true
        },
        {
            name: 'field',
            selector: row => row.field,
            sortable: true
        },
        {
            name: 'band',
            selector: row => row.band,
            sortable: true
        },
    ];

    const dataToTable = []
    props.data.map(obj => (
        dataToTable.push(obj)
    ))

    const expandRow = ({ data }) => {
        const display = new Display('fin')

        Object.entries(data).map(([item, value]) => (
            ((item !== 'composedBy') ? (
                display.addFragments(item, value)
            ) : (
                display.addAditionals(<IndividualContainer data={value} header={"Composed by"} />)
            ))
        ))

        return (display.getFinal())
    }

    return (
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

export { FinalContainer }
