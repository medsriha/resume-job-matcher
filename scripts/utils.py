import os
import glob
from pypdf import PdfReader
import docx
# import win32com.client as win32
# from win32com.client import constants
import random
import re
import json


class TextProcessor (object):

    def __init__(self) -> None:
        pass

    def remove_extra_spaces(self, text) -> str:
        # Remove tabs and multip space
        clean_text = re.sub(r" +", " ", text)
        # Strip extract space from front and end
        clean_text = clean_text.strip()

        return clean_text

    def replace_tabs(self, text):
        """Replace tab with 4 spaces"""
        return re.sub(r"\t", "    ", text)

    def remove_punct(self, text) -> str:
        # Remove punctuation
        clean_text = re.sub(r"\W+\s*", " ", text)
        # Remove extra space
        clean_text = self.remove_extra_spaces(clean_text)

        return clean_text

    def sent_tokenizer(self, text) -> list:
        # Split text into sentences using punctuation, spaces and upper case letters
        return re.split(r"(?<=[.!?•])\s+(?=[A-Z])", text)

    def remove_unicode(self, text) -> str:
        """Match any Unicode character that is not in the range of ASCII characters (0x00-0x7F) and replace it with an empty string."""
        return re.sub(r"[^\x00-\x7F]", "", text)

    def resplit_text_by_tab(self, seqs) -> list:
        """Split each sentence in a list"""
        res = []
        for seq in seqs:
            splits = re.split(r" {4,}", seq)
            for split in splits:
                res.append(split)
        return res

    def strip_spaces_around_dash(self, text) -> str:
        "Remove space after or before dashes"
        return re.sub(r"\s*-\s*", "-", text)

    def remove_nonalphanum(self, text):
        "Remove non alpha num strings from a list of strings"
        return re.sub(r"[^\w\s]", "", text).replace("_", "").strip()


class TextExtractor(object):

    def __init__(self, file_path: str, k: int = None) -> None:

        if not os.path.exists(file_path):
            Exception(f"File path {file_path} does not exist")

        self.file_path = file_path
        self.cleaner = TextProcessor()
        self.k = k

    def __is_pdf_or_word(self, file_path: str) -> bool:
        # Make sure the provided file is a PDF
        assert file_path.endswith(
            ('pdf', 'docx', 'doc', 'txt')), f'{file_path} is not a PDF file nor a Word document'
        return True

    # def __doc_to_docx(self, file_path: str) -> None:
    #     # Opening MS Word
    #     word = win32.gencache.EnsureDispatch('Word.Application')
    #     doc = word.Documents.Open(file_path)
    #     doc.Activate()

    #     # Rename path with .docx
    #     new_file_abs = os.path.abspath(file_path)
    #     new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    #     # Save and Close
    #     word.ActiveDocument.SaveAs(
    #         new_file_abs, FileFormat=constants.wdFormatXMLDocument
    #     )
    #     doc.Close(False)
    #     # Remove doc file after done
    #     os.remove(file_path)

    def __get_resumes_location(self) -> list:

        if os.path.isdir(self.file_path):
            dirs = glob.glob(self.file_path + "**/*")
            if len(dirs) > 0:
                # subdirectories
                files = glob.glob(self.file_path + "**/*")
            else:
                # No subdirectories
                files = glob.glob(self.file_path + "/**")

            if len(files) == 0:
                raise Exception(
                    f"No files found in this directory {self.file_path}")

            # Multiple files
            if self.k:
                # Randomly pick n number of files (dev)
                files = random.choices(population=files, k=self.k)

        else:
            # Single file
            if self.__is_pdf_or_word(self.file_path):
                # path to a known file
                return glob.glob(self.file_path)

        return files

    def parse(self) -> dict:
        """
        Read PDF files from the specified file path and extract the text from each page. 
        (dev) User can specify a random number of PDF files to return

        Returns:
            dict: A dictionary containing the extracted text from each page of the PDF files as value and file name as key.

        """

        output = {}

        files_paths = self.__get_resumes_location()

        for file_path in files_paths:
            if file_path.endswith('pdf'):
                output[file_path] = self.cleaner.replace_tabs(
                    self.__parse_pdf(file_path))
            elif file_path.endswith(('docx', 'doc')):

                if file_path.endswith("doc"):
                    # Convert doc to docx
                    self.__doc_to_docx(file_path)
                    file_path += 'x'

                output[file_path] = self.cleaner.replace_tabs(
                    self.__parse_word(file_path))
            elif file_path.endswith('txt'):
                output[file_path] = self.cleaner.replace_tabs(
                    self.__parse_txt(file_path))
            else:
                # TODO: move to logging
                print(f'{file_path} is not a PDF file nor a Word document')

        return output

    def __parse_pdf(self, file_name: str) -> str:

        # Temporarly variable to store each page from the PDF
        tmp = ""

        try:
            with open(file_name, "rb") as pdf_file:
                pdf_reader = PdfReader(pdf_file,)
                count = len(pdf_reader.pages)

                for i in range(count):
                    page = pdf_reader.pages[i]
                    if not tmp:
                        # Add newline between pdf pages
                        tmp += "\n"
                    tmp += page.extract_text()

            return tmp

        except Exception as e:
            print(f"Error reading file {file_name}: {str(e)}")

    def __parse_word(self, file_name: str) -> str:
        doc = docx.Document(file_name)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)

        return '\n'.join(text)

    def __parse_txt(self, file_name):
        with open(file_name, "r", encoding="utf-8") as text_file:
            text = text_file.read()

        return text


def checkpoint(data, append_file_path, is_user=False):
    """Append data into an existing or new json file"""
    # Step 1: Read the existing JSON data from the file (if it exists)
    try:
        with open(append_file_path, "r", encoding="utf-8") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn"t exist, start with an empty dictionary
        existing_data = {}

    # Step 2: Append new dictionary to the existing dictionary
    for idx, values in data.items():
        # Categroy already created
        if idx in existing_data:
            if is_user:
                # If checkpoint refers to
                # extracting data from resume, then
                # don't append
                continue
            # If checkpoint refers to
            # extracting data from indeed, then append
            for key, value in values.items():
                if key not in existing_data[idx]:
                    existing_data[idx][key] = value
        else:
            existing_data[idx] = values

    # Step 3: Write the updated dictionary back to the JSON file
    with open(append_file_path, "w", encoding="utf-8") as json_file:
        json.dump(existing_data, json_file, indent=4)
