from flask import Flask, request, redirect, url_for, flash
import subprocess
import json

from taskserve.utils import render_task_row

app = Flask(__name__)


@app.route('/')
def home():

    pending = subprocess.check_output(['task', 
                'status:pending', 'export'], text=True)
    waiting = subprocess.check_output(['task', 
                'status:waiting', 'export'], text=True)

    tasks = json.loads(pending) + json.loads(waiting)

    tasks.sort(key=lambda t: t.get('urgency', ''), reverse=True)
    
    rows = "".join([render_task_row(task) for task in tasks])

    return f"""
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='style.css')}">
      </head>
      <h1>TaskServe</h1>
      <body>
        <form method="POST" action="/add" class="add-form">
          <input id="input-add" name="desc" placeholder="New task description" />
          <input name="tags" placeholder="Enter tags as +tag" />
          <input name="project" placeholder="Enter project" />
          <input name="due" placeholder="Due data?" />
          <button type="submit">Add</button>
        </form>
        <form method="POST" action="/mod" class="mod-form">
          <input id="input-id" name="identity" placeholder="ID" />
          <input id="input-mod" name="mod" placeholder="Enter modification..." />
          <button type="submit">Mod</button>
        </form>
        <a href="{ url_for('burndown') }">Burndown Daily</a>
        <div id="output-box">dummy text</div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Description</th>
                    <th>Tags</th>
                    <th>Project</th>
                    <th>Due</th>
                    <th>Urgency</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
      </body>
    </html>
    """

@app.route('/add', methods=["POST"])
def add():
    desc = request.form.get("desc", "")
    tags = request.form.get("tags", "")
    project = request.form.get("project", "")
    due = request.form.get("due", "")
    if desc.strip():
        subprocess.run(["task", "add", desc, 
                        tags, f"pro:{project}",
                        f"due:{due}"])
    return redirect("/")

@app.route('/mod', methods=["POST"])
def mod():
    identity = request.form.get("identity", "")
    mod = request.form.get("mod", "")
    if mod.strip() and identity.strip():
        subprocess.run(["task", identity, "modify",  mod])
    return redirect("/")

@app.route('/delete', methods=["POST"])
def delete():
    identity = request.form.get("id", "")
    if identity.strip():
        subprocess.run(["task", "rc.confirmation=no", identity, "del"])
    return redirect("/")

@app.route('/complete', methods=["POST"])
def complete():
    identity = request.form.get("id", "")
    if identity.strip():
        subprocess.run(["task", "rc.confirmation=no", identity, "done"])
    return redirect("/")

@app.route('/burndown', methods=["GET"])
def burndown():
    output = subprocess.check_output(["task", "burndown.daily"], text=True)
    return f""" 
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='style.css')}">
      </head>
      <h1>TaskServe</h1>
      <a href="{ url_for('home') }">Home</a>
      <body>
      <div class="burndown">{output}<div>
      </body>
      <html>
      """
