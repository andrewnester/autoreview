import os
import openai
import json
import uuid
from pathlib import Path


def main():
    apikey = os.environ["INPUT_APIKEY"]
    input_files = os.environ["INPUT_FILES"]

    files = [i.replace('"', "").replace("'", "")
             for i in input_files.split(",")]
    if not files or len(files) == 0:
        print("No files to review, skipping")
        return

    openai.api_key = apikey
    print("Requesting code reviews for:", files)

    code_reviews = get_code_review(files)
    summary = get_code_review_summary(code_reviews).replace('"', '\\"')
    set_multiline_output("codeReview", summary)


def set_multiline_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        delimiter = uuid.uuid1()
        print(f'{name}<<{delimiter}', file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)


def get_code_review(files):
    code_reviews = {}
    for file in files:
        code_review = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user",
                                              "content": generate_message(file)
                                              }])
        code_reviews[file] = code_review.choices[0].message.content
    return code_reviews


def get_code_review_summary(code_reviews):
    msg = """Generate summary code improvement based on multiple code reviews.
    Input is in JSON format where the key is file
      name and value is code review. 
      Output should be in Markdown format and include file names next to suggestions. Also include code recommendations in the same message\n\n%s""" % json.dumps(
        code_reviews)

    summary = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                           messages=[{"role": "user",
                                                      "content": msg}])
    return summary.choices[0].message.content


def generate_message(file_path):
    file_content = Path(os.path.join(".", file_path)).read_text()
    return "Provide code review. The code to review below\n%s" % file_content


if __name__ == "__main__":
    main()
