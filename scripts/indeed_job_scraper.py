import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import re
from datetime import datetime, timedelta

class ExtractJobsFromIndeed(object):
    def __init__(self, 
                 headless = False,
                 # Search criteria
                 params = {"q": "data science", 
                           "l": "chicago IL",
                           "fromage": "7",
                           "radius": "35"},
                url = "https://www.indeed.com/jobs?"):
                
        # Webdriver configuration
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})
        option.add_argument("--enable--javascript")
        option.add_argument("--disable-gpu")
        option.add_argument("--no-sandbox")
        option.add_argument("--enable-automation")
        option.add_argument("--disable-infobar")
        option.add_argument("--disable-dev-shm-usage")

        self.params = params
        
        # Whether to show the browser while scrapping the data
        if headless:
            option.add_argument("--headless")
            
        # Intiate driver
        self.driver = webdriver.Chrome(options=option)
        
        # Construct final url with user"s fiter
        url = url + urllib.parse.urlencode(params)
        # First call
        self.driver.get(url)
        # Store data in memory prior to disk
        self.__details = []


    def __get(self, attiribute, by = None, element = None) -> str:
        
        if element:
            element = element
        else:
            element = self.driver
            
        try:
            return element.find_element(by, attiribute).text
        except NoSuchElementException as e:
            return 'Error: ' + repr(e)

    def __get_job_details(self) -> None:
        """
        helper function -> Scrape job details from indeed.com
        """        

        try:
            # Close sign up popup
            self.driver.find_element(By.XPATH, '//button[@aria-label="close"]').click()
        except NoSuchElementException:
            # No popup window this time
            pass
        
        # Extract all webelements with job information
        web_elements = self.driver.find_elements(By.XPATH, '//td[@class="resultContent"]')

        for elem in web_elements:

            dic = {}
            # Click on content
            elem.click()
            # wait until job preview finishes loading
            time.sleep(5)
            # Posting date on indeed
            date = self.__get('//span[@class="date"]', By.XPATH, elem)
            # Process the raw date and convert it into the proper format
            if "Today" in date:
                # Today
                dic["job_post_date"] = datetime.now().strftime("%m/%d/%Y")
            else:
                try:
                    days = int(re.sub("[^0-9]", "", date))
                    dic["job_post_date"] = (datetime.now() - timedelta(days=days)).strftime("%m/%d/%Y")
                except ValueError as e:
                    dic["job_post_date"] = 'Error: ' + repr(e)
                
                
            # Filter params
            dic["filter_job_title"] = self.params["q"]
            # Job title
            dic["job_title"] = self.__get("jobTitle", By.CLASS_NAME, elem)
            # Company name
            dic["company_name"] = self.__get("companyName", By.CLASS_NAME, elem)
            # Job location
            dic["companyLocation"] = self.__get("companyLocation", By.ID)
            # filter info
            dic["locationFromFilter"] = self.params["l"]
            # Detailed job description
            dic["jobDescriptionText"] = self.__get("jobDescriptionText", By.ID)
            # Benefit
            dic["benefits"] =  self.__get("benefits", By.ID)
            # Comp and other
            dic["salaryInfoAndJobType"] = self.__get("salaryInfoAndJobType", By.ID)
            # Section. May lists job type such full time
            dic["jobDetailsSection"] = self.__get("jobDetailsSection", By.ID)
            # Append into a list
            self.__details.append(dic)
            # sleep to avoid blocking
            time.sleep(5)
    
   
    def get_job_details(self) -> list:
        
        """
        Scrapes job details from indeed.com
        """ 
        
        page_number = 1
        
        while page_number < 2:
            # Run extraction batch - links from this function will
            # be appended into a csv file 
            self.__get_job_details()
            # Move to the next page using pagination
            page_number += 1
            try:
                # Pagination
                self.driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-next"]').click()
            except NoSuchElementException:
                # No more page to scrape, the job is done
                break
        print(f">>> Complete: {page_number} pages were crawled")
        return self.__details


if __name__ == "__main__":
    
    data = ExtractJobsFromIndeed().get_job_details()

    file_path = "../data/indeed-jobs.json"

    # Step 1: Read the existing JSON data from the file (if it exists)
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty dictionary
        existing_data = []

    # Step 2: Append your new dictionary to the existing dictionary
    for elem in data:
        existing_data.append(elem)
    
    # Step 3: Write the updated dictionary back to the JSON file
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(existing_data, json_file, indent=4)