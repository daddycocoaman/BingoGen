import logging
import os
import azure.functions as func
from ..card import typeDict

def main(req: func.HttpRequest) -> func.HttpResponse:
    response = '<br>'.join([f'<a href=http://{os.environ["WEBSITE_HOSTNAME"]}/{k}>{k}</a>' for k in typeDict.keys()])
    return func.HttpResponse(response, mimetype="text/html")
