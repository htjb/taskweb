from flask import Flask, request, redirect, url_for
import subprocess
import json

app = Flask(__name__)

def render_task_row(task):
    project = task.get('project', '')
    due = task.get('due', '')
    if due:
        due = due[:4] + '-' + due[4:6] + '-' + due[6:8]
    tags = " ".join(task.get('tags', []))
    urgency = task.get('urgency', 0)

    if urgency <5:
        color = '#d1d1d1'
    elif urgency <10:
        color = '#ffdd78'
    else:
        color = '#ff5d52'


    return f"""
    <tr style="background-color: {color}">
        <td>{task['id']}</td>
        <td>{task['description']}</td>
        <td>{tags}</td>
        <td>{project}</td>
        <td>{due}</td>
        <td>{urgency}</td>
        <td>
            <form method="POST" action="/delete" onsubmit="return confirm('Delete task {task['id']}?');">
                <input type="hidden" name="id" value="{task['id']}">
                <button type="submit">Del</button>
            </form>
            <form method="POST" action="/complete" onsubmit="return confirm('Complete task {task['id']}?');">
                <input type="hidden" name="id" value="{task['id']}">
                <button type="submit">Com</button>
            </form>
        </td>
    </tr>
    """

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
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        <p>Number of tasks: {len(tasks)}</p>
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
