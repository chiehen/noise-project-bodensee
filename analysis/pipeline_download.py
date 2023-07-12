import os
import subprocess
import shutil
import gitlab


def download_pipeline_artifacts(pa_token: str, project_id: int, pipeline_id: int, directory,
                                accepted_artifact_types: list[str] = ["archive"]) -> str:
    """
    Downloads all artifacts of the given pipeline. Can provide a list of different types of artifacts
    Will download in given directory. Will create a folder for each artifact zip.
    """

    gl = gitlab.Gitlab('https://gitlab.lrz.de', private_token=pa_token)
    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    print(pipeline)
    jobs = pipeline.jobs.list(get_all=True)

    print(f"Using dir: {directory} for #{pipeline_id} with {len(jobs)} jobs")
    for job in jobs:
        if len([j for j in job.artifacts if j["file_type"] in accepted_artifact_types]) == 0: continue
        # create a new directory for each job
        print(f"Downloading artifacts for job {job.name} with id {job.id}")
        try:
            os.mkdir(os.path.join(directory, str(job.id)))
        except FileExistsError:
            print(f"Directory {os.path.join(directory, str(job.id))} already exists. Continuing")
            continue

        # write jobname to file
        with open(os.path.join(directory, str(job.id), "jobname.txt"), "w") as f:
            f.write(job.name)

        got_job = project.jobs.get(job.id)
        # download and unzip artifacts

        zipdir = os.path.join(directory, str(job.id), "artifacts.zip")
        with open(zipdir, "wb") as f:
            got_job.artifacts(streamed=True, action=f.write)
        subprocess.run(["unzip", "-o", zipdir, "-d", os.path.join(directory, str(job.id))])
        os.unlink(zipdir)
        print(f"Downloaded artifacts for job {job.name} with id {job.id}")

        # check if there is an experiment.zip file
        if os.path.exists(os.path.join(directory, str(job.id), "experiment.zip")):
            # inflate
            subprocess.run(["unzip", "-o", os.path.join(directory, str(job.id), "experiment.zip"), "-d",
                            os.path.join(directory, str(job.id))])
            # remove zip
            os.unlink(os.path.join(directory, str(job.id), "experiment.zip"))
        else:
            print(f"WARNING: No experiment.zip found for job {job.name} with id {job.id}")
            shutil.rmtree(os.path.join(directory, str(job.id)))

    return directory

download_pipeline_artifacts(os.environ["GITLAB_USER_KEY"], 140225, 1485147, "./artifacts")