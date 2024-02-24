const chai = require("chai");
const expect = chai.expect;
const nock = require("nock");

const data = require("../mock.json");
const depolyer = require("../src/deployer.js");
const { assert } = require("console");

//Docker REST API https://docs.docker.com/engine/api/v1.41
describe("testDepolyer", async function () {
  //Set the environment variables
  //TODO better mock checks for posts see https://github.com/nock/nock#specifying-request-body
  const mockService = nock(
    `http://${process.env.DOCKERHOSTNAME}:${process.env.DOCKERPORT}`
  )
    .persist()
    .get("/smoke")
    .reply(200, JSON.stringify({ test: "good" }))
    .get("/containers/test/json")
    .reply(200, JSON.stringify(data.running))
    .get("/containers/down/json")
    .reply(200, JSON.stringify(data.down))
    .post("/containers/good/start")
    .reply(204)
    .post("/containers/bad/start")
    .reply(404, JSON.stringify({ message: "No such conainter:c2ada9df5af8" }))
    .post("/containers/good/stop")
    .reply(204)
    .post("/containers/bad/stop")
    .reply(404, JSON.stringify({ message: "No such conainter:c2ada9df5af8" }))
    .post("/containers/create?name=good", { Image: "alpine" })
    .reply(200, {
      Id: "e90e34656806",
      Warnings: [],
    })
    .post("/containers/create?name=other", { Image: "no-image" })
    .reply(404, {
      message: "No such image: bad",
    })
    .post("/build")
    .reply(200);

  describe("#getContinerByName()", async function () {
    it("should return status of continer", async () => {
      //TEST CASE
      const statusUp = await depolyer.checkContainerRunningByName("test");
      const statusDown = await depolyer.checkContainerRunningByName("down");
      expect(statusUp.status).to.equal("running");
      expect(statusDown.status).to.equal("stopped");
    });

    it("should error on invalid continer name", async () => {
      const invalidContainer = await depolyer.checkContainerRunningByName(
        "bad"
      );
      expect(invalidContainer.status).to.equal("error");
    });
  });

  describe("#startContainerByName(tag)", async () => {
    it("should start container in docker", async () => {
      const goodName = await depolyer.startContinerByName("good");
      expect(goodName).to.be.true;
    });

    it("should fail on a bad name", async () => {
      const badName = await depolyer.startContinerByName("bad");
      expect(badName).to.be.false;
    });
  });

  // TODO maybe add more edge cases
  describe("#stopContainerByName(tag)", async () => {
    it("should stop container in docker", async () => {
      const goodName = await depolyer.stopContinerByName("good");
      expect(goodName).to.be.true;
    });

    it("should fail if the continer name is wrong", async () => {
      const badName = await depolyer.stopContinerByName("bad");
      expect(badName).to.be.false;
    });
  });

  describe("#buidContainer(tag)", async () => {
    it("should build a container with docker", async () => {
      const container = await depolyer.buildContainer("good", "alpine");
      expect(container.created).to.be.true;
      expect(container.id).to.equal("e90e34656806");
      expect(container.error).to.equal("");
    });

    it("shold fail if the image isn't found", async () => {
      const badContainer = await depolyer.buildContainer("other", "no-image");

      expect(badContainer.created).to.be.false;
      expect(badContainer.id).to.equal("");
      expect(badContainer.error).to.equal("error creating container");
    });
  });
  //describe("#buidImage(dir, tag)"), function () {};
});
