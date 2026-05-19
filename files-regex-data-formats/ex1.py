from pathlib import Path
from typing import Union
import datetime

def archive_log_files(log_directory: Union[str, Path], archive_date: str) -> list[Path]:
    """
    Finds and renames all .log files in a directory with a date stamp.

    Args:
        log_directory (Union[str, Path]): The directory to scan.
        archive_date (str): The date stamp to use for renaming (YYYY-MM-DD).

    Returns:
        list[Path]: A list of the new Path objects for the renamed files.
    
    Raises:
        TypeError: If an argument has an invalid type.
        ValueError: If an argument has an invalid value or format.
    """
    if not isinstance(log_directory, (str, Path)):
        raise TypeError(f"Log directory {str(log_directory)} must be a string or a Path object, recieved {type(log_directory).__name__!r}")
    
    # normalise to Path so .is_dir() always works
    log_directory = Path(log_directory)                    
    
    if not log_directory.exists() and not log_directory.is_dir():
        raise ValueError(f"Log directory {str(log_directory)!r} does not exist or is not a directory")
    
    if not (isinstance(archive_date, str)):
        raise TypeError(f"Archive date must be a string, recieved {type(archive_date).__name__!r}")
    
    # TODO: The archive_date string must be validated to ensure it matches the YYYY-MM-DD format. If the format is invalid, raise a ValueError
    # format validation via datetime
    try:                                                   
        datetime.date.fromisoformat(archive_date)
    except ValueError:
        raise ValueError(
            f"archive_date {archive_date!r} is not a valid date in YYYY-MM-DD format"
        )

    archived_files = []

    # Loop through all files in the directory
    for file in log_directory.iterdir():
        if file.is_file() and file.suffix == '.log':
            new_path = file.with_name(f"{file.stem}-{archive_date}.log")
            
            file.rename(new_path)
            archived_files.append(new_path)
    return archived_files

    

if __name__ == "__main__":          # only runs when executing the file directly
    log_dir = Path("/tmp/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    archive_log_files(log_dir, "2023-10-27")
    archive_log_files("/tmp/logs", "2023-10-28")