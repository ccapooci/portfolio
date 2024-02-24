# CSC-519-DevOps-Pipeline

## Accomplishments
- Added security Ansible playbook for initial manual setup of VCLs, removing unnecessary packages and updating old ones
- Researched and tested how to connect to the coffee-project within the Docker container, enabling VCL port 80 and exposing port 3000 on the docker container and direct traffic from 80 to 3000
- Implemented GH Actions workflow that deploys the coffee-project to staging.
- Created workflow to run the coffee-project within a docker container.
- Set up branch protection rules where code linting and automated tests need to pass prior to merging a pull request and require pull request to merge into develop and main

[Corey's Commit](https://github.ncsu.edu/ashon/CSC-519-DevOps-Pipeline/pull/26/commits/603d92f228d1e017c9e164b26f3c9146a19fbe4d)

[Andrew's Commit](https://github.ncsu.edu/ashon/CSC-519-DevOps-Pipeline/pull/29/commits/798a0195f0c2b119b614c74cf40d551beee6b2be)

[Isaac's Commit](https://github.ncsu.edu/ashon/CSC-519-DevOps-Pipeline/commit/75cfa0662d3309130da5ac9f7eeb3f41ce27c335)

## Additional Project Scope
- Add Security Ansible Playbook to remove/update relevant packages for staging and production
- Build a feature to add application rollback for the coffee-project. This would an engineer to rollback a broken release to a working version using a GitHub action.
- Add a GitHub action to calculate the code coverage of the test suite.
- Add performance analysis for the staging and production coffee-projects. The performance analysis will measure the launch response time of the coffee-project app in both stages of the DevOps pipeline. 

## Next Steps

### Corey
- Work with Isaac to investigate/implement security features, such as a secrets scanner and CVE scanner. 
- Add performance testing for the coffee-project in the staging and production environments. This would allow us to compare the performance of the releases.

### Isaac
- Pair program to create a GitHub action to automate rollback for the coffee-project. This would allow us to rollback a broken release to a working version. 
- Work with Corey to investigate/implement security features, such as a secrets scanner and CVE scanner. 

### Andrew
- Pair program to create a GitHub action to automate rollback for the coffee-project. This would allow us to rollback a broken release to a working version. 
- Add a GitHub action to calculate the code coverage of the test suite.

## Retrospective

### What worked
- Pair programming- We gain a lot of context in a session so it eliminates the need for knowledge transfer between individuals. In addition, it helps to get rid of blockers a lot faster instead of thinking in our own heads.
- Working on features proactively rather than close to the deadline. It allowed the resolving of issues/blockers early.
- Referencing the demo video for Ansible setups (by Corey) has been super helpful for us to reproduce on our own machines.

### What didn't work
- Communications were not received promptly due to our google chat notification settings. This caused a delay in response.
- There was trouble connecting to our VCL from Github Actions. We overcomplicated the workflow for deployment by testing merges into main and develop to test event triggers and conditions, which was time consuming.

### What to do differently
- For future meetings/work sessions, be open to communication channels in case a response is needed from one another.
- Alert in advanced future meetings/work sessions.
