# This searches for configuration files; they are located where modelselector is first found, travelsing
# upwards: that is the main initialization script for configuration files and should be more resistent.

import os

# Because the filename depends on where we call the script from. It could be even more complicated for you.
def filename(namestring):
    # Start with the current directory and move up until the root directory is reached
    current_dir = os.getcwd()
    print(current_dir)
    step_count = 0
    
    while True:
        # Check if the "modelselector.py" file exists in the current directory
        if os.path.exists(os.path.join(current_dir, "modelselector.py")):
            print(os.path.join(current_dir, "modelselector.py"))
            # If found, return the namestring prefixed with "../" based on the step count
            return '../' * step_count + namestring
        
        # Move up to the parent directory
        current_dir = os.path.dirname(current_dir)
        
        # Increment the step count
        step_count += 1
        
        # Break if we reach the root directory and still haven't found the file
        if current_dir == os.path.dirname(current_dir):
            break
    
    # If the file is not found, return namestring as-is (this part will probably yield an error)
    return namestring

# Example usage:
if __name__ == "__main__":
    # If it does not exist, error is handler in the caller: it handles it's own not-exist exceptions.
    namestring = "model_select.json"
    result = filename(namestring)
    print(result)  # This will print either "../path/to/example_file.txt" or just "example_file.txt" depending on the location of the script

    namestring = "models_config.json"
    result = filename(namestring)
    print(result)  # This will print either "../path/to/example_file.txt" or just "example_file.txt" depending on the location of the script
