import {IndividualContainer} from "./individual";
import DataTable from "react-data-table-component";
import Display from "./display";

const SciFContainer = (props) => {

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
            name: 'Status',
            selector: row => row.status,
            sortable: true
        },
        {
            name: 'isValid',
            selector: row => row.isvalid.toString(),
            sortable: true
        },
    ];

    const expandRow = ({data}) => {
        const display = new Display('scif')

        console.log(data)
        Object.entries(data).map(([item, value]) => {
            if (item !== 'scies' && item !== 'processed'){
                display.addFragments(item, value)
            }
            if (item === 'scies'){
                display.addAditionals(<IndividualContainer data={value} header="raw scies linked" />)
            }
            if (item === 'processed'){
                display.addAditionals(<IndividualContainer data={value} header="processed scies linked" />)
            }

        })

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

export { SciFContainer }