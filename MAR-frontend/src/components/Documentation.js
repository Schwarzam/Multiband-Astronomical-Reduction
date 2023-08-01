
const Documentation = () => {

  return (
    <div className="max-w-5xl m-auto py-10">
        <p className="font-bold text-xl">Multiband Astronomical Reduction</p>
        <p className="font-bold text-lg pt-10">Front Controller</p>

        <p>
        The front controller is the main part of the MAR frontend and where all the operations are performed. At the top, the server status is displayed to show if the server is online and responding to requests, and the server process indicates what the server is currently processing. If the server is not processing at the moment, the state is set as "Available". The server status and server process are periodically updated, but there is also a refresh button to update the state and a "reset threads" button to use in case the machine breaks, freezes, or crashes. If the "reset threads" button doesn't solve the problem, it is better to restart the Docker container.
        </p>

        <p>
        Below the buttons, you can find all the types of data that can be fetched. To optimize what is being fetched, you can select what you want and then click the "Fetch" button below. Note that some objects in the calendar are not reloaded unless you clear them and then fetch them again. The calendar allows you to slide through dates and view the data you are fetching.
        </p>

        <p className="font-bold text-lg pt-10">Adding Data</p>
        <p>
          In the front controller, at the bottom, there is a "scan folder" component used to search for files in the indicated folder. You may also use a constraint to look for files that only contain a certain pattern in their names. The root folder of the project is in /reductionmedia, so you always need to pass /reductionmedia/$folder or only /reductionmedia and look for all files inside. This scan procedure will add every valid FITS image inside the selected folder and classify it as BIAS, FLAT or SCI image. These are called individual files.
        </p>

        <p className="font-bold text-lg pt-10">Logs</p>
        <p>
        In the front controller, there is a "Logs" component. If the server is processing something, you can see the logs there. Once the process is done, this log is saved and then goes to the "Operations History" tab in the side menu, where you can download it. You can also use the logs to look for CRITICAL errors that will appear in red, and to see if the pipeline is frozen or not.
        </p>

        <p className="font-bold text-lg pt-10">Configuration</p>
        <p>
        The configuration section in the side menu is pretty straightforward.
        </p>

        <p className="font-bold text-lg pt-10">Query</p>
        <p>
        The query section is used to search for any objects in the database.
        </p>
    
    </div>
    
  );
}

export default Documentation