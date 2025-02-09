import os
from settings import TEMPLATE_FOLDER


def load_template(template_name: str) -> str:
    with open(os.path.join(TEMPLATE_FOLDER, template_name), "r") as fl:
        txt = fl.read()
    return txt
