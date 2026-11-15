from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hospital-secret-key'

db = SQLAlchemy(app)

# ─── Models ───────────────────────────────────────────────────────────────────

class Patient(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    age        = db.Column(db.Integer, nullable=False)
    gender     = db.Column(db.String(10), nullable=False)
    phone      = db.Column(db.String(20))
    address    = db.Column(db.String(200))
    blood_group= db.Column(db.String(5))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')

class Doctor(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone        = db.Column(db.String(20))
    email        = db.Column(db.String(100))
    available    = db.Column(db.Boolean, default=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')

class Ward(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(50), nullable=False)
    capacity  = db.Column(db.Integer, nullable=False)
    occupied  = db.Column(db.Integer, default=0)
    ward_type = db.Column(db.String(50))

class Appointment(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    patient_id   = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id    = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appt_date    = db.Column(db.Date, nullable=False)
    appt_time    = db.Column(db.String(10), nullable=False)
    reason       = db.Column(db.String(200))
    status       = db.Column(db.String(20), default='Scheduled')  # Scheduled / Completed / Cancelled
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

# ─── Dashboard ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    stats = {
        'patients':     Patient.query.count(),
        'doctors':      Doctor.query.count(),
        'appointments': Appointment.query.filter_by(status='Scheduled').count(),
        'wards':        Ward.query.count(),
    }
    today_appts = (Appointment.query
                   .filter_by(appt_date=date.today())
                   .order_by(Appointment.appt_time)
                   .all())
    return render_template('index.html', stats=stats, today_appts=today_appts)

# ─── Patients ─────────────────────────────────────────────────────────────────

@app.route('/patients')
def patients():
    search = request.args.get('q', '')
    if search:
        all_patients = Patient.query.filter(Patient.name.ilike(f'%{search}%')).all()
    else:
        all_patients = Patient.query.order_by(Patient.created_at.desc()).all()
    return render_template('patients.html', patients=all_patients, search=search)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        p = Patient(
            name       = request.form['name'],
            age        = int(request.form['age']),
            gender     = request.form['gender'],
            phone      = request.form.get('phone', ''),
            address    = request.form.get('address', ''),
            blood_group= request.form.get('blood_group', ''),
        )
        db.session.add(p)
        db.session.commit()
        flash('Patient registered successfully.', 'success')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', patient=None)

@app.route('/patients/edit/<int:pid>', methods=['GET', 'POST'])
def edit_patient(pid):
    p = Patient.query.get_or_404(pid)
    if request.method == 'POST':
        p.name        = request.form['name']
        p.age         = int(request.form['age'])
        p.gender      = request.form['gender']
        p.phone       = request.form.get('phone', '')
        p.address     = request.form.get('address', '')
        p.blood_group = request.form.get('blood_group', '')
        db.session.commit()
        flash('Patient updated.', 'success')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', patient=p)

@app.route('/patients/delete/<int:pid>', methods=['POST'])
def delete_patient(pid):
    p = Patient.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Patient deleted.', 'warning')
    return redirect(url_for('patients'))

# ─── Doctors ──────────────────────────────────────────────────────────────────

@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        d = Doctor(
            name            = request.form['name'],
            specialization  = request.form['specialization'],
            phone           = request.form.get('phone', ''),
            email           = request.form.get('email', ''),
            available       = 'available' in request.form,
        )
        db.session.add(d)
        db.session.commit()
        flash('Doctor added successfully.', 'success')
        return redirect(url_for('doctors'))
    return render_template('doctor_form.html', doctor=None)

@app.route('/doctors/edit/<int:did>', methods=['GET', 'POST'])
def edit_doctor(did):
    d = Doctor.query.get_or_404(did)
    if request.method == 'POST':
        d.name           = request.form['name']
        d.specialization = request.form['specialization']
        d.phone          = request.form.get('phone', '')
        d.email          = request.form.get('email', '')
        d.available      = 'available' in request.form
        db.session.commit()
        flash('Doctor updated.', 'success')
        return redirect(url_for('doctors'))
    return render_template('doctor_form.html', doctor=d)

@app.route('/doctors/delete/<int:did>', methods=['POST'])
def delete_doctor(did):
    d = Doctor.query.get_or_404(did)
    db.session.delete(d)
    db.session.commit()
    flash('Doctor deleted.', 'warning')
    return redirect(url_for('doctors'))

# ─── Appointments ─────────────────────────────────────────────────────────────

@app.route('/appointments')
def appointments():
    all_appts = (Appointment.query
                 .order_by(Appointment.appt_date.desc(), Appointment.appt_time)
                 .all())
    return render_template('appointments.html', appointments=all_appts)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        a = Appointment(
            patient_id = int(request.form['patient_id']),
            doctor_id  = int(request.form['doctor_id']),
            appt_date  = datetime.strptime(request.form['appt_date'], '%Y-%m-%d').date(),
            appt_time  = request.form['appt_time'],
            reason     = request.form.get('reason', ''),
            status     = 'Scheduled',
        )
        db.session.add(a)
        db.session.commit()
        flash('Appointment booked.', 'success')
        return redirect(url_for('appointments'))
    patients = Patient.query.order_by(Patient.name).all()
    doctors  = Doctor.query.filter_by(available=True).order_by(Doctor.name).all()
    return render_template('appointment_form.html', appointment=None,
                           patients=patients, doctors=doctors)

@app.route('/appointments/status/<int:aid>/<string:status>', methods=['POST'])
def update_appointment_status(aid, status):
    a = Appointment.query.get_or_404(aid)
    if status in ('Completed', 'Cancelled', 'Scheduled'):
        a.status = status
        db.session.commit()
        flash(f'Appointment marked as {status}.', 'success')
    return redirect(url_for('appointments'))

@app.route('/appointments/delete/<int:aid>', methods=['POST'])
def delete_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    db.session.delete(a)
    db.session.commit()
    flash('Appointment deleted.', 'warning')
    return redirect(url_for('appointments'))

# ─── Wards ────────────────────────────────────────────────────────────────────

@app.route('/wards')
def wards():
    all_wards = Ward.query.all()
    return render_template('wards.html', wards=all_wards)

@app.route('/wards/add', methods=['GET', 'POST'])
def add_ward():
    if request.method == 'POST':
        w = Ward(
            name      = request.form['name'],
            capacity  = int(request.form['capacity']),
            occupied  = int(request.form.get('occupied', 0)),
            ward_type = request.form.get('ward_type', ''),
        )
        db.session.add(w)
        db.session.commit()
        flash('Ward added.', 'success')
        return redirect(url_for('wards'))
    return render_template('ward_form.html', ward=None)

@app.route('/wards/edit/<int:wid>', methods=['GET', 'POST'])
def edit_ward(wid):
    w = Ward.query.get_or_404(wid)
    if request.method == 'POST':
        w.name      = request.form['name']
        w.capacity  = int(request.form['capacity'])
        w.occupied  = int(request.form.get('occupied', 0))
        w.ward_type = request.form.get('ward_type', '')
        db.session.commit()
        flash('Ward updated.', 'success')
        return redirect(url_for('wards'))
    return render_template('ward_form.html', ward=w)

@app.route('/wards/delete/<int:wid>', methods=['POST'])
def delete_ward(wid):
    w = Ward.query.get_or_404(wid)
    db.session.delete(w)
    db.session.commit()
    flash('Ward deleted.', 'warning')
    return redirect(url_for('wards'))

# ─── Seed demo data ───────────────────────────────────────────────────────────

def seed():
    if Doctor.query.count() == 0:
        doctors = [
            Doctor(name='Dr. Priya Sharma',  specialization='Cardiology',    phone='9000000001', email='priya@hospital.com'),
            Doctor(name='Dr. Rahul Mehta',   specialization='Neurology',     phone='9000000002', email='rahul@hospital.com'),
            Doctor(name='Dr. Anita Rao',     specialization='Pediatrics',    phone='9000000003', email='anita@hospital.com'),
            Doctor(name='Dr. Vikram Singh',  specialization='Orthopedics',   phone='9000000004', email='vikram@hospital.com'),
        ]
        db.session.add_all(doctors)
    if Ward.query.count() == 0:
        wards = [
            Ward(name='General Ward A', capacity=20, occupied=12, ward_type='General'),
            Ward(name='ICU',            capacity=10, occupied=7,  ward_type='Intensive Care'),
            Ward(name='Pediatric Ward', capacity=15, occupied=5,  ward_type='Pediatric'),
            Ward(name='Maternity Ward', capacity=12, occupied=8,  ward_type='Maternity'),
        ]
        db.session.add_all(wards)
    db.session.commit()

# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed()
    app.run(debug=True)
