def manage_tags(existing_tags: dict, *simple_tags, **key_value_tags) -> dict:
    """
    Applies simple and key-value tags to an existing dictionary of tags.

    Args:
        existing_tags: The initial dictionary of tags.
        *simple_tags: Positional string arguments to be added as tags with a
                      value of 'true'. Duplicates should be ignored.
        **key_value_tags: Keyword arguments to be added or used to overwrite
                          existing tags.

    Returns:
        A new dictionary with all tags merged.
    """
    
    merged = existing_tags.copy()
    
    for key in simple_tags:
        merged[key] = 'true'
        
    if key_value_tags:
        merged.update(key_value_tags)
        
    return merged
    
initial = {'owner': 'dev-team', 'env': 'dev'}
final_tags = manage_tags(
    initial,
    'billable',              # A simple tag
    'critical',              # Another simple tag
    env='staging',           # A key-value tag that overwrites an existing key
    cost_center='xyz-123'    # A new key-value tag
)

print(final_tags)