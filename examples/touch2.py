from pyrunner import Task
from pathlib import Path

class TouchTask(Task):
    """
    This task wraps the "touch" command, and stores the token in a directory 
    next to the created file. 
    """

    def add_args(self, parser):
        parser.add_argument("file", help="File to create")

    def command(self, args):
        return "touch {}".format(args.file)

    def experiment_folder(self, args):
        """
        The token directory is next to the created file, of
        the form ".tokens-<filename>
        """
        folder = Path(args.file).parent
        name = Path(args.file).name
        return Path(folder) / '.tokens-{}'.format(name)


if __name__ == '__main__':
    TouchTask().run()
