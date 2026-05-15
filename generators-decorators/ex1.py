def read_log_lines(filepath):
    """
    Creates a generator that reads a log file, yielding valid, non-comment lines.

    Args:
        filepath (str): The path to the log file.

    Yields:
        str: A stripped, non-empty, non-comment line from the file.
    """

    with open(filepath, "r") as file:
        for line in file:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith('#'):
                continue

            yield stripped