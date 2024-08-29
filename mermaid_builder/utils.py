import base64
import json
import zlib


def js_string_to_byte(data):
    return bytes(data, 'ascii')


def js_bytes_to_string(data):
    return data.decode('ascii')


def js_btoa(data):
    return base64.b64encode(data)


def pako_deflate(data):
    compress = zlib.compressobj(9, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
    compressed_data = compress.compress(data)
    compressed_data += compress.flush()
    return compressed_data


def get_mermaid_live_url(diagram_markdown: str):
    data = {"code": diagram_markdown, "mermaid": {"theme": "default"}}
    byte_str = js_string_to_byte(json.dumps(data))
    deflated = pako_deflate(byte_str)
    data_encode = js_btoa(deflated)
    link = 'http://mermaid.live/view#pako:' + js_bytes_to_string(data_encode)
    return link
