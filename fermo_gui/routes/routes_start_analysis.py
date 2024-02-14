"""Routes for pages related to data input and processing.

Copyright (c) 2022-present Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pathlib import Path
from typing import Union

from celery.result import AsyncResult
from flask import (
    render_template,
    redirect,
    url_for,
    session,
    Response,
    current_app,
    request,
)

from fermo_gui.analysis.analysis_manager import start_fermo_core
from fermo_gui.analysis.general_manager import GeneralManager as GenManager
from fermo_gui.config.extensions import socketio
from fermo_gui.forms.analysis_input_forms import AnalysisInput
from fermo_gui.routes import bp


@bp.route("/analysis/start_analysis/", methods=["GET", "POST"])
def start_analysis() -> Union[str, Response]:
    """Render start analysis page, get and store data, init analysis.

    Notes: On every GET, the page prepares a new job (job ID + upload directory)
    On POST (form.validate_on_submit()), the asynchronous job is started

    Returns:
        On GET, the "start_analysis" page, on POST a redirect to the "job_submitted" p.
    """
    # TODO(MMZ 14.2.24): Cover with tests
    form = AnalysisInput()

    if request.method == "GET":
        task_id = GenManager().create_uuid(current_app.config.get("UPLOAD_FOLDER"))
        task_upload_path = GenManager().create_upload_dir(
            current_app.config.get("UPLOAD_FOLDER"), task_id
        )
        session["task_id"] = task_id
        session["task_upload_path"] = task_upload_path
        return render_template("start_analysis.html", form=form)

    if form.validate_on_submit():
        params = {"email": form.email.data}

        GenManager.store_data_as_json(
            session["task_upload_path"],
            f"{session['task_id']}.params.json",
            params,
        )

        data = {
            "job_id": session["task_id"],
            "upload_path": session["task_upload_path"],
            "root_url": request.base_url.partition("/analysis/start_analysis/")[0],
            "email": params.get("email"),
            "email_notify": True,
        }

        if "localhost" in data["root_url"] or "127.0.0.1" in data["root_url"]:
            data["email_notify"] = False
        elif params.get("email") is None:
            # TODO(MMZ 13.2.24): change to the correct params data structure
            data["email_notify"] = False
        elif current_app.config.get("MAIL_USERNAME") is None:
            data["email_notify"] = False

        start_fermo_core.apply_async(
            kwargs={"data": data},
            task_id=session["task_id"],
        )
        return redirect(url_for("routes.job_submitted", job_id=session["task_id"]))


@bp.route("/analysis/job_submitted/<job_id>/", methods=["GET"])
def job_submitted(job_id: str) -> str:
    """Serves as placeholder during calculation.

    Arguments:
        job_id: the job identifier, provided by the URL variable

    Returns:
        The rendered "job_submitted.html" page
    """
    # TODO(MMZ 14.2.24): Cover with tests
    job_data = {
        "task_id": job_id,
        "root_url": request.base_url.partition("/analysis/job_submitted/")[0],
    }
    return render_template("job_submitted.html", job_data=job_data)


@socketio.on("startup_event")
def handle_startup_message(data: dict):
    """Debug function to check responsiveness of socket.io

    Arguments:
        data: a JSON-derived dictionary
    """
    print("received json: " + str(data))


@socketio.on("get_status")
def check_job_status(data: str):
    """Serve job status upon request.

    Note: Celery does not differentiate between non-existing and non-running jobs.
    To prevent endless loops on non-existing jobs, existence of upload folder is
    verified: no folder, no job run

    Arguments:
        data: JSON-derived dict with job ID to check status of
    """
    # TODO(MMZ 14.2.24): Cover with tests
    if (
        not Path(current_app.config.get("UPLOAD_FOLDER"))
        .joinpath(data.get("task_id"))
        .exists()
    ):
        socketio.emit("job_status", {"status": "job_not_found"})
    else:
        try:
            result = AsyncResult(data.get("task_id"))
            outcome = result.result if result.ready() else None
            match outcome:
                case True:
                    socketio.emit("job_status", {"status": "job_successful"})
                case False:
                    socketio.emit("job_status", {"status": "job_failed"})
                case None:
                    socketio.emit("job_status", {"status": "job_running"})
        except ValueError:
            socketio.emit("job_status", {"status": "job_not_found"})
