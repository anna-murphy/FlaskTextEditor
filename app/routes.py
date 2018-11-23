from app import app
from flask import render_template, redirect, url_for
from app.forms import EditForm
from os import listdir

@app.route('/')
@app.route('/index')
def index():
    files = listdir("files")
    return render_template("list_files.html", title="All files in '/files'", files=files)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="404 Error"), 404
app.register_error_handler(404, page_not_found)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", title="500 Internal Error"), 500
app.register_error_handler(500, internal_server_error)

@app.route('/<file_name>/view')
def view_file(file_name):
    file_contents = []
    try:
        with open("files/" + file_name) as f:
            for line in f:
                file_contents.append(line)
    except:
        return redirect(url_for("edit_file", file_name=file_name))
    return render_template("view_file.html", title=file_name, file_contents=file_contents)

@app.route('/<file_name>/edit', methods=['POST', 'GET'])
def edit_file(file_name):
    form = EditForm()
    if form.validate_on_submit():
        file_name = form.title.data
        try:
            with open("files/" + file_name, "+r") as f:
                f.seek(0)
                f.truncate()
                f.write(form.content.data)
        except:
            with open("files/" + file_name, "w") as f:
                f.seek(0)
                f.truncate()
                f.write(form.content.data)
        return redirect(url_for('view_file', file_name=file_name))
    file_contents = ""
    try:
        with open("files/" + file_name) as f:
            for line in f:
                file_contents += line
    except:
        pass     
    form.title.data = file_name
    form.content.data = file_contents
    return render_template('doc.html', form=form, title=file_name)
