import os
import time
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './PythonSpamFilter/evaluate'
TRAIN_FOLDER = './PythonSpamFilter/data'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TRAIN_FOLDER'] = TRAIN_FOLDER

app.config['TRAINED_DATA'] = True
app.config['CLASS_AMT'] = 0
app.config['VOCAB_AMT'] = False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_for_output():
    for index in range(10):
        if os.path.exists("./output.txt"):
            doc = open("./output.txt", "r")
            docstr = doc.read()
            doc.close()
            return get_default_page() + docstr
        time.sleep(0.25)
    return get_default_page() + "<p>Evaluation Timed Out</p>"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form.get('eval200') or request.form.get('eval'):
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return get_default_page() + "<p>Error occurred, please try again</p>"
            os.system("rm PythonSpamFilter/evaluate/*")
            files = request.files.getlist("file")
            print(len(files))
            
            for file in files:
                
                # If the user does not select a file, the browser submits an
                # empty file without a filename.
                if file.filename == '':
                    flash('No selected file')
                    return get_default_page() + "<p>Please select a file</p>"
            
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            model = "data200.model"
            if request.form.get('eval'):
                model = "data.model"
            os.system(f"python3 PythonSpamFilter/evaluate.py --folder PythonSpamFilter/evaluate --checkpoint {model}")
            return check_for_output()
        if request.form.get('train'):
           os.system("rm PythonSpamFilter/data/*")
           files = request.files.getlist("file")
           for file in files:
               if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['TRAIN_FOLDER'], filename))
           return get_default_page() + initial_train_input()
        if request.form.get('continue'):
            classAmt = int(request.form.get("classAmt"))
            vocabAmt = int(request.form.get("vocabSize"))
            if classAmt != -1 and vocabAmt != -1:
                app.config['CLASS_AMT'] = classAmt
                app.config['VOCAB_AMT'] = vocabAmt
                return get_default_page() + selected_train_input(classAmt,vocabAmt) + other_train_settings(classAmt, vocabAmt)
        if request.form.get('startTrain'):
            classNameString = ""
            classRegexString = ""
            classAmt = app.config['CLASS_AMT']
            vocabAmt = app.config['VOCAB_AMT']
            for i in range(classAmt):
                classNameString+=request.form.get("className"+str(i))+","
                classRegexString+=request.form.get("classRegex"+str(i))+","
            os.system(f"python3 PythonSpamFilter/train.py --folder PythonSpamFilter/data --c {str(classAmt)} --v {str(vocabAmt)} --cs \"{classNameString}\" --rs \"{classRegexString}\"")
            app.config['TRAINED_DATA'] = True
            return get_default_page()


    return get_default_page()

def get_default_page():
    pageText = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value="Upload and Evaluate with Pre-trained Data" name="eval200"><br>
      <input type=submit value="Upload and Train" name="train">
    '''
    if (app.config['TRAINED_DATA']):
        pageText += '''
        <input type=submit value="Evaluate with Trained Data" name="eval">'''
    pageText += "</form>"
    return pageText

def initial_train_input():
    return f'''
    <br><br><h2>Train Settings</h2>
    <form method=post enctype=multipart/form-data>
      <label>Class Amount </label><input type=number name=classAmt><br>
      <label>Vocabulary Amount </label><input type=number name=vocabSize><br>
      <input type=submit value="Continue" name="continue">
    </form>
    '''

def selected_train_input(c,v):
    return f'''
    <br><br><h2>Train Settings</h2>
    <form method=post enctype=multipart/form-data>
      <label>Class Amount </label><input type=number name=classAmt value={c} readonly><br>
      <label>Vocabulary Amount </label><input type=number name=vocabSize value={v} readonly><br>
      <input type=submit value="Continue" name="continue">
    </form>
    '''

def other_train_settings(classAmt, vocabSize):
    returnstring = "<br><br><form method=post enctype=multipart/form-data>"
    for c in range(classAmt):
        returnstring += f"<input type=text name=className{c} placeholder=ClassName{c}><br>"
        returnstring += f"<input type=text name=classRegex{c} placeholder=\"Regex for FileName\"{c}><br>"
    returnstring += '''<input type=submit value="Start Training" name=startTrain></form>'''
    returnstring += '''<br><br><p>Tip: For ham use regex ^[0-9] and for spam use regex ^s</p>'''
    return returnstring

if __name__ == '__main__':
    app.secret_key="super secret key"
    app.run(host="0.0.0.0", port=80)