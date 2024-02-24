// Started with https://github.ncsu.edu/CSC-510/Mocking/test/testMain.js

const chai = require("chai");
const expect = chai.expect;
const nock = require("nock");
const { kill } = require("process");

const github = require("../src/github.js");

// Load mock data
const mockData = require("../mockGithub.json")
const GITHUB_API_URL = "https://github.ncsu.edu/api/v3";

//////////////////////////////
// TEST SUITE FOR GITHUB TOOL
//////////////////////////////
describe('testGithub()', function () {
    describe('#createRepo()', function () {
        const mock = nock(GITHUB_API_URL)
            .persist()
            .post("/user/repos")
            .reply(200, JSON.stringify(mockData.createRepo));

        it('should return the correct repo name', async function () {
            let repoName = "testrepo";
            let testToken = "token";
            let returnData = await github.createRepo(repoName, testToken);

            expect(returnData.data.name).to.equal(repoName);
        });
    });

    describe('#updateFile()', function () {
        let repoName = "testrepo";
        let user = "testuser";
        let fileName = "README.md";
        let contents = "contents";
        let commitMessage = "commit message";
        let branch = "main";
        let blobSha = "sha";
        let testToken = "token";
        var mock = nock(GITHUB_API_URL)
            .persist()
            .put("/repos/testuser/testrepo/contents/README.md")
            .reply(200, JSON.stringify(mockData.updateFile));

        it('return the correct filename', async function () {
            let returnData = await github.updateFile(repoName, user, fileName, blobSha, contents, commitMessage, branch, testToken);

            expect(returnData.data.content.path).to.equal(fileName);
        });
    });

    describe('#addCollaborator()', function () {
        let invitee = "invitee";
        let owner = "testuser";
        let repoName = "testrepo";
        let testToken = "token";
        const mock = nock(GITHUB_API_URL)
            .persist()
            .put("/repos/" + owner + "/" + repoName + "/collaborators/" + invitee)
            .reply(200, JSON.stringify(mockData.addCollaborator));

        it('should return the correct invitee user name', async function () {
            let returnData = await github.addCollaborator(repoName, owner, invitee, testToken);

            expect(returnData.data.invitee.login).to.equal(invitee);
        });
    });

    describe('#forkRepo()', function () {
        let owner = "testuser";
        let repoName = "testrepo";
        let testToken = "token";
        const mock = nock(GITHUB_API_URL)
            .persist()
            .post("/repos/" + owner + "/" + repoName + "/forks")
            .reply(202, JSON.stringify(mockData.forkRepo));

        it('should return the correct fork JSON data', async function () {
            let returnData = await github.forkRepo(repoName, owner, testToken);

            expect(returnData.data.parent.owner.login).to.equal(owner);
            expect(returnData.data.name).to.equal(repoName);
            expect(returnData.data.parent.full_name).to.equal(owner+"/"+repoName);
        });
    });

    describe('#createFile()', function () {
        let repoName = "Hello-World";
        let user = "octocat";
        let fileName = "notes/hello.txt";
        let contents = "contents";
        let commitMessage = "commit message";
        let branch = "main";
        let testToken = "token";
        var mock = nock(GITHUB_API_URL)
            .persist()
            .put("/repos/octocat/Hello-World/contents/notes/hello.txt")
            .reply(200, JSON.stringify(mockData.createFile));

        it('return the correct filename', async function () {
            let returnData = await github.createFile(repoName, user, fileName, contents, commitMessage, branch, testToken);

            expect(returnData.data.content.path).to.equal(fileName);
        });
    });

    describe('#getUser()', function () {
        let testToken = "token";
        var mock = nock(GITHUB_API_URL)
            .persist()
            .get("/user")
            .reply(200, JSON.stringify(mockData.getUser));

        it('return the correct user', async function () {
            let returnData = await github.getUser(testToken);

            expect(returnData.data.login).to.equal("octocat");
        });
    });

    describe('#getBlobInfo()', function () {
        let testToken = "token";
        let repoName = "testrepo";
        let user = "testuser";
        let filePath = "README.md";
        var mock = nock(GITHUB_API_URL)
            .persist()
            .get("/repos/"+ user +"/"+ repoName + "/contents/" + filePath)
            .reply(200, JSON.stringify(mockData.getBlobInfo));

        it('return the correct user', async function () {
            let returnData = await github.getBlobInfo(repoName, user, filePath, testToken);

            expect(returnData.data.path).to.equal(filePath);
        });
    });
});