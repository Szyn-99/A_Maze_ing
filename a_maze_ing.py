
def validate_lines(config_lines: list[str]) -> dict[str:int | str]:
    tokens_to_return = {"WIDTH": 0, "HEIGHT": 0, "EXIT": 0,"ENTRY": 0, "OUTPUT_FILE": None, "PERFECT": 0}
    
    tokens_to_search_dict = {"WIDTH": 0, "HEIGHT": 0, "EXIT": 0,"ENTRY": 0, "OUTPUT_FILE": 0, "PERFECT": 0}
    
    tokens_to_search_list = ["WIDTH", "HEIGHT", "EXIT","ENTRY", "OUTPUT_FILE", "PERFECT"]
    
    for line in config_lines:
        for token in tokens_to_search_list:
            if token == "WIDTH" and token in line:
                tokens_to_search_dict["WIDTH"] += 1
                tokens_to_return["WIDTH"] = int(line.split("=")[1])
            elif token == "HEIGHT" and token in line:
                tokens_to_search_dict["HEIGHT"] += 1
                tokens_to_return["HEIGHT"] = int(line.split("=")[1])
            elif token == "EXIT" and token in line:
                tokens_to_search_dict["EXIT"] += 1
                tokens_to_return["EXIT"] = int(line.split("=")[1])
            elif token == "ENTRY" and token in line:
                tokens_to_search_dict["ENTRY"] += 1
                tokens_to_return["ENTRY"] = int(line.split("=")[1])
            elif token == "OUTPUT_FILE" and token in line:
                tokens_to_search_dict["OUTPUT_FILE"] += 1
                tokens_to_return["OUTPUT_FILE"] = line.split("=")[1]
            elif token == "PERFECT" and token in line:
                tokens_to_search_dict["PERFECT"] += 1
                tokens_to_return["PERFECT"] = line.split("=")[1]
    for token in tokens_to_search_dict:
        if tokens_to_search_dict[token] > 1:
            raise ValueError("Parsing Error: Too many tokens in config")
            return False
        
    return tokens_to_return
def empty_outputf_trigger(output_file: str) -> bool:
    if output_file is None or output_file == "":
        return True
    for i in output_file:
        if i != " ":
            return False
    return True
def validate_tokens(config_tokens: dict) -> None:
    tokens = [key for key in config_tokens.keys()]
    for key in tokens:
        if key == "WIDTH" and config_tokens[key] > 300 and not None:
            raise ValueError("Width cannot be that High/None.")
        elif key == "WIDTH" and config_tokens[key] <= 0 and not None:
            raise ValueError("Width cannot be that Low/None.")
        elif key == "HEIGHT" and config_tokens[key] > 300 and not None:
            raise ValueError ("Height cannot be that High/None.")
        elif key == "HEIGHT" and config_tokens[key] <= 0 and not None:
            raise ValueError ("Height cannot be that Low/None.")
        elif key == "ENTRY" and config_tokens[key] > 1 and not None:
            raise ValueError ("Only one entry is allowed.")
        elif key == "EXIT" and config_tokens[key] > 1 and not None:
            raise ValueError ("Only one exit is allowed.")
        elif key == "OUTPUT_FILE" and empty_outputf_trigger(config_tokens[key]) and not None:
            raise ValueError ("Output file name cannot be Empty/None.")
        elif key == "PERFECT" and config_tokens[key] not in ("True" ,"False") and  not None:
            raise ValueError ("Acceptable 'Perfect' format is 'True' or 'False'.")
        
def main() -> None:
    try:
        with open("config.txt", "r") as f:
            config_lines = [line.strip() for line in f]
            tokens = validate_lines(config_lines)
            # print(tokens)
            validate_tokens(tokens)
            print(f"value ->{tokens['OUTPUT_FILE']}<-", end = "")
            
    except Exception as e:
        print("An Error Occured")
        print(f"Details: {e}")

if __name__ == "__main__":
    main()
            