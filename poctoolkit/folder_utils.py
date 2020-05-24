
import os
import glob


def files_from_directory(src_dir, regex='*.*'):
    """
    return a list of all files in src_dir that match the regex
    """
    filename_regex = os.path.join(src_dir, regex)
    filelist = glob.glob(filename_regex)
    return filelist


def absoluteFilePaths(directory: str):
    """
    Get list of absolute paths of all files in directory
    """
    filepaths = []
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            filepaths.append(os.path.abspath(os.path.join(dirpath, f)))
    return filepaths


def pageFilename(filepath: str, page: str) -> str:
    """
    Append page to filename, assumes filename has an extension
    """

    filename, extension = os.path.splitext(filepath)
    page_filepath = f"{filename}_page_{page}{extension}"
    return page_filepath
