import click
import os


@click.group()
@click.pass_context
def todo(ctx):
    '''Simple CLI Todo App'''
    ctx.ensure_object(dict)
    todo_file_path = './todo.txt'
    # Create todo.txt if it doesn't exist
    if not os.path.exists(todo_file_path):
        with open(todo_file_path, 'w') as f:
            f.write("0\n")

    # Open todo.txt – first line contains latest ID, rest contain tasks and IDs
    with open(todo_file_path) as f:
        content = f.readlines()

    # Transfer data from todo.txt to the context
    ctx.obj['LATEST'] = int(content[0].strip())
    ctx.obj['TASKS'] = {en.split('```')[1].strip(): en.split('```')[
        0] for en in content[1:]}


@todo.command()
@click.pass_context
def tasks(ctx):
    '''Display tasks'''
    if ctx.obj['TASKS']:
        click.echo('YOUR TASKS\n**********')
        # Iterate through all the tasks stored in the context
        for task_id, task in ctx.obj['TASKS'].items():
            click.echo('• ' + task + ' (ID: ' + task_id + ')')
        click.echo('')
    else:
        click.echo('No tasks yet! Use ADD to add one.\n')


@todo.command()
@click.pass_context
@click.option('-add', '--add_task', prompt='Enter task to add')
def add(ctx, add_task):
    '''Add a task'''
    if add_task:
        task_id = str(ctx.obj['LATEST'] + 1)
        # Add task to list in context
        ctx.obj['TASKS'][task_id] = add_task
        click.echo('Added task "' + add_task + '" with ID ' + task_id)
        # Open todo.txt and write current index and tasks with IDs (separated by " ```\n ")
        curr_ind = str(ctx.obj['LATEST'] + 1)
        tasks = ['{} ```\n{}'.format(t_id, t)
                 for t_id, t in ctx.obj['TASKS'].items()]
        with open('./todo.txt', 'w') as f:
            f.writelines([curr_ind + '\n'] + tasks)


@todo.command()
@click.pass_context
@click.option('-fin', '--fin_taskid', prompt='Enter ID of task to finish', type=int)
def done(ctx, fin_taskid):
    '''Delete a task by ID'''
    task_id = str(fin_taskid)
    # Find task with associated ID
    if task_id in ctx.obj['TASKS'].keys():
        task = ctx.obj['TASKS'][task_id]
        # Delete task from task list in context
        del ctx.obj['TASKS'][task_id]
        click.echo('Finished and removed task "' +
                   task + '" with id ' + task_id)
        # Open todo.txt and write current index and tasks with IDs (separated by " ```\n ")
        if ctx.obj['TASKS']:
            curr_ind = str(ctx.obj['LATEST'] + 1)
            tasks = ['{} ```\n{}'.format(t_id, t)
                     for t_id, t in ctx.obj['TASKS'].items()]
            with open('./todo.txt', 'w') as f:
                f.writelines([curr_ind + '\n'] + tasks)
        else:
            # Resets ID tracker to 0 if the list is empty
            with open('./todo.txt', 'w') as f:
                f.write("0\n")
    else:
        click.echo('Error: no task with id ' + task_id)


if __name__ == '__main__':
    todo()
