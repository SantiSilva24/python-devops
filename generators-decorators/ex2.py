# Must be ran with the terminal pointing to the correct path:
# cd python-devops/generators-decorators

def read_config_file(filepath):
    """
    Validates the filepath and yields each line from the file.

    Args:
        filepath (str): The path to the configuration file.

    Yields:
        str: A single line from the file.
    """
    if not isinstance (filepath, str):
        print("Incorrect file path format")
        return None
    
    with open(filepath, "r") as file:
        for line in file:
            yield line


def filter_config_lines(lines):
    """
    Filters an iterable of lines, yielding stripped, non-empty, non-comment lines.

    Args:
        lines (iterable): An iterable producing string lines.

    Yields:
        str: A line that is not a comment or empty.
    """
    for line in lines:
       stripped = line.strip()
       
       if not stripped:
           continue
       if stripped.startswith('#'):
           continue
       yield stripped


def parse_config_lines(lines):
    """
    Parses an iterable of clean config lines into (section, key, value) tuples.

    Args:
        lines (iterable): An iterable producing clean config lines.

    Yields:
        tuple: A tuple in the format (section, key, value).
    """
    
    current_section = None

    for line in lines:

        # Detect section headers
        if line.startswith('['):
            current_section = line.strip('[]')
            continue

        # Split key/value
        line_parts = line.split()

        if len(line_parts) < 2:
            continue

        key = line_parts[0]
        value = line_parts[2]

        yield (current_section, key, value)
        
for line in parse_config_lines(filter_config_lines(read_config_file("app.cfg"))):
    print(line)