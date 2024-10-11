import subprocess


def docker_build():
    print("Creating docker image")
    subprocess.run(["docker", "build", "-t", "{{ project-prefix }}-{{ app-name }}", "."])

def docker_run():
    print("Running docker image")
    command = [
        "docker", "run",
        "-p", "8501:8501",  # Port mapping
        "-it", "{{ project-prefix }}-{{ app-name }}"
    ]
    subprocess.run(command)
