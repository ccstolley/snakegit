     ____              _         ____ _ _   
    / ___| _ __   __ _| | _____ / ___(_) |_ 
    \___ \| '_ \ / _` | |/ / _ \ |  _| | __|
     ___) | | | | (_| |   <  __/ |_| | | |_ 
    |____/|_| |_|\__,_|_|\_\___|\____|_|\__|

(Walt, may the Snakes be with you)

This is a set of tools which (hopefully) simplify our
development process by standardizing the way we work and 
integrating more tightly with Python


Install
-----------------

To install from bash, run:

    bash <(curl https://raw.github.com/NarrativeScience/snakegit/master/bin/install.sh)

and answer all of the prompts. Note, that even though 
the installer asks for your github password, it is not
stored anywhere on your system. It is used one time to
acquire a github authorization token which is stored on
you system.


Git Aliases
-----------------

Most SnakeGit functionality is encapsulated as git aliases.
Having said this, all functions are simply scripts (sh
or python), which can be called directly, but it can be
convenient to just use the git aliases.

Here is a list of the current aliases provided by SnakeGit

* build          - build a Python project (install all of its
    dependencies locally)
* dev-clean      - clean up a Python project 
* gearbox        - run GearBox commands (more later)
* lint           - run Python linting tools
* pullreq        - Create a Github pull request
* upload-package - Upload a python package to our pypi server 
* sdist          - Create a source distribution for use with
    upload-package
* snakeupdate    - Update your SnakeGit package
* sphinx         - Generate Sphinx documentation
* test           - Run Python test and coverage tools

All of these tools are designed to be run from a project
directory. For example, if you are ready to upload ns_utils
to pypi you would issue the following commands:

    ~/src/ns_utils -) > git sdist
    ~/src/ns_utils -) > git upload-package

and the source distribution would be build and then uploaded
to the pypi server.


Conventions
==========================

SnakeGit is heavily dependent on conventions.  Not very many,
but if they are not followed, the results may be unexpected.

First and foremost, SnakeGit assumes that you have completed
its configuration process.  Details such as Github and PyPi
credentials and are pulled from the configuration files.  So,
please complete the configuration.

For Python projects, SnakeGit assumes that the project contains
a valid setup.py file and a requirements.txt.

The setup.py file should (minimally) specify the name and version
of the project.  This information is used extensively to create
metadata for various tasks.  Of course, other data can be included.
If you plan to use SnakeGit to generate Sphinx documentation, you
must also include the "provides" data, so that Sphinx knows which
packages it is going to generate docs for.

The requirements.txt file lists all of the build/run requirements for the
project.  The requirements file is a pip requirements formatted file.
It can be easily generated by executing

    ~/src/ns_utils -) > pip freeze > requirements.txt

from an environment which contains your dependencies.  After running this
command, you may want to review your requirements.txt file to make sure
that it hasn't included any test depedencies, for example.

On that note, requirements.txt should not include test requirements. If you
depend on libraries for running tests, they should be placed in a file called
test-requirements.txt which follows the same format of the requirements.txt.


Library Dependencies
---------------------

Python dependencies are managed via pip, as described above. In order to
simplify local development and to avoid being paralized by the central
PyPi server, SnakeGit caches all dependency source files locally. It is
expected that these will be added to Git. By default, all cached dependency
files are stored in "<project_dir>/vendor/cache".  The 'git snakeinit' task
will configure this directory to be stored.  

All dependencies are installed into a Virtualenv which is local to the project.
This Virtualenv is located, by default, in vendor/python. This should not be
stored in version control.  The 'git snakeinit' task will add this directory
to your project's .gitignore file so that they won't be stored.


Task Documentation
==========================


git build
---------------------

Creates a Virtualenv in `pwd`/vendor/python, then installs the requirements as
defined by the requirements.txt


git dev-clean
--------------------

Remove all build artifacts as well as the local Virtualenv


git gearbox
-------------------

This will be documented elsewhere


git lint
------------------

Run various linting tools against the current project.  Currently, this supports
PyLint, Pep8 and PyFlakes. The options are as follows:

    Usage: lint.sh
    -l              Run PyLint
    -p              Run Pep8
    -f              Run PyFlakes
    -s=value        Lint the specified src directory
    -o=dirctory     Write to the specified output directory
    -m=value        Module to lint

Some linters require the directory to be set and others require the module. To
be safe, you can supply both the -s and -m options like this:

    ~/src/ns_utils -) > git lint -l -s src -m pypi

This will run PyLint on the pypi module in the ./src directory 


git pullreq
--------------------------

Creates a GitHub pull request for the currently checked out branch.
The convention relied upon by the pullreq command is that local and remote
branches have the same name.

    optional arguments:
      -h, --help      Show a help message and exit.
      --title TITLE   Pull request title. Required.
      --body  BODY    Pull request description. Required.
      --base  BRANCH  Branch to create the pull request against. Optional,
                  defaults to master.
      --no-push       Do not perform a push before creating the pull request.
                  The default behaviour is to push the local branch to a
                  remote branch with the same name.
      --list-members  List members of the organization NarrativeScience and exit.
                  This list will contain valid values for the --to argument.
      --to JOE,ED     Comma-seperated list of pull request recipients. Required,
                  recipients must be members of the NarrativeScience
                  organization.

example run:

    git pullreq --title 'print url for created pull request' \
            --body 'print url for created pull request' \
            --to turtlebender,waltaskew \
    Counting objects: 7, done.
    Delta compression using up to 2 threads.
    Compressing objects: 100% (4/4), done.
    Writing objects: 100% (4/4), 487 bytes, done.
    Total 4 (delta 3), reused 0 (delta 0)
    To git@github.com:NarrativeScience/snakegit.git
    * [new branch]      feature/printurl -> feature/printurl
    created pull request at https://github.com/NarrativeScience/snakegit/pull/10

This command was issued from the local branch feature/printurl,
and thus created a remote branch of the same name.

It then created a pull request for this new remote branch against remote master.
turtlebender and waltaskew were notified of the pull request using the
@name syntax in the pull request description.

The url for the new GitHub pull request was then printed out.


git sdist
-------------------------

Simply calls python setup.py sdist in the current environment


git snakeupdate
------------------------

Updates your SnakeGit install.  Doesn't take any options, but might
require additional configuration.


git snakeinit
-----------------------

Configure a git project for use with SnakeGit.  Configures .gitignores
and vendor cache directories


git sphinx
-----------------------

Generate Sphinx documentation (including apidocs).  Currently, requires
a `pwd`/docs/source directory to exist and contain the conf.py for Sphinx


git test
----------------------

Run a set of Python tests with optional coverage checks.  The usage is:

    test [options]

    -h                    Show this message
    -x                    Generate an XUnit compatible report
    -c                    Generate a test coverage report
    -p=<pkg>              Which package should have coverage measured
    -w=<dir>              Which directory holds the tests


git upload
--------------------

Upload the project to our PyPi server.  This requires that you have already
run git sdist
