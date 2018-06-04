# pyrunner
Python task runner, that wraps a script

Features
- Write a `.running` token that prevents the task from being ran multiple times.
- Write a `.done` token at the end of the task, so that it is not ran twice.

## Installation

`pip install git+https://github.com/cdancette/pyrunner.git`

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

## Python example

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
