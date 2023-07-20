import os

command = "git branch --merged"
output = os.popen(command).read()

branches = output.strip().split("\n")

for branch in branches:
    branch_name = branch.strip().lstrip("*")
    if branch_name != "main":
        delete_command = f"git branch -d {branch_name}"
        os.system(delete_command)
        print(f"Deleted branch: {branch_name}")