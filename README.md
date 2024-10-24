# axonops-csv-extractor

This is a Python application that AxonOps users can use to extract their data to CSV for subsequent usage.



## Instructions

### **1. Clone the Repository**

First, clone the GitHub repository to your local machine:

```bash
git clone https://github.com/axonops/axonops-csv-extractor.git
cd axonops-csv-extractor
```

### **2. Generate your AxonOps API token for your organisation**

Login to your AxonOps console, for the SaaS console go to http://console.axonops.com. Once you have logged in, choose the organisation you want to create an API token for. Then enter the API Tokens section:

<img width="1076" alt="Screenshot 2024-10-24 at 13 16 07" src="https://github.com/user-attachments/assets/6533429a-892b-4a46-90d9-93b3617c5660">

From there, click create a new API Token. Give the token a name, expiry period, select the clusters you want to be able to access with the token and select the Readonly Role

<img width="602" alt="Screenshot 2024-10-24 at 13 18 16" src="https://github.com/user-attachments/assets/7cfc852e-5797-464d-afdf-7228d4b39dd4">

Click the Generate button and then you can copy the API token generated to use in Step 3.

<img width="604" alt="Screenshot 2024-10-24 at 13 20 00" src="https://github.com/user-attachments/assets/4632bd45-e444-46c9-b139-13aca0ec3924">


### **3. Set-up your AxonOps organisation and API tokens as environment variables**

To interact with the AxonOps APIs you need to store your organisation and API key as environment variables or add a `.env` to the root directory of the repo. 

See `.env-example` - copy this to a file called `.env` and update it. This file is in .gitignore and will not be committed.

```bash
AXONOPS_ORG_ID="youraxonopsorg"
AXONOPS_API_SECRET_TOKEN="yourapitoken"
```

### **4. Set Up a Python Virtual Environment**

Create a virtual environment in the project directory using `.venv` as the directory name. This ensures that all Python dependencies are installed in an isolated environment specific to this project:

```bash
python3 -m venv .venv
```

This command creates a directory named `.venv` inside your project directory, which contains the virtual environment.

### **5. Activate the Virtual Environment**

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

### **6. Install Required Packages**

With the virtual environment activated, install all necessary packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all specified packages into the virtual environment.

### **7. Run the Python Script**

Now that all dependencies are installed, you can run your Python script:

```bash
python <script-name>.py
```

Replace `<script-name>` with the name of your Python script file.

### **8. Deactivate the Virtual Environment**

Once you are done working, deactivate the virtual environment to return to your system's default Python environment:

```bash
deactivate
```

These steps ensure that your project's dependencies are managed separately from other projects and avoid conflicts between package versions.
