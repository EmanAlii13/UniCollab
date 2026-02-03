import argparse

from app.services.project_service import ProjectService


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    create = sub.add_parser("create-project")
    create.add_argument("--title")
    create.add_argument("--desc")
    create.add_argument("--leader")

    join = sub.add_parser("join-project")
    join.add_argument("--project-id")
    join.add_argument("--user-id")

    approve = sub.add_parser("approve-request")
    approve.add_argument("--project-id")
    approve.add_argument("--user-id")

    args = parser.parse_args()
    service = ProjectService()

    if args.command == "create-project":
        pid = service.create_project(args.title, args.desc, args.leader)
        print(pid)

    elif args.command == "join-project":
        print(service.request_join(args.project_id, args.user_id))

    elif args.command == "approve-request":
        print(service.approve_request(args.project_id, args.user_id))


if __name__ == "__main__":
    main()


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    create = sub.add_parser("create-project")
    create.add_argument("--title")
    create.add_argument("--desc")
    create.add_argument("--leader")

    join = sub.add_parser("join-project")
    join.add_argument("--project-id")
    join.add_argument("--user-id")

    approve = sub.add_parser("approve-request")
    approve.add_argument("--project-id")
    approve.add_argument("--user-id")

    args = parser.parse_args()
    service = ProjectService()

    if args.command == "create-project":
        pid = service.create_project(args.title, args.desc, args.leader)
        print(pid)

    elif args.command == "join-project":
        print(service.request_join(args.project_id, args.user_id))

    elif args.command == "approve-request":
        print(service.approve_request(args.project_id, args.user_id))


if __name__ == "__main__":
    main()
