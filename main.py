import uvicorn
import supportemailsender
import os
import json
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import traceback
from PIL import Image
from fastapi.responses import FileResponse
import re
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import os
from starlette.responses import FileResponse
from fastapi import HTTPException
import uuid
from chatapi import router as chatapi
from fastapi import Header
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
from uuid import UUID, uuid4
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import emailsender
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
import SupportMailSender
import supportemailsender
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

files_dir = os.path.expanduser("~/Documents/Pydroid3")  # Update the path accordingly

# Create a subdirectory if needed
subdirectory = "uploads"
subdirectory_path = os.path.join(files_dir, subdirectory)
os.makedirs(subdirectory_path, exist_ok=True)

print(subdirectory_path)
# Now, you can use 'subdirectory_path' for your file operations

profile_picture_directory = "profilepictures"

root = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

user_profiles_file = "emails.json"

print(os.getcwd())


class SessionData(BaseModel):
    username: str

logging.basicConfig(filename="server.log", level=logging.DEBUG)

cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

def read_user_profiles():
    try:
        with open(user_profiles_file, "r") as file:
            user_profiles_data = json.load(file)
        return user_profiles_data.get("accounts", {})
    except FileNotFoundError:
        return {}

user_profiles: dict[str, dict[str, str]] = read_user_profiles()



def check_login(email, password):
    try:
        with open('mails.json', 'r') as file:
            data = json.load(file)
            if "accounts" in data and isinstance(data["accounts"], list):
                for account in data["accounts"]:
                    if (
                        isinstance(account, dict) and
                        account.get("email", "").lower().strip() == email.lower().strip() and
                        account.get("password", "") == password
                    ):
                        return True
                return False
            else:
                print(f"Unexpected data structure in 'mails.json'.")
                return True
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading 'mails.json'.")
        return False

def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return bool(re.fullmatch(regex, email))

def check_mail(key):
    try:
        with open('mails.json', 'r') as file:
            data = json.load(file)
            if "accounts" in data and isinstance(data["accounts"], list):
                return any(isinstance(item, dict) and item.get("email", "").lower().strip() == key.lower().strip() for item in data["accounts"])
            else:
                print(f"Unexpected data structure in 'mails.json'.")
                return False
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading 'mails.json'.")
        return False
        
def check_username(key):
    try:
        with open('mails.json', 'r') as file:
            data = json.load(file)
            if "accounts" in data and isinstance(data["accounts"], list):
                return any(isinstance(item, dict) and item.get("username", "").lower().strip() == key.lower().strip() for item in data["accounts"])
            else:
                print(f"Unexpected data structure in 'mails.json'.")
                return False
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error reading 'mails.json'.")
        return False

def get_pfp_by_username(username):
    profile_picture_folder = "profilepictures"
    picture_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".svg"]

    try:
        with open('mails.json', 'r') as file:
            data = json.load(file)
            print("Data from 'mails.json':", data)  # Add this line for debugging

            if "accounts" in data and isinstance(data["accounts"], list):
                matching_accounts = [item for item in data["accounts"] if isinstance(item, dict) and item.get("email", "").lower().strip() == username.lower().strip()]
                if matching_accounts:
                    user_account = matching_accounts[0]
                    # Check if the user account has a picture
                    for extension in picture_extensions:
                        picture_path = f"{profile_picture_folder}/{os.path.basename(user_account['picture'])}{extension}"
                        if os.path.exists(picture_path):
                            return picture_path

                    print(f"No picture found for the user: {username} ({picture_path})")
                    return None
                else:
                    print(f"No account found with email: {username}")
                    return None
            else:
                print("Unexpected data structure in 'mails.json'.")
                return None
    except FileNotFoundError:
        print("'mails.json' file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding 'mails.json'. Check if it's a valid JSON file.")
        return None
        
def new_email(new_email, password, username):
    try:
        with open('mails.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"accounts": []}

    data["accounts"].append({"email": new_email, "password": password, "username": username, "picture": "profilepictures/" + new_email + "file"})

    with open('mails.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def save_picture_to_user_account(username: str, picture_path: str):
    try:
        # Remove the file extension from the picture path
        picture_path_without_extension = os.path.splitext(picture_path)[0]

        # Assuming 'mails.json' contains a dictionary with 'accounts'
        # Update the 'picture' value for the specified 'username'
        # Save the modified dictionary back to 'mails.json'
        with open('mails.json', 'r') as file:
            data = json.load(file)
        
        for account in data.get('accounts', []):
            if account['username'] == username:
                account['picture'] = picture_path_without_extension

        with open('mails.json', 'w') as file:
            json.dump(data, file, indent=2)

        return True
    except Exception as e:
        print(f"Error saving picture path to user account: {e}")
        return False

@app.get("/")
async def main():
    with open(os.path.join(root, 'index.html')) as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")

@app.get("/loginhere")
async def main():
    with open(os.path.join(root, 'login.html')) as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")


@app.get("/test/{item_id},{test}")
async def read_item(item_id, test):
    return {"item_id": item_id, "message": test}

@app.get("/create/{mail_id},{username},{password_id}")
async def getmail(mail_id: str, password_id: str, username: str):
    Check = check(mail_id)
    email_exist = check_mail(mail_id)
    username_exist = check_username(username)

    if username_exist:
	    return {username: 'is already in use'}
	   
    if email_exist:
        return {mail_id: 'is already in use'}

    if Check:
        new_email(mail_id, password_id, username)
        emailsender.SendEmail(mail_id,username)
        return {"email": mail_id, "password": password_id}
    else:
        return {"Message": "Pleae type your Email again"}


@app.get("/login/{email_id},{password_id}")
async def login(email_id: str, password_id: str, response: Response):
    login_successful = check_login(email_id, password_id)

    if login_successful:
        # Assuming you have a user identifier (e.g., email) for the session
        session_identifier = email_id

        # Create a new session
        session = uuid4()
        data = SessionData(username=email_id)  # You can modify this based on your needs

        # Store the session in the backend
        await backend.create(session, data)

        # Attach the session cookie to the response
        cookie.attach_to_response(response, session)

        return {"message": "Login successful. Session created."}
    else:
        return {"message": "Login failed. Invalid credentials."}

        
@app.get("/register")
async def main():
    with open(os.path.join(root, 'register.html')) as fh:
        data = fh.read()
    return Response(content=data, media_type="text/html")
  
@app.get("/SupportPage")
async def SupportPage():
	with open(os.path.join(root, 'SupportSite.html')) as fh:
		data = fh.read()
	return Response(content=data, media_type="text/html")
	
@app.get("/supportapi/{account},{msg}")
async def Supportapi(account, msg: str):
# Open a text file in write mod
	SupportMailSender.SendEmail(account,account)
	with open("SupportMessages.txt", "a") as file:
    # Write the variables to the fil
		file.write(f"{account}: {msg}\n")

	print(msg)
	print(account)

@app.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    print(session_data)
    return session_data


@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(cookie)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"
    
from fastapi import HTTPException

@app.get("/getProfilePicture/{username}")
async def get_profile_picture(username: str):
    picture = get_pfp_by_username(username)
    
    if picture:
        return FileResponse(picture, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
@app.get("/grey_circle")
async def unloadprofilepicturemain():
	return FileResponse("grey_circle.png")

@app.get("/account-settings")
async def SupportPage():
	with open(os.path.join(root, 'account-settings.html')) as fh:
		data = fh.read()
	return Response(content=data, media_type="text/html")
	

# Assuming you have some directory to store uploaded profile pictures
profile_picture_directory = "profilepictures"

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str

# This function should be replaced with your actual authentication logic
async def fake_decode_token(token: str):
    return User(username="fakeuser", email="fake@example.com")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await fake_decode_token(token)

from fastapi import HTTPException, Form, UploadFile, File

# ... (other imports)
from pathlib import Path

@app.post("/uploadProfilePicture")
async def upload_profile_picture(username: str = Form(...), picture: UploadFile = File(...)):
    try:
        # Determine the file extension from the content type
        file_extension = os.path.splitext(picture.filename)[1].lower()

        # Ensure the extension is allowed (you can customize this list)
        allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".svg"}
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=415, detail="Unsupported file type")

        # Construct the destination with the correct file extension
        destination = f"{profile_picture_directory}/{username}file{file_extension}"

        # Check if the destination exists and is a directory
        if os.path.exists(destination) and os.path.isdir(destination):
            return {"message": "Profile picture already exists"}

        with open(destination, "wb") as file:
            file.write(picture.file.read())

        if save_picture_to_user_account(username, destination):
            return {"message": "Profile picture uploaded successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"User not found: {username}")
    except Exception as e:
        # Handle exceptions, print or log the error message
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Make sure to close the file if it was opened
        if 'file' in locals() and not file.closed:
            file.close()
          
@app.get("/admin-page")
async def AdminPage():
	with open(os.path.join(root, 'admin-page.html')) as fh:
		data = fh.read()
	return Response(content=data, media_type="text/html")

# Assuming your support messages are stored in a file named 'SupportMessages.txt'
support_messages_file = "SupportMessages.txt"

@app.delete("/delete_support_message/{message_number}")
async def delete_support_message(message_number: int):
    try:
        with open(support_messages_file, "r") as file:
            messages = file.readlines()

        if 1 <= message_number <= len(messages):
            deleted_message = messages.pop(message_number - 1)

            with open(support_messages_file, "w") as file:
                file.writelines(messages)

            return {"deleted_message": deleted_message.strip()}

        else:
            raise HTTPException(status_code=400, detail="Invalid message number")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_support_message/{line_number}")
async def get_support_message(line_number: int):
    try:
        # Read support messages from the file
        with open("supportmessages.txt", "r") as file:
            messages = file.readlines()

        # Check if the line_number is within the valid range
        if 1 <= line_number <= len(messages):
            return PlainTextResponse(content=messages[line_number - 1], status_code=200)
        else:
            raise HTTPException(status_code=400, detail="Invalid line number")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
class MessageInput(BaseModel):
    admin_message: str
    sender_email: str  # Added field for the sender's email

@app.post("/send_message")
async def send_message(recipient_email: str = Form(...), message_content: str = Form(...)):
    try:
        print(f"Recipient's Email: {recipient_email}")
        print(f"Message Content: {message_content}")
        #emailsend
        supportemailsender.SendEmail(recipient_email,message_content)
        # Print the recipient's email and message content
        print(f"Recipient's Email: {recipient_email}")
        print(f"Message Content: {message_content}")
        #emailsender.SendEmail(mail_id,username)

        # You can add logic here to send the message to the recipient's email

        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

origins = ["*"]  # Replace with the actual origins of your front-end.

app.mount("/static", StaticFiles(directory="static"), name="static")


def save_uploaded_file(file: UploadFile, filename: str):
    with open(filename, "wb") as f:
        f.write(file.file.read())


def cleanup_old_files(directory: str, minutes_old: int):
    current_time = datetime.now()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (current_time - modified_time) > timedelta(minutes=minutes_old):
                os.remove(file_path)

@app.get("/uploadyourpicture")
async def uploadyourpicture():
	with open(os.path.join(root, 'upload_picture.html')) as fh:
		data = fh.read()
	return Response(content=data, media_type="text/html")

@app.get("/downloadyourpicture")
async def downloadyourpicture():
	with open(os.path.join(root, 'download_picture.html')) as fh:
		data = fh.read()
	return Response(content=data, media_type="text/html")


# ...

@app.get("/download-picture/{uuid}")
async def download_picture(uuid: str):
    # Check if the file with the provided UUID exists
    file_path = os.path.join(subdirectory_path, f"{uuid}.jpg")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Picture not found")
# This endpoint should be tiggered periodically (e.g., using a cron job)

def cleanup_pictures():
    cleanup_old_files(subdirectory_path, minutes_old=2)
    return {"message": "Cleanup completed"}
       
@app.post("/upload-picture/")
async def upload_picture(file: UploadFile = File(...)):
    # Generate a unique UUID key for the picture
    picture_uuid = str(uuid.uuid4())
    
    # Save the uploaded picture with the UUID as the filename
    file_path = os.path.join(subdirectory_path, f"{picture_uuid}.jpg")
    
    with open(file_path, "wb") as image:
        image.write(file.file.read())
    
    # Return the UUID as a response
    return {"uuid": picture_uuid}

    
@app.get("/chat")
async def downloadyourpicture():
	with open(os.path.join(root, 'chathtml.html')) as fh:
		data = fh.read()
	return Response(content=data, media_type="text/html")

test = cleanup_pictures()
print(test) 
