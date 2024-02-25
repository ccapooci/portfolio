const axios = require("axios");
const tar = require("tar-fs");

//dockerApi is compatable docker socket argument for dockerode Docker();
//dockerApi = { host: "127.0.0.1", port: 2375 };
//Reads HOSTNAME and PORT from env variables
dockerApi = { host: process.env.DOCKERHOSTNAME, port: process.env.DOCKERPORT };
console.log(dockerApi);

const buildImage = async (dir, tag) => {
  //post to docker api
  const tarStream = tar.pack(dir);
  try {
    await axios.post(
      `http://${dockerApi.host}:${dockerApi.port}/build?t=${tag}`,
      tarStream,
      {
        headers: { "Content-Type": "x-application/x-tar" },
      }
    );
    return true;
  } catch (err) {
    return false;
  }
};

const buildContainer = async (name, image) => {
  console.log(
    `http://${dockerApi.host}:${dockerApi.port}/containers/create?name=${name}`
  );
  try {
    const response = await axios.post(
      `http://${dockerApi.host}:${dockerApi.port}/containers/create?name=${name}`,
      {
        Image: image,
      }
    );
    return { created: true, id: response.data.Id, error: "" };
  } catch (error) {
    return { created: false, id: "", error: "error creating container" };
  }
};

//Return true if container started, false if not started
const startContinerByName = async (name) => {
  //post to docker api
  try {
    const response = await axios.post(
      `http://${dockerApi.host}:${dockerApi.port}/containers/${name}/start`
    );
    return true;
  } catch (err) {
    return false;
  }
};

const stopContinerByName = async (name) => {
  try {
    await axios.post(
      `http://${dockerApi.host}:${dockerApi.port}/containers/${name}/stop`
    );
    return true;
  } catch (err) {
    return false;
  }
};
//Query Docker Web Api to see if continer is running
const checkContainerRunningByName = async (name) => {
  try {
    const response = await axios.get(
      `http://${dockerApi.host}:${dockerApi.port}/containers/${name}/json`
    );
    const returnStatus = response.data.State.Running;
    if (returnStatus === true) {
      return {
        status: "running",
        message: `Container ${name} runnign`,
      };
    }
    return { status: "stopped", message: "Invalid image name" };
  } catch (err) {
    return { status: "error", message: "Invalid image name" };
  }
};

exports.startContinerByName = startContinerByName;
exports.checkContainerRunningByName = checkContainerRunningByName;
exports.stopContinerByName = stopContinerByName;
exports.buildContainer = buildContainer;
