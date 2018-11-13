from flask import render_template, request, url_for, redirect

from app.flask_app import app
from app.models.models import Sondaggio


@app.route("/new_sondaggio", methods=['GET', 'POST'])
def new_sondaggio():
    if request.method == 'GET':
        return render_template('form_page.html')
    if request.method == 'POST':
        input = request.form.get('text')
        sondaggio = Sondaggio(id=input)
        sondaggio.populate(
            encode=input,
            title=input)
        sondaggio.put()
        return redirect('/')
