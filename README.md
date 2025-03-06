# BokoHacks 2025 - README2
An overview of the hackathon project made by Kayla Vincent, Makenna Wilson, and Brittany Hale for Texas State University's 2025 BokoHacks hackathon!
# Tools and Resources
A free version of ChatGPT was utilized for debugging help and supplementing information about the programming languages. Websites like GeeksForGeeks and Stack Overflow were used to problem-solve and brainstorm solutions to the included vulnerabilities. VirusTotal was used to scan uploaded documents. Used resources located in the original README.md file. Additional tools include the Python library bleach, which had to be imported for input sanitization. Python, SQLite, Flask, and VS Code were used to develop this program.
# Requirements
- Python 3.8 or higher → <a href="https://www.python.org/downloads/">Download Python</a>
- Pip (Python package installer)
- SQLite → <a href="https://www.sqlite.org/download.html">Download SQLite</a> (Optional if you want binaries otherwise; dependencies should install automatically)
- Modern web browser (Chrome/Firefox recommended)
- Text editor or IDE VS Code recommended → <a href="https://code.visualstudio.com/docs/python/environments">VS Code Setup</a>
# Demo Video 
Click here to watch the video!
# Setup Instructions
1. Clone the repository:<br>
https://github.com/bathtub76/hackathon2025.git
2. Set up git and create virtual environment:<br>
cd Boko-Hacks-2025-main<br>
python -m venv .venv<br>
.venv\Scripts\activate 
3. Install dependencies:<br>
pip install -r requirements.txt<br>
pip install bleach
4. Start the application:
python app.py
5. Open <a href="http://localhost:5000/">http://localhost:5000/</a> in your browser
# Testing Guide
1. Creating a new user:
   - Captcha was updated to include 8 randomized characters that can include a mix of numbers and upper/lowercase letters instead of an unchanging number-based Captcha.
   - Password requirements were set and password verification is now implemented. In order to register a new user, passwords must be at least 12 characters, include at least one uppercase and lowercase letter, a number, and a special character. The password must be re-entered in another text box to verify the chosen password.<br>
   
2. Creating a new note:
   - In the section labeled "Sample Test Inputs" at the bottom of the page, there is an area dedicated to test inputs for notes creation. This is to make your life easier! Feel free to use any other test input to see the newest notes functionality.<br>
        
3. 401(k) Portal:
   - Previously, there was a race condition with the contribute processes; if the "Make Contribution" button was pressed several times quickly, the "Personal Funds" amount could become negative since there was nothing in place to ensure the value for amount wasn't being read before it was updated by a previous process. We added a lock to make sure additional processes will wait before reading or altering the amount inside "Personal Funds".<br>
     
4. Document Upload:
   - The file upload size was unrestricted, so we restricted it to 100 KB. Realistically, we'd like this to be 50 MB, but for testing purposes, we made it smaller.
   - We implemented virus checking for the file upload, but it doesn't work as intended because of the HTTP status of the web application that we couldn't change. We used VirusTotal to check file insecurity before being saved to the system; malicious files are to be rejected and deleted. Due to the insecure nature of the HTTP connection the files are coming from, VirusTotal will flag any file uploaded as malicious. This makes it difficult to show VirusTotal allowing files to be uploaded. This functionality is currently commented out in files.py to showcase the file upload size restriction, but here are steps to see it/how we were able to use it:
     
  * Create a VirusTotal account at https://www.virustotal.com/gui/home/upload.
  * Under the top right arrow down, go to API Key. There the API key is availiable.
  * A .gitignore file was created in our project linked to an .env file. Inside the .env file is the "VIRUS_TOTAL_API_KEY = putAPIKeyhere" variable. The API key can be switched out if needed.
  * In the files.py file, we have "VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")" to get the API key. This is part of the commented out code.
  * To uncomment the code and comment out the unused part, add ''' on line 14 and remove the ''' on line 222.
  * Run the web application like normal. When a file is uploaded, you'll see a message claiming VirusTotal has flagged the file as malicious even when it is not due to the HTTP connection.
    
# Future Improvements
- Add multi-factor authentication using an email the user inputs when they first create their account. Due to timing restrictions, we could not implement this, but we had the idea to create a new column for the User database. This new column would hold user emails, and after logging into the account, it would take the user to another page for two-factor authentication.
  
- Use HTTPS instead of HTTP. If this site were to be published, rather than just run off of the localhost, a certificate could be obtained to upgrade the site from HTTP to HTTPS.
  
- The upgrade to HTTPS would also allow the successful integration of VirusTotal into the code. VirusTotal would scan uploaded files for malicious content and delete them if any malware is found inside. However, the HTTP protocol causes files to automatically be flagged as "insecure" and deletes them regardless of the file's content.
  
- Implement a better Captcha that either functions as a game for engagement or is harder to read to prevent bots. We attempted to blur it, but the text size made it difficult to read and distinguish characters that looked similar. 
  
- Add a Content Security Policy header to restrict inline Javascript and inline CSS. This would help prevent actions like Cross-Site Scripting and Click-jacking. We were able to do this previously, but took it out of the code due to timing restrictions and formatting issues with the CSS.
  
- Increase security for admins.
  
# Sample Test Inputs
User Creation:<br>
Example Passwords:<br>
goodINPUT123$%<br>
badpassword<br><br>
Notes Creation:<br>
Example Title (tests max char length of 150): &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&<br><br>
Example Content I (tests bleaching):<br>
&lt;script&gt;alert(&#39;This is a bad script!&#39;);&lt;/script&gt;<br>
&lt;p&gt;This is a &lt;strong&gt;safe&lt;/strong&gt; paragraph.&lt;/p&gt;<br><br>
Example Content II (tests max char length of 2000):
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
