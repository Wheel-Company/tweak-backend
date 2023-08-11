import base64, re
from rest_framework.schemas import AutoSchema
from django.conf import settings
import requests
import json


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


# def send_fcm(device, notification=None, data=None):
#     url = 'https://fcm.googleapis.com/fcm/send'
#     headers = {
#         'Authorization': 'key=%s'%settings.FCM_SERVER_KEY,
#         'Content-Type': 'application/json; UTF-8',
#     }
#     content = {
#         'to':device.fcm_token
#     }
#     if notification:
#         content['notification'] = notification
#     if data:
#         content['data'] = data
#     if 'android' in data:
#         content['notification']['android_channel_id'] = data['android']['channelId']
#     if 'ios' in data:
#         content['content_available'] = True
#     r = requests.post(url, data=json.dumps(content), headers=headers)
#     result = json.loads(r.text)
#     FcmHistory(
#         body=json.dumps({
#             'device':device.id,
#             'data':data,
#             'result':result
#         })
#     ).save()
#     if result['success'] == 0:
#         device.valid = False
#         device.save()
#     #     device.delete()


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