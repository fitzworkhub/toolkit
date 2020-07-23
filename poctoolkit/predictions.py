"""
Functions to handle predictions
"""
import csv
import json
import os

from config import PROD_CLIENT
from indico.queries import ModelGroupPredict, JobStatus


def read_prediction(prediction_file):
    """
    Read prediction json file and return prediction list
    """
    with open(prediction_file) as f:
        predictions = json.load(f)
    return predictions


def predict(samples, model_id, client=PROD_CLIENT):
    """
    Get json predictions for each sample in samples

    Arguments:
        samples {List[str]} -- list of page text
        model_id {int} -- model_id number (found in the models Explain page)
        client {IndicoClient} -- Indico Client object containing auth data

    Returns:
        List[dict] -- list containing json output from indico predict api call

    """

    job = client.call(ModelGroupPredict(model_id=model_id, data=samples))

    predictions = client.call(JobStatus(id=job.id, wait=True)).result
    return predictions


def get_top_classification(classification_preds):
    """
    Given a list of classification prediction dicts, return the highest
    confidence label as well as confidence value
    """
    labels = []
    confidences = []
    for pred in classification_preds:
        label = max(pred, key=pred.get)
        labels.append(label)
        confidences.append(pred[label])

    return labels, confidences


def predictions_to_csv(prediction_files, csv_filepath="predictions.csv"):
    """
    Given a list of prediction json data, write to csv_filepath with format
    Identifier |  Label  |   Value  |  Confidence
    -----------+---------+----------+-------------

    If prediction_files is provided, create list of predictions by reading
    files
    """
    if prediction_files:
        prediction_lists = [
            read_prediction(prediction_file) for prediction_file in prediction_files
        ]

    with open(csv_filepath, mode="w") as prediction_handle:
        fieldnames = ["Filename", "Label", "Value", "Confidence"]
        writer = csv.DictWriter(prediction_handle, fieldnames=fieldnames)
        writer.writeheader()

        for prediction_list, prediction_filepath in zip(
            prediction_lists, prediction_files
        ):
            filename = os.path.basename(prediction_filepath)
            filename = os.path.splitext(filename)[0] + ".pdf"
            for prediction in prediction_list:
                value = prediction["text"]
                label = prediction["label"]
                confidence = prediction["confidence"][label]
                csv_row = {
                    "Filename": filename,
                    "Label": label,
                    "Value": value,
                    "Confidence": confidence,
                }
                writer.writerow(csv_row)
