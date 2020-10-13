from github import Github
import os


def get_user():
    Token_for_aa = "1798a0271a97a8ebc0df51d7fc6822c257755bdd"
    Token = "a625ce0d9bcc8e0ec9e58ac9d0dd5638815aaea6"
    g = Github(Token)
    user = g.get_user()
    return user

def create_remote_repo(repo_name):
    user = get_user()

    try:
        repo = user.get_repo(repo_name)
    except Exception as ex:
        if(str(ex).startswith('404')):
            # create if not present
            repo = user.create_repo(repo_name)
        else:
            raise ex
    
    repo_path = os.path.join(os.getcwd(), repo_name)

    onlyfiles = [f for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))]
    for f in onlyfiles:
        print("adding %s to repo " %(f))
        fp = open(os.path.join(repo_path, f), 'r')
        file_content = fp.read()
        # 1->filename 2->commit message 3-> file_content
        create_file=repo.create_file(f, "initial commit", file_content , branch="master")
        print("File created --- %s" %(str(create_file)))


dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]

for directory in dirs:
    create_remote_repo(directory)