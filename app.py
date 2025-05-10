from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load tasks from the JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks to the JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

# Routes
@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_title = request.form['task']
    due_date = request.form.get('due_date', '')
    description = request.form.get('description', '')
    tasks = load_tasks()
    tasks.append({'title': task_title, 'description': description, 'done': False, 'due_date': due_date})
    save_tasks(tasks)
    print("Task Title:", task_title)
    print("Due Date:", due_date)

    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    deleted_task = tasks.pop(task_id - 1)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route("/mark/<int:task_index>", methods=["POST"])
def mark_done(task_index):
    tasks = load_tasks()  # 🔧 you missed this line
    if 0 <= task_index - 1 < len(tasks):
        tasks[task_index - 1]["done"] = True
    save_tasks(tasks)
    return redirect("/")


@app.route('/search', methods=['GET', 'POST'])
def search_task():
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        tasks = load_tasks()
        filtered_tasks = [task for task in tasks if keyword in task['title'].lower()]
        if not filtered_tasks:
            return render_template('index.html', tasks=tasks, search_task=False, no_results=True)
        return render_template('index.html', tasks=filtered_tasks, search_results=True)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = load_tasks()
    index = task_id - 1
    if request.method == 'POST':
        tasks[index]['title'] = request.form.get('title', '')
        tasks[index]['description'] = request.form.get('description', '')
        tasks[index]['due_date'] = request.form.get('due_date', '')
        save_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('edit.html', task=tasks[index], index=task_id)

                                            
if __name__ == '__main__':
    app.run(debug=True)
