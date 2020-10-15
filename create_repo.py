from github import Github
import time
import os

class Github_Helper:
    def __init__(self):
        self.user_krmanupa = None
        self.user_for_aa_org = None
        self.github_accessor_for_aa_org = None
        self.github_accessor_for_krmanupa = None
        self.org_name = "azureautomation"
        self.Token_for_aa_org = "" #replace while using
        self.Token_for_krmanupa = "" #replace while using

    def init_org_github_acc(self):
        if self.github_accessor_for_aa_org == None and self.user_for_aa_org == None:
            self.github_accessor_for_aa_org = Github(self.Token_for_aa_org)
            self.user_for_aa_org = self.github_accessor_for_aa_org.get_user()

    def init_user_github_acc(self):
        if self.github_accessor_for_krmanupa == None and self.user_krmanupa == None:
            self.github_accessor_for_krmanupa = Github(self.Token_for_krmanupa)
            self.user_krmanupa = self.github_accessor_for_krmanupa.get_user()
    
    def add_file_to_repo(self, repo, repo_path, file_to_add):
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
    
    def create_remote_repo_user_level(self, repo_name):
        self.init_user_github_acc()

        try:
            repo = self.user_krmanupa.get_repo(repo_name)
            print(repo)
        except Exception as ex:
            if(str(ex).startswith('404')):
                # create if not present
                print("Repo not found under user 'krmanupa' creating new repo named %s" %(repo_name))
                repo = self.user_krmanupa.create_repo(repo_name)
            else:
                raise ex
        
        repo_path = os.path.join(os.getcwd(), repo_name)

        onlyfiles = [f for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))]
        for f in onlyfiles:
            self.add_file_to_repo(repo, repo_path, f)

    def create_remote_repo(self, repo_name):
        self.init_org_github_acc()
        org = self.github_accessor_for_aa_org.get_organization(self.org_name)

        try:
            repo = org.get_repo(repo_name)
        except Exception as ex:
            if(str(ex).startswith('404')):
                # create if not present
                print("Repo not found under org creating new repo named %s" %(repo_name))
                repo = org.create_repo(repo_name)
            else:
                raise ex
        
        repo_path = os.path.join(os.getcwd(), repo_name)

        onlyfiles = [f for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))]
        for f in onlyfiles:
            self.add_file_to_repo(repo, repo_path, f)

dirs = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f) and f != ".git"]

github_helper = Github_Helper()
for directory in dirs:
    github_helper.create_remote_repo_user_level(directory)

# user, g = get_user()
# org = g.get_organization('azureautomation')
# repo = org.get_repo('test-kranthi')
# fp = open(os.path.join(os.getcwd(), "test", "test2.py"))
# file_content = fp.read()
# create_file = repo.create_file("test2.py", "initial commit", file_content, branch="master")
# print("File created --- %s" %(str(create_file)))
