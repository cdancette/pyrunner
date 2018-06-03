from pyrunner import Task

class BasicTouchTask(Task):
    """
    This task wraps the "touch" command and stores the
    state in the current directory. 
    Thus it can only be run once from each directory.
    """

    def command(self, args):
        return "touch"

    def experiment_folder(self, args):
        return ".experiment/"


if __name__ == '__main__':
    BasicTouchTask().run()
