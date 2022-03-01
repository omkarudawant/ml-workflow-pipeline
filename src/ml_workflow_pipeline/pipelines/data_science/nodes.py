"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""
# pylint: disable=invalid-name
from google.cloud import storage
import logging
from typing import Any, Dict
from datetime import datetime
import numpy as np
import pandas as pd


def train_model(
        train_x: pd.DataFrame, train_y: pd.DataFrame, parameters: Dict[str, Any]
) -> np.ndarray:
    """Node for training a simple multi-class logistic regression model. The
    number of training iterations as well as the learning rate are taken from
    conf/project/parameters.yml. All the data as well as the parameters
    will be provided to this function at the time of execution.
    """
    num_iter = parameters["example_num_train_iter"]
    lr = parameters["example_learning_rate"]
    X = train_x.to_numpy()
    Y = train_y.to_numpy()

    # Add bias to the features
    bias = np.ones((X.shape[0], 1))
    X = np.concatenate((bias, X), axis=1)

    weights = []
    # Train one model for each class in Y
    for k in range(Y.shape[1]):
        # Initialise weights
        theta = np.zeros(X.shape[1])
        y = Y[:, k]
        for _ in range(num_iter):
            z = np.dot(X, theta)
            h = _sigmoid(z)
            gradient = np.dot(X.T, (h - y)) / y.size
            theta -= lr * gradient
        # Save the weights for each model
        weights.append(theta)

    # Return a joint multi-class model with weights for all classes
    return np.vstack(weights).transpose()


def predict(model: np.ndarray, test_x: pd.DataFrame) -> np.ndarray:
    """Node for making predictions given a pre-trained model and a test set."""
    X = test_x.to_numpy()

    # Add bias to the features
    bias = np.ones((X.shape[0], 1))
    X = np.concatenate((bias, X), axis=1)

    # Predict "probabilities" for each class
    result = _sigmoid(np.dot(X, model))

    # Return the index of the class with max probability for all samples
    return np.argmax(result, axis=1)


def store_file_to_gcs(key_path, bucket_name, local_file_name):
    # Setting credentials using the downloaded JSON file
    client = storage.Client.from_service_account_json(json_credentials_path=key_path)
    # Creating bucket object
    bucket = client.get_bucket(bucket_name)
    # Name of the object to be stored in the bucket
    object_name_in_gcs_bucket = bucket.blob(local_file_name)
    # Name of the object in local file system
    object_name_in_gcs_bucket.upload_from_filename(local_file_name)
    print(f'File transferred to {bucket_name + "/" + local_file_name}')


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/536053624715/secrets/sa-tzar-key-cloud-build/versions/1"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    payload = response.payload.data.decode("UTF-8")
    return payload


def report_accuracy(predictions: np.ndarray, test_y: pd.DataFrame) -> None:
    """Node for reporting the accuracy of the predictions performed by the
    previous node. Notice that this function has no outputs, except logging.
    """
    # Get true class index
    target = np.argmax(test_y.to_numpy(), axis=1)
    # Calculate accuracy of predictions
    accuracy = np.sum(predictions == target) / target.shape[0]
    curr_date_time_stamp = str(datetime.now())
    with open(f"accuracy{curr_date_time_stamp}.txt", "w") as file:
        file.write(f"Iris model accuracy is {str(accuracy)}")

    key_data = access_secret_version(
        project_id='tzar-project',
        secret_id='sa-tzar-key-cloud-build',
        version_id=1
    )

    with open('sa-key.json', 'w') as file:
        file.write(key_data('private_key'))

    store_file_to_gcs(
        key_path='sa-key.json',
        bucket_name='tzar_bkt',
        local_file_name=f'accuracy{curr_date_time_stamp}.txt'
    )

    # Log the accuracy of the model
    log = logging.getLogger(__name__)
    log.info("Model accuracy on test set: %0.2f%%", accuracy * 100)


def _sigmoid(z):
    """A helper sigmoid function used by the training and the scoring nodes."""
    return 1 / (1 + np.exp(-z))
