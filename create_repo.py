from github import Github
import time
import os


def get_user():
    Token_for_aa = "1798a0271a97a8ebc0df51d7fc6822c257755bdd"
    # Token = "a625ce0d9bcc8e0ec9e58ac9d0dd5638815aaea6"
    g = Github(Token_for_aa)
    user = g.get_user()
    print(user)
    return user, g

def add_file_to_repo(repo, repo_path, file_to_add):
    max_retries = 3
    retry_count = 1

    while retry_count <= max_retries:
        if retry_count > 1:
            print("File addition failed, retrying for %s time"%(retry_count))
            sleep_seconds = retry_count * 60
            time.sleep(sleep_seconds)
        
        try:
            print("Adding %s to repo %s" %(file_to_add, repo))
            fp = open(os.path.join(repo_path, file_to_add), 'r')
            file_content = fp.read()
            # 1->filename 2->commit message 3-> file_content
            repo.create_file(file_to_add, "initial commit", file_content , branch="master")
            print("File %s added successfully" %(file_to_add))
            break
        except Exception as ex:
            print("Exception encountered : %s"%(str(ex)))
            retry_count = retry_count + 1
            continue


def create_remote_repo(repo_name):
    user, g = get_user()
    org = g.get_organization('azureautomation')

    try:
        repo = org.get_repo(repo_name)
        print(repo)
    except Exception as ex:
        if(str(ex).startswith('404')):
            # create if not present
            repo = org.create_repo(repo_name)
            print("no repo found")
        else:
            raise ex
    
    repo_path = os.path.join(os.getcwd(), repo_name)

    onlyfiles = [f for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))]
    for f in onlyfiles:
        add_file_to_repo(repo, repo_path, f)


# dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]

# for directory in dirs:
#     create_remote_repo(directory)

dir_path = os.path.join(os.getcwd(), "test")

# user, g = get_user()
# org = g.get_organization('azureautomation')
# repo = org.get_repo('test-kranthi')
# fp = open(os.path.join(os.getcwd(), "test", "test2.py"))
# file_content = fp.read()
# create_file = repo.create_file("test2.py", "initial commit", file_content, branch="master")
# print("File created --- %s" %(str(create_file)))