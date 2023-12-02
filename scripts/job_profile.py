import json
import re
from utils import TextProcessor
from . import constants


class Profile(object):

    def __init__(self, in_path, out_path) -> dict:
        self.in_path = in_path
        self.out_path = out_path
        

    def __create(self, text) -> list:
        """
        Extract details from job desctiption and structure them by section.
        Start of each section is found using regex

        Args:
            text (str): Job description in a text format

        Returns:
            Dict: details listed per section found
        """
        
        details = {}
        tokens = text.splitlines(keepends=True)
        is_section = False
        
        pattern = re.compile(constants.REGEX_PATTERNS['section_pattern'])
        cleaner = TextProcessor()
        
        for token in tokens:

            tmp_token = cleaner.remove_punct(token)
            if not tmp_token: 
                continue

            # Find if a sentence has the compiled pattern
            match = pattern.match(token.strip())
            
            if match:
                sticky = tmp_token
                details[sticky] = []
                is_section = True
            elif tmp_token.istitle() or tmp_token.isupper():
                sticky = tmp_token
                details[sticky] = []
                is_section = True
            elif is_section:
                details[sticky].append(token)
            else:
                if 'other' not in details:
                    details['other'] = []
                details['other'].append(token)

        return details

    def create(self) -> None:
        # Read from file
        try:
            with open(self.in_path, "r", encoding="utf-8") as json_file:
                jobs = json.load(json_file)
        except FileNotFoundError:
            print(f'file in {self.in_path} not found')


        if len(jobs) == 0:
            raise Exception("File in {self.in_path} exists but it's empty")
        
        # Parse and load into existing dictionary
        for job_catergory, values in jobs.items():
            for ids, job_dt in values.items():
                if "jobDescriptionText" in job_dt:
                    jobs[job_catergory][ids]['parsed'] = self.__create(job_dt["jobDescriptionText"])
                else:
                     jobs[job_catergory][ids]['parsed'] = []

        # Update the file with the new details then write to disk
        with open(self.out_path, 'w', encoding='utf-8') as json_file:
            json.dump(jobs, json_file, ensure_ascii=False, indent=4)

    
if __name__== "__main__":
    Profile(in_path='../data/indeed-jobs.json', out_path='../data/job-profile.json').create()
