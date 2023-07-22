from requests import post, get, Response, patch
from .utils import write_devteamtask_json, get_data_json


API_URL: str = ""
with open(".env") as envFile:
    API_URL = envFile.readline().split("API_URL=")[1]
    envFile.close()


def get_auth_token(username: str, password: str) -> Response:
    data = {"username": username, "password": password}

    response = post(url=f"{API_URL}/auth-token/", data=data)

    if response.status_code == 200:
        write_devteamtask_json("access_token", response.json()["token"])

    return response.json()


def get_projects():
    token = get_data_json("access_token")
    
    projects_data: list[dict] = []

    response = get(
        url=f"{API_URL}/projects",
        headers={
            "Authorization": f"Token {token}",
        },
    )
    
    if response.status_code != 200:
        return response.json()
    
    for item in response.json():
        projects_data.append(f"{item['id']} | {item['name']}")

    return projects_data

def get_all_task_projects(projectId: str):
    token = get_data_json("access_token")
    
    task_projects: list[dict] = []

    if projectId == 'use-cache':    
        try:
            projectId = get_data_json("cache")['project_id']
        except KeyError:
            pass


    response = get(
        url=f"{API_URL}/projects/{projectId}/?fields=tasks_set",
        headers={
            "Authorization": f"Token {token}",
        },
    )
    
    if response.status_code != 200:
        return response.json()
    
    for item in response.json()['tasks_set']:
        task_projects.append(f"id: {item['id']} | status: {item['status']['name']} | name: {item['name']}")

    return task_projects


def mark_task_as_done(taskId: str):
    token = get_data_json("access_token")
    

    response = patch(
        url=f"{API_URL}/tasks/{taskId}/",
        data={"status": 3},
        headers={
            "Authorization": f"Token {token}",
        },
    )
    
    if response.status_code != 200:
        return response.json()
    
    return "Task marked as completed successfuly"

# print(get_auth_token("talismar", "admin123"))
# print(get_projects())
