import json
import re
from utils import TextProcessor

REGEX_PATTERNS = {"section_pattern": r"^\b[A-Z][A-Za-z\s]+\b[:\r\n\s]$"}


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
        pattern = re.compile(REGEX_PATTERNS['section_pattern'])
        cleaner = TextProcessor()
        
        for token in tokens:

            tmp_token = cleaner.remove_punct(token)
            if not tmp_token: 
                continue

            match = pattern.match(token.strip())
            
            if match:
                sticky = tmp_token
                details[sticky] = []
                is_section = True
            elif tmp_token.istitle():
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
            raise Exception('File in {self.in_path} exists but empty')
        
        # Parse and load into existing dictionary
        for i in range(len(jobs)):
            jobs[i]['parsed'] = self.__create(jobs[i]["jobDescriptionText"])

        # Update the file with the new details then write to disk
        with open(self.out_path, 'w', encoding='utf-8') as json_file:
            json.dump(jobs, json_file, ensure_ascii=False, indent=4)

    
if __name__== "__main__":
    Profile(in_path='../data/indeed-jobs.json', out_path='../data/job-profile.json').create()
