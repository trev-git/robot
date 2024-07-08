import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
CONFIG_DIR = os.path.join(ROOT_DIR, "config")


def pose2str(pose):
    return "[" + ",".join([f"{v:.1f}" for v in pose]) + "]"
