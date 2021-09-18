import json, os


def append_new_data(model_data, file):
    f = open(file, encoding="utf-8", mode='r+')
    data = json.load(f)
    # d = []
    count = 0
    for j in model_data:
        count=0
        for i in data:
            if j.user_say in i['message'] and j.response in i['response']:
                count+=1
        if count==0:
            data.append({"message": j.user_say, "response":j.response})

    f.seek(0)
    json.dump(data, f, indent=2)

def append_new_intent(model_data, file):
    f = open(file, encoding="utf-8", mode='r+')
    data = json.load(f)
    count = 0
    for j in model_data:
        count=0
        for i in data:
            if j['message'] in i['message'] and j['response'] in i['response']:
                count+=1
        if count==0:
            data.append({"message": j['message'], "response":j['response']})

    f.seek(0)
    json.dump(data, f, indent=2)
