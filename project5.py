from flask import Flask, url_for, render_template, request, redirect, flash,g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import PyPDF2
import google.generativeai as genai

text1=""

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add these configurations for file uploads
app.secret_key = "your_secret_key"  # needed for flashing messages
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define the function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return f"Text extraction failed: {str(e)}"

db = SQLAlchemy(app)

class Blog(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/')
def providence():
    return render_template('index.html')

@app.route('/pdff', methods=['GET', 'POST'])
def pdff():
    global text1
    extracted_text = None
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser submits an empty file
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract text from the uploaded PDF
            extracted_text = extract_text_from_pdf(file_path)
            text1 = extracted_text
            print("It's here", text1)
            flash(f'File {filename} uploaded and text extracted successfully!')
            print("Here")
            # Pass the extracted text to the template
            return render_template('pdf.html')
        else:
            flash('Only PDF files are allowed!')
            return redirect(request.url)
    
    return render_template('upload.html', extracted_text=extracted_text)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit' , methods=['GET','POST'])
def submit():
    if(request.method=='POST'):
        title = (request.form['title'])
        description = (request.form['description'])
        blog = Blog(title=title , description=description)
        db.session.add(blog)
        db.session.commit()
        return redirect('/read')
    return render_template('submit.html')


@app.route('/delete/<int:sno>' ,  methods=['GET','POST'])
def delete(sno):
    b = Blog.query.filter_by(sno=sno).first()
    db.session.delete(b)
    db.session.commit()
    return redirect("/read")


@app.route('/update/<int:sno>' , methods=['GET','POST'])
def update(sno):
    if(request.method=='POST'):
        title = (request.form['title'])
        description = (request.form['description'])
        b = Blog.query.filter_by(sno=sno).first()
        b.title = title
        b.description = description
        db.session.add(b)
        db.session.commit()
        return redirect('/read')
    else:
        blog = Blog.query.filter_by(sno=sno).first()
        return render_template('update.html',blog=blog)
    

@app.route('/individual/<int:sno>' , methods=['GET','POST'])
def individual(sno):
    blog = Blog.query.filter_by(sno=sno).first()
    return render_template('individual.html',blog=blog)

@app.route('/read')
def read():
    blog = Blog.query.all()
    return render_template('read.html',blog=blog)


@app.route('/temp3')
def temp3():
    return render_template('pdf.html')



@app.route('/gemini', methods=['GET','POST'])
def gemini():
    global text1
    if(request.method=='POST'):
        return render_template('about.html')
    print("Value of text1 is ", text1)
    genai.configure(api_key="AIzaSyBttgCnl9LsxRAZ6lAOr_P52YNGx_RwSlg")
    model = genai.GenerativeModel(
                model_name='gemini-2.0-flash',
                tools='code_execution')
    response = model.generate_content(f'Write a Cover letter for the resume {text1}. Just give the letter and nothing else. Keep it concise under 300 words.')
    print(response.text)
    return render_template('cover.html',response_text=response.text)

@app.route('/gemini1', methods=['GET','POST'])
def gemini1():
    global text1
    if(request.method=='POST'):
        return render_template('about.html')
    print("Value of text1 is ", text1)
    genai.configure(api_key="AIzaSyBttgCnl9LsxRAZ6lAOr_P52YNGx_RwSlg")
    model = genai.GenerativeModel(
                model_name='gemini-2.0-flash',
                tools='code_execution')
    response = model.generate_content(f'Write a Linkedin message asking for the referal for Job ID XXX999 for the resume {text1}. Just give the message and nothing else. Keep it concise under 100 words.')
    print(response.text)
    return render_template('cover.html',response_text=response.text)

@app.route('/gemini2', methods=['GET','POST'])
def gemini2():
    global text1
    if(request.method=='POST'):
        return render_template('about.html')
    print("Value of text1 is ", text1)
    genai.configure(api_key="AIzaSyBttgCnl9LsxRAZ6lAOr_P52YNGx_RwSlg")
    model = genai.GenerativeModel(
                model_name='gemini-2.0-flash',
                tools='code_execution')
    response = model.generate_content(f'Give learning path recommendations for the resume {text1}. Do not ask any followup question. Just give the path on the basis of resume and nothing else.')
    print(response.text)
    return render_template('cover.html',response_text=response.text)



if(__name__=="__main__"):
    app.run(debug=True)