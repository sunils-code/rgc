# rgc

## Table of contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

### Prerequisites

- Python 3 installed on your system.
- DB Browser Sqlite

## Installation

1. **Create and activate the virtual environment**

- Navigate to the project directory.

- Create the virtual environment.

- Example (Windows):

  ```
  python -m venv env
  ```

- Example (Unix/macOS):

  ```
  python3 -m venv env
  ```

- Activate the virtual environment.

- Example (Windows):

  ```
  .\env\Scripts\activate
  ```

- Example (Unix/macOS):

  ```
  source env/bin/activate
  ```

2. **Install Dependencies**

- pip install -r requirements.txt

1. **Running backend data processing to generate sqlite db file**

- In terminal navigate to ~/rgc/src/
- run `python main.py`
- this will generate sqlite db file `rgc_data.db` in ~/rgc/
- this db file can be inspected using DB Browser Sqlite `https://sqlitebrowser.org/dl/`

2. **Running streamlit front end**

- in terminal navigate to ~/rgc/src/frontend/
- Run `streamlit run app.py` in terminal to start the application.
- Navigate to `http://localhost:8501` in your web browser.

3. **Running pytests**

- in terminal navigate to ~/rgc/tests/
- Run `pytest <file_name>`
