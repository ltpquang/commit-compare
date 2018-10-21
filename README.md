# Commit Compare

This Python script try to inspect 2 Git branches and list out which commits represent in  branch but not in the other.

### Requirement

[GitPython](https://github.com/gitpython-developers/GitPython) is required

```
$  pip install gitpython
```

### Before running

Make sure both branches you want to check is up to date to remote repo.

### Running

```
$  ./rlscm.py <branch_A> <optional_branch_B>
```
The above command will find out which commit represent in `branch_A` but not in `branch_B`, if `branch_B` is not specified, `master` branch will be used instead.