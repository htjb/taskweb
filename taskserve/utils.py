
def render_task_row(task):
    project = task.get('project', '')
    due = task.get('due', '')
    if due:
        due = due[:4] + '-' + due[4:6] + '-' + due[6:8]
    tags = " ".join(task.get('tags', []))
    urgency = task.get('urgency', 0)

    return f"""
    <tr>
        <td>{task['id']}</td>
        <td>{task['description']}</td>
        <td>{tags}</td>
        <td>{project}</td>
        <td>{due}</td>
        <td>{urgency}</td>
        <td>
            <form method="POST" action="/delete" onsubmit="return confirm('Delete task {task['id']}?');">
                <input type="hidden" name="id" value="{task['id']}">
                <button type="submit">D</button>
            </form>
            <form method="POST" action="/complete" onsubmit="return confirm('Complete task {task['id']}?');">
                <input type="hidden" name="id" value="{task['id']}">
                <button type="submit">C</button>
            </form>
        </td>
    </tr>
    """
