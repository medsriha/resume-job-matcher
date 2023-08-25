
"""
Extract data from input resume such email, phone, number, work experience, education then create a user profile
"""

import re
import spacy
from utils import TextProcessor

# Load the English model
nlp = spacy.load("en_core_web_lg")

CONTACT_INFO = {'contact information', 'personal information', 'contact'}
OBJECTIVE = {'objective', 'career objective', 'professional objective', 'summary', 'employment objective', 'professional goals', 'career goal'}
SKILLS = {'transferable skills', 'language competencies and skills', 'software skills', 'technologies', 'areas of experience', 'computer knowledge', 'competencies', 'summary of qualifications', 'other skills', 'technical proficiencies', 'soft skills', 'areas of knowledge', 'aualifications', 'career related skills', 'professional skills', 'credentials', 'proficiencies', 'qualifications', 'skills', 'other abilities', 'transferable skillslanguage skills', 'computer skills', 'technical experience', 'personal skills', 'areas of expertise', 'technical skills', 'languages', 'programming languages', 'specialized skills'}
EDUCATION = {'academic training', 'programs', 'educational background', 'academic qualification', 'education', 'academic background', 'course project experience', 'educational qualifications', 'courses', 'courses relevant to the job', 'apprenticeships', 'related courses', 'educational training', 'certifications', 'licenses', 'education and training'}
EXPERIENCE = {'professional experience', 'working history', 'professional activities', 'project', 'personal projects', 'military service', 'college activities', 'freelance experience', 'volunteer experience', 'training', 'experience', 'special training', 'professional affiliations', 'leadership experience', 'volunteer work', 'career related experience', 'freelance', 'related experience', 'army experience', 'internship experience', 'project portfolio', 'technical expertise', 'professional background', 'professional employment', 'teaching experience', 'academic experience', 'professional employment history', 'career summary', 'professional training', 'military experience', 'projects', 'employment data', 'additional achievements', 'additional experience', 'relevant experience', 'professional associations', 'work history', 'research experience', 'related course projects', 'volunteering', 'internships', 'accomplishments', 'employment history', 'activities', 'military background', 'work experience', 'programming experience'}
ACCOMPLISHMENT = {'research projects', 'honorsmemberships and honors', 'conference presentations', 'thesis', 'highlights', 'exhibits', 'awards and honors', 'current research interests', 'conventions', 'awards', 'activities and honors', 'research grants', 'achievements and accomplishments', 'dissertations', 'publications', 'presentations', 'theses', 'grants and scholarships', 'achievement', 'professional publications', 'papers', 'memberships honors', 'memberships and honorshonors', 'awards and recognition', 'awards and achievements'}
MISC = {'civic activities', 'references', 'professional development', 'additional information', 'salary history', 'refere', 'public speaking engagements', 'extra-curricular activities', 'availability', 'community involvement', 'professional memberships', 'interest and hobbies', 'interests', 'digital', 'memberships', 'athletic involvement', 'affiliations', 'associations', 'extracurricular activities', 'interests and hobbies', 'conferences and presentations', 'references from linkedin'}
ALL_TITLES = {'academic training', 'programs', 'working history', 'personal projects', 'professional development', 'military service', 'apprenticeships', 'volunteer experience', 'training', 'awards and honors', 'special training', 'professional affiliations', 'leadership experience', 'current research interests', 'competencies', 'volunteer work', 'technical proficiencies', 'aualifications', 'educational training', 'professional skills', 'professional employment', 'course project experience', 'career summary', 'transferable skillslanguage skills', 'digital', 'projects', 'additional achievements', 'research grants', 'technical experience', 'affiliations', 'associations', 'theses', 'interests and hobbies', 'related course projects', 'grants and scholarships', 'areas of expertise', 'volunteering', 'education', 'awards and recognition', 'programming languages', 'professional experience', 'academic background', 'professional activities', 'objective', 'career objective', 'educational qualifications', 'conference presentations', 'thesis', 'highlights', 'exhibits', 'areas of experience', 'computer knowledge', 'experience', 'awards and achievements', 'conventions', 'soft skills', 'career related experience', 'freelance', 'areas of knowledge', 'extra-curricular activities', 'technical expertise', 'community involvement', 'professional employment history', 'employment objective', 'contact', 'employment data', 'memberships', 'athletic involvement', 'publications', 'personal skills', 'contact information', 'languages', 'employment history', 'activities', 'programming experience', 'conferences and presentations', 'references from linkedin', 'research projects', 'civic activities', 'honorsmemberships and honors', 'language competencies and skills', 'additional information', 'professional goals', 'technologies', 'refere', 'educational background', 'summary of qualifications', 'other skills', 'related experience', 'career related skills', 'availability', 'internship experience', 'project portfolio', 'credentials', 'professional background', 'awards', 'teaching experience', 'professional memberships', 'qualifications', 'other abilities', 'activities and honors', 'personal information', 'computer skills', 'additional experience', 'relevant experience', 'presentations', 'extracurricular activities', 'papers', 'achievement', 'professional objective', 'courses', 'technical skills', 'accomplishments', 'certifications', 'work experience', 'project', 'references', 'transferable skills', 'related courses', 'software skills', 'college activities', 'freelance experience', 'career goal', 'salary history', 'public speaking engagements', 'army experience', 'courses relevant to the job', 'proficiencies', 'skills', 'academic experience', 'summary', 'professional training', 'military experience', 'interest and hobbies', 'academic qualification', 'interests', 'education and training', 'achievements and accomplishments', 'dissertations', 'professional associations', 'work history', 'research experience', 'professional publications', 'memberships and honorshonors', 'internships', 'memberships honors', 'military background', 'licenses', 'specialized skills'}

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
    "date_pattern": r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}|\d{1,2}[ /\.-]\d{4}|Present|Current|to current|to present)",
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
        #self.tokens = re.split(r"\n| {4,}", self.text)

        self.key = key
        self.cleaner = TextProcessor()


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
        if text in EXPERIENCE or re.findall(REGEX_PATTERNS["experience_pattern"], text):
            return True
        return False


    def __is_section_skills(self, text) -> bool:
        """
        If section title is skills.
        
        Returns:
            bool: 
        """
        if text in SKILLS or re.findall(REGEX_PATTERNS["skills_pattern"], text):
            return True
        return False
    

    def __is_section_education(self, text) -> bool:
        """
        If section title is education.
        
        Returns:
            bool: 
        """
        if text in EDUCATION or re.findall(r"(Education|EDUCATION)(?: and|AND)? (Training|TRAINING)", text):
            return True
        return False


    def get_section(self, section = None) -> list:
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
        tokens = self.text.splitlines(keepends=True)

        for token in tokens:
            # Remove punct from text and lower case it
            tmp_token = self.cleaner.remove_punct(token).lower()
            
            if not tmp_token: 
                continue
            elif is_section and not fct(tmp_token) and tmp_token not in ALL_TITLES:
                details.append(token)
            elif tmp_token in ALL_TITLES and not fct(tmp_token):
                # i.e, if text is a section title and section title is not experience
                is_section = False
            elif fct(tmp_token):
                # Found the required section
                is_section = True

        return "".join(details)

    def get_experience(self):
        """
        Extract experience from raw resume using multiple logics.

        Returns:
            str: 
        """

        tokens = self.get_section(section='experience').splitlines(True)
        details = {}
        dates_list = []
        is_date_found  = False
        
        for token in tokens:
            
            dates = self.__get_position_year(self.cleaner.remove_punct(token))
            if len(dates) == 1: 
                # Found one date, second date is probably in the nextline or after
                dates_list.append(dates[0])

            
            if len(dates) == 2 and len(dates_list) == 2:
                # Found two dates on the same line and have one date in the list
                raise Exception("Inconcisency found in one of the lines")
            
            elif len(dates) > 2 or len(dates_list) > 2:
                raise Exception(f"{max(len(dates), len(dates_list))} dates found in a single line")
                        
            elif len(dates) == 2 or len(dates_list) == 2:
                # Found two dates on the same line or missing second date was found
                if len(dates) == 2: # keys
                    key_date = tuple(dates)
                else:
                    key_date = tuple(dates_list)
                    
                # Append sentence
                details[key_date] = [token]
                is_date_found  = True
                # Empty 
                dates_list = []
            elif is_date_found and len(dates) == 0:
                # Date already found, next is to collect all the details 
                # that comes after until next date
                details[key_date].append(token)
            else:
                print('discard', token)

        return details

    def create(self):
        """
        Return a dictionary with resume data
        """

        return {"index": self.key,
                "name": self.get_names(),
                "email": self.get_emails(),
                "phone_number": self.get_phone_numbers(),
                "links": self.get_links(),
                "experience": self.get_experience(),
                "skills": self.get_section(section="skills"),
                "education": self.get_section(section="education") }

if __name__ == "__main__":
    from utils import TextExtractor
    import pandas as pd
    import pprint
    
    path = "C:\\Users\\medSr\\Documents\\resume-job-matcher\\resumes\\MISC\\MohamedSriha-Discord.pdf"
    path ="C:\\Users\\medSr\\Documents\\resume-job-matcher\\resumes\\FITNESS\\39805617.pdf"
    resume_txt = TextExtractor(file_path = path).convert_pdf()
    profile = Profile(resume=resume_txt, key=path)
    print(profile.get_section('experience'))
    # profile.get_experience()
    # pprint.pprint(profile.get_experience())
    # print(Profile(resume=resume_txt, key=path).create())
    
    # resume_txt = TextExtractor(file_path = path).convert_pdf()
    # data = [Profile(resume=v, key=k).create() for k, v in resume_txt.items()]
    # df = pd.DataFrame(data=data)
    # df.to_csv("./Profiles.csv", encoding="utf-8", sep="|")
    # print(Profile(resume=resume_txt, key=path).get()["education"])
    # Profile(resume=resume_txt, key=path).get()
    # pattern = r"(\d{4}))"
    # print(re.findall(pattern, "2022-present", flags=re.IGNORECASE))