import os
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask

app = Flask(__name__)


def get_shell_script_output_using_communicate():
    session = Popen(['./run_kedro.sh'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception("Error " + str(stderr))
    return stdout.decode('utf-8')


def get_shell_script_output_using_check_output():
    stdout = check_output(['./run_kedro.sh']).decode('utf-8')
    return stdout


@app.route("/")
def hello_world():
    return '<pre>' + get_shell_script_output_using_check_output() + '</pre>'


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
