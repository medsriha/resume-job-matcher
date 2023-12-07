# user_profile.py
"""
Extract data from input resume such email, phone, number, work experience, education then create a user profile
"""

import re
from utils import TextProcessor
import numpy as np
import warnings
from constants import constants
import spacy
# Spacy model
nlp = spacy.load('en_core_web_lg')


class Profile(object):

    def __init__(self, resume, zero_shot_model):

        if type(resume) == str:
            self.text = resume
        else:
            raise Exception(f"Resume must be str and not {type(resume)}")

        # Text cleaning (i.e. remove punctuation)
        self.cleaner = TextProcessor()
        # Strip spaces between dashes
        self.tokens = self.cleaner.strip_spaces_around_dash(self.text)
        # Remove unicode from tokens
        self.tokens = self.cleaner.remove_unicode(self.tokens)
        # Split resume into sentence
        self.tokens = self.tokens.splitlines(keepends=True)
        # Resplit text using other delimeter not included in splitlines()
        self.tokens = self.cleaner.resplit_text_by_tab(self.tokens)
        # Remove empty strings
        self.tokens = [
            sent for sent in self.tokens if self.cleaner.remove_nonalphanum(sent)]
        # ner
        self.doc = nlp(' '.join(self.tokens))
        # zero shot model
        self.model = zero_shot_model
        # Stores all the text captured by the get_section()
        # function
        self.cashe = set()

    def add_to_cashe(self, value) -> None:
        """Add captured values in a cashe"""
        if value not in self.cashe:
            self.cashe.add(value)

    def get_emails(self) -> str:
        """
        Extract email addresses from a given string using RegEx.

        Returns:
            Str: Email address listed on the resume
        """
        emails = re.findall(
            constants.REGEX_PATTERNS["email_pattern"], self.text)
        if emails:
            # The first email is assumed to be the user"s email address
            email = emails[0]
            self.add_to_cashe(email)
            return email
        return None

    def get_names(self) -> str:
        """Extracts and returns a list of names from the given 
        text using spaCy"s named entity recognition.

        Returns:
            Str: User name listed on the resume
        """
        names = [ent.text for ent in self.doc.ents if ent.label_ == "PERSON"]
        if names:
            name = names[0]
            self.add_to_cashe(name)
            return name
        return None

    def get_links(self) -> dict:
        """
        Find links of any type in a given string using RegEx.

        Returns:
            Dict: links listed on the resume including Linkedin and github
        """
        dic = {"linkedin": None,
               "github": None,
               "other": []}

        links = re.findall(constants.REGEX_PATTERNS["link_pattern"], self.text)
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

            self.add_to_cashe(link)
        return dic

    def get_phone_numbers(self) -> str:
        """
        Extract phone numbers from a given string using RegEx.

        Returns:
            Str: Phone number listed on the resume
        """

        phone_numbers = re.findall(
            constants.REGEX_PATTERNS["phone_pattern"], self.text)
        if phone_numbers:
            phone_number = phone_numbers[0]
            self.add_to_cashe(phone_number)
            return phone_number
        return None

    def __get_section(self, text, section) -> bool:
        """
        Returns:

        """

        if section == "contact":
            if text in constants.CONTACT_INFO:
                return True
        elif section == "experience":
            if text in constants.EXPERIENCE or re.findall(constants.REGEX_PATTERNS["experience_pattern"], text):
                return True
        elif section == "skills":
            if text in constants.SKILLS or re.findall(constants.REGEX_PATTERNS["skills_pattern"], text):
                return True
        elif section == "education":
            if text in constants.EDUCATION or re.findall(r"(Education|EDUCATION)(?: and|AND)? (Training|TRAINING)", text):
                return True
        elif section == "objective":
            if text in constants.OBJECTIVE:
                return True
        elif section == "accomplishment":
            if text in constants.ACCOMPLISHMENT:
                return True
        elif section == "misc":
            if text in constants.MISC:
                return True
        else:
            raise Exception(f"Unknown section {section}")

        return False

    def get_section(self, section=None) -> list:
        """
        Extract details from raw resume

        Args:
            text (str): The string from which to extract experience.

        Returns:
            List: details listed under the provided section
        """
        if not section:
            raise Exception(
                "Section name is unknown. Please provide one of the following input (experience, skills, and education)")

        details = {}
        is_section = False

        for token in self.tokens:
            # Remove punct from text and lower case it
            tmp_token = self.cleaner.remove_punct(token).lower()

            if not tmp_token:
                continue
            elif is_section and not self.__get_section(text=tmp_token, section=section) and tmp_token not in constants.ALL_TITLES:
                # If text is not a section title
                details[sticky].append(token)
                if token not in self.cashe:
                    self.cashe.add(token)
            elif tmp_token in constants.ALL_TITLES and not self.__get_section(text=tmp_token, section=section):
                # i.e, if text is a section title and section title is not experience
                is_section = False
            elif self.__get_section(text=tmp_token, section=section):
                # Found the required section
                is_section = True
                sticky = tmp_token
                details[sticky] = []
                if token not in self.cashe:
                    self.cashe.add(token)
        return details

    def not_captured_sections(self):
        """
        Capture paragraphs with section title, usually objective or summary. 
        This may be usefull for debugging as well.
        """
        details = []

        for token in self.tokens:

            if not self.cleaner.remove_punct(token):
                # Discard empty lines
                continue

            elif token not in self.cashe:
                # If line is not found in cashe, then
                # it"s considered non-captured section
                details.append(token)

        return details

    def parse_education(self):
        """
        Group education details by school name, degree, graduation year, etc.
        Multiple groups may exist within a single resume - multiple schools and degrees.

        Returns:
            Dict: Dictionary with education details grouped by school name, degree, etc

        """
        warnings.filterwarnings("ignore")

        details = {}
        # Identify then extract only education details from resume
        educations = self.get_section(section="education")

        for key, lines in educations.items():
            details[key] = {}
            # Holds education group number
            count = 0
            cleaned = []

            # Remove empty punctuation and empty strings
            for line in lines:

                clean_line = self.cleaner.remove_punct(line)

                if clean_line and clean_line.lower() not in constants.STOPWORDS:
                    cleaned.append(line)

            # Pass all the sentences to a zero shot model
            results = self.model(
                cleaned, constants.ZERO_SHOT_CLASSES["education"])

            for res in results:
                # Best of all
                pos = np.argmax(res["scores"])

                label = res["labels"][pos]
                sent = res['sequence']

                if label in ["institution name", "school name", "university name"]:
                    label = "school_name"
                elif label in ["project", "coursework"]:
                    label = "coursework/projects"
                else:
                    label = re.sub(r"\s", "_", label)

                if count == 0 or label == start:
                    # Mark the start of each group
                    start = label
                    count += 1
                    # Create a new group
                    details[key]["edu_" + str(count)] = {label: [sent]}

                elif label != start:
                    # Still parsing the same education group
                    if label in details[key]["edu_" + str(count)]:
                        if sent not in details[key]["edu_" + str(count)][label]:
                            details[key]["edu_" +
                                         str(count)][label].append(sent)
                    else:
                        details[key]["edu_" + str(count)][label] = [sent]

        # Place raw data in final results
        details['raw'] = educations

        return details

    def create(self) -> dict:
        """
        Return a dictionary with resume data parsed and stored by section
        """

        results = {"resume":
                   {
                       "contact_info": {
                           "contact_info": self.get_section(section="contact"),
                           "name": self.get_names(),
                           "email": self.get_emails(),
                           "phone_number": self.get_phone_numbers(),
                           "links": self.get_links()
                       },
                       "objective": self.get_section(section="objective"),
                       "experience": self.get_section("experience"),
                       "skills": self.get_section(section="skills"),
                       "education": self.parse_education(),
                       "accomplishment": self.get_section(section="accomplishment"),
                       "misc": self.get_section(section="misc"),
                   }
                   }
        # Extract text not caputred by the above steps
        other = self.not_captured_sections()

        if other:
            results["other"] = other

        return results


if __name__ == "__main__":
    from transformers import pipeline
    from utils import TextExtractor, checkpoint
    from tqdm import tqdm

    pipe = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-9")
    resume_txt = TextExtractor(file_path="../data/resume/").parse()
    data = {}
    # Extract details from each resume
    for i, (key, resume) in tqdm(enumerate(resume_txt.items())):
        if i % 100 == 0 and i > 0:
            # Save results every 100 records
            checkpoint(
                data, append_file_path="../data/user-profile-new.json", is_user=True)
            # Empty memory
            data = {}
        # Extract information from resume
        data[key] = Profile(resume=resume, zero_shot_model=pipe).create()
    if len(data) > 0:
        # Have data left in memory after the above iteration is done
        checkpoint(
            data, append_file_path="../data/user-profile-new.json", is_user=True)
    print('Done!')