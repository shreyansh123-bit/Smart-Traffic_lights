from roboflow import Roboflow
rf = Roboflow(api_key="Qx9xrX1X9K1zcyTUxl6b")
project = rf.workspace("shrey-kadft").project("smart-traffic-light-97bp7")
version = project.version(13)
dataset = version.download("yolov9")
