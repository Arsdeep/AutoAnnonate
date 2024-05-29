import os
import google.generativeai as genai
import glob
import sys
import argparse
import shutil

# Set your GEMINI API key here
GEMINI_API_KEY = 'your key'

# Function to display progress bar
def displayProgressBar(filesDone, totalFiles):
    # Define the length of the progress bar
    bar_length = 50
    # Calculate the percentage of files processed
    percent = 100.0 * filesDone / totalFiles
    # Calculate the length of the filled part of the bar
    filled_length = int(bar_length * filesDone // totalFiles)
    # Create the progress bar string
    bar = chr(9608) * filled_length + '-' * (bar_length - filled_length)
    
    # Print the progress bar
    sys.stdout.write(f'\r[{bar}] {percent:.1f}%')
    sys.stdout.flush()

# Function to count the total number of files in a directory and its subdirectories
def count_files(folder_path):
    total_files = 0
    # Iterate through all folders in the given path
    for folder in sorted(glob.glob(f'{folder_path}/*')):
        if os.path.isdir(folder):
            # Recursively count files in subdirectories
            total_files += count_files(folder)
        else:
            # Count files
            total_files += 1
    return total_files

# Function to get the content with comments from the Generative AI model
def getContentWithComments(relative_path, content):
    response = model.generate_content(f"""You're a Code commentor, your job is to only write comments when provided code and output only the modified raw code with comments without using markdown. You MUST NOT modify the code in any way.
    Write comments in the following file {relative_path} with code content -
    
    {content}
    
    If the code doesn't make sense or the content of code doesn't seem like code send response 'NONE' only.""").text
    return response

# Function to process files from source directory to destination directory
def process_files(src_dir, dst_dir):

    def readExclusionFile(file_name):
        with open(file_name, 'r') as file:
            content = file.readlines()
            content = [line.strip() for line in content]
        return content
    

    excluded_extension_list = []
    excluded_folder_list = []

    # Read contents of extension_exclusion_list.txt and folder_exclusion_list.txt if they exist and make a list of it
    if os.path.exists("./extension_exclusion_list.txt"):
        excluded_extension_list = readExclusionFile('extension_exclusion_list.txt')
    if os.path.exists("./folder_exclusion_list.txt"):
        excluded_folder_list = readExclusionFile('folder_exclusion_list.txt')

    filesDone = 0                           # For Progress Bar
    totalFiles = count_files(src_dir)       # For Progress Bar

    for root, dirs, files in os.walk(src_dir):
        # Filter out directories that start with '.'

        if(args.excludeHiddenDirs):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        # Copy Exluded folders as it is
        if(os.path.basename(root) in excluded_folder_list):
            if os.path.exists(os.path.join(dst_dir, root)):
                print(f"\n\nExcluded Directory '{root}' already exists, Skipping...\n")
            else:
                print(f"\n\nCopying Excluded Directory '{root}' without changes...\n")
                shutil.copytree(root, os.path.join(dst_dir, root))
                filesDone += count_files(root)
                displayProgressBar(filesDone, totalFiles)
            continue

        for file in files:
            # Skip if current file is this script or exclusion files
            if file == os.path.basename(__file__) or file == "extension_exclusion_list.txt" or file == "folder_exclusion_list.txt":
                filesDone += 1
                displayProgressBar(filesDone, totalFiles)
                continue

            # Construct the full file path
            src_file_path = os.path.join(root, file)
            
            # Calculate the relative path to recreate the directory structure in the destination directory
            rel_path = os.path.relpath(src_file_path, src_dir)
            dst_file_path = os.path.join(dst_dir, rel_path)

            # Create the directory structure in the destination directory
            dst_file_dir = os.path.dirname(dst_file_path)
            if not os.path.exists(dst_file_dir):
                os.makedirs(dst_file_dir)

            # Copy Exluded files as it is
            if file.startswith('.') or file.endswith(tuple(excluded_extension_list)):
                print(f"\n\nCopying Excluded file '{src_file_path}' without changes...'\n")
                shutil.copy(src_file_path, dst_file_path)
                filesDone += 1
                displayProgressBar(filesDone, totalFiles)
                continue
            
            # Read the content from the source file
            with open(src_file_path, 'r') as src_file:
                content = src_file.read()
            
            # Get the new content with comments
            new_content = getContentWithComments(rel_path, content)
            
            # Write the new content to the destination file
            try:
                with open(dst_file_path, 'w', encoding='utf-8') as dst_file:
                    if(new_content == "NONE"):
                        dst_file.write(content)
                    else:
                        dst_file.write(new_content)
                print(f"\n\nSuccessfully Created New File '{rel_path}'\n")
            except Exception as e:
                print(f"\n\nCould Not Create File '{rel_path}': {e}\n")
            finally:
                filesDone += 1
                displayProgressBar(filesDone, totalFiles)

def handleExclusionFile():
    default_extension_list = ['.txt', '.ico', '.gz', '.jpg', '.obj', '.lib', '.dll', '.pdb', '.svg', '.pyc', '.xlsx', '.tar', '.docx', '.war', '.jpeg', '.a', '.jar', '.ipynb', '.so', '.class', '.pptx', '.pdf', '.zip', '.ear', '.gif', '.exe', '.o', '.png', '.json', '.gitignore']

    default_folder_list = ['__pycache__', '.idea', '.bzr', '.pytest_cache', 'tmp', 'output', 'venv', '.cache', '.hg', 'node_modules', '.gradle', '.docker', 'test_output', 'out', '.svn', '.vscode', '.vs', 'node_modules_cache', '.next', '.history', 'coverage', '.git', 'bower_components', 'temp', 'env', '.settings', 'dist', 'logs', 'backup', 'tests_output', '.sass-cache', 'build']

    if not os.path.exists("./extension_exclusion_list.txt"):
        choice = str(input("extension Exclusion List doesn't exist. Do you want to create default list? (Y/n) - "))
        if (choice.lower()!= 'n'):
            # Write to extension_exclusion_list.txt
            with open('extension_exclusion_list.txt', 'w') as file:
                for item in default_extension_list:
                    file.write("%s\n" % item)
        else:
            print("Extension Exclusion List Not Created, Continuing...")
    else:
        print("Extension Exclusion List exists, Continuing...")


    if not os.path.exists("./folder_exclusion_list.txt"):
        choice = str(input("Folder Exclusion List doesn't exist. Do you want to create default list? (Y/n) - "))
        if (choice.lower()!= 'n'):
            # Write to folder_exclusion_list.txt
            with open('folder_exclusion_list.txt', 'w') as file:
                for item in default_folder_list:
                    file.write("%s\n" % item)
        else:
            print("Folder Exclusion Not Created, Continuing...")
    else:
        print("Folder Exclusion List exists, Continuing...")



if __name__ == "__main__":
    # Configure the Generative AI model with the API key
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-1.0-pro')

    parser = argparse.ArgumentParser(description="Example script to demonstrate argparse")

    parser.add_argument('--out', type=str, default='./Generated', help='Sets the relative/absolute Output directory')
    parser.add_argument('--src', type=str, default='./', help='Sets the relative/absolute Source directory')
    parser.add_argument('--excludeHiddenDirs', type=lambda x: (str(x).lower() != 'false'), default=True, help="Set true/false to Exclude Hidden Directories (beginning with '.') from Scan")

    # Parse the arguments
    args = parser.parse_args()

    # Source and destination directories
    src_directory = args.src
    dst_directory = args.out

    # Remove the destination directory if it already exists
    if os.path.exists(dst_directory):
        choice = str(input("Output Directory already exists. Do you want to continue overwriting? (y/N) - "))
        if (choice.lower()!= 'y'):
            print("Exiting...")
            exit()
        else:
            shutil.rmtree(dst_directory)
            print("Continuing...\n")
            
    handleExclusionFile()

    print("\nGenerating Code...")
    # Process the files
    process_files(src_directory, dst_directory)
    sys.stdout.write('\nCompleted!\n')