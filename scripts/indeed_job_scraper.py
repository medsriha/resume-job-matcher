import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import re
from datetime import datetime, timedelta

class ExtractJobLinksFromIndeed(object):
    def __init__(self, 
                 headless = False, 
                 params = {"q": "machine learning engineer", 
                           "l": "chicago IL",
                           "fromage": "7",
                           "radius": "35"},
                           url = "https://www.indeed.com/jobs?"):
                
        # Webdriver configuration
        option = webdriver.EdgeOptions()
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
        self.driver = webdriver.Edge(options=option)
        
        # Construct final url with user's fiter
        url = url + urllib.parse.urlencode(params)
        # First call
        self.driver.get(url)
        # main
        self.save_job_details()

    def __save_job_details(self):
        """
        helper function -> Scrape job details from indeed.com
        """        

        try:
            # Close sign up popup
            self.driver.find_element(By.XPATH, "//button[@aria-label='close']").click()
        except:
            pass
        
        # Extract all webelements with job information
        web_elements = self.driver.find_elements(By.XPATH, "//td[@class='resultContent']")

        with open ("./indeed-jobs.csv", "a", encoding="utf-8") as w:
            # Create the writer
            writer = csv.writer(w, delimiter='|')

            for elem in web_elements:

                dic = {}
                # Click on content
                elem.click()
                # wait until job preview appears
                time.sleep(5)
                # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
                # Posting date on indeed
                date = elem.find_element(By.XPATH, "//span[@class='date']").text
                # Process the raw date and convert it into the proper format
                if 'Today' in date:
                    # Today
                    dic['job_post_date'] = datetime.now().strftime('%m/%d/%Y')
                else:
                    days = int(re.sub('[^0-9]', '', date))
                    dic['job_post_date'] = (datetime.now() - timedelta(days=days)).strftime('%m/%d/%Y')
                # Job title
                dic['job_title'] = elem.find_element(By.CLASS_NAME, "jobTitle").text
                # Filter params
                dic['filter_job_title'] = self.params['q']   
                try:
                    # Company name
                    dic['company_name'] = elem.find_element(By.CLASS_NAME, "companyName").text
                except NoSuchElementException:
                    dic['company_name'] = ''
                # Job location
                dic['location'] = elem.find_element(By.CLASS_NAME, "companyLocation").text
                # filter info
                dic['filter_location'] = self.params['l']
                # Detailed job description
                dic['innerHTML'] =  self.driver.find_element(By.CLASS_NAME, "jobsearch-jobDescriptionText").get_attribute('innerHTML')
                # Append into a csv file
                writer.writerow(dic.values())
                # sleep to avoid blocking
                time.sleep(5)
    
   
    def save_job_details(self):
        
        """
        Scrapes job details from indeed.com
        """ 
        
        page_number = 1
        
        while True:
            # Run extraction batch - links from this function will
            # be appended into a csv file 
            self.__save_job_details()
            # Move to the next page using pagination
            page_number += 1
            try:
                # Pagination
                self.driver.find_element(By.XPATH, "//a[@data-testid='pagination-page-next']").click()
            except NoSuchElementException:
                # No more page to scrape, the job is done
                print(f'>> Complete: {page_number} pages were crawled')
                return 


if __name__ == '__main__':
    ExtractJobLinksFromIndeed()
    