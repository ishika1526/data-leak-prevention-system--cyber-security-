# Data Leak Prevention System (DLP)

**Domain:** Cybersecurity  
**Developed by:** Ishika

## 1. Project Overview

The Data Leak Prevention System is a Python-based web application designed to detect sensitive information and simulate protection against accidental data exposure.

It scans user-provided text or uploaded files, identifies sensitive information, assigns severity levels, and applies policy-based actions.

## 2. Objectives

- Detect sensitive information.
- Identify potential data leakage.
- Classify detected information according to severity.
- Apply protection actions based on configured policies.
- Maintain event logs for monitoring.

## 3. Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- JSON

## 4. Key Features

- Interactive web dashboard.
- Username and leak-channel selection.
- Text input and file upload.
- Sensitive data detection.
- Severity classification.
- Policy-based action handling.
- Event logging and findings display.

## 5. Detection Categories

- Credit Card Numbers
- PAN Numbers
- Phone Numbers
- Email Addresses

## 6. System Actions

| Action | Description |
|---|---|
| BLOCKED | Stops the simulated transfer |
| MASKED | Hides sensitive values |
| WARNED | Displays a warning |
| ALLOWED | Permits content without detected sensitive data |

## 7. Supported Leak Channels

- Email
- USB
- Cloud Upload
- Chat

## 8. Project Workflow

1. User enters text or uploads a file.
2. System scans the content.
3. Sensitive information is identified.
4. Severity is assigned.
5. Configured policies determine the action.
6. Findings and event logs are displayed.

## 9. How to Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 10. Project Limitations

This is an educational DLP simulator. It demonstrates detection and simulated policy actions. It does not directly monitor real network traffic or block actual email, USB, or cloud transfers.

## 11. Conclusion

The project demonstrates how Python and Streamlit can be used to build a basic Data Leak Prevention solution that identifies sensitive information and helps reduce accidental data exposure.
