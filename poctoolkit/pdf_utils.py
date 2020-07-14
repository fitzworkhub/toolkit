"""
Functions for manipulating PDF files

Current functionality:
- count pages
- convert to png
"""
import os
import sys
import random
import tempfile
import shutil
from .folder_utils import pageFilename
from PyPDF2 import PdfFileReader, PdfFileWriter
from sh import convert
from typing import Iterable
import json


from indico.queries.documents import DocumentExtraction
from indico.queries import JobStatus, RetrieveStorageObject


def count_pages(filename: str) -> int:
    with open(filename, "rb") as f:
        pdf = PdfFileReader(f)
        if pdf.isEncrypted:
            pdf.decrypt("")
        n_pages = pdf.getNumPages()
    return n_pages


def pdf_to_png(pdf_filepath: str, output_filepath: str) -> None:
    try:
        convert(
            "-density",
            "300",
            pdf_filepath,
            "-depth",
            "8",
            "-strip",
            "-background",
            "white",
            "-alpha",
            "remove",
            output_filepath,
        )
        return

    except Exception as e:
        print("ERROR: %s" % pdf_filepath)
        print(e)
        return


def separate_pdf(pdf_input_path: str, pdf_output_path: str, pages: Iterable) -> None:

    # create staging file for filename issues
    staging_file_handle = tempfile.TemporaryFile()

    with open(pdf_input_path, "rb") as f:
        shutil.copyfileobj(f, staging_file_handle)
        staging_file_handle.seek(0)

    pdf = PdfFileReader(staging_file_handle)
    if pdf.isEncrypted:
        pdf.decrypt("")

    for page in pages:
        out_pdf = PdfFileWriter()
        output_filepath = pageFilename(pdf_output_path, page)
        out_pdf.addPage(pdf.getPage(page))
        with open(output_filepath, "wb") as f:
            out_pdf.write(f)
    staging_file_handle.close()


def split_pdf_pages(pdf_input_path: str, output_folder: str, max_pages=None):
    """
    Split pdf into individual pages and save to output_folder with name
    filename + _page_x.pdf

    if max_pages is provided, only take up to the amount provided.
    Pages will be selected at random
    """
    # create staging file for filename issues
    staging_file_handle = tempfile.TemporaryFile()

    with open(pdf_input_path, "rb") as f:
        shutil.copyfileobj(f, staging_file_handle)
        staging_file_handle.seek(0)

    pdf = PdfFileReader(staging_file_handle, strict=False)
    if pdf.isEncrypted:
        pdf.decrypt("")

    page_numbers = range(pdf.numPages)

    # Take random page numbers if max_pages is provided
    if max_pages and pdf.numPages > max_pages:
        page_numbers = random.sample(page_numbers, max_pages)

    for page_num in page_numbers:
        out_pdf = PdfFileWriter()
        pdf_page_filepath = pageFilename(pdf_input_path, page_num)
        pdf_filename = os.path.basename(pdf_page_filepath)
        output_filepath = os.path.join(output_folder, pdf_filename)
        out_pdf.addPage(pdf.getPage(page_num))
        with open(output_filepath, "wb") as f:
            out_pdf.write(f)
    staging_file_handle.close()


def pdf_extraction(pdf_filepaths, client, config):
    """
    get pdf extraction dictionary objects
    """
    pdf_extractions = []
    failed_files = []
    jobs = client.call(
        DocumentExtraction(files=pdf_filepaths, json_config=json.dumps(config))
    )

    for i, j in enumerate(jobs):
        try:
            job = client.call(JobStatus(id=j.id, wait=True))
            doc_extract = client.call(RetrieveStorageObject(job.result))
            pdf_extractions.append(doc_extract)
        except:
            failed_files.append(pdf_filepaths[i])

    return pdf_extractions, failed_files
