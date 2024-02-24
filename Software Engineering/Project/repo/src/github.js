// Started with https://github.ncsu.edu/CSC-510/Mocking/github.js

const axios = require('axios');
const urlRoot = "https://github.ncsu.edu/api/v3";


// Taken from https://github.ncsu.edu/CSC-510/REST/blob/main/index.js
function getDefaultOptions(endpoint, method, token) {
	var options = {
		url: urlRoot + endpoint,
		method: method,
		headers: {
			"User-Agent": "CSC510-REST-WORKSHOP",
			"content-type": "application/json",
			"Authorization": `token ${token}`
		}
	};
    return options;
}

async function getUser(token)
{
	let options = getDefaultOptions("/user", "GET", token);
	
	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				resolve(response);
		});
	});
}

async function createRepo(repo, token)
{
	// GitHub documentation for creation a repo.
	// https://docs.github.com/en/enterprise-server@3.3/rest/reference/repos#create-a-repository-for-the-authenticated-user
	let options = getDefaultOptions("/user/repos", "POST", token);
    options.data = { name      :  repo,
                     auto_init : "true" }

	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				// https://github.com/axios/axios
                resolve(response);
		});	
	});
};

async function updateFile(repoName, user, fileName, fileShaBlob, contents, commitMessage, branchName, token) {
    // Github documentation for updating a particular file.
    // https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents
	let options = getDefaultOptions("/repos/" + user + "/" + repoName + "/contents/" + fileName, "PUT", token);
    let base64 = Buffer.from(contents).toString("base64")
    options.data = {
        message: commitMessage,
        content: base64,
        branch: branchName,
        sha: fileShaBlob
    };

	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				// https://github.com/axios/axios
                resolve(response);
		});	
	});
}

async function getBlobInfo(repoName, user, filePath, token) {
	let options = getDefaultOptions("/repos/"+ user +"/"+ repoName + "/contents/" + filePath, "GET", token);
 
	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				// https://github.com/axios/axios
                console.log(response.data)
                resolve(response);
		});	
	});
}

async function createFile(repoName, user, fileName, contents, commitMessage, branchName, token) {
    // Github documentation for updating a particular file.
    // https://docs.github.com/en/rest/reference/repos#create-or-update-file-contents
	let options = getDefaultOptions("/repos/" + user + "/" + repoName + "/contents/" + fileName, "PUT", token);
    let base64 = Buffer.from(contents).toString("base64")
    options.data = {
        message: commitMessage,
        content: base64,
        branch: branchName
    };

	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				// https://github.com/axios/axios
                resolve(response);
		});	
	});
}

async function addCollaborator(repoName, user, invitee, token) {
    // Github documentation for adding a collaborator.
    // https://docs.github.com/en/rest/reference/collaborators#add-a-repository-collaborator
    let options = getDefaultOptions("/repos/" + user + "/" + repoName + "/collaborators/" + invitee, "PUT", token);
    options.data = {
        permission: "admin"
    };

	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				// https://github.com/axios/axios
                resolve(response);
		});	
	});    
}

async function forkRepo(repoName, owner, token) {
    // Github documentation for forking repo.
    // https://docs.github.com/en/rest/reference/repos#create-a-fork
    let options = getDefaultOptions("/repos/" + owner + "/" + repoName + "/forks", "POST", token);
    options.data = {
        permission: "admin"
    };

	// Send a http request to url and specify a callback that will be called upon its return.
	return new Promise(function(resolve, reject)
	{
		axios(options)
			.then(function (response) {
				// https://github.com/axios/axios
                resolve(response);
		});	
	});    
}

exports.createRepo = createRepo;
exports.updateFile = updateFile;
exports.addCollaborator = addCollaborator;
exports.forkRepo = forkRepo;
exports.getBlobInfo = getBlobInfo;
exports.getUser = getUser;
exports.createFile = createFile;