from flask import Flask, redirect, render_template, url_for
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os

from form import Form, UpdateForm

app = Flask(__name__)
app.config.from_object(__name__)
DEBUG = True
# Protection
app.secret_key = "MySecretKey"
csrf = CSRFProtect(app)


@app.route('/', methods=('GET', 'POST'))
def submit():
    form = Form()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('home.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UpdateForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'photos', filename))
        return redirect(url_for('success'))
    return render_template('update.html', form=form)


@app.route('/success', methods=('GET', 'POST'))
def success():
    return "Caricamento riuscito"
