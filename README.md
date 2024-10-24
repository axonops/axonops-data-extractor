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