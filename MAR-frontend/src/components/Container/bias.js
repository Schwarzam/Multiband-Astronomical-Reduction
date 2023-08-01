import { IndividualContainer } from "./individual";
import DataTable from "react-data-table-component";
import Display from "./display";
import Separator from '../Body/separator'

const BiasContainer = (props) => {

  const columns = [
    {
      name: 'ID',
      selector: row => row.id,
      sortable: true
    },
    {
      name: 'status',
      selector: row => row.status,
      sortable: true
    },
    {
      name: 'isValid',
      selector: row => row.isvalid.toString(),
      sortable: true
    },
  ];

  const expandRow = ({ data }) => {
    const display = new Display('bias');
    Object.keys(data).forEach((item) => {
      const value = data[item];
      if (item !== 'bias') {
        display.addFragments(item, value);
      } else {
        display.addAditionals(<IndividualContainer data={value} header={"Bias linked"} />);
      }
    });
    return display.getFinal();
  };

  const dataToTable = [...props.data];

  if (props.data) {
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
    );
  }
  return <></>;
};

export { BiasContainer };
