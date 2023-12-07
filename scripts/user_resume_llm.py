from openai import OpenAI
import os
from utils import TextExtractor
from constants import constants


class Resume(object):

    def __init__(self, resume_name, max_tokens) -> None:
        self.path = "../data/resume/" + resume_name
        self.text = resume_txt = TextExtractor(file_path=self.path).parse()[self.path]
        self.max_tokens = max_tokens
        self.resume_name = resume_name

        if type(self.text) != str or not self.text:
            raise Exception(f"Resume must be str and not {type(self.text)}")


    def extract(self) -> None:
        """Use ChatGPT 3.5-turbo to extract resume data and save them into a JSON file"""

        prompt=f"As an HR specialist, evaluate the provided document to verify its status as a resume. If it does not qualify as a resume, return N/AS. Otherwise, organize the information according to the specified template and present the results in JSON format. Only include details explicitly present in the resume, using N/A for any missing information.\n\nRESUME: {self.text}\n\nTEMPLATE: " + constants.TEMPLATE

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        # API call
        print('Waiting to hear back from OpenAI....')
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "assistant",
                    "content": prompt,
                }
            ],
            max_tokens = self.max_tokens,
            top_p = 1,
            temperature=1.0,
            model="gpt-3.5-turbo",
        )
        # Extract the response
        results = response.choices[0].message.content
        
        # Check if response is valid
        if results == 'N/A' or not results:
            raise Exception('The provided input is not a resume')

        print(f">>> success extracting infromatiomn from resume {self.resume_name}")

        return results


if __name__ == "__main__":
    import argparse
    from utils import checkpoint
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("-max_tokens", "--max_tokens", help="Maximum token for ChatGPT", type=int, default = 2000)
    parser.add_argument("-f", "--resume_name", help="Resume name", type=str)        
    args = parser.parse_args()

    if not args.resume_name:
        raise Exception('Not resume was provided.')
    
    if not args.max_tokens:
        raise Exception('Max token must be between 100 and 4096')

    results = Resume(resume_name=args.resume_name, max_tokens=args.max_tokens).extract()

    # Save response in the disk
    checkpoint(json.loads(results), append_file_path="../data/user-resumes.json", is_user=True)
