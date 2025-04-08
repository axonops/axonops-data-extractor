# AxonOps™ Data Extractor

The AxonOps Data Extractor is a Python utility designed to extract and download data from AxonOps. This tool is particularly useful for integrating into data pipelines, data warehouses or ETL workflows

You simply add your AxonOps API keys as environment variables, create a report config (see `data/queryconfig/query_config_example.json`) and then run one of the scripts.

To get it working, load the Python dependencies in `requirements.txt` into your Python environment and then run the corresponding Python script below.

## Monthly Data
```
usage: axonops_monthly_csv_extractor.py [-h] -o OUTPUTDIR -q QUERYCONFIG -m MONTHOFYEAR [-d]

AxonOps Monthly CSV Extractor

options:
  -h, --help            show this help message and exit
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        The file path to a directory for outputting the CSV data.
  -q QUERYCONFIG, --queryconfig QUERYCONFIG
                        File path to the JSON configuration file listing the queries to run and extract to CSV. See the README.md for more information on this configuration file.
  -m MONTHOFYEAR, --monthofyear MONTHOFYEAR
                        The month of year in format YYYYMM for which data will be extracted to CSV. This can not be in the future nor the current month
  -d, --deletejson      If set, the downloaded JSON will be kept in the output directory. By default it is automatically deleted after being converted to CSV.
```
**Note:** please ensure that there is sufficient disk space at the location you choose to output the CSV - they can be large.


For example
```bash
python axonops_monthly_csv_extractor.py --outputdir data/results/mydata --queryconfig data/queryconfig/myqueries.json --monthofyear 202409
```

This will extract all the data for `September 2024` returned by the queries in myqueries.json and store it as CSV files in data/results/mydata

## Hourly Data
```
usage: axonops_hourly_csv_extractor.py [-h] -o OUTPUTDIR -q QUERYCONFIG -m HOUROFYEAR [-d]

AxonOps Monthly CSV Extractor

options:
  -h, --help            show this help message and exit
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        The file path to a directory for outputting the CSV data.
  -q QUERYCONFIG, --queryconfig QUERYCONFIG
                        File path to the JSON configuration file listing the queries to run and extract to CSV. See the README.md for more information on this configuration file.
  -hy HOUROFYEAR, --hourofyear HOUROFYEAR
                        The hour of year in format YYYYMMDDHH for which data will be extracted to CSV. This can not be in the future nor the current hour
  -d, --deletejson      If set, the downloaded JSON will be kept in the output directory. By default it is automatically deleted after being converted to CSV.
```

For example

```bash
python axonops_hourly_csv_extractor.py --outputdir data/results/mydata --queryconfig data/queryconfig/myqueries.json -hourofyear 20240923
```

This will extract all the data for `9th September 2024 23:00` returned by the queries in myqueries.json and store it as CSV files in data/results/mydata

***
- [Setup Instructions](#setup-instructions)
  - [Query Configuration Setup](#query-configuration-setup)
    - [JSON Field Information](#json-field-information)
    - [How to find values for `axon_query`](#how-to-find-values-for-axon_query)
  - [Setup Steps](#setup-steps)
    * [Clone the Repository](#1-clone-the-repository)
    * [Generate an AxonOps API token for your organisation](#2-generate-an-axonops-api-token-for-your-organisation)
    * [Set-up your AxonOps organisation and API tokens as environment variables](#3-set-up-your-axonops-organisation-and-api-tokens-as-environment-variables)
    * [Set Up a Python Virtual Environment](#4-set-up-a-python-virtual-environment)
    * [Activate the Virtual Environment](#5-activate-the-virtual-environment)
    * [Install Required Python Packages](#6-install-required-python-packages)
    * [Run the Python Script](#7-run-the-python-script)
    * [Deactivate the Virtual Environment](#8-deactivate-the-virtual-environment)


## Setup Instructions

### Query Configuration Setup

The `--queryconfig` argument should be pointing at a JSON file that defines the queries to run, the results of which will be converted to CSV. There is an example you can see in `data/queryconfig/query_config_example.json`.

The file looks roughly like this:

```JSON
{
    "clusters": ["mycassandracluster1","mycassandracluster2","mycassandracluster3"],
    "queries": [
        {
            "description": "Live Disk Space Used by DC and Keyspace",
            "unit": "bytes (SI)",
            "axon_query": "sum(cas_Table_LiveDiskSpaceUsed{function='Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces',scope!=''}) by (dc, keyspace)",
            "file_prefix": "live_disk_per_keyspace"
        },
        {
            "description": "Total Coordinator Reads by DC and Keyspace",
            "unit": "rps",
            "axon_query": "sum(cas_Table_CoordinatorReadLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)",
            "file_prefix": "total_coordinator_table_reads_per_dc",
            "field_renames": [
                {"rename": "scope", "value": "table"}
            ]
        }
    ]
}
```
#### JSON Field Information

* ***clusters***: Add the names of your clusters connected to AxonOps in the `clusters` list.
* ***queries***: For each of the clusters in entered, this is the list of queries that will be run and the results converted to CSV.
  *  ***description***: A human readable description of the query
  *  ***unit***: the unit returned
  *  ***axon_query***: the AxonOps query to run the results of which will be converted to CSV.
  *  ***file_prefix***: The file prefix that will be used in the name of the CSV. This must be unique.
  *  ***field_renames***: (optional) Sometimes, the JSON API response has fields returned that can be named better.

### How to find values for `axon_query`

In AxonOps we using a query language that is very similar to PromQL to query for retrieving metrics.

If there is a metric you want to extract to CSV, navigate to the dashboard it is on:

<img width="608" alt="Screenshot 2024-10-25 at 10 26 40" src="https://github.com/user-attachments/assets/75b61e81-9192-4019-9b8d-a1aa6328d42c">

Then edit the graph containing the metric you want to extract:

<img width="675" alt="Screenshot 2024-10-25 at 10 31 47" src="https://github.com/user-attachments/assets/465ad98f-87e0-4023-bfa7-096267572ba0">

One in the edit window, click on `VISUALIZATION` tab:

<img width="1082" alt="Screenshot 2024-10-25 at 10 27 20" src="https://github.com/user-attachments/assets/5a5355d9-48d8-4f28-810e-fd158c4b0351">

From there you can see the `Query` value for this graph. In this example it is defined as:
```
host_CPU_Percent_Merge{time='real',dc=~'$dc',rack=~'$rack',host_id=~'$host_id'}
```
This query has some templated variables `$dc, $rack, $host_id` - these are used to pass in parameters selected in the dashboard GUI and we dont want these for extraction purposes, unless you want to substitute values in for the extract.

You have several options with this query. The first option `host_CPU_Percent_Merge` will return a large volume of data, it will return the raw values for every single server in the cluster. Things to consider as an alternative is to group the data by dc, keyspace or whatever way you want to group the data. Additionally you can use aggregate functions like `sum` etc.. Visit the [AxonOps documentation](https://docs.axonops.com/monitoring/metricsdashboards/querysyntax/) to find out more.

### Setup Steps

You need to install Python 3 for this application, a good resource is the official Python website. You can find installation instructions and download links for various operating systems there. 
- [Python Downloads](https://www.python.org/downloads/) - This page provides the latest releases of Python for Windows, macOS, and other platforms, along with detailed installation instructions.

#### **1. Clone the Repository**

First, clone the GitHub repository to your local machine:

```bash
git clone https://github.com/axonops/axonops-csv-extractor.git
cd axonops-csv-extractor
```

#### **2. Generate an AxonOps API token for your organisation**

Login to your AxonOps console. For the SaaS console go to https://console.axonops.com. 

Once you have logged in, choose the organisation you want to create an API token for. Then enter the API Tokens section:

<img width="1076" alt="API Tokens" src="https://github.com/user-attachments/assets/6533429a-892b-4a46-90d9-93b3617c5660">

From there, click create a new API Token. Give the token a name, expiry period, select the clusters you want to be able to access with the token and select the Readonly Role

<img width="602" alt="Create New Token" src="https://github.com/user-attachments/assets/7cfc852e-5797-464d-afdf-7228d4b39dd4">

Click the Generate button and then you can copy the API token to use in Step 3.

<img width="604" alt="Generated Token" src="https://github.com/user-attachments/assets/4632bd45-e444-46c9-b139-13aca0ec3924">

(obviously that token is not valid 😊)

#### **3. Set-up your AxonOps organisation and API tokens as environment variables**

To interact with the AxonOps APIs to query its data you need to store your organisation and API key as environment variables in a new `.env` you need to create in the root directory of the repo. 

See `.env-example` - copy this to a file called `.env` and update it with your organisation id and the API token you generated. This file is in .gitignore and will not be committed.

```bash
AXONOPS_ORG_ID="youraxonopsorg"
AXONOPS_API_SECRET_TOKEN="yourapitoken"
```

For self-hosted AxonOps users you can also add a `AXONOPS_DASH_URL` variable to point at your own installation of AxonOps.

#### **4. Set Up a Python Virtual Environment**

Create a virtual environment in the project directory using `.venv` as the directory name. This ensures that all Python dependencies are installed in an isolated environment specific to this project:

```bash
python3 -m venv .venv
```

This command creates a directory named `.venv` inside your project directory, which contains the virtual environment.

#### **5. Activate the Virtual Environment**

Activate the virtual environment to start using it. The activation command depends on your operating system:

- **On macOS and Linux:**

  ```bash
  source .venv/bin/activate
  ```

- **On Windows (Command Prompt):**

  ```cmd
  .venv\Scripts\activate.bat
  ```

- **On Windows (PowerShell):**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

Once activated, your terminal prompt should change to indicate that you are working within the virtual environment.

#### **6. Install Required Python Packages**

With the virtual environment activated, install all necessary packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all specified packages into the virtual environment.

#### **7. Run the Python Script**

Now that all dependencies are installed, you can run the main Python script:

```bash
python axonops_monthly_csv_extractor.py [options]
```

Usage:
```bash
usage: axonops_monthly_csv_extractor.py [-h] -o OUTPUTDIR -q QUERYCONFIG -m MONTHOFYEAR [-d]

AxonOps CSV Extractor

options:
  -h, --help            show this help message and exit
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        The file path to a directory for outputting the CSV data.
  -q QUERYCONFIG, --queryconfig QUERYCONFIG
                        File path to the JSON configuration file listing the queries to run and extract to CSV. See the README.md for more information on this configuration file.
  -m MONTHOFYEAR, --monthofyear MONTHOFYEAR
                        The month of year in format YYYYMM for which data will be extracted to CSV. This can not be in the future nor the current month
  -d, --deletejson      If set, the downloaded JSON will be kept in the output directory. By default it is automatically deleted after being converted to CSV.
```


#### **8. Deactivate the Virtual Environment**

Once you are done working, deactivate the virtual environment to return to your system's default Python environment:

```bash
deactivate
```

***

*This project may contain trademarks or logos for projects, products, or services. Any use of third-party trademarks or logos are subject to those third-party's policies. AxonOps is a registered trademark of AxonOps Limited. Apache, Apache Cassandra, Cassandra, Apache Spark, Spark, Apache TinkerPop, TinkerPop, Apache Kafka and Kafka are either registered trademarks or trademarks of the Apache Software Foundation or its subsidiaries in Canada, the United States and/or other countries. Elasticsearch is a trademark of Elasticsearch B.V., registered in the U.S. and in other countries. Docker is a trademark or registered trademark of Docker, Inc. in the United States and/or other countries.*
