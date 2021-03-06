import os
import glob


def files_from_directory(src_dir, regex="*.*"):
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


def get_folder_differences(src_folder, dst_folder):
    pdf_filepaths = files_from_directory(src_folder, "*.pdf")
    processed_paths = files_from_directory(dst_folder)

    src_filenames = set(map(os.path.basename, pdf_filepaths))
    dst_filenames = set(map(os.path.basename, processed_paths))
    compute_files = src_filenames.difference(dst_filenames)
    compute_filepaths = [
        os.path.join(src_folder, compute_file) for compute_file in compute_files
    ]
    return compute_filepaths


def check_folder(data_path):
    """
    Check if data_path exists, if not create datapath
    """
    if not os.path.exists(data_path):
        os.mkdir(data_path)
