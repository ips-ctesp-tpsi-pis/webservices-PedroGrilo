"""
 Basic webservice application

"""
# -*- coding: utf-8 -*-

import json

USERS = [
    {
        "id": 1,
        "name": "Ana",
        "age": 22,
    },
    {
        "id": 2,
        "name": "Paulo",
        "age": 25,
    }
]


def httpOk(req):
    json_string = json.dumps(req, ensure_ascii=False).encode('utf8')
    return {
        'status': '200 OK',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json_string.decode(),
    }


def httpFail(body):
    return {
        "status": "404 NotFound",
        "headers": {},
        "body": body
    }


def parse_request(request):
    try:
        if request['url'] == '/users/' or request['url'] == '/users':
            return httpOk(USERS)
        elif "/users/" in request['url']:
            x = request['url'].split("/")
            founded = False
            for usr in USERS:
                if usr.get("id") == int(x[2]):
                    founded = True
                    return httpOk(usr)
            if not founded:
                print("User not found")
                return httpFail("User not found")
        else:
            raise Exception()
    except:
        return httpFail("404 Not found")


def deleteUser(request):
    try:
        x = request['url'].split("/")
        for i in range(len(USERS)):
            if USERS[i]['id'] == int(x[2]):
                del USERS[i]
                break
        return httpOk("Deleted")
    except:
        return httpFail("Error")


def updateUser(request):
    try:
        x = request['url'].split("/")
        for i in range(len(USERS)):
            if USERS[i]['id'] == int(x[2]):
                jsonUsers = json.loads(request['body'])
                USERS[i].update(jsonUsers)
                break
        return httpOk("Updated successfully")
    except Exception as e:
        error = "Error : " + str(e)
        return httpFail(error)


def controller(request):
    print(request)
    if request["method"] == "GET":
        return parse_request(request)
    elif request["method"] == "POST":
        USERS.append((json.loads(request['body'])))
        return httpFail("User added successfully")
    elif request["method"] == "DELETE":
        return deleteUser(request)
    elif request["method"] == "PUT":
        return updateUser(request)
    else:
        return httpFail("Method unavailable")
