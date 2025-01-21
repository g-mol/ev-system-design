# Streamlit Project

This project is a Streamlit application that is used to help you design an electric vehicle system.

The project is available online at [https://ev-system-design.streamlit.app/](https://ev-system-design.streamlit.app/).

## Requirements

- **Python 3.12** (or later)
- A terminal or command prompt to run the application
- Internet access to install dependencies

---

## Setup Instructions

### Step 1: Install Python

1. Download Python 3.12 from the [official Python website](https://www.python.org/downloads/).
2. During installation, ensure the following options are checked:
    - **Add Python to PATH** (important for command-line use).
    - Install recommended options.

   After installation, confirm Python is installed by running the following command in your terminal or command prompt:

   ```bash
   python --version

You should see something like `Python 3.12.x`.

---

### Step 2: Download the Project Files

1. Download the project `.zip` file
2. Extract the `.zip` file into a folder on your computer.

---

### Step 3: Install Dependencies

1. Open a terminal or command prompt and navigate to the project folder where the `requirements.txt` file is located.
   Use the following command to change directories:
   ```bash
   cd path_to_project_folder
   ```
   Replace `path_to_project_folder` with the actual path to your extracted project folder.

2. Install the required libraries by running:
   ```bash
   pip install -r requirements.txt
   ```

   This command installs all necessary dependencies (e.g., Streamlit, pandas, plotly, numpy).

   **Note:** If `pip` is not recognized, ensure Python is installed correctly and added to PATH.

---

### Step 4: Run the Application

1. After installing dependencies, run the application using the following command:
   ```bash
   streamlit run main.py
   ```

2. A URL will appear in the terminal, similar to this:
   ```
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

3. Open the Local URL (e.g., `http://localhost:8501`) in your web browser. The Streamlit app should load.

---

## Troubleshooting

- **`pip` or `streamlit` not recognized:**
    - Ensure Python is installed and added to PATH.
    - Try restarting your terminal or command prompt.

- **Dependencies fail to install:**
    - Update `pip` by running:
      ```bash
      pip install --upgrade pip
      ```
    - Then, try installing the dependencies again.

- **App doesn't load in the browser:**
    - Manually copy the Local URL (e.g., `http://localhost:8501`) from the terminal and paste it into your browser.
