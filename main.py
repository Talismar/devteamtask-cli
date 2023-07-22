#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import src.utils as utils
from src.client import get_projects, get_all_task_projects, mark_task_as_done
    
parser = ArgumentParser(
    prog="DevTeamTask",
    formatter_class=RawDescriptionHelpFormatter,
    description="""
----------------- DevTeamTask CLI ---------------
 A management task software for development team
-------------------------------------------------
    """,
    epilog="By Talismar F. C.",
)


parser.add_argument("--login", nargs=2, metavar="", type=str, help="enter the username and password", default=False)
parser.add_argument('-rt','--register-token', metavar="", help="register token for users as register by provider")
parser.add_argument("--version", action="version", version="1.0")
parser.add_argument('-td',"--task-done", metavar="", type=int, help="add task as done - add task id", default=False)


project_group = parser.add_argument_group(title="projects", description="Project operation")
project_group.add_argument(
    "-lp",
    "--list-projects",
    action="store_true",
    help="list the id and name of all the projects I'm a part of"
)
project_group.add_argument('-sp-in-cache','--set-project-id-in-cache', metavar="", help="set project id as default on cache system")
project_group.add_argument('-ltp','--list-task-project', metavar="", help="lists all tasks in a project")

args = parser.parse_args()
# print(args)

if args.register_token:
    utils.write_devteamtask_json("access_token", args.register_token)


if args.login:
    username = args.login[0]
    password = args.login[1]


if args.list_projects:
    projects = get_projects()

    if type(projects) == list:
        [print(project) for project in projects]
    else:
        print(projects)

if args.set_project_id_in_cache is not None:
    utils.write_devteamtask_json("cache", {"project_id": args.set_project_id_in_cache})

if args.list_task_project is not None:
    task_projects = get_all_task_projects(args.list_task_project)

    if type(task_projects) == list:
        [print(project) for project in task_projects]
    else:
        print(task_projects)


if args.task_done:
    result = mark_task_as_done(args.task_done)
    print(result)