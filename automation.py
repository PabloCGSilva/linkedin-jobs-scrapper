from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import re
from datetime import datetime
import traceback

# LinkedIn credentials
username = 'pablo.carlos.silva@outlook.com'
password = ':dm&%kB)6~2XTph'

# Set up Firefox options
options = webdriver.FirefoxOptions()
options.headless = False  # Set to True if you want to run in headless mode
options.log.level = "trace"

# Initialize the Firefox driver
service = FirefoxService(GeckoDriverManager().install())

try:
    driver = webdriver.Firefox(service=service, options=options)

    # Navigate to LinkedIn login page
    print("Navigating to LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Enter username
    print("Entering username...")
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    time.sleep(1)

    # Enter password
    print("Entering password...")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    time.sleep(1)

    # Click login button
    print("Clicking login button...")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "global-nav")))

    # Allow 30 seconds for manual verification
    print("Please verify the login manually within 30 seconds...")
    time.sleep(30)

    # Navigate to the job search page with specified filters
    job_search_url = "https://www.linkedin.com/jobs/search/?currentJobId=3959224934&eBP=CwEAAAGQ23dD43S-GW7I8xcX6y3uDMFofeURIoxdLK2g_kGjaZ1B4BBfw921cPFAERNq98tYIMSm6yqQ44fbJMNrNC1h2fA4UufptmB6sNeOtP6V69SNhrkUc7RfTFQ9S5fg6JBE_pDbg7EAivABg3pQiQhs9_CGi2jj7esDswDnpoQasuW2b8ZYI0PXX3jQ_P3A7_QpOCU3E7jRznKqHJk4TmyDy6spinE6BRguhklI2xSuJU7wJEAPLpNp5eGR0Jt1NcJ8r6HYjS9H9DpKn-RLBjtCEvCekgKXnSuHup_L7SSkLUjukq3KoAsnm8mj-GuP2sBekp5dn2EGI4r0dASt403Pnbfb2bBDxgT6ukktVpR_ug-WkZVmYoSX2Zasi10WZ-U6Gr6mB22QsOtyO3yiDFQloLWdzbD3dSnw2JV0WK8mqoNIAFYD49dFnqokKFQzID980zjtCGZKpikaTCMkoeyQKYeY1jY&f_WT=2&geoId=92000000&keywords=support+python&location=Worldwide&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"
    print(f"Navigating to job search page: {job_search_url}...")
    driver.get(job_search_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-card-container')))
    time.sleep(5)

    # Get the total number of job results
    try:
        total_results_element = driver.find_element(By.XPATH, "//small[contains(@class, 'jobs-search-results-list__text')]")
        total_results_text = total_results_element.text.strip()
        total_results = int(re.search(r'\d+', total_results_text).group())
        print(f"Total job results: {total_results}")
    except Exception as e:
        print(f"Could not find total results element: {e}")
        total_results = 0
        print("Total job results not found, setting to 0.")

    # Get the job search title for naming the HTML file
    job_search_title_element = driver.find_element(By.ID, "results-list__title")
    job_search_title = job_search_title_element.get_attribute('title').strip().replace(" ", "_")

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create HTML file name and title with the date
    html_output_path = f"{current_date}_{job_search_title}.html"
    html_title = f"Job Listings - {current_date}"
    print(f"HTML file will be saved as: {html_output_path}")

    job_details = []

    # Calculate total number of pages
    jobs_per_page = 25
    total_pages = (total_results // jobs_per_page) + (1 if total_results % jobs_per_page != 0 else 0)
    print(f"Total pages: {total_pages}")

    for current_page in range(total_pages):
        # Scrape job details
        print(f"Scraping job details for page {current_page + 1}...")
        jobs = driver.find_elements(By.CLASS_NAME, 'job-card-container')

        for job in jobs:
            try:
                # Scroll the job into view
                driver.execute_script("arguments[0].scrollIntoView();", job)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(job))
                job.click()
                time.sleep(2)  # Wait for the job description to load

                title_element = job.find_element(By.CLASS_NAME, 'job-card-list__title').text.strip()
                link = job.find_element(By.CLASS_NAME, 'job-card-container__link').get_attribute('href')
                company_element = job.find_element(By.CLASS_NAME, 'job-card-container__primary-description').text.strip()
                description_element = driver.find_element(By.CLASS_NAME, 'jobs-description__container').text.strip()

                # Extract the main part of the link
                link_match = re.match(r"https://www.linkedin.com/jobs/view/\d+/", link)
                if link_match:
                    link = link_match.group(0)

                job_details.append({
                    "title": title_element,
                    "company": company_element,
                    "link": link,
                    "description": description_element
                })

                # Logging each job card scraped
                print(f"Job: {title_element} - {company_element}")

            except Exception as e:
                print(f"An error occurred while scraping a job: {e}")
                traceback.print_exc()

        # Navigate to the next page if there are more pages
        if current_page < total_pages - 1:
            try:
                next_page_button = driver.find_element(By.XPATH, f"//button[@aria-label='Page {current_page + 2}']")
                if next_page_button:
                    driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
                    next_page_button.click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-card-container')))
                    time.sleep(5)
            except Exception as e:
                print(f"An error occurred while navigating to the next page: {e}")
                traceback.print_exc()
                break

    # Generate HTML with job details
    with open(html_output_path, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write(f"<html><head><title>{html_title}</title></head><body>")
        htmlfile.write(f"<h1>{html_title}</h1>")
        htmlfile.write("<ul>")

        for job in job_details:
            htmlfile.write(f"<li><a href='{job['link']}'>{job['title']} at {job['company']}</a><br>{job['description']}</li>")

        htmlfile.write("</ul>")
        htmlfile.write("</body></html>")

    print(f"HTML generated successfully: {html_output_path}")

    # Verify if the total number of job listings changed during scraping
    final_total_results_element = driver.find_element(By.XPATH, "//small[contains(@class, 'jobs-search-results-list__text')]")
    final_total_results_text = final_total_results_element.text.strip()
    final_total_results = int(re.search(r'\d+', final_total_results_text).group())

    if final_total_results != total_results:
        print(f"Warning: The total number of job listings changed from {total_results} to {final_total_results} during scraping.")

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()

finally:
    # Quit the WebDriver session
    if driver:
        driver.quit()
