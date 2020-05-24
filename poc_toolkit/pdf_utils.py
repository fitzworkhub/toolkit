"""
Functions for manipulating PDF files

Current functionality:
- count pages
- convert to png
"""
from folder_utils import pageFilename
from PyPDF2 import PdfFileReader, PdfFileWriter
from sh import convert
from typing import Iterable
import json


from indico.queries.documents import DocumentExtraction
from indico.queries import JobStatus, RetrieveStorageObject


def count_pages(filename: str) -> int:
    with open(filename, 'rb') as f:
        pdf = PdfFileReader(f)
        if pdf.isEncrypted:
            pdf.decrypt('')
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
            '-alpha',
            'remove',
            output_filepath
        )
        return

    except Exception as e:
        print("ERROR: %s" % pdf_filepath)
        print(e)
        return


def separate_pdf(
        pdf_input_path: str,
        pdf_output_path: str,
        pages: Iterable) -> None:

    with open(pdf_input_path, 'rb') as f:
        pdf = PdfFileReader(f)
        if pdf.isEncrypted:
            pdf.decrypt('')

        for page in pages:
            out_pdf = PdfFileWriter()
            output_filepath = pageFilename(pdf_output_path, page)
            out_pdf.addPage(pdf.getPage(page))
            with open(output_filepath, 'wb') as f:
                out_pdf.write(f)


def pdf_extraction(files, client, config):
    """
    get pdf extraction dictionary objects
    """
    pdf_extractions = []
    failed_files = []
    jobs = client.call(
        DocumentExtraction(
            files=files,
            json_config=json.dumps(config)
        )
    )

    for i, j in enumerate(jobs):
        try:
            job = client.call(JobStatus(id=j.id, wait=True))
            doc_extract = client.call(RetrieveStorageObject(job.result))
            pdf_extractions.append(doc_extract)
        except:
            failed_files.append(files[i])

    return pdf_extractions, failed_files
