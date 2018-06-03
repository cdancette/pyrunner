import argparse
import sys
import os
from pathlib import Path
import subprocess

class Task:

    def experiment_folder(self, args):
        """
        Override this method to return the folder where 
        the done / running tokens will be saved.
        """
        raise NotImplementedError()

    def run_path(self, args):
        """
        You may override this method using the args used with the script to 
        return the path to the .running token

        :return Path
        """
        return Path(self.experiment_folder(args)) / '.running'
    
    def done_path(self, args):
        """
        You may this method using the args used with the script
        to return the path to the .done token
        """
        return Path(self.experiment_folder(args)) / '.done'

    def is_done(self, args):
        return self.done_path(args).is_file()

    def try_running(self, args):
        run_path = self.run_path(args)

        try:
            run_path.touch(exist_ok=False)
            return True
        except FileExistsError:
            return False

    def rm_running(self, args):
        run_path = self.run_path(args)
        run_path.unlink()

    def write_done(self, args):
        run_path = self.run_path(args)
        done_path = self.done_path(args)
        run_path.unlink()
        done_path.touch(exist_ok=False)

    def command(self, args):
        """
        The command to run. 
        """
        raise NotImplementedError()

    def run_task(self, args, unknown_args):
        """
        This function will by default run the command.
        You may override it to run custom commands.
        It should return the error code (0 if success, everything else is error).
        """
        return os.system(self.command(args) + " " + " ".join(unknown_args))

    def add_args(self, parser):
        # add your args
        pass

    def run(self):
        parser = argparse.ArgumentParser()
        self.add_args(parser)
        args, unknown_args = parser.parse_known_args()

        # create experiment folder if not exists
        Path(self.experiment_folder(args)).mkdir(parents=True, exist_ok=True)
        
        if self.is_done(args):
            print("Command already done. Exciting")
            sys.exit(0)

        if not self.try_running(args):
            print("Command already running. Exciting")
            sys.exit(1)

        result = self.run_task(args, unknown_args)
        if result != 0:
            print("An error occured while running the command.")
            self.rm_running(args)
            sys.exit(result)
        self.write_done(args)
        

class ConsoleTask(Task):

    def __init__(self, experiment_dir, command=None):
        self.experiment_dir = experiment_dir
        self.command = command

    def experiment_folder(self, args):
        return self.experiment_dir

    def run_task(self, args=None, unknown_args=None):
        output = subprocess.run(self.command)
        return output.returncode


def console():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_folder")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    task = ConsoleTask(
        args.experiment_folder,
        command=args.command
    )
    task.run()
