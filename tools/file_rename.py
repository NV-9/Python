from pathlib import Path 
import re


class FileRenameTool:
    """
    File Rename Tool
    ----------------
    A tool for renaming files in a directory based on a regex pattern.

    """

    source_path: Path
    destination_path: Path
    match_regex: str
    target_regex: str
    in_place: bool

    files: list[Path]

    def __init__(self, source_path: Path, *, in_place: bool = False, match_regex: str = None, target_regex: str = None, destination_path: Path = None):
        self.source_path = source_path
        self.destination_path = destination_path
        self.in_place = in_place
        self.match_regex = match_regex
        self.target_regex = target_regex
        self.files = []

    def find(self):
        """
        Find files in the source directory based on regex
        """
        if not self.source_path.exists() or not self.source_path.is_dir():
            raise ValueError(f"Source path {self.source_path} does not exist or is not a directory.")
        self.files = [f for f in self.source_path.iterdir() if f.is_file() and re.match(self.match_regex, f.name)]

    def order(self, by_name: bool = True, by_created_time: bool = False):
        """
        Order files based on an option.
        """
        if by_name:
            self.files.sort(key=lambda f: f.name)
        elif by_created_time:
            self.files.sort(key=lambda f: f.stat().st_ctime)
    
    def rename(self):
        """
        Rename files based on the specified regex pattern.
        """
        if self.in_place:
            target_path = self.source_path
        else:
            target_path = self.destination_path
        if target_path and not target_path.exists():
            target_path.mkdir(parents=True)
        for file in self.files:
            new_name = file.name
            if self.match_regex and self.target_regex:
                match = re.match(self.match_regex, file.name)
                if match:
                    new_name = re.sub(self.match_regex, self.target_regex, file.name)
            new_file = target_path / new_name
            if new_file.exists():
                new_file.unlink() 
            file.rename(new_file)

