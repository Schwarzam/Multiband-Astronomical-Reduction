import React, { useState, useEffect } from "react";
import axios from "axios";

const tables = [  {    
    "table_name": "files_individualfile",    
    "columns": [
        {"column_name": "id"},      
        {"column_name": '"obsDate"'},      
        {"column_name": "field"},
        {"column_name": "file_type"},
        {"column_name": "exptime"},
        {"column_name": "band"},
        {"column_name": "file_name"},
        {"column_name": "file_path"},
        {"column_name": "ovfile"},
        {"column_name": "ovthumb"},
        {"column_name": "thumb"},
        {"column_name": "modeavg"},
        {"column_name": "medianavg"},
        {"column_name": "noiseavg"},
        {"column_name": "medianrms"},
        {"column_name": "noiserms"},
        {"column_name": "bpmask"},
        {"column_name": '"processedDate"'},
        {"column_name": "comments"},
        {"column_name": "status"},
        {"column_name": "comments"},
        {"column_name": "isvalid"},
        {"column_name": "processed_id"},
        {"column_name": "sci_id"},
        {"column_name": "superflat_id"},
    ]
  },
  {
    "table_name": "files_finaltiles",
    "columns": [
        {"column_name": "id"},       
        {"column_name": "field"},
        {"column_name": "band"},
        {"column_name": "file_path"},
        {"column_name": "weight_path"},
        {"column_name": "file_thumb"},
        {"column_name": "weight_thumb"},
        {"column_name": "modeavg"},
        {"column_name": "medianavg"},
        {"column_name": "noiseavg"},
        {"column_name": "medianrms"},
        {"column_name": "noiserms"},
        {"column_name": "date"},
        {"column_name": "status"},
        {"column_name": "comments"},
        {"column_name": "isvalid"},
    ]
  }
]

const QueryMaker = (props) => {
  const [_, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState("");
  const [selectedColumns, setSelectedColumns] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [query, se] = useState("");

  useEffect(() => {

  }, []);

//   const fetchTables = async () => {
//     try {
//         //TODO
//       const response = await axios.get(
//         //TODO
        
//         //`${process.env.REACT_APP_SERVER_IP}/tables`
//       );
//       setTables(response.data);
//     } catch (error) {
//       console.log(error);
//     }
//   };

  const handleTableChange = (event) => {
    setSelectedTable(event.target.value);
  };

  const handleColumnChange = (event) => {
    const selected = Array.from(event.target.selectedOptions, (option) =>
      option.value
    );
    setSelectedColumns(selected);
  };

  const handleStartDateChange = (event) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event) => {
    setEndDate(event.target.value);
  };

  const generateQuery = () => {
    if (selectedTable && selectedColumns.length > 0) {
      const columnList = selectedColumns.join(", ");
      const constraint =
        startDate && endDate
          ? `WHERE {DATE_COLUMN} BETWEEN '${startDate}' AND '${endDate}'`
          : "";
      const query = `SELECT ${columnList} FROM ${selectedTable} ${constraint}`;
      props.setQuery(query);
    }
  };

  return (
    <div className="flex justify-center items-center mt-16">
      <div className="bg-white rounded-lg shadow-lg p-8 mx-auto">
        <h2 className="text-2xl font-bold mb-4">SQL Query Maker</h2>
        <div className="flex mb-4">
        <div className="mr-4">
          <label
            htmlFor="table-select"
            className="block text-gray-700 font-bold mb-2"
          >
            Select a table:
          </label>
          <select
            id="table-select"
            value={selectedTable}
            onChange={handleTableChange}
            className="border border-gray-400 rounded px-3 py-2 w-full"
          >
            <option value="">--Select a table--</option>
            {tables.map((table) => (
              <option key={table.table_name} value={table.table_name}>
                {table.table_name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label
            htmlFor="column-select"
            className="block text-gray-700 font-bold mb-2"
          >
            Select columns:
          </label>
          <select
            id="column-select"
            multiple
            value={selectedColumns}
            onChange={handleColumnChange}
            className="border border-gray-400 rounded px-3 py-2 w-full"
          >
            {selectedTable &&
              tables
                .find((table) => table.table_name === selectedTable)
                .columns.map((column) => (
                  <option key={column.column_name} value={column.column_name}>
                    {column.column_name}
                  </option>
                ))}
          </select>
        </div>
      </div>
      <div className="mb-4">
        <label htmlFor="start-date" className="block text-gray-700 font-bold mb-2">
          Start date:
        </label>
        <input
          id="start-date"
          type="date"
          value={startDate}
          onChange={handleStartDateChange}
          className="border border-gray-400 rounded px-3 py-2 w-full"
        />
      </div>
      <div className="mb-4">
        <label htmlFor="end-date" className="block text-gray-700 font-bold mb-2">
          End date:
        </label>
        <input
          id="end-date"
          type="date"
          value={endDate}
          onChange={handleEndDateChange}
          className="border border-gray-400 rounded px-3 py-2 w-full"
        />
      </div>
      <button
        className="border border-slate-900 hover:bg-slate-500 font-bold py-2 px-4 rounded"
        onClick={generateQuery}
      >
        Generate Query
      </button>
      {query && (
        <div className="mt-4">
          <p className="font-bold">Generated Query:</p>
          <code className="bg-gray-200 py-2 px-4 rounded-lg block mt-2">
            {query}
          </code>
        </div>
      )}
    </div>
    </div>
  )};

export default QueryMaker;