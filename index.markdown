---
layout: page
no_sidebar: true
---

Overview
=================

This is a proposal to the workflow for snakegit to use to facilitate a common set of workflow steps and consistency in branching, releasing, etc.

The stages of the workflow were determined to be the following

* work on a feature or a bug fix
* request a code review of the work
* possibly update the code from comments in the review
* finish the work and publish it
* lather, rinse repeat

A closely related workflow is to create and deploy a release.  The steps in that workflow are as follows

* cut a release candidate
* deploy a release candidate
* test the release candidate
* possibly update the release candidate based on test results
* release the release candidate
* deploy the release
* enjoy a frosty beverage

Below, we represent this flow in all of it's graphical goodness.

![workflow](/images/daily_workflow.png)

Hopefully, these workflow steps line up with the way most people are working today.

Having codified the steps at the high level, the next challenge was to translate these steps into actual actions that need to be taken at the git/server level.
Along with this we also tried to come up with good command names for the workflow steps.  Our standards for these names were (in no particular order):

* lack of ambiguity
* minimal length
* maximum flexibility



![git_view](/images/git_view.png)


Proposed snake commands:

### snake workon <feature>

Either start or continue work on a feature or bug branch.  If the feature branch does not exists, this will create a new branch off of master and create a tracking branch. If the branch does exist, this switches to that branch.

If the branch is named after a Jira item or has the --jira flag, this will update the issue in jira automatically



Example Usage:

snake workon automate_nginx_config
snake workon inf-213
snake workon automate_nginx_config --jira inf-213

Alternative Command:
snake feature start <feature>
snake mk_branch <feature>

### snake request-review

Submit a request for a review.  This should push the branch and submit the pull request to the specified user. If no branch is specified, this will issue a request for the current branch

Example Usage:


snake request-review 
snake request-review --feature <featurename>
snake request-review --reviewer <reviewer name>

Alternative Command:

snake pull-request

### snake review [approve,reject]

Mark a review as completed.  If the review is rejected, it must supply comments.  If the review is approved, it will tag and push the branch.

Example Usage:

snake review approve
snake review reject -m “comment”

### snake finish

Finish working on a feature/bug branch.  This will assume that a review tag is present.  It will then merge the branch into master and push master to github.  It will make sure that all branches are up to date with the remote server before pushing/pulling.


Example Usage:

snake promote

Alternative Command:

snake feature complete
snake release complete


