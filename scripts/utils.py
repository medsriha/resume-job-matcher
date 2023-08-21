import os
import glob
from pypdf import PdfReader
import random
import re

class TextCleaner(object):

    def __init__(self) -> None:
        pass

    def remove_tabs(self, text) -> str:
        # Remove tabs and multip space
        clean_text = re.sub(r" +", " ", text)
        # Strip extract space from front and end
        clean_text = clean_text.strip()

        return clean_text
    
    def remove_punct(self, text) -> str:
        # Remove punctuation
        clean_text = re.sub(r'\W+\s*', ' ', text)
        # Remove extra space
        clean_text = self.remove_tabs(clean_text)

        return clean_text

class TextExtractor(object):
    
    def __init__(self, file_path:str, k:int = None) -> None:
        
        if not os.path.exists(file_path):
            Exception(f"File path {file_path} does not exist")     
        
        self.file_path = file_path

        self.k = k

        if '.' in file_path:
            # Read extension
            self.extension = self.file_path.split(".")[-1]
            # Make sure the provided file is a PDF
            assert self.extension == 'pdf', f'{file_path} is not a PDF file'
            self.is_dir = False
        else:
            # Provided file is a directory
            self.is_dir = True

    def __pdf_location(self) -> list:
        
        if not self.is_dir:
            # path to a known pdf file
            return glob.glob(self.file_path)
        
        # Multiple files
        if self.k:
            # Randomly pick n pdf files (dev)
            pdf_files =  random.choices(population = glob.glob(self.file_path +  "*\\*.pdf"), k = self.k)
        else:
            # Or extract all the files
            pdf_files =  glob.glob(self.file_path + "*\\*.pdf")

        if not pdf_files:
            raise Exception(f"No PDF files found in this directory {self.file_path}")
 

        return pdf_files
    
    def convert_pdf(self) -> dict:

        """
        Read PDF files from the specified file path and extract the text from each page. 
        (dev) User can specify a random number of PDF files to return

        Returns:
            dict: A dictionary containing the extracted text from each page of the PDF files as value and file name as key.

        """
        
        output = {}
        
        pdf_files = self.__pdf_location()
        
        for file in pdf_files:
            # Temporarly variable to store each page from the PDF
            tmp = ""
            
            try:
                with open(file, "rb") as f:
                    pdf_reader = PdfReader(f,)
                    count = len(pdf_reader.pages)
                    
                    for i in range(count):
                        page = pdf_reader.pages[i]
                        tmp += page.extract_text()
                        
                    output[file] = tmp

            except Exception as e:
                print(f"Error reading file {file}: {str(e)}")

        return output

