from flask import Flask, render_template, request , redirect, session , jsonify, send_file
from Rulebased import RuleBasedChatbot # Import class จากไฟล์ myclass.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import bcrypt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(10), nullable=False)
    create_when =db.Column(db.Date, server_default=func.date('now'))
    
    def __init__(self,email,password,name,role):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role
        
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = 'member'
        
        # check email is already
        existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            return redirect('/')
        
        
        new_user = User(name=name,email=email,password=password,role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')
    return render_template('register.html')

@app.route('/', methods=['GET','POST']) 
def login():  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            session['role'] = user.role
            
            if user.role == 'member':
                return redirect('/index')
            elif user.role == "admin":
                return redirect('/admin')
        else:
            return render_template('login.html', error='Invalid user')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    # รับข้อมูลที่ส่งมาจากคำร้อง AJAX
    data = request.get_json()
    id_to_delete = data['id']

    # ให้ใช้ session ของ SQLAlchemy เพื่อดึงและลบข้อมูล
    row_to_delete = User.query.get(id_to_delete)
    db.session.delete(row_to_delete)
    db.session.commit()

    # ส่งข้อความกลับไปยังเบราว์เซอร์
    message = f"ลบรายการที่ ID {id_to_delete} เรียบร้อย"
    return jsonify({'message': message})

@app.route('/index')
def index():
    email = session['email']
    user = User.query.filter_by(email=email).first()
    return render_template('index.html', data=user)

@app.route('/admin')
def admin():
    data = User.query.all()
    return render_template('admin.html',data=data)

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    chatbot = RuleBasedChatbot() # Call from Rulebased.py
    response = chatbot.respond(user_input)
    
    # Check if the response is a path to an image
    if is_image(response):
        # If it's an image, send the file
        return send_file(response, mimetype='image/png')
    else:
        # If it's text, return as text
        return response

def is_image(file_path):
    # Check if the file exists and has a valid image extension
    return os.path.isfile(file_path) and any(ext in file_path.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif'])

if __name__ == '__main__':
    app.run(debug=True, port=3000)