# pyrunner

A simple Python task runner. Use it as a CLI, or wrap your own scripts with 
the python interface.

Features
- Prevent a task to be running twice simultaneously.
- Prevent a task to be launched again when it is already completed.

It implements this by writing token files `.done` and `.running` in a 
specified task directory. One directory = One task.

Crash recovery :
Say you launched multiple tasks for all subdirectories: `ls | xargs -I % command %`, 
and the command crashes in the middle. Now how do you run only the unfinished tasks ?

You can use pyrunner to run the your tasks, and then the second run will only start 
unfinished tasks.

It can also be used as a poor man's parallel library.
Instead of ``ls | xargs -P 2 -I % command %` you can run `ls | xargs -I % pyrunner %/.tokens command %` in two shells. 
Each shell will pick up the pending tasks.

## Installation

`pip install pyrunner`

## CLI usage

You can use it as a cli, like this : 

```bash
pyrunner <tokens-folder> <command>
```

For example

```bash
pyrunner .tokens/ touch file.txt
```

Will create a file called file.txt.

Another example : 

```bash
pyrunner .tokens/ bash -c "date > date.txt"
```
This command will save the current date in the file `date.txt`. 
If you run it again it will not run.

## Python Usage

You can also use your command arguments to determine the tokens folder (and avoid duplicating it as an argument).
For this, you need to wrap your script in a python class.

A basic task that creates a file

```python
from pyrunner import Task

class TouchTask(Task):

    def command(self):
        return "touch"
    
    def experiment_folder(self, args):
        return "." # return current folder

if __name__ == "__main__":
    TouchTask().run()
```

More complex examples are in the examples/ directory.
