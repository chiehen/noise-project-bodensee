import os
import subprocess
import shutil
import gitlab


def download_pipeline_artifacts(pa_token: str, project_id: int, pipeline_id: int, directory, accepted_artifact_types: list[str] = ["archive"]) -> str:
    gl = gitlab.Gitlab('https://gitlab.lrz.de', private_token=pa_token)
    project = gl.projects.get(project_id)
    pipeline = project.pipelines.get(pipeline_id)
    print(pipeline)
    jobs = pipeline.jobs.list(get_all=True)

    
    print(f"Using temp dir: {directory} for #{pipeline_id} with {len(jobs)} jobs")
    for job in jobs:
        if len([j for j in job.artifacts if j["file_type"] in accepted_artifact_types]) == 0: continue
        # create a new directory for each job
        try:
            os.mkdir(os.path.join(directory, str(job.id)))
        except FileExistsError:
            print(f"Directory {os.path.join(directory, str(job.id))} already exists. Deleting contents.")
            for f in os.listdir(os.path.join(directory, str(job.id))):
                os.remove(os.path.join(directory, str(job.id), f))

        # write jobname to file
        with open(os.path.join(directory, str(job.id), "jobname.txt"), "w") as f:
            f.write(job.name)

        got_job = project.jobs.get(job.id)
        # download and unzip artifacts

        zipfn = os.path.join(directory, str(job.id), "artifacts.zip")
        with open(zipfn, "wb") as f:
            got_job.artifacts(streamed=True, action=f.write)
        subprocess.run(["unzip", "-o", zipfn, "-d", os.path.join(directory, str(job.id))])
        os.unlink(zipfn)
        print(f"Downloaded artifacts for job {job.name} with id {job.id}")

        # check if there is an experiment.zip file
        if os.path.exists(os.path.join(directory, str(job.id), "experiment.zip")):
            # inflate
            subprocess.run(["unzip", "-o", os.path.join(directory, str(job.id), "experiment.zip"), "-d", os.path.join(directory, str(job.id))])
            # remove zip
            os.unlink(os.path.join(directory, str(job.id), "experiment.zip"))
        else:
            print(f"WARNING: No experiment.zip found for job {job.name} with id {job.id}")
            shutil.rmtree(os.path.join(directory, str(job.id)))

    return directory
