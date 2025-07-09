from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, render_template, redirect, flash, url_for


app = Flask(__name__)
app.secret_key = '9862769977'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

# --- MODELS ---
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# --- SCHEMAS ---
class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Job
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# --- ROUTES ---
@app.route('/')
def home():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(10).all()
    return render_template('home.html', jobs=jobs)


# --------------------
# USER ROUTES
# --------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    if not credentials or 'username' not in credentials or 'password' not in credentials:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=credentials['username']).first()
    if user and user.check_password(credentials['password']):
         flash("Login successful!", "success")
         return redirect(url_for('home'))
    else:
        flash("Invalid username or password", "danger")
        return redirect(url_for('home'))


# --------------------
# JOB ROUTES (API)
# --------------------
@app.route('/jobs')
def jobs():
    title_query = request.args.get('title')
    location_query = request.args.get('location')
    try:
        page = max(int(request.args.get('page', 1)), 1)
        limit = max(int(request.args.get('limit', 5)), 1)
    except ValueError:
        return jsonify({"error": "Invalid page or limit"}), 400

    query = Job.query
    if title_query:
        query = query.filter(Job.title.ilike(f"%{title_query}%"))
    if location_query:
        query = query.filter(Job.location.ilike(f"%{location_query}%"))

    pagination = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=limit)

    return jsonify({
        "page": page,
        "limit": limit,
        "total": pagination.total,
        "jobs": jobs_schema.dump(pagination.items)
    })

@app.route('/job/<int:job_id>')
def get_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return job_schema.jsonify(job)

@app.route('/job', methods=['POST'])
def create_job():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    errors = job_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_job = Job(
    title=data['title'], 
    location=data['location'],
    description=data.get('description'))

    db.session.add(new_job)
    db.session.commit()
    return job_schema.jsonify(new_job), 201

@app.route('/job/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    errors = job_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    job.title = data.get('title', job.title)
    job.location = data.get('location', job.location)
    db.session.commit()
    return job_schema.jsonify(job), 200

@app.route('/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        flash('Job not found.', 'danger')
        return redirect('/view-jobs')
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect('/view-jobs')


# --------------------
# HTML ADMIN VIEWS
# --------------------
@app.route('/view-jobs')
def view_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/add-job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        description = request.form.get('description')
        
        if not title or not location or not description:
            flash('Please fill in all fields.', 'danger')
            return redirect('/add-job')
        
        new_job = Job(title=title, location=location, description=description)
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job added successfully!', 'success')
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
        job.description = request.form.get('description')
        db.session.commit()
        flash("Job updated successfully!", "success")
        return redirect('/view-jobs')

    return render_template('edit_job.html', job=job)


# --------------------
# ERROR HANDLERS
# --------------------
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

# --------------------
# APP STARTUP
# --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
