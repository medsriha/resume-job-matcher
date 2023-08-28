import json
from utils import TextProcessor

JOB_DESC = {"job summary", "objective", "the role", "key responsibilities", "duties", "Description"}
SKILLS = {"preferred skills", "skills", "set yourself apart with", "competence", "qualifications", "requirements"}
BENEFIT = {"benefits", "You will benefit from", "Benefits of Working Here"}
EDUCATION = {"education"}
ALL_TITLES = {"job summary", "objective", "the role", "key responsibilities", "duties", "skills", "competence", "qualifications", "requirements", "benefits", "education" }

class Profile(object):

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.cleaner = TextProcessor()

    # def __get_section(self, text, section) -> bool:
    #     if section == "description":
    #         if text in JOB_DESC:
    #             return True
    #     elif section == "skills":
    #         if text in SKILLS:
    #             return True
    #     elif section == "benefit":
    #         if text in BENEFIT:
    #             return True
    #     elif section == "education":
    #         if text in EDUCATION:
    #             return True
    #     else:
    #         raise Exception(f"Unknown section {section}")
        
    #     return False
    
    # def get_section(self, text, section = None) -> list:
    #     """
    #     Extract details from raw resume

    #     Args:
    #         text (str): The string from which to extract experience.

    #     Returns:
    #         List: details listed under the provided section
    #     """
    #     if not section:
    #         raise Exception("Section name is unknown. Please provide one of the following input (experience, skills, and education)")
        
    #     details = {}
    #     is_section = False
    #     tokens = text.splitlines(keepends=True)

    #     for token in tokens:
    #         # Remove punct from text and lower case it
    #         tmp_token = self.cleaner.remove_punct(token).lower()
    #         if not tmp_token: 
    #             continue
    #         elif is_section and not self.__get_section(text = tmp_token, section=section) and tmp_token not in ALL_TITLES:
    #             # If text is not a section title
    #             details[sticky].append(token)
    #         elif tmp_token in ALL_TITLES and not self.__get_section(text = tmp_token, section=section):
    #             # i.e, if text is a section title and section title is not experience
    #             is_section = False
    #         elif self.__get_section(text = tmp_token, section=section):
    #             # Found the required section
    #             is_section = True
    #             sticky = tmp_token
    #             details[sticky] = []

    #     return details

    # def create(self) -> dict:
    #     try:
    #         with open(self.file_path, "r", encoding="utf-8") as json_file:
    #             jobs = json.load(json_file)
    #     except FileNotFoundError:
    #         print(f'file in {self.file_path} not found')


    #     if len(jobs) == 0:
    #         raise Exception('File in {self.file_path} exists but empty')
        
    #     for i in range(len(jobs)):
                
    #             jobs[i]['parsed'] = {"job_description": self.get_section(jobs[i]["jobDescriptionText"], section='description'),
    #                                  "skills": self.get_section(jobs[i]["jobDescriptionText"], section='skills'),
    #                                  "education": self.get_section(jobs[i]["jobDescriptionText"], section='education'),
    #                                  "benefit": self.get_section(jobs[i]["jobDescriptionText"], section='benefit')
    #                                  }


    #     return jobs
    
if __name__== "__main__":
    text_document = ""
    title_pattern = re.compile(r'^[A-Z][a-zA-Z\s\d:]+:$')
    text_li = text_document.splitlines(keepends=True)
    with open("../data/indeed-jobs.json", "r", encoding="utf-8") as json_file:
        jobs = json.load(json_file)
        s = set()
    j = [job["jobDescriptionText"].splitlines(keepends=True) for job in jobs]
    for job in j:
        for line in job:
            if title_pattern.match(line.strip()):
                if line not in s:
                    s.add(line)