# axonops-capacity-report

extrapolate=false&sampleResolution=5&bucketResolution=1&maxResult=2048


## Ollama Setup

Here are the instructions to download and install Ollama on macOS, Windows, and Linux, and then install and start using Llama 3.2:

### macOS

1. **Download Ollama**:
   - Visit the official Ollama website to download the macOS installer.

2. **Install Ollama**:
   - Double-click the downloaded installer and follow the on-screen instructions to complete the installation.

3. **Verify Installation**:
   - Open Terminal and type `ollama`. You should see a list of commands if installed correctly.

4. **Install Llama 3.2 Model**:
   - In Terminal, run:
     ```bash
     ollama pull llama3:8b
     ```

5. **Start Using Llama 3.2**:
   - Run the model with:
     ```bash
     ollama run llama3:8b
     ```

### Windows

1. **Download Ollama**:
   - Visit the official Ollama website and download the Windows installer.

2. **Install Ollama**:
   - Locate the downloaded file, double-click it, and follow the installation instructions.

3. **Verify Installation**:
   - Open Command Prompt and type `ollama`. You should see a list of commands if installed correctly.

4. **Install Llama 3.2 Model**:
   - In Command Prompt, execute:
     ```bash
     ollama pull llama3:8b
     ```

5. **Start Using Llama 3.2**:
   - Run the model with:
     ```bash
     ollama run llama3:8b
     ```

### Linux

1. **Download and Install Ollama**:
   - Open Terminal and run:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```

2. **Verify Installation**:
   - In Terminal, type `ollama` to confirm installation by checking for available commands.

3. **Install Llama 3.2 Model**:
   - Execute in Terminal:
     ```bash
     ollama pull llama3:8b
     ```

4. **Start Using Llama 3.2**:
   - Run the model with:
     ```bash
     ollama run llama3:8b
     ```

These steps will help you set up and interact with Llama 3.2 using Ollama from this python app