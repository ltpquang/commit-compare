import os
import sys
import codecs
import copy
import time

########
# Install gitpython before running
# $ - pip install gitpython
from git import Repo 

def get_id(commit):
    return 
    return u"{} by {}".format(commit.summary, commit.author.name)

def build_dict(ids):
    result = {}
    for id in ids:
        if "Bump" in id:
            continue
        if id in result:
            result[id] += 1
        else:
            result[id] = 1
    return result

def format_number_count(count):
    if count == 1:
        return "ONCE"
    elif count == 2:
        return "TWICE"
    else:
        return "{} TIMES".format(count)

def print_not_in_master(commit, count_in_branch, branch_name):
    print(u"/**")
    print(u" * " + commit.summary)
    print(u" *     by " + commit.author.name)
    print(u" *     represents {} in {}".format(format_number_count(count_in_branch), branch_name.upper()))
    print(u" *     but DOESN'T represent in MASTER")
    print(u" */\n")

def print_in_master_but_not_enough(commit, count_in_master, count_in_branch, branch_name):
    print(u"/**")
    print(u" * " + commit.summary)
    print(u" *     by " + commit.author.name)
    print(u" *     represents {} in {}".format(format_number_count(count_in_branch), branch_name.upper()))
    print(u" *     but represents {} in MASTER".format(format_number_count(count_in_master)))
    print(u" */\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: $ - python rlscm.py <branch_name>')
        exit(1)

    # Repo object used to programmatically interact with Git repositories
    repo_path = os.getcwd()
    repo = Repo(repo_path)
    
    # Check that the repository loaded correctly
    if repo.bare:
        print('Could not load repository')
        exit(1)

    branch_name = sys.argv[1]
    base_branch_name = "master" if len(sys.argv) < 3 else sys.argv[2]
    parent_commit = repo.merge_base(repo.branches['{}'.format(base_branch_name)], repo.branches['{}'.format(branch_name)])[0]
    parent_hex = parent_commit.hexsha

    branch_commits = list(repo.iter_commits('{}...{}'.format(branch_name, parent_hex)))
    branch_summaries = map(lambda commit: commit.summary, branch_commits)
    branch_summaries_count_dict = build_dict(branch_summaries)

    master_commits = list(repo.iter_commits('{}...{}'.format(base_branch_name, parent_hex)))
    master_summaries = map(lambda commit: commit.summary, master_commits)
    master_summaries_count_dict = build_dict(master_summaries)

    print(" * * *")
    print(" * ")
    print(" *    Compare {} and {}".format(branch_name.upper(), base_branch_name.upper()))
    print(" *    from mutual ancestor {} - {}".format(parent_hex, parent_commit.summary))
    print(" * ")
    print(" * * * * * * * * * * * *\n")
    time.sleep(2)
    for key in branch_summaries_count_dict:
        if key not in master_summaries_count_dict:
            print_not_in_master(next(x for x in branch_commits if x.summary == key), branch_summaries_count_dict[key], branch_name)
        elif branch_summaries_count_dict[key] != master_summaries_count_dict[key]:
            print_in_master_but_not_enough(next(x for x in branch_commits if x.summary == key), master_summaries_count_dict[key], branch_summaries_count_dict[key], branch_name)
    time.sleep(1)
    print(" * * *")
    print(" * ")
    print(" *    All done!")
    print(" * ")
    print(" * * * * * * * * * * * *\n")