from requests import Response, get, patch, post

from .utils import get_data_json, write_devteamtask_json

API_URL: str = ""
with open(".env") as envFile:
    API_URL = envFile.readline().split("API_URL=")[1]
    envFile.close()


def get_auth_token(email: str, password: str) -> Response:
    data = {"email": email, "password": password}

    response = post(url=f"{API_URL}/user/authentication/token", data=data)

    if response.status_code == 200:
        write_devteamtask_json("access_token", response.json().get("access_token"))
        write_devteamtask_json("refresh_token", response.json().get("refresh_token"))

    return response.json()


def refresh_token():
    refresh_token = get_data_json("refresh_token")

    if refresh_token is not None:
        data = {"refresh_token": refresh_token}

        response = post(url=f"{API_URL}/user/authentication/refresh_token", data=data)

        if response.status_code == 200:
            write_devteamtask_json("access_token", response.json().get("access_token"))
            write_devteamtask_json(
                "refresh_token", response.json().get("refresh_token")
            )


def get_projects():
    token = get_data_json("access_token")

    projects_data: list[dict] = []

    response = get(
        url=f"{API_URL}/project/project",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    if response.status_code != 200:
        return response.json()

    for item in response.json().get("projects"):
        projects_data.append(f"{item['id']} | {item['name']}")

    return projects_data


def get_all_task_projects(projectId: str):
    token = get_data_json("access_token")

    task_projects: list[dict] = []

    if projectId == "use-cache":
        try:
            projectId = get_data_json("cache")["project_id"]
        except KeyError:
            pass

    response = get(
        url=f"{API_URL}/project/project/{projectId}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    if response.status_code != 200:
        if response.status_code == 401:
            refresh_token()

        return response.json()

    for item in response.json()["project_data"]["tasks"]:
        task_projects.append(
            f"id: {item['id']} | status: {item['status']['name']} | name: {item['name']}"
        )

    return task_projects


def get_all_status_id_done_by_project(projectId: str):
    token = get_data_json("access_token")

    if projectId == "use-cache":
        try:
            projectId = get_data_json("cache")["project_id"]
        except KeyError:
            pass

    response = get(
        url=f"{API_URL}/project/project/{projectId}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    if response.status_code != 200:
        if response.status_code == 401:
            refresh_token()

        return response.json()

    for item in response.json()["project_data"]["status"]:
        if item["name"] == "Done":
            return item["id"]


def mark_task_as_done(taskId: str):
    token = get_data_json("access_token")
    cache = get_data_json("cache")

    if "status_id" in cache:
        status_id = cache["status_id"]

        response = patch(
            url=f"{API_URL}/project/task/{taskId}",
            json={"status_id": status_id},
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        if response.status_code != 200:
            return response.json()

        return "Task marked as completed successfuly"

    return "Error when trying to mark a task as ready"
