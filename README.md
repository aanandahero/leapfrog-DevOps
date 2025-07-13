# 📘 DevJobs – Flask Project

Welcome to **DevJobs** – a simple job board built with Flask.

---

## 🎯 Features

✅ User Registration and Login  
✅ Add new job (with title, location, description)  
✅ View all jobs  
✅ Edit jobs  
✅ Delete jobs  
✅ Flash messages using Bootstrap  
✅ Navigation bar with links

---

## ⚙️ Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- SQLite

---

## 🚀 Getting Started

1️⃣ Clone the repo: https://github.com/aanandahero/leapfrog-DevOps.git



2️⃣ Install dependencies: pip install -r requirements.txt



3️⃣ Run the app: python app.py


4️⃣ Open in browser:http://localhost:5000


---

## 🌐 Routes

### API
- POST `/register`
- POST `/login`
- GET `/jobs`
- GET `/job/<id>`
- POST `/job`
- PUT `/job/<id>`
- POST `/delete-job/<id>`

### HTML Pages
- `/view-jobs` — View all jobs
- `/add-job` — Add new job
- `/edit-job/<id>` — Edit existing job

---

## 🗂️ Folder Structure

/backend
app.py
/templates
base.html
add_job.html
edit_job.html
jobs.html
/jobs.db



---

## 📌 Database

- SQLite DB: `jobs.db`
- Tables:
  - User: id, username, password_hash
  - Job: id, title, location, description, created_at

---

## What I did Each day?

Day 1:
Today I learned how Git works and why it’s essential in DevOps.
Practiced basic commands like init, commit, and push. Got into a problem while pushing into, will solve it tomorrow. 

Day 2:
Learned about Continuous Integration today!
Explored how CI helps automate code testing using tools like GitHub Actions.

Day 3:
Learned about Continuous Integration today!
Explored how CI helps automate code testing using tools like GitHub Actions.

Day 4:
Feeling lazy today, so I took it easy and learned basics of YAML and setting it up in VS code.

Day 5:  
Dived into CI/CD pipelines today! 
Explored how YAML powers GitHub Actions for automating builds and deployments.
Slowly connecting the DevOps dots!

Day 6:  Skipped cause of health problem.

Day 7:  
Learned some cool GitHub tricks today:
Pressed . to edit in-browser
Added a .gitignore file
Set up my personal README profile 

Day 8: 
Set up the Flask backend for DevJobs project:
✅ Created virtual env in PowerShell
✅ Installed Flask
✅ Built and tested base route

Day 9:  Skipped again due to health.

Day 10: 
Missed yesterday, but back on track!
Added a /jobs route to my Flask backend
Returns mock job listings in JSON
Simple, but progress is progress!

Day 11:  
Today I added a dynamic route to my Flask API!
GET /job/<id> now returns a single job
JSON-based responses
Returns error message if not found
Baby steps into building RESTful APIs

Day 12:  
Today I implemented a POST API in Flask!
Created /job endpoint
Accepts JSON data to add new job info
Practiced with Postman and curl
Feeling more backend-ready every day! 

Day 13:  
Added a simple DELETE /job/<id> route to my Flask API today.
Tested it in Postman — works as expected!

Day 14:
Today I added a PUT endpoint to update job data by ID in my Flask API.
Used Postman to test — smooth and clean! Learning how real-world APIs work, step by step.

Day 15:Today I added basic persistence to my Flask API using a JSON file.
Now the job data doesn't reset every time the server restarts 
Feels like real backend progress!

Day 16:  
Added dynamic filtering to my Flask API using query parameters!
Now I can fetch jobs by title, location, or both — just like real-world search filters 

Day 17:  
Today I implemented pagination in my Flask API using ?page=1&limit=2 query parameters.
Now job listings load in chunks — just like real apps do.

Day 18:  
Today I added a basic login system to my Flask API!
It checks hardcoded username & password, and returns login success/fail response. Simple start, big potential

Day 19:  
I added a created_at timestamp to each job posting in my Flask API.
Now every new job includes the time it was created — a small touch that makes the backend feel real

Day 20:  
Sorted job listings in my Flask API by created_at timestamp so the newest jobs appear first.
Small UX detail, but makes a huge difference for real-world use

Day 21: 
Built my first simple frontend with Flask!
Now /view-jobs displays all job listings in a clean HTML page using Jinja2 templates.

Day 22:  
I created a frontend form in Flask that lets users post jobs!
The form sends data to the backend and instantly updates the job listings.

Day 23:
I added delete functionality to my full-stack job board!
Now users can remove job posts directly from the frontend via a button — simple, clean, effective

Day 24:  
Today I added full Edit functionality to my Flask job board!
Now each job can be updated with a simple form from the frontend. 

Day 25:  
I implemented JSON file persistence for my Flask job board!
No more losing jobs on restart — all Create, Edit, and Delete actions now write directly to a local jobs.json file.

Day 26:  
Today I migrated my DevJobs Flask app from storing data in JSON files to using a real SQLite database with SQLAlchemy ORM.

Day 27:  
Today I expanded my Flask app with a User system!
Now users can register and login using a real database, not hardcoded credentials.

Day 28:  
Today I added session management to my Flask app!
Now users stay logged in across pages until they log out manually. 

Day 29: 
Integrated Flask with SQLAlchemy and Marshmallow for full CRUD and user auth. Now my DevJobs app has a real database backend and cleaner JSON APIs.

Day 30: 
Tested my Flask REST API in Postman! Saved a full collection for easy sharing and documentation.

Day 31:
Learned how to write automated tests in Postman
Validated my Flask Job Board API responses
Turning manual checks into repeatable automated tests!  

Day 32:
User registration now saves password hashes.
Login verifies hashed passwords.  

Day 33:
Fixed DB errors in my Flask app by resetting SQLite. Now saving description field for jobs too! Next up: learning migrations.  

Day 34:  
Successfully tested full job CRUD functionality in my Flask app! Added jobs with title, location & description
Viewed detailed listings
Edited job info via form

Day 35:  
Improved Flask app UI with Bootstrap
Upgraded /add-job, /edit-job, /view-jobs pages
Better UX, real-world feel!

Day 36:  
Introduced reusable base.html in Flask
Added Bootstrap Navbar across pages
Cleaner UI, easier navigation

Day 37:  
Integrated a shared Bootstrap navbar into my Flask job portal! Now every page has a clean, consistent look.

Day 38:  
Added Flask flash messages to my job portal. Every action now has instant feedback for users!

Day 39:  
Today I added a new home page route that publicly lists jobs in a nice card layout. Now visitors see recent jobs right on the landing page.

Day 40: 
Added search functionality to my Flask DevJobs app. Now you can filter jobs by title or location on the View Jobs page.

Day 41:
Documented my entire project on GitHub!
Wrote a detailed README with:
Features & Tech stack,Routes & DB schema,Day-by-day progress log (40 days!)

Day 42:
Today I completely revamped my Flask job board UI: Bootstrap icons, search bar, hover animations, and sleek card layouts. 




---

## 👨‍💻 Author

Ananda Sagar Thapa




