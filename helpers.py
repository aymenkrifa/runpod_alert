import subprocess
from typing import List
from datetime import datetime


def get_pod_info():
    command_output = subprocess.check_output(["runpodctl", "get", "pod"])

    # Convert the output to a string and split it into lines
    output_lines = command_output.decode("utf-8").strip().split("\n")

    pod_infos = []

    if len(output_lines) > 1:
        # The first line contains the header, so we skip it
        for pod_info in output_lines[1:]:
            fields = pod_info.split("\t")

            # Create a dictionary for each pod
            pod_dict = {
                "time": datetime.now().strftime("%d/%m/%Y at %H:%M"),
                "id": fields[0],
                "name": fields[1],
                "gpu": fields[2],
                "image_name": fields[3],
                "status": fields[4],
            }

            pod_infos.append(pod_dict)

            return pod_infos
    else:
        return None


def get_pod_per_id(pod_id):
    pod_infos: List[dict] = get_pod_info()
    if pod_infos:
        for index, _ in enumerate(pod_infos):
            if _.get("id") == pod_id:
                return pod_infos[index]
