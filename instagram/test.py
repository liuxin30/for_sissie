# -*- coding: utf-8 -*-
import json

with open("new_3.json", "r") as f:
    out = f.read()

ret = json.loads(out)
edge_followed_by = ret["data"]["user"]["edge_followed_by"]
page_info = edge_followed_by["page_info"]
print(page_info)
end_cursor = page_info["end_cursor"]
print(type(end_cursor))
print(end_cursor)