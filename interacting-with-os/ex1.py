import shutil
from pathlib import Path

def create_backup(source_dir: str | Path, dest_dir: str | Path) -> None:
    """
    Creates a clean backup of a source directory to a destination directory.

    If the destination directory exists, it is removed before copying.

    Args:
        source_dir (Union[str, Path]): The directory to back up.
        dest_dir (Union[str, Path]): The directory to create the backup in.
    """
    # Input validation.
    for path in [source_dir, dest_dir]:
        if not isinstance(path, (str, Path)):
            raise TypeError(f"Path {str(path)} must be a string or a Path object, recieved {type(path).__name__!r}")
    
    # normalise to Path so .is_dir() always works
    source_dir = Path(source_dir)  

    if not source_dir.exists() or not source_dir.is_dir():
        raise ValueError(f"Could not find {source_dir} or it is not a directory")
    
    # Check if the destination exists; if yes, remove it.
    dest_dir = Path(dest_dir)

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    
    # Copy the source to the destination.
    shutil.copytree(source_dir, dest_dir)


    