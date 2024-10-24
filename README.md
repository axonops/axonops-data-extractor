# axonops-csv-extractor

This is a Python application that AxonOps users can use to extract their data to CSV for subsequent usage.

## Instructions

To run the extractor you must setup your Python environment and API keys to access AxonOps.

### Python Setup and AxonOps API Key

You need to install Python 3 for this application, a good resource is the official Python website. You can find installation instructions and download links for various operating systems there. 
- [Python Downloads](https://www.python.org/downloads/) - This page provides the latest releases of Python for Windows, macOS, and other platforms, along with detailed installation instructions.



#### **1. Clone the Repository**

First, clone the GitHub repository to your local machine:

```bash
git clone https://github.com/axonops/axonops-csv-extractor.git
cd axonops-csv-extractor
```

#### **2. Generate an AxonOps API token for your organisation**

Login to your AxonOps console. For the SaaS console go to http://console.axonops.com. 

Once you have logged in, choose the organisation you want to create an API token for. Then enter the API Tokens section:

<img width="1076" alt="API Tokens" src="https://github.com/user-attachments/assets/6533429a-892b-4a46-90d9-93b3617c5660">

From there, click create a new API Token. Give the token a name, expiry period, select the clusters you want to be able to access with the token and select the Readonly Role

<img width="602" alt="Create New Token" src="https://github.com/user-attachments/assets/7cfc852e-5797-464d-afdf-7228d4b39dd4">

Click the Generate button and then you can copy the API token to use in Step 3.

<img width="604" alt="Generated Token" src="https://github.com/user-attachments/assets/4632bd45-e444-46c9-b139-13aca0ec3924">

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
python axonops_cav_extractor.py ....
```

#### **8. Deactivate the Virtual Environment**

Once you are done working, deactivate the virtual environment to return to your system's default Python environment:

```bash
deactivate
```

These steps ensure that your project's dependencies are managed separately from other projects and avoid conflicts between package versions.
