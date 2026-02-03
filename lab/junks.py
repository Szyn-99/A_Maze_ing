def validate_tokens(config_tokens: dict) -> None:
    tokens = [key for key in config_tokens.keys()]
    width = config_tokens["WIDTH"]
    height = config_tokens["HEIGHT"]
    for key in tokens:
        if key == "WIDTH" and config_tokens[key] > 300 and not None:
            raise ValueError("Width cannot be that High/None.")
        elif key == "WIDTH" and config_tokens[key] <= -300 and not None:
            raise ValueError("Width cannot be that Low/None.")
        elif key == "HEIGHT" and config_tokens[key] > 300 and not None:
            raise ValueError ("Height cannot be that High/None.")
        elif key == "HEIGHT" and config_tokens[key] <= -300 and not None:
            raise ValueError ("Height cannot be that Low/None.")
        elif key == "OUTPUT_FILE" and empty_outputf_trigger(config_tokens[key]) and not None:
            raise ValueError ("Output file name cannot be Empty/None.")
        elif key == "PERFECT" and config_tokens[key] not in ("True" ,"False") and  not None:
            raise ValueError ("Acceptable 'Perfect' format is 'True' or 'False'.")
    if config_tokens["EXIT"]["x"] >= width or config_tokens["EXIT"]["y"] >= height:
        raise ValueError(f'Invalid Exit: ({config_tokens["EXIT"]["x"]}, {config_tokens["EXIT"]["y"]})')
    elif config_tokens['ENTRY']['x'] >= width or config_tokens["ENTRY"]["y"] >= height:
        raise ValueError(f'Invalid Entry: ({config_tokens["ENTRY"]["x"]}, {config_tokens["ENTRY"]["y"]})')
    