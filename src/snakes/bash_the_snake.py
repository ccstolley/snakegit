import os.path

profile_d = """
# in your project directory call snakeskin to activate
function snakeskin()
{
    export OLDPATH=$PATH
    if [ -f snake.cfg ]
    then
        test -f vendor/python/bin/activate || git snake build
        source vendor/python/bin/activate
        export PATH=$PATH:~/.snakegit/bin
    else
        echo "Not a Snakegit Project"
    fi
}

# when you are done call shed to deactivate the virtualenv
# to return your previous environment
function shed()
{
    deactivate > /dev/null 2>&1 ; true
    export PATH=$OLDPATH
}

export PATH=$PATH:~/.snakegit/bin:$SNAKEGIT_HOME
"""

profile_string = "for i in ~/.profile.d/* ; do source $i ; done"

def main():
    """docstring for main"""
    if not os.path.exists(os.path.expanduser('~/.profile.d')):
        print "~/.profile.d/ created"
        os.mkdir(os.path.expanduser('~/.profile.d'))
    with open(os.path.expanduser('~/.profile.d/snakegit.rc'), 'w') as handle:
       handle.write(profile_d) 
    # If ~/.bash_profile exists, .profile won't get read, so better check
    file_to_write = os.path.expanduser('~/.bash_profile')
    if not os.path.exists(file_to_write):
        file_to_write = os.path.expanduser('~/.profile')
    with open(os.path.expanduser('~/.profile'), 'r') as handle:
        append_to_profile = not profile_string in handle.read()

    if append_to_profile:
        with open(os.path.expanduser('~/.profile'), 'a') as handle:
            handle.write(profile_string)

    print """Your ~/.profile has been updated to include the snake functions.
To use these changes right now call

    source ~/.profile

    """

if __name__ == '__main__':
    main()
