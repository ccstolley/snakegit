#!/bin/sh

function git_new_feature(){
    FEATURE_NAME=$1;
    if [ "x$FEATURE_NAME" == "x" ]; then
    echo "usage: git snake feature-branch <featurename>";
    return 1;
    fi
    git checkout develop;
    DEVELOP_CHECK=$?;
    if [ $DEVELOP_CHECK -ne 0 ]; then
    echo "Couldnt checkout develop branch... bailing";
    return 1;
    fi
    git pull;
    PULL_CHECK=$?;
    if [ $PULL_CHECK -ne 0 ]; then
        echo "Couldnt update/pull develop branch... bailing";
    return 1;
    fi
    FEATURE_BRANCH="feature/${FEATURE_NAME}";

    git checkout -b $FEATURE_BRANCH;
    git push origin $FEATURE_BRANCH;
    git branch --set-upstream $FEATURE_BRANCH  origin/$FEATURE_BRANCH;
}


function git_new_release(){
    RELEASE_NAME=$1;
    if [ "x$RELEASE_NAME" == "x" ]; then
    echo "usage: git snake release-branch <release-tag>";
    return 1;
    fi
    git checkout develop;
    DEVELOP_CHECK=$?;
    if [ $DEVELOP_CHECK -ne 0 ]; then
    echo "Couldnt checkout develop branch... bailing";
    return 1;
    fi
    git pull;
    PULL_CHECK=$?;
    if [ $PULL_CHECK -ne 0 ]; then
        echo "Couldnt update/pull develop branch... bailing";
    return 1;
    fi
    RELEASE_BRANCH="release/${RELEASE_NAME}";

    git checkout -b $RELEASE_BRANCH;
    git push origin $RELEASE_BRANCH;
    git branch --set-upstream $RELEASE_BRANCH  origin/$RELEASE_BRANCH;
}


function git_follow_develop(){
    #
    # util to locally follow the develop branch
    #
    git checkout --track -b develop origin/develop
}


function git_merge_develop(){
    #
    # merge a feature or release branch into develop
    #
    BRANCH_NAME=$1;
    if [ "x$BRANCH_NAME" == "x" ]; then
    echo "usage: git snake branch-merge <branch-name>";
    return 1;
    fi
    git checkout develop;
    DEVELOP_CHECK=$?;
    if [ $DEVELOP_CHECK -ne 0 ]; then
    echo "Couldnt checkout develop branch... bailing";
    return 1;
    fi
    git pull;
    PULL_CHECK=$?;
    if [ $PULL_CHECK -ne 0 ]; then
        echo "Couldnt update/pull develop branch... bailing";
    return 1;
    fi
    git merge --no-ff $BRANCH_NAME
    git push
}

function git_merge_release(){
    #
    # merge develop into the master branch and tag a release
    #
    RELEASE_TAG=$1;
    if [ "x$RELEASE_TAG" == "x" ]; then
        echo "usage: git snake merge-release <TAG>";
        return 1;
    fi
    # check develop is pulled and up to date
    git checkout develop
    git checkout pull
    git checkout master
    MASTER_CHECK=$?;
    if [ $MASTER_CHECK -ne 0 ]; then
    echo "Couldnt checkout master branch... bailing";
    return 1;
    fi
    git pull
    PULL_CHECK=$?;
    if [ $PULL_CHECK -ne 0 ]; then
        echo "Couldnt update/pull master branch... bailing";
    return 1;
    fi
    git merge --no-ff develop
    git push
    git tag -a $RELEASE_TAG
    git push --tags
}

