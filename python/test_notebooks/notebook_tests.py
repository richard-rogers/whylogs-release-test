import os
import subprocess

import papermill as pm

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(TEST_DIR, os.pardir, os.pardir)
OUTPUT_NOTEBOOK = "output.ipynb"
skip_notebooks = [
    "Guest Session.ipynb",
    "Single_Image_Tracing_Profile_to_WhyLabs.ipynb",
    "Pyspark_Profiling.ipynb",
    "WhyLabs_Sagemaker-PyTorch.ipynb",
    "Kafka_Example.ipynb",
    "Writing_to_WhyLabs.ipynb",
    "Writing_Reference_Profiles_to_WhyLabs.ipynb",
    "flask_with_whylogs.ipynb",
    "BigQuery_Example.ipynb",
    "Segments.ipynb",
    "Writing_Regression_Performance_Metrics_to_WhyLabs.ipynb",
    "Writing_Classification_Performance_Metrics_to_WhyLabs.ipynb",
    "Getting_Started_with_WhyLabsV1.ipynb",
    "Getting_Started_with_UDFs.ipynb",
    "Writing_Feature_Weights_to_WhyLabs.ipynb",
    "Image_Logging.ipynb",
    "Writing_Ranking_Performance_Metrics_to_WhyLabs.ipynb",
    "Image_Logging_Udf_Metric.ipynb",
    "mnist_exploration.ipynb",
    "performance_estimation.ipynb",
    "Embeddings_Distance_Logging.ipynb",  # skipped due to data download
    "whylogs_Audio_examples.ipynb",  # skipped because of Kaggle data download and API key for whylabs upload
    "Logging_with_Debug_Events.ipynb",  # skipped because of API key required with whylabs writing
    "NLP_Summarization.ipynb",
    "Multi dataset logger.ipynb",
    "Pyspark_and_Constraints.ipynb",
    "LocalStore_with_Constraints.ipynb",  # skipped because it has over 4 minutes of thread.sleep in it
    "KS_Profiling.ipynb",  # skipped because this takes a few minutes to run
    "Monitoring_Embeddings.ipynb",  # skipped because needs user input
]


# https://docs.pytest.org/en/6.2.x/example/parametrize.html#a-quick-port-of-testscenarios
def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


def process_notebook(notebook_filename):
    """
    Checks if an IPython notebook runs without error from start to finish. If so, writes the
    notebook to HTML (with outputs) and overwrites the .ipynb file (without outputs).
    """
    try:
        pm.execute_notebook(notebook_filename, OUTPUT_NOTEBOOK, timeout=180)
    except Exception as e:
        print(f"Notebook: {notebook_filename} failed test with exception: {e}")
        raise

    print(f"Successfully executed {notebook_filename}")


class TestNotebooks:
    git_files = (
        subprocess.check_output("git ls-tree --full-tree --name-only -r HEAD", shell=True).decode("utf-8").splitlines()
    )

    # Get just the notebooks from the git files
    notebooks = [fn for fn in git_files if fn.endswith(".ipynb") and os.path.basename(fn) not in skip_notebooks]
    scenarios = [(notebook, {"notebook": notebook}) for notebook in notebooks]

    def test_all_notebooks(self, notebook):
        process_notebook(os.path.join(PARENT_DIR, notebook))
