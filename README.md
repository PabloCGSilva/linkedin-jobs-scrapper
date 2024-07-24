### LinkedIn Job Scraper

This script uses Selenium to scrape job listings from LinkedIn and saves them to an HTML file.

#### Prerequisites

1. Python 3.x
2. `pip` (Python package installer)
3. A LinkedIn account

#### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/linkedin-job-scraper.git
    cd linkedin-job-scraper
    ```

2. Create a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add your LinkedIn credentials:

    ```env
    LINKEDIN_USERNAME=your_linkedin_email
    LINKEDIN_PASSWORD=your_linkedin_password
    ```

#### Usage

1. Update the `job_search_url` variable in the script with the desired LinkedIn job search URL.

2. Run the script:

    ```sh
    python linkedin_job_scraper.py
    ```
