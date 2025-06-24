from flask import Flask, jsonify, request
from datetime import datetime
from flask import render_template
from flask import render_template, redirect
from datetime import datetime
from flask import render_template, redirect





app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to DevJobs API!"

import json
import os

DATA_FILE = 'jobs.json'

def load_jobs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_jobs(jobs):
    with open(DATA_FILE, 'w') as file:
        json.dump(jobs, file, indent=2)

job_data = load_jobs()


@app.route('/jobs')
def jobs():
    title_query = request.args.get('title')
    location_query = request.args.get('location')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    filtered_jobs = job_data

    if title_query:
        filtered_jobs = [job for job in filtered_jobs if title_query.lower() in job['title'].lower()]
    if location_query:
        filtered_jobs = [job for job in filtered_jobs if location_query.lower() in job['location'].lower()]

    filtered_jobs = sorted(filtered_jobs, key=lambda x: x.get("created_at", ""), reverse=True)

    start = (page - 1) * limit
    end = start + limit
    paginated_jobs = filtered_jobs[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(filtered_jobs),
        "jobs": paginated_jobs
    })





@app.route('/job/<int:job_id>')
def get_job(job_id):
    job_data = [
        {"id": 1, "title": "Backend Developer", "location": "Kathmandu"},
        {"id": 2, "title": "DevOps Engineer", "location": "Remote"},
    ]
    for job in job_data:
        if job["id"] == job_id:
            return jsonify(job)
    return jsonify({"error": "Job not found"}), 404

@app.route('/job', methods=['POST'])
def create_job():
    job = request.get_json()
    if not job or 'title' not in job or 'location' not in job:
        return jsonify({"error": "Missing title or location"}), 400

    new_job = {
        "id": job_data[-1]["id"] + 1 if job_data else 1,
        "title": job['title'],
        "location": job['location'],
        "created_at": datetime.now().isoformat()
    }

    job_data.append(new_job)
    

    return jsonify(new_job), 201



@app.route('/job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    for job in job_data:
        if job["id"] == job_id:
            job_data.remove(job)
            save_jobs(job_data) 
            return jsonify({"message": "Job deleted successfully"}), 200
    return jsonify({"error": "Job not found"}), 404


@app.route('/job/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    for job in job_data:
        if job['id'] == job_id:
            job['title'] = data.get('title', job['title'])
            job['location'] = data.get('location', job['location'])
            save_jobs(job_data)  
            return jsonify(job), 200
    return jsonify({"error": "Job not found"}), 404

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()

    # Hardcoded credentials
    valid_username = "admin"
    valid_password = "password123"

    if not credentials or 'username' not in credentials or 'password' not in credentials:
        return jsonify({"error": "Missing username or password"}), 400

    if credentials['username'] == valid_username and credentials['password'] == valid_password:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/view-jobs')
def view_jobs():
    sorted_jobs = sorted(job_data, key=lambda x: x.get("created_at", ""), reverse=True)
    return render_template('jobs.html', jobs=sorted_jobs)

@app.route('/add-job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')

        if not title or not location:
            return "Missing title or location", 400

        new_job = {
            "id": job_data[-1]["id"] + 1 if job_data else 1,
            "title": title,
            "location": location,
            "created_at": datetime.now().isoformat()
        }

        job_data.append(new_job)
        

        return redirect('/view-jobs')

    return render_template('add_job.html')


@app.route('/delete-job/<int:job_id>', methods=['POST'])
def delete_job_from(job_id):
    global job_data
    job_data = [job for job in job_data if job["id"] != job_id]
    return redirect('/view-jobs')

@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = next((j for j in job_data if j["id"] == job_id), None)
    if not job:
        return "Job not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        if title and location:
            job["title"] = title
            job["location"] = location
        return redirect('/view-jobs')

    return render_template('edit_job.html', job=job)



if __name__ == '__main__':
    app.run(debug=True)
