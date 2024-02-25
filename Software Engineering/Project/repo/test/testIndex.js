const chai = require("chai");
const expect = chai.expect;
const nock = require("nock");
var request = require('supertest');

const data = require("../mockIndex.json");

process.env.NODE_ENV = 'test';

const index = require("../src/index.js");

describe('app responder test', function() {
   var postDialogCreate = nock("https://chat.robotcodelab.com")
                  .persist() 
                  .post("/api/v4/actions/dialogs/open")
                  .reply(200, JSON.stringify(data.data));

   describe('POST /create', function() {
       it('should respond to POST /create', function (done) {
          request(index.app)
                 .post('/create')
                 .expect(200)
                 .end(done) 
       });
   });

   describe('POST /deploy', function() {
        it('should respond to POST /deploy', function (done) {
           request(index.app)
                  .post('/deploy')
                  .expect(200)
                  .end(done) 
        });
   });

   describe('POST /submitcreate', function() {

      var postMessage = nock("https://chat.robotcodelab.com")
                  .post("/posts")
                  .reply(200, JSON.stringify(data.data));

        it('should respond to POST /submitcreate', function (done) {
           request(index.app)
                  .post('/submitcreate')
                  .send(data.create)
                  .expect(200)
                  .end(done) 
        });
   });

   describe('POST /submitdeploy', function() {
      var postMessage = nock("https://chat.robotcodelab.com")
                  .post("/posts")
                  .reply(200, JSON.stringify(data.data));
      
        it('should respond to POST /submitdeploy', function (done) {
           request(index.app)
                  .post('/submitdeploy').send(data.deploy)
                  .expect(200)
                  .end(done) 
        });
   });
});