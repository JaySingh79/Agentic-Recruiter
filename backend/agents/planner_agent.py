def create_plan(matches: dict, experience: int) -> list:
    return [
        {'phase': 'warmup', 'type': 'behavioral'},
        {'phase': 'skills', 'type': 'technical', 'skills': list(matches.keys())},
        {'phase': 'scenario', 'type': 'case'},
        {'phase': 'wrapup', 'type': 'closing'}
    ]