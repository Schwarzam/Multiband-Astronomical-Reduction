import DataTable from "react-data-table-component";
import { ProcessedFile } from "./processedFile";
import Display from "./display";

import Separator from '../Body/separator'

const GenericalContainer = (props) => {

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
    {
      name: 'ObsDate',
      selector: row => row.obsDate,
      sortable: true
    },
    {
      name: 'status',
      selector: row => row.status,
      sortable: true
    },
    {
      name: 'Name',
      selector: row => row.file_name,
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
    const display = new Display('generical')

    Object.entries(data).map(([item, value]) => (
      (item !== 'sci' ? (
        display.addFragments(item, value)
      ) : (
        display.addAditionals(<ProcessedFile data={value} header={"Processed File Infos"} />)
      ))
    ))

    return (display.getFinal())
  }

  return (
    <div className="h-full mb-24">

      <div className={props.header && 'outline outline-offset-2 outline-1'}>
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
    </div>
  )
}

export { GenericalContainer }
