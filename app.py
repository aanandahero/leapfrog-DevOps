from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "created_at": self.created_at.isoformat()
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# --- Routes ---
@app.route('/')
def home():
    return "Welcome to DevJobs API!"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    if not credentials or 'username' not in credentials or 'password' not in credentials:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=credentials['username']).first()

    if user and user.password == credentials['password']:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/jobs')
def jobs():
    title_query = request.args.get('title')
    location_query = request.args.get('location')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    query = Job.query
    if title_query:
        query = query.filter(Job.title.ilike(f"%{title_query}%"))
    if location_query:
        query = query.filter(Job.location.ilike(f"%{location_query}%"))

    jobs = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=limit)
    
    return jsonify({
        "page": page,
        "limit": limit,
        "total": jobs.total,
        "jobs": [job.to_dict() for job in jobs.items]
    })

@app.route('/job/<int:job_id>')
def get_job(job_id):
    job = Job.query.get(job_id)
    if job:
        return jsonify(job.to_dict())
    return jsonify({"error": "Job not found"}), 404

@app.route('/job', methods=['POST'])
def create_job():
    data = request.get_json()
    if not data or 'title' not in data or 'location' not in data:
        return jsonify({"error": "Missing title or location"}), 400

    new_job = Job(title=data['title'], location=data['location'])
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201

@app.route('/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return "Job not found", 404
    db.session.delete(job)
    db.session.commit()
    return redirect('/view-jobs')

@app.route('/job/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    job.title = data.get('title', job.title)
    job.location = data.get('location', job.location)
    db.session.commit()
    return jsonify(job.to_dict()), 200

@app.route('/view-jobs')
def view_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/add-job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        if not title or not location:
            return "Missing title or location", 400
        new_job = Job(title=title, location=location)
        db.session.add(new_job)
        db.session.commit()
        return redirect('/view-jobs')
    return render_template('add_job.html')

@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return "Job not found", 404
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.location = request.form.get('location')
        db.session.commit()
        return redirect('/view-jobs')
    return render_template('edit_job.html', job=job)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
