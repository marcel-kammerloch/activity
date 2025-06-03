import requests
import base64
import os
from dotenv import load_dotenv
import sys
import time

# Load .env file
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "marcel-kammerloch"
REPO_NAME = "activity"
FILE_PATH = "file.txt"
BRANCH = "main"

GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"

GITHUB_API_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# def readFile():
#     with open(FILE_PATH, 'r') as currentFile:
#         content = currentFile.read()
#     return content

# def updateFile(newContent):
#     with open(FILE_PATH, 'w') as file:
#         file.write(newContent)

# def incrementNumberOfFile():
#     currentNumber = int(readFile())

#     newNumber = str(currentNumber + 1)

#     updateFile(newNumber)

#     return newNumber

def getFileSha(debug=False):
    response = requests.get(GITHUB_API_URL, headers=GITHUB_API_HEADERS)
    status = response.status_code
    json = response.json()

    if status == 200:
        return str(response.json()["sha"]) 
    elif debug is True: 
        return { status, json }
    else:
        return None

def updateFileOnGithub(content, fileSha):
    encodedContent = base64.b64encode(content.encode()).decode()
    data = {
        "message": "Update file via API",
        "content": encodedContent,
        "branch": BRANCH
    }

    if fileSha:
        data["sha"] = fileSha

    response = requests.put(GITHUB_API_URL, headers=GITHUB_API_HEADERS, json=data)
    status = response.status_code

    if (status == 200) or (status == 201):
        print("File successfully updated")
    else: 
        print(f"Error: {status}, {response.json()}")

def main():
    try:
        newContent =  str(int(time.time() * 1000))

        fileSha = getFileSha()

        updateFileOnGithub(newContent, fileSha)

    except Exception as e:
        print(f"Something went wrong: {e}")

def __test__():
    try:
        # Test if .env is correctly loaded
        print(f".env file {"NOT " if GITHUB_TOKEN is None else "successfully"} loaded")

        # Test reading file
        # content = readFile()
        # if(content is None): raise Exception("Content of File is None")

        # Test if github api is working
        fileSha = getFileSha(debug=True)
        if(isinstance(fileSha, (int, float))): raise Exception(f"fileSha is not a string. Error: {fileSha}")
    except Exception as e:
        print(f"Error: {e}")

if(__name__ == "__main__"):
    if (len(sys.argv) > 1) and ((sys.argv[1] == "-t" ) or (sys.argv[1] == "--test")):
        print("Testing...")
        __test__()
    else:
        main()

# python main.py -t