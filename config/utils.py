import base64, re
from rest_framework.schemas import AutoSchema
from django.conf import settings
import requests
import json
import openai
import os

class CustomSchema(AutoSchema):
    schema_list = []
    schema_create = []
    schema_retrieve = []
    schema_update = []
    schema_partial_update = []
    schema_delete = []

    def __init__(self, schema):
        super(CustomSchema, self).__init__(None)
        if "list" in schema:
            self.schema_list = schema["list"]
        if "create" in schema:
            self.schema_create = schema["create"]
        if "retrieve" in schema:
            self.schema_retrieve = schema["retrieve"]
        if "update" in schema:
            self.schema_update = schema["update"]
        if "partial_update" in schema:
            self.schema_partial_update = schema["partial_update"]
        if "delete" in schema:
            self.schema_delete = schema["delete"]

    def is_list(self, path, method):
        return method == "GET" and not "{id}" in path

    def is_create(self, path, method):
        return method == "POST" and not "{id}" in path

    def is_retrieve(self, path, method):
        return method == "GET" and "{id}" in path

    def is_update(self, path, method):
        return method == "PUT" and "{id}" in path

    def is_partial_update(self, path, method):
        return method == "PATCH" and "{id}" in path

    def is_delete(self, path, method):
        return method == "DELETE" and "{id}" in path

    def get_manual_fields(self, path, method):
        super().get_manual_fields(path, method)

        if self.is_list(path, method):
            return self.schema_list
        elif self.is_create(path, method):
            return self.schema_create
        elif self.is_retrieve(path, method):
            return self.schema_retrieve
        elif self.is_update(path, method):
            return self.schema_update
        elif self.is_partial_update(path, method):
            return self.schema_partial_update
        elif self.is_delete(path, method):
            return self.schema_delete


def decode_base64(data, altchars=b"+/"):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub("[^a-zA-Z0-9%s]+" % altchars, "", data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return base64.b64decode(data, altchars)



# API 키를 환경 변수에서 읽어옵니다.
api_key = os.environ.get("OPENAI_API_KEY")
# organization = os.environ.get("OPENAI_ORGANIZATION")

# API 키가 존재하는지 확인합니다.
if api_key is None:
    raise Exception("API 키를 찾을 수 없습니다. 환경 변수를 설정하세요.")

# OpenAI API 키 설정
openai.api_key = api_key

openai.organization = "org-6fqXgACDDoBpHMfmZjuFrJcG"

def grammar_correction(text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Please correct the following text: '{text}'\n\nCorrected text:",
        max_tokens=50  # 적절한 길이로 조절
    )
    
    return response.choices[0].text.strip()