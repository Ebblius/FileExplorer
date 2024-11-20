import os
from logger import Logger
import stat
import pwd
import grp

class FileStatAdapter:
    def __init__(self, path: str, stats : os.stat_result) -> None:
        self.path = path
        self.stats = stats

    def is_dir(self) -> bool:
        return stat.S_ISDIR(self.stats.st_mode)

    def is_regularfile(self) -> bool:
        return stat.S_ISREG(self.stats.st_mode)

    def is_symbolic(self) -> bool:
        return stat.S_ISLNK(self.stats.st_mode)
    
    def get_name(self) -> str:
        return os.path.basename(self.path)

    def get_accesstime(self) -> int:
        return self.stats.st_atime

    def get_modificationtime(self) -> int:
        return self.stats.st_mtime

    def get_changetime(self) -> int:
        return self.stats.st_ctime

    def get_username(self) -> str:
        return pwd.getpwuid(self.stats.st_uid).pw_name

    def get_groupname(self) -> str:
        return grp.getgrgid(self.stats.st_gid).gr_name

    def get_size(self) -> int:
        return self.stats.st_size


class PathManager:
    def __init__(self, current_path: str) -> None:
        if not os.path.exists(current_path):
            err = ValueError(f"Path does not exist: {current_path}")
            Logger().get_logger().error(f'Raised: [{err}]')
            raise err
        self.current_path = os.path.abspath(current_path)
        self.history = [self.current_path]
        self.future = []

    def go_back(self) -> bool:
        if len(self.history) > 1:
            self.future.append(self.history.pop())
            self.current_path = self.history[-1]
            return True
        else:
            return False

    def go_forward(self) -> bool:
        if self.future:
            self.history.append(self.future.pop())
            self.current_path = self.history[-1]
            return True
        else:
            return False 
        
    def go_parent_folder(self) -> bool:
        if self.is_root(self.current_path):
            return False;
        self.history.append(self.current_path)
        self.current_path = os.path.abspath(os.path.join(self.current_path, os.pardir))
        return True

    def change_path(self, new_path: str) -> None:
        if not os.path.exists(new_path):
            err = ValueError(f"Path does not exist: {new_path}")
            Logger().get_logger().error(f'Raised: [{err}]')
            raise err
        self.history.append(os.path.abspath(new_path))
        self.future.clear() 
        self.current_path = os.path.abspath(new_path)

    def get_current_path(self) -> str:
        return self.current_path
    
    def is_root(self, child_path: str) -> bool:
        abs_path = os.path.abspath(child_path)
        return abs_path == os.path.abspath(os.path.join(child_path, os.pardir))
    
    def get_filestats(self, path: str) -> FileStatAdapter:
        if not os.path.exists(path):
            err = ValueError(f"Path does not exist: {path}")
            Logger().get_logger().error(f'Raised: [{err}]')
            raise err
        return FileStatAdapter(path, os.stat(path))