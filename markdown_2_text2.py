""" Description """
import os
import shutil
import argparse
import zipfile
from typing import Optional
from bs4 import BeautifulSoup

current_directory = os.getcwd()


def convert_markdown_to_text(markdown_text: str) -> Optional[str]:
    """
    Converts markdown text to plain text.
    Args:
        markdown_text: The markdown text to convert.
    Returns:
        The converted text, or None if the conversion fails.
    """
    try:
        soup = BeautifulSoup(markdown_text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Failed to convert markdown text: {e}")
        return None


def remove_html_tags(text: str) -> str:
    """
    Removes HTML tags from the given text.
    Args:
        text: The text to remove HTML tags from.
    Returns:
        The text with HTML tags removed.
    """
    return text.replace('<', '').replace('>', '')


def simplify_newlines(text: str) -> str:
    """
    Simplifies multiple newlines in the given text.
    Args:
        text: The text to simplify newlines in.
    Returns:
        The text with simplified newlines.
    """
    return '\n'.join(filter(None, text.split('\n')))


def walk_directory(directory: str) -> list:
    """
    Walks the directory tree and returns a list of markdown files.
    Args:
        directory: The directory to walk.
    Returns:
        A list of markdown files.
    """
    source_files = []
    for root, dir, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                source_files.append(os.path.join(root, file))
    return source_files


def unzip_file(zip_file_path: str) -> Optional[str]:
    """ Unzip files from zip in specified path 'zip_file_path' to \
        'unzipped_source_files' directory'.
    Args: 
        zip_file_path: string path to the zip file to handle
    Returns: Directory files are unzipped into"""
    unzip_directory = os.path.join(current_directory, 'unzipped_source_files')
    if os.path.exists(unzip_directory):
        shutil.rmtree(unzip_directory)
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_directory)
            return unzip_directory
    except zipfile.BadZipfile:
        print("The ZIP file is corrupted or invalid.")
    except FileNotFoundError:
        print("The ZIP file or extract path was not found.")
    except PermissionError:
        print("You do not have permission to access the ZIP file or extract path.")
    except Exception as e:
        print(f"An error occurred: {e}")


def convert_files(markdown_files_to_convert: list, output_file_path: str) -> None:
    """
    Converts markdown files to text and saves them in a single output file.
    Args:
        markdown_files_to_convert: A list of markdown files to convert.
        output_file_path: The path to the output file.
    """
    all_text = ""
    for file in markdown_files_to_convert:
        if not os.path.isfile(file):
            print(f"Skipping {file}: not a file")
            continue
        try:
            with open(file, 'r', encoding='utf-8') as markdown_file:
                markdown_text = markdown_file.read()
                converted_text = convert_markdown_to_text(markdown_text)
                if converted_text:
                    converted_text = remove_html_tags(converted_text)
                    converted_text = simplify_newlines(converted_text)
                    all_text += converted_text + "\n\n"
                    print(f"Converted {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Error creating output directory: {e}")
            return
    try:
        with open(output_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(all_text)
        print(f"Saved all converted text to {output_file_path}")
    except Exception as e:
        print(f"Error writing to output file: {e}")


def cleanup() -> None:
    """ Cleanup unzipped source files. """
    unzip_dir = os.path.join(current_directory, "unzipped_source_files")
    if os.path.exists(unzip_dir):
        if os.path.isdir(unzip_dir):
            shutil.rmtree(unzip_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert markdown files to text files')
    parser.add_argument('--input', type=str, required=False,
                        help='Path to the directory containing markdown files or path to zip file',
                        default="/home/kirtlekw6478/Downloads/DevDocs.zip")
    parser.add_argument('--output', type=str, required=False,
                        help='Path to the directory where text files will be saved',
                        default="/home/kirtlekw6478/code/python/markdown_2_text/output/")
    args = parser.parse_args()
    if args.input.endswith('.zip'):
        working_directory = unzip_file(args.input)
        markdown_files = walk_directory(working_directory)
    else:
        markdown_files = walk_directory(args.input)
    convert_files(markdown_files, args.output)

    cleanup()
    print('Done')
