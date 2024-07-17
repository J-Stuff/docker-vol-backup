import docker


def run_backup():
    client = docker.DockerClient(base_url='unix://socket')