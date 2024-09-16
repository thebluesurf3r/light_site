# Job Application Tracker for LinkedIn

## Overview
This Python project automates the process of tracking job applications submitted via LinkedIn by extracting key details from application confirmation emails and storing the data in a PostgreSQL database for easy access and analysis.

The system securely retrieves emails from Gmail using `IMAP`, extracts relevant information such as the organization name, job title, job location, and the date and time of the application, and upserts the data into a PostgreSQL database. It also identifies and handles any missing or ambiguous data (e.g., 'Unknown' designations).

## Features
- **Secure Credential Handling**: Credentials for Gmail and the database are encrypted using `Fernet` encryption for secure storage.
- **Email Parsing**: Retrieves job application emails via `IMAP`, and parses the content using regular expressions and `BeautifulSoup` to extract details.
- **Data Storage in PostgreSQL**: Automatically upserts application details (organization, job title, location, date) into a PostgreSQL database, avoiding duplicates.
- **Data Analysis**: Provides insights into missing data (e.g., unknown job titles) and generates reports saved as CSV or Pickle files.
- **Time Zone Conversion**: Automatically converts email timestamps to Indian Standard Time (IST) for consistent data storage.
  
## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/job-application-tracker.git
   cd job-application-tracker
