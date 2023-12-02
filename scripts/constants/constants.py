# constants.py
from nltk.corpus import stopwords
"""This module defines project-level constants."""


CONTACT_INFO = {"contact information", "personal information", "contact"}
OBJECTIVE = {"objective", "career objective", "professional objective", "professional summary",
             "career overview", "executive profile", "summary", "employment objective", "professional goals", "career goal"}
SKILLS = {"transferable skills", "highlights", "language competencies and skills", "software skills", "technologies", "areas of experience", "computer knowledge", "competencies", "summary of qualifications", "other skills", "technical proficiencies", "soft skills", "areas of knowledge", "aualifications",
          "career related skills", "professional skills", "credentials", "proficiencies", "qualifications", "skills", "other abilities", "transferable skillslanguage skills", "computer skills", "technical experience", "personal skills", "areas of expertise", "technical skills", "languages", "programming languages", "specialized skills"}
EDUCATION = {"academic training", "programs", "educational background", "academic qualification", "academic projects", "education", "academic background", "course project experience", "relevant certifications",
             "educational qualifications", "courses", "courses relevant to the job", "apprenticeships", "related courses", "educational training", "certifications", "licenses", "education and training", "education and certification"}
EXPERIENCE = {"professional experience", "working history", "professional activities", "project", "personal projects", "military service", "college activities", "freelance experience", "volunteer experience", "training", "experience", "special training", "professional affiliations", "leadership experience", "volunteer work", "career related experience", "freelance", "related experience", "army experience", "internship experience", "project portfolio", "technical expertise", "professional background",
              "professional employment", "teaching experience", "academic experience", "professional employment history", "career summary", "professional training", "military experience", "projects", "employment data", "additional achievements", "additional experience", "relevant experience", "professional associations", "work history", "research experience", "related course projects", "volunteering", "internships", "employment history", "activities", "military background", "work experience", "programming experience"}
ACCOMPLISHMENT = {"accomplishments", "research projects", "notable projects", "honorsmemberships and honors", "conference presentations", "thesis", "exhibits", "awards and honors", "current research interests", "conventions", "awards", "activities and honors", "research grants",
                  "achievements and accomplishments", "dissertations", "publications", "presentations", "theses", "grants and scholarships", "achievement", "professional publications", "papers", "memberships honors", "memberships and honorshonors", "awards and recognition", "awards and achievements"}
MISC = {"civic activities", "references", "professional development", "additional information", "salary history", "refere", "public speaking engagements", "extra-curricular activities", "availability", "community involvement", "professional memberships",
        "interest and hobbies", "interests", "digital", "memberships", "athletic involvement", "affiliations", "associations", "extracurricular activities", "interests and hobbies", "conferences and presentations", "references from linkedin"}

ALL_TITLES = set.union(*[EXPERIENCE, CONTACT_INFO, OBJECTIVE, SKILLS, EDUCATION, ACCOMPLISHMENT, MISC])

ZERO_SHOT_CLASSES = {'education': ["degree", "field of study", "institution name", "school name", "university name", "date", "city", "country", "state",
                                   "coursework", "awards", "GPA", "thesis", "project", "academic achievement", "extracurricular activitie"],
                     "experience": ["company name", "job responsibilities", "job title", "date", "city", "country", "state"]}

REGEX_PATTERNS = {
    "section_pattern": r"^\b[A-Z][A-Za-z\s]+\b[:\r\n\s]$",
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\d{3}[-\s.]\d{3}[-\s.]\d{4}",
    "link_pattern": r"\b(?:https?://|www\.)\S+\b",
    "date_pattern": r"(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}|\d{1,2}[ /\.-]\d{4}|Present|Current|to current|to present)",
    "experience_pattern": r"(Professional|Work|Internship|Volunteer|Volunteering|Leadership|Research|Teaching|PROFESSIONAL|WORK|INTERNSHIP|VOLUNTEER|VOLUNTEERING|LEADERSHIP|RESEARCH|TEACHING)\s+(Experience|experience|EXPERIENCE|Expertise|expertise|EXPERTISE|History|history|HISTORY|Activities|activities|ACTIVITIES)",
    "skills_pattern": r"(Technical|Summary|Hard|TECHNICAL|SUMMARY|HARD)(?: of|OF)? (Proficiencies|Qualifications|Expertise|Skills|SKILLS|PROFICIENCIES|QUALIFICATIONS|EXPERTISE)"
}
# stopwords
STOPWORDS = stopwords.words('english')
