from PyPDF2 import PdfReader
from docx import Document
import os
import json
import io

dirc = os.path.join(os.getcwd(), "documents")

prev_data = open("prev_file.json", "r").read()

prev_files = json.loads(prev_data)
new_file = {'files': []}


for file in os.listdir(dirc):
    try:
        if file in prev_files['files']:
            print("Skipping file...", file, end="\n")
        else:
            append_file = io.open("corpus.txt", "a", encoding='utf-8')
            print("Reading File...")
            if file.split('.')[-1] == 'pdf':
                print("Found PDF.")
                file_path = os.path.join(dirc, file)
                pdf = PdfReader(file_path)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                text += "\n\n"
                append_file.write(text)
                print("Text extracted !\n")
                new_file["files"].append(file)

            elif file.split('.')[-1] == 'txt':
                print("Found TXT\n")
                new_file["files"].append(file)

            elif file.split('.')[-1] == 'docx':
                print("Found DOCX\n")
                file_path = os.path.join(dirc, file)
                doc = Document(file_path)
                text = ""
                for page in doc.paragraphs:
                    text += page.text
                text += "\n\n"
                append_file.write(text)
                new_file["files"].append(file)
                print("Text extracted !\n")

            elif file.split('.')[-1] == 'xlsx':
                print("Found XLSX\n")
                new_file["files"].append(file)
    except Exception:
        print(f"There was a problem reading this file [{file}]\n")
        continue


print("Adding file names to previous files...")
new_file['files'].extend(prev_files['files'])

with open("prev_file.json", "w") as jfile:
    jdata = json.dumps(new_file)
    jfile.write(jdata)
