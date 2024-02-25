# CSC-519-DevOps-Pipeline

## Accomplishments

- Developed Ansible playbook for staging and production, including building the docker container for the coffee-project
- Built the docker container for running ansible playbooks
- Created a workflow for linting and formatting the coffee-project
- Set up self-hosted runner for our PR workflows
- Created a workflow for running the automated tests

[Corey's Commit](https://github.ncsu.edu/ashon/CSC-519-DevOps-Pipeline/pull/16/commits/c363aff08c58b0ce6001eb32df0a2f946ee4cc1e)

[Andrew's Commit](https://github.ncsu.edu/ashon/CSC-519-DevOps-Pipeline/pull/19/commits/d3b28080a02caf5e56d0f21a8b28083a69742e06)

[Isaac's Commit](https://github.ncsu.edu/ashon/CSC-519-DevOps-Pipeline/pull/18/commits/a2a812cc41ac8c6a3af87a18f38df8d11bd65b84)

## Next Steps

### Corey
- Test that browser can connect to coffee-project inside of VCL and docker
- Security ansible playbook

### Isaac
- Ansible playbook to deploy coffee-project to staging/production
- Add Deploy Github Actions Workflow - Staging

### Andrew
- Add branch protection rules in Github
- Add Deploy Github Actions Workflow - Production

## Retrospective

### What worked
- Setting up the Github Project Board, and creating issues to track progress
- Asynchronous chat room to provide constant communication
- Google meets to align on goals
- Creating pull requests for our work/deliverables
- Splitting up pipeline into sub-pipelines to make it easier to digest

### What didn't work
- It's sometimes too difficult to see what a particular script in a PR for example is doing without viewing a video or other piece of evidence
- Hosting a self-runner that works with a sub-module, since NCSU does not allow the basic, universal runners
- Being able to use third party Github Actions is strongly limited due to NCSU Github restrictions

### What to do differently
- Provide instructions/videos for scripts or deliverables that require further instruction/context
- Sharing details that would impact the team in a timely manner