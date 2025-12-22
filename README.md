# IQAC Portal

This is a simple Flask-based web application for an Internal Quality Assurance Cell (IQAC) to manage faculty reports and audits.

## Features

- Role-based access control (auditor, university_iqac_coordination, registrar, vice_chancellor, director, iqac_coordinators, hod, faculty).
- Admin panel to manage institutes.
- Faculty can submit their details and reports.
- A multi-level approval process for faculty reports.
- Auditors can review reports, conduct audits using a questionnaire, and assign grades.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will be running at `http://127.0.0.1:5000`.

## Roles and Credentials

The default credentials for the roles are defined in the `app.py` file.

| Role                               | Username                         | Password        |
| ---------------------------------- | -------------------------------- | --------------- |
| Auditor                            | `auditor`                        | `1234`          |
| University IQAC Coordination       | `university_iqac_coordination`   | `adminpass`     |
| Registrar                          | `registrar`                      | `registrarpass` |
| Vice Chancellor                    | `vice_chancellor`                | `vcpass`        |
| Director                           | `director`                       | `directorpass`  |
| IQAC Coordinators                  | `iqac_coordinators`              | `iqacpass`      |
| HOD                                | `hod`                            | `hodpass`       |
| Faculty                            | `faculty`                        | `facultypass`   |

**Note:** These are development credentials and should be replaced with a secure authentication system in a production environment.

## Data Storage

The application uses JSON files for data storage:
- `institutes.json`: Stores the list of institutes.
- `faculty_details.json`: Stores faculty information.
- `faculty_reports.json`: Stores faculty reports and their approval status.
- `credits.json`: Stores the grades assigned to institutes by auditors.

These files are created automatically when the application runs.
