
"""
Extract data from input resume such email, phone, number, work experience, education then create a user profile
"""

import re
import spacy
from utils import TextCleaner

# Load the English model
nlp = spacy.load("en_core_web_lg")

RESUME_SECTIONS = {
    "Accomplishments",
    "Achievements and Accomplishments",
    "Additional Achievements",
    "Additional Information",
    "Availability",
    "Awards",
    "Awards and Honors",
    "Awards and Recognition",
    "Certifications",
    "Computer Skills",
    "Conferences and Presentations",
    "Contact Information",
    "Courses Relevant to the Job",
    "Education",
    "Education and Training",
    "Employment History",
    "Experience",
    "Extracurricular Activities",
    "Grants and Scholarships",
    "Highlights",
    "Honors",
    "Interest and Hobbies",
    "Interests and Hobbies",
    "Internship Experience",
    "Language Skills",
    "Languages",
    "Leadership Experience",
    "Licenses",
    "Memberships Honors",
    "Memberships and Honors",
    "Military Service",
    "Objective",
    "Personal Information",
    "Personal Projects",
    "Professional Affiliations",
    "Professional Development", 
    "Research Experience",
    "Professional Experience",
    "Professional Goals",
    "Technical Skills",
    "Professional Memberships",
    "Professional Skills",
    "Programming Languages",
    "Project Portfolio",
    "Projects",
    "Public Speaking Engagements",
    "Publications",
    "Qualifications",
    "References",
    "References from LinkedIn",
    "Research Experience",
    "Salary History",
    "Skills",
    "Soft Skills",
    "Software Skills",
    "Summary",
    "Summary of Qualifications",
    "Teaching Experience",
    "Technical Expertise",
    "Technical Proficiencies",
    "Transferable Skills",
    "Volunteer Experience",
    "Volunteer Work",
    "Volunteering",
    "Work Experience",
    "Work History",
    "QUALIFICATIONS",
    "ACCOMPLISHMENTS",
    "SOFT SKILLS",
    "RESEARCH EXPERIENCE",
    "PERSONAL INFORMATION",
    "CONFERENCES AND PRESENTATIONS",
    "ADDITIONAL INFORMATION",
    "WORK HISTORY",
    "INTERESTS AND HOBBIES",
    "CERTIFICATIONS",
    "PROGRAMMING LANGUAGES",
    "PROFESSIONAL DEVELOPMENT",
    "RESEARCH EXPERIENCE",
    "PROFESSIONAL SKILLS",
    "HIGHLIGHTS",
    "INTEREST AND HOBBIES",
    "PROJECT PORTFOLIO",
    "REFERENCES",
    "MEMBERSHIPS AND HONORS",
    "SOFTWARE SKILLS",
    "TEACHING EXPERIENCE",
    "EDUCATION AND TRAINING",
    "PUBLICATIONS",
    "VOLUNTEERING",
    "PROFESSIONAL GOALS",
    "TECHNICAL SKILLS",
    "CONTACT INFORMATION",
    "ACHIEVEMENTS AND ACCOMPLISHMENTS",
    "SUMMARY OF QUALIFICATIONS",
    "PROFESSIONAL MEMBERSHIPS",
    "REFERENCES FROM LINKEDIN",
    "VOLUNTEER EXPERIENCE",
    "LANGUAGES",
    "VOLUNTEER WORK",
    "TECHNICAL EXPERTISE",
    "AWARDS AND RECOGNITION",
    "LICENSES",
    "INTERNSHIP EXPERIENCE",
    "OBJECTIVE",
    "MEMBERSHIPS HONORS",
    "PUBLIC SPEAKING ENGAGEMENTS",
    "LEADERSHIP EXPERIENCE",
    "EMPLOYMENT HISTORY",
    "GRANTS AND SCHOLARSHIPS",
    "SUMMARY",
    "HONORS",
    "AWARDS AND HONORS",
    "COMPUTER SKILLS",
    "EXTRACURRICULAR ACTIVITIES",
    "PROFESSIONAL EXPERIENCE",
    "EXPERIENCE",
    "TECHNICAL PROFICIENCIES",
    "PERSONAL PROJECTS",
    "SALARY HISTORY",
    "TRANSFERABLE SKILLS",
    "ADDITIONAL ACHIEVEMENTS",
    "LANGUAGE SKILLS",
    "AWARDS",
    "PROFESSIONAL AFFILIATIONS",
    "COURSES RELEVANT TO THE JOB",
    "SKILLS",
    "AVAILABILITY",
    "MILITARY SERVICE",
    "EDUCATION",
    "WORK EXPERIENCE",
    "PROJECTS"}

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
    "date_pattern": r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}|\d{1,2}[ /\.-]\d{4}|present|current|Present|Current)",
    "experience_pattern": r"(Professional|Work|Internship|Volunteer|Volunteering|Leadership|Research|Teaching|PROFESSIONAL|WORK|INTERNSHIP|VOLUNTEER|VOLUNTEERING|LEADERSHIP|RESEARCH|TEACHING)\s+(Experience|experience|EXPERIENCE|Expertise|expertise|EXPERTISE|History|history|HISTORY|Activities|activities|ACTIVITIES)",
    "skills_pattern": r"(Technical|Summary|Hard|TECHNICAL|SUMMARY|HARD)(?: of|OF)? (Proficiencies|Qualifications|Expertise|Skills|SKILLS|PROFICIENCIES|QUALIFICATIONS|EXPERTISE)"
    }


class Profile(object):
    
    def __init__(self, resume, key):
        
        if not key:
            raise Exception(f"Must provide a key to proceed")
        
        if type(resume) == str:
            self.text = resume
        else:
            self.text = resume[key]

        self.doc = nlp(self.text)
        self.tokens = re.split(r"\n| {4,}", self.text)
        
        self.key = key
        self.cleaner = TextCleaner()
        
    def get_emails(self):
        """
        Extract email addresses from a given string using RegEx.

        Returns:
            list: A list containing all the extracted email addresses.
        """
        emails = re.findall(REGEX_PATTERNS["email_pattern"], self.text)
        if emails:
            # The first email is assumed to be the user"s email address
            return emails[0]
        return None
        
    def get_names(self):
        """Extracts and returns a list of names from the given 
        text using spaCy"s named entity recognition.

        Returns:
            list: A list of strings representing the names extracted from the text.
        """
        names = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        if names:
            return names[0]  
        return None
        
    def get_links(self):
        """
        Find links of any type in a given string using RegEx.
        
        Returns:
            list: A list containing all the found links.
        """
        dic = {"linkedin": None, 
               "github": None, 
               "other": []}
        
        links = re.findall(REGEX_PATTERNS["link_pattern"], self.text)
        for link in links:
            # Normalize
            lower = link.lower()
            if "github" in lower:
                dic["github"] = link
            elif "linkedin" in lower:
                dic["linkedin"] = link
            else:
                if lower not in dic["other"]:
                    dic["other"].append(link)
        return dic

    def get_phone_numbers(self) -> str:
        """
        Extract phone numbers from a given string using RegEx.

        Returns:
            list: A list containing all the extracted phone numbers.
        """
        phone_numbers = re.findall(REGEX_PATTERNS["phone_pattern"], self.text)
        if phone_numbers: return phone_numbers[0]
        return None
    
    def __get_position_year(self, text) -> list:
        """
            Extract position and year from a given string.

            Args:
                text (str): The string from which to extract position and year.

            Returns:
                list: A list containing the extracted position and year.
        """
    
        matches = re.findall(REGEX_PATTERNS["date_pattern"], text)

        return matches
    
    def __is_section_experience(self, text) -> bool:
        """
        If section title is work experience.
        
        Returns:
            bool: 
        """
        if text in ("EXPERIENCE", "experience", "Experience", "Accomplishments", "ACCOMPLISHMENTS") or\
              re.findall(REGEX_PATTERNS["experience_pattern"], text):
            return True
        return False


    def __is_section_skills(self, text) -> bool:
        """
        If section title is skills.
        
        Returns:
            bool: 
        """
        if text in ("SKILLS", "skills", "Skills", "Qualifications", "QUALIFICATIONS", "Highlights", "HIGHLIGHTS") or\
            re.findall(REGEX_PATTERNS["skills_pattern"], text):
            return True
        return False
    

    def __is_section_education(self, text) -> bool:
        """
        If section title is education.
        
        Returns:
            bool: 
        """
        if text in ("EDUCATION", "education", "Education") or re.findall(r"(Education|EDUCATION)(?: and|AND)? (Training|TRAINING)", text):
            return True
        return False


    def get_section(self, section = None):
        """
        Extract experience from raw resume using multiple logics.

        Args:
            text (str): The string from which to extract experience.

        Returns:
            str: A string containing all the extracted experience.
        """
        if section:
            if section == "experience":
                fct = self.__is_section_experience
            elif section == "skills":
                fct = self.__is_section_skills
            elif section == "education":
                fct = self.__is_section_education
            else:
                raise Exception("Section name is unknown. Please provide one of the following input (experience, skills, and education)")
        else:
            raise Exception("Section name is unknown. Please provide one of the following input (experience, skills, and education)")
        
        details = []
        is_section = False

        for token in self.tokens:
            # Validation text
            tmp_txt = self.cleaner.remove_punct(token)
            if tmp_txt:
                if is_section and tmp_txt not in RESUME_SECTIONS :
                    details.append(self.cleaner.remove_tabs(token))

                elif tmp_txt in RESUME_SECTIONS and not fct(tmp_txt):
                    # If text is a section title and section text does not meet the pattern
                    is_section = False

                elif fct(tmp_txt):
                    # Found section
                    is_section = True

        details = " ".join(details)

        if section == 'experience':
            # Extract dates
            # for item in details:
            date = self.__get_position_year(details)
                # if date:
            print(date)
            
        return details
        
    
    
    def create(self):
        """
        Return a dictionary with resume data
        """
        #return [ent.text for ent in nlp(self.get_section(section = "experience")) if ent.label_ == "ORG"]

        return {"index": self.key,
                "name": self.get_names(),
                "email": self.get_emails(),
                "phone_number": self.get_phone_numbers(),
                "links": self.get_links(),
                "experience": self.get_section(section = "experience"),
                "skills": self.get_section(section="skills"),
                "education": self.get_section(section="education") }

if __name__ == "__main__":
    from utils import TextExtractor
    import pandas as pd

    path = "C:\\Users\\medSr\\Documents\\resume-job-matcher\\resumes\\MISC\\MohamedSriha-Discord.pdf"
    path ="C:\\Users\\medSr\\Documents\\resume-job-matcher\\resumes\\CHEF\\10333299.pdf"
    resume_txt = TextExtractor(file_path = path).convert_pdf()
    Profile(resume=resume_txt, key=path).create()['experience']
    # print(Profile(resume=resume_txt, key=path).create())
    
    # resume_txt = TextExtractor(file_path = path).convert_pdf()
    # data = [Profile(resume=v, key=k).create() for k, v in resume_txt.items()]
    # df = pd.DataFrame(data=data)
    # df.to_csv("./Profiles.csv", encoding="utf-8", sep="|")
    # print(Profile(resume=resume_txt, key=path).get()["education"])
    # Profile(resume=resume_txt, key=path).get()
    # pattern = r"(\d{4}))"
    # print(re.findall(pattern, "2022-present", flags=re.IGNORECASE))