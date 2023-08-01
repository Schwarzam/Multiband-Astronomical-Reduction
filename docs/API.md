## marServer API documentation

To access any point on the API, you need to retrieve the request headers and set the data to your desired specifications.

The header should consist of an Authorization key with the Bearer token provided by the server during login.

The login process occurs at the following endpoint:

### ```/reduction/auth/login ``` 

```python
import requests

payload = {"username": username, "password": password}
response = requests.post(url, json=payload)
```

This response will contain the token that should be used in any subsequent request headers in the following manner:

```python
header = {
        'headers': {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    }
```

## Endpoints

It is important to mention that the following endpoints can be used directly in the MAR-frontend search/execute tool.

We describe all marServer endpoints and their respective functions, which enable the necessary mar operations to reduce S-PLUS data.

The endpoints are listed below:

 - [Individual Images](#individual)
 - [Coadded Images](#finaltiles)
 - [Bias block](#biasblock)
 - [Flat block by filter](#flatbyfilter)
 - [Flat block (all filters)](#flatblock)
 - [Sci block by filter](#scibyfilter)
 - [Sci block (all filters)](#sciblock)
 - [Super Flats](#superflat)
 - [12 filter images](#fieldimage)

Each request should include a data type (body) that defines the request. For example:

```python
data = {
    "type": "get"
}
```

This type of request is used to retrieve a specific type of file from the endpoint. However, the request is incomplete as we need to specify what we want to retrieve, which may vary from endpoint to endpoint. For instance, we may define that we want all files from January 1st, 2018 to March 10th, 2018:

```python
data = {
    "type": "get",
    "startDate": "2018-01-01",
    "endDate": "2018-03-10"
}
```

Searching for this on the individualfile endpoint, for example, will retrieve all files within this date range. Searching on the biasblock endpoint will retrieve all bias blocks within this date range, and so on.

It is important to understand how the reduction works and the order in which everything is done.

### Example

Here, we will describe the endpoints and list any additional parameters that each one may accept. Parameters marked with "||" may be used with any other parameter. For example:

- get
    - startDate, endDate
    - id
    - || valid
    - || contains

This defines the "get" type, which may be used with either "startDate" and "endDate" or "id" to select a specific image by its ID. The "valid" parameter may be added to search for invalid files. All parameters containing **||** at the start are optional and may be added to any queries. For example:

```python
data = {
    "type": "get",
    "startDate": "2018-01-01",
    "endDate": "2018-03-10",
    "valid": 0, ## Fetching for invalid data.
    "contains": "STRIPE82" ## Fetching for files containing the "STRIPE82" pattern in their names. 
}
```


<br/>
<br/>

#### <span id="individual"> ```/reduction/individualfile``` </span>

The individualfile endpoint correspond to the ```files_individualfiles``` table in the database. This table contains all raw scanned files, bias, skyflats, scies and also this table will contain processed files (scies after process).

##### types and parameters:

- get
    - startDate, endDate
    - contains (file name matching pattern)
    - id
    - || valid
    - || contains

---

- validate (set reverse of current)
    - id 

---

- setstatus 
    - id, status

--- 

- setcomment 
    - id, comment

<br/>

#### <span id="finaltiles"> ```/reduction/finaltiles``` </span>

The finaltiles endpoint correspond to the coadded images, that are the final product of the MainSurvey of S-PLUS. 

##### types and parameters:

- get
    - id 
    - startDate, endDate 
    - startDate, endDate, contains, flag (Get images that contain that flag)
    - field (Eg. ```STRIPE82_0001```)
    - field, band
    - contains (field matching pattern)
    - || valid 
    - || contains

---

- process (this will reduce determined field and filter corresponding to id)
    - id 
    - || code (execution code, selecting operations wanted)


--- 

- processfield (process all filters from determined field with all individuals available)
    - field
    - || code 
    - || status (status to set all processed)

---

- setstatus 
    - id, status 
    - startDate, endDate, contains, flag, status (set status of determined observations)

--- 

- setsubstatus (set status of all individuals linked to this coadded)
    - id, status 

--- 

- setsuperflat (link a superflat (fringe) by id to all individuals that compose this field (next time reducing will use this))
    - field, band, superflatid  

--- 

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

---

- setflag (changes image flag)
    - id, flag

<br/>

#### <span id="biasblock"> ```/reduction/biasblock``` </span>

The biasblock endpoint correspond to the blocks of bias created to make master bias. 

##### types and parameters:

- get
    - id 
    - startDate, endDate 
    - || valid 

---

- create (creates a bias block with all valid bias from start to end dates)
    - startDate, endDate

---

- process (this will reduce determined field and filter corresponding to id)
    - id 
    - || code (execution code, selecting operations wanted)

--- 

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

--- 

- setstatus (in bias block if status == 1, its processed)
    - id, status 

---

- register (useful to register a previously processed frame).
    - filepath

<br/>

#### <span id="flatbyfilter"> ```/reduction/flatbyfilter``` </span>

The flatblockbyfilter endpoint is related to filter specific master flat blocks. It's designed to handle one specific filter flat block at time. 

- get
    - id 
    - startDate, endDate 
    - || valid 

---

- create (creates a flat block with all valid flats from specific filter and start to end dates)
    - startDate, endDate, band

---

- process (this will reduce determined field and filter corresponding to id)
    - id 
    - || code (execution code, selecting operations wanted)

--- 

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

--- 

- setstatus (in flat block if status == 1, its processed)
    - id, status 

---

- register (useful to register a previously processed frame).
    - filepath

<br/>

#### <span id="flatblock"> ```/reduction/flatblock``` </span>

The flatblock endpoint is related to master flat blocks containing all filters. This is easier to work if reducing all filters at once. 

- get
    - id 
    - startDate, endDate 
    - || valid 

---

- create (creates a flat block with all valid flats from specific filter and start to end dates)
    - startDate, endDate
    - || contains (patterns that filenames will contain (split by ,))

---

- process (this will reduce determined field and filter corresponding to id)
    - id 

--- 

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

--- 

- setstatus (in flat block if status == 1, its processed)
    - id, status 


<br/>

#### <span id="scibyfilter"> ```/reduction/scibyfilter``` </span>

The scibyfilter endpoint is related to filter specific sci blocks. It's designed to handle one specific filter sci block at time. 

- get
    - id 
    - startDate, endDate 
    - || valid 

---

- create (creates a sci by filter block with all valid scies from specific filter and start to end dates)
    - startDate, endDate
    - || contains (patterns that filenames will contain (split by ,))

---

- process (this will reduce determined field and filter corresponding to id)
    - id 

--- 

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

--- 

- setstatus (if status == 1, its processed)
    - id, status 

---

- setsubstatus (set status of all linked raw and processed objects with the desired block. Usefull to re-reduce)
    - id, status

--- 

- setsuperflat (change superflat linked to all raw)
    - id, superflatid 


<br/>

#### <span id="sciblock"> ```/reduction/sciblock``` </span>

The sciblock endpoint is related to filter specific sci blocks. It's designed to handle one specific filter sci block at time. 

- get
    - id 
    - startDate, endDate 
    - || valid 

---

- create (creates a sci block with all valid scies from specific filter and start to end dates)
    - startDate, endDate
    - || contains (patterns that filenames will contain (split by ,))

---

- process (this will reduce determined field and filter corresponding to id)
    - id 

--- 

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

--- 

- setstatus (in sci block if status == 1, its processed)
    - id, status 

---

- setsubstatus (set status of all linked raw and processed objects with the desired block. Useful to re-reduce)
    - id, status

--- 

- setsuperflat (change superflat linked to all raw)
    - id, superflatid 


<br/>

#### <span id = "superflat"> ```/reduction/superflat``` </span>

The superflat endpoint is related to superflat frames creation (Eg. Fringe frames). 

- get
    - id 
    - startDate, endDate
    - || valid 

---

- setcomment 
    - id, comment 

--- 

- validate (set reverse of current)
    - id 

--- 

- register (useful to register a previously processed frame).
    - filepath



<br/>

#### <span id = "fieldimage"> ```/reduction/fieldimage``` </span>

The field endpoint is related to the creation of a 12 filter image using trilogy, this is useful to check the quality of astrometry among all filters. 

- get
    - id 
    - field
    - contains
    - || valid 

---

- setcomment 
    - id, comment 

---

- setflag
    - id, flag

--- 

- process ((re)create the image)
    - field


## Other Endpoints:

The following endpoints are separated because they are not useful in the search/execute MAR-frontend tool.

#### <span> ```/reduction/get_process``` </span>

This endpoint is used to retrieve the current "state" or process of what is being done in the pipeline.

This endpoint retrieves the logs of the current process.

#### <span> ```/reduction/clear_logs``` </span>

This endpoint clears the logs.

#### <span> ```/reduction/scan_folder``` </span>

This function scans RAW fits files and adds them to the database. A parameter "path" should be passed in the body of the request indicating the path of the folder relative to the reductionmedia folder.

#### <span> ```/reduction/reset_thread``` </span>

This endpoint attempts to perform a hard reset on the thread pool. (It may be safer to restart the docker container.)

#### <span>```/reduction/get_queue```</span>

This endpoint retrieves the next processes in the queue.

#### <span>```/reduction/removeQueue```</span>

This endpoint removes a process from the queue by passing its ID.

#### <span>```/reduction/getConf```</span>

This endpoint fetches the current MAR Python package and pipeline configuration.

#### <span>```/reduction/setItemConf```</span>

This endpoint requires the "section", "item", and "value" of the parameter to be modified.

#### <span>```/reduction/getOperation```</span>

This endpoint retrieves the current progress of the pipeline (how many fields and images processed).

#### <span>```/reduction/rawQuery```</span>

This endpoint should have a "query" in its body. It allows for a SELECT query to be made directly to the database.
