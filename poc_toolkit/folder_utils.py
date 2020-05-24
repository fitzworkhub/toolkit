
import os


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
