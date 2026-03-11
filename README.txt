=============================================
RECORD MANAGEMENT SYSTEM (RMS)
Author: Sean Looc
Date: November 11, 2025
=============================================
---------------------------------------------
HOW TO RUN THE PROJECT
---------------------------------------------

1. REQUIREMENTS
   - Python (version 3.10 or higher)
   - MySQL Server or XAMPP
   - Flask and Flask-MySQLdb modules

2. INSTALL REQUIRED MODULES
   Open Command Prompt (CMD) and type:
pip install flask
pip install flask-mysqldb
pip install werkzeug

3. IMPORT DATABASE
- Open MySQL Workbench or phpMyAdmin.
- Create a new database named `rms_db`.
- Import the file `rms_db.sql` included in this project.

Default Admin Account:
• Username: admin
• Password: admin123

4. RUN THE SYSTEM
- Open Command Prompt.
- Change directory to where the `app.py` file is located.
  Example:
  ```
  cd Desktop\rms
  ```
- Run the Flask app using:
  ```
  python app.py
  ```
- Open your web browser and go to:
  ```
  http://localhost:5000
  ```


---------------------------------------------
END OF FILE
---------------------------------------------