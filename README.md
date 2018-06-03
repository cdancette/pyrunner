# pyrunner
Python task runner, that wraps a script

Features
- Write a `.running` token that prevents the task from being ran multiple times.
- Write a `.done` token at the end of the task, so that it is not ran twice.


## Example

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
