# ML Workflow Pipeline

## Overview

This is a Kedro project, which was generated using `Kedro 0.17.7`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://kedro.readthedocs.io/en/stable/11_faq/01_faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
pip install -r src/requirements.txt
```

## How to run Kedro

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
kedro test
```

To configure the coverage threshold, look at the `.coveragerc` file.


## How to deploy this kedro project as a Python app in a container image to Cloud Run 


Take a look at the [Cloud Run documentation](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service) to get started.

 - Take a look at the `main.py` and make changes in it according to your preference.
 - Add dependencies in the `requirements.txt` file which is inside the root directory of this repo and you can also add dependencies in `src/requirements.txt` for the kedro project.
 - After this take a look at the `Dockerfile` which is inside the root directory of this repo and make changes according to your preferences.

After all this prep-work makde sure you have `google cloud sdk` installed in your system and run the `gcloud run deploy` command to deploy your app to cloud run.
