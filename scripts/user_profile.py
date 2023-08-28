
"""
Extract data from input resume such email, phone, number, work experience, education then create a user profile
"""

import re
import spacy
from utils import TextProcessor
import json
# Load the English model
nlp = spacy.load("en_core_web_lg")

CONTACT_INFO = {"contact information", "personal information", "contact"}
OBJECTIVE = {"objective", "career objective", "professional objective", "summary", "employment objective", "professional goals", "career goal"}
SKILLS = {"transferable skills", "highlights", "language competencies and skills", "software skills", "technologies", "areas of experience", "computer knowledge", "competencies", "summary of qualifications", "other skills", "technical proficiencies", "soft skills", "areas of knowledge", "aualifications", "career related skills", "professional skills", "credentials", "proficiencies", "qualifications", "skills", "other abilities", "transferable skillslanguage skills", "computer skills", "technical experience", "personal skills", "areas of expertise", "technical skills", "languages", "programming languages", "specialized skills"}
EDUCATION = {"academic training", "programs", "educational background", "academic qualification", "education", "academic background", "course project experience", "educational qualifications", "courses", "courses relevant to the job", "apprenticeships", "related courses", "educational training", "certifications", "licenses", "education and training"}
EXPERIENCE = {"professional experience", "working history", "professional activities", "project", "personal projects", "military service", "college activities", "freelance experience", "volunteer experience", "training", "experience", "special training", "professional affiliations", "leadership experience", "volunteer work", "career related experience", "freelance", "related experience", "army experience", "internship experience", "project portfolio", "technical expertise", "professional background", "professional employment", "teaching experience", "academic experience", "professional employment history", "career summary", "professional training", "military experience", "projects", "employment data", "additional achievements", "additional experience", "relevant experience", "professional associations", "work history", "research experience", "related course projects", "volunteering", "internships", "employment history", "activities", "military background", "work experience", "programming experience"}
ACCOMPLISHMENT = {"accomplishments", "research projects", "honorsmemberships and honors", "conference presentations", "thesis", "exhibits", "awards and honors", "current research interests", "conventions", "awards", "activities and honors", "research grants", "achievements and accomplishments", "dissertations", "publications", "presentations", "theses", "grants and scholarships", "achievement", "professional publications", "papers", "memberships honors", "memberships and honorshonors", "awards and recognition", "awards and achievements"}
MISC = {"civic activities", "references", "professional development", "additional information", "salary history", "refere", "public speaking engagements", "extra-curricular activities", "availability", "community involvement", "professional memberships", "interest and hobbies", "interests", "digital", "memberships", "athletic involvement", "affiliations", "associations", "extracurricular activities", "interests and hobbies", "conferences and presentations", "references from linkedin"}
ALL_TITLES = {"academic training", "programs", "working history", "personal projects", "professional development", "military service", "apprenticeships", "volunteer experience", "training", "awards and honors", "special training", "professional affiliations", "leadership experience", "current research interests", "competencies", "volunteer work", "technical proficiencies", "aualifications", "educational training", "professional skills", "professional employment", "course project experience", "career summary", "transferable skillslanguage skills", "digital", "projects", "additional achievements", "research grants", "technical experience", "affiliations", "associations", "theses", "interests and hobbies", "related course projects", "grants and scholarships", "areas of expertise", "volunteering", "education", "awards and recognition", "programming languages", "professional experience", "academic background", "professional activities", "objective", "career objective", "educational qualifications", "conference presentations", "thesis", "highlights", "exhibits", "areas of experience", "computer knowledge", "experience", "awards and achievements", "conventions", "soft skills", "career related experience", "freelance", "areas of knowledge", "extra-curricular activities", "technical expertise", "community involvement", "professional employment history", "employment objective", "contact", "employment data", "memberships", "athletic involvement", "publications", "personal skills", "contact information", "languages", "employment history", "activities", "programming experience", "conferences and presentations", "references from linkedin", "research projects", "civic activities", "honorsmemberships and honors", "language competencies and skills", "additional information", "professional goals", "technologies", "refere", "educational background", "summary of qualifications", "other skills", "related experience", "career related skills", "availability", "internship experience", "project portfolio", "credentials", "professional background", "awards", "teaching experience", "professional memberships", "qualifications", "other abilities", "activities and honors", "personal information", "computer skills", "additional experience", "relevant experience", "presentations", "extracurricular activities", "papers", "achievement", "professional objective", "courses", "technical skills", "accomplishments", "certifications", "work experience", "project", "references", "transferable skills", "related courses", "software skills", "college activities", "freelance experience", "career goal", "salary history", "public speaking engagements", "army experience", "courses relevant to the job", "proficiencies", "skills", "academic experience", "summary", "professional training", "military experience", "interest and hobbies", "academic qualification", "interests", "education and training", "achievements and accomplishments", "dissertations", "professional associations", "work history", "research experience", "professional publications", "memberships and honorshonors", "internships", "memberships honors", "military background", "licenses", "specialized skills"}

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
    "date_pattern": r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|\d{1,2}[ /\.-]\d{4}|Present|Current|to current|to present)",
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

        self.key = key
        self.cleaner = TextProcessor()


    def get_emails(self) -> str:
        """
        Extract email addresses from a given string using RegEx.

        Returns:
            str: Email address listed on the resume
        """
        emails = re.findall(REGEX_PATTERNS["email_pattern"], self.text)
        if emails:
            # The first email is assumed to be the user"s email address
            return emails[0]
        return ''
        
    def get_names(self) -> str:
        """Extracts and returns a list of names from the given 
        text using spaCy"s named entity recognition.

        Returns:
            str: Person name listed on the resume
        """
        names = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        if names:
            return names[0]  
        return ''
        
    def get_links(self) -> dict:
        """
        Find links of any type in a given string using RegEx.
        
        Returns:
            dict: links listed on the resume including Linkedin and github
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
            str: Phone number listed on the resume
        """
        phone_numbers = re.findall(REGEX_PATTERNS["phone_pattern"], self.text)
        if phone_numbers: return phone_numbers[0]
        return ''
    


    def __get_section(self, text, section) -> bool:

        """
        Returns:

        """

        if section == "contact":
            if text in CONTACT_INFO:
                return True
        elif section == "experience":
            if text in EXPERIENCE or re.findall(REGEX_PATTERNS["experience_pattern"], text):
                return True
        elif section == "skills":
            if text in SKILLS or re.findall(REGEX_PATTERNS["skills_pattern"], text):
                return True
        elif section == "education":
            if text in EDUCATION or re.findall(r"(Education|EDUCATION)(?: and|AND)? (Training|TRAINING)", text):
                return True
        elif section == "objective":
            if text in OBJECTIVE:
                return True
        elif section == "accomplishment":
            if text in ACCOMPLISHMENT:
                return True
        elif section == "misc":
            if text in MISC:
                return True
        else:
            raise Exception(f"Unknown section {section}")
        
        return False

    def get_section(self, section = None) -> list:
        """
        Extract details from raw resume

        Args:
            text (str): The string from which to extract experience.

        Returns:
            List: details listed under the provided section
        """
        if not section:
            raise Exception("Section name is unknown. Please provide one of the following input (experience, skills, and education)")
        
        details = {}
        is_section = False
        tokens = self.text.splitlines(keepends=True)

        for token in tokens:
            # Remove punct from text and lower case it
            tmp_token = self.cleaner.remove_punct(token).lower()
            
            if not tmp_token: 
                continue
            elif is_section and not self.__get_section(text = tmp_token, section=section) and tmp_token not in ALL_TITLES:
                # If text is not a section title
                details[sticky].append(token)
            elif tmp_token in ALL_TITLES and not self.__get_section(text = tmp_token, section=section):
                # i.e, if text is a section title and section title is not experience
                is_section = False
            elif self.__get_section(text = tmp_token, section=section):
                # Found the required section
                is_section = True
                sticky = tmp_token
                details[sticky] = []

        return details


    def create(self) -> dict:
        """
        Return a dictionary with resume data
        """

        return {
            "index": self.key, 
                "resume": 
                {
                    "contact_info": {"contact_info": self.get_section("contact"),
                                     "name": self.get_names(), 
                                     "email": self.get_emails(),
                                     "phone_number": self.get_phone_numbers(),
                                     "links": self.get_links()
                                     },
                    "objective": self.get_section("objective"),
                    "experience": self.get_section(section="experience"),
                    "skills": self.get_section(section="skills"),
                    "education": self.get_section(section="education"),
                    "accomplishment": self.get_section(section="accomplishment"),
                    "misc": self.get_section(section="misc") 
                }
            }

if __name__ == "__main__":

    from utils import TextExtractor
    # Where all the resumes are saved
    path = "C:\\Users\\medSr\\Documents\\resume-job-matcher\\resumes\\"
    # Extract and convert all the resumes from the provided location into text
    resume_txt = TextExtractor(file_path = path).convert_pdf()
    # Extract details from each resume 
    data = [Profile(resume=resume, key=key).create() for key, resume in resume_txt.items()]
    # Load the resumes into a json file
    with open('../data/profiles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)