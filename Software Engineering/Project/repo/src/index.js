const express = require('express');
const data = require('./dialog.json');
const axios = require('axios');
const uuid = require('uuid');
const responder = require('./responder.js');
const gh = require('./github.js')
const deployer = require('./deployer.js')
const { updateLocale } = require('yargs');

const port = 3000;
const status_ok = { "status": "OK" };

const app = express();

// Web Service to handle the /slash commands
app.use(express.json());
app.use(express.urlencoded({
    extended: true
}));

function error(status, msg) {
  var err = new Error(msg);
  err.status = status;
  return err;
}

// Handle the /createbot command
app.post('/create', function(req, res, next){
    // Spawn the Interactive Dialog for create
    // Need to get the Submit Action work
    let payload = data.create;
    payload.trigger_id = req.body.trigger_id;
    payload.url = process.env.SUBMIT_CREATE_URL;
    payload.dialog.callback_id = uuid.v4();
    postDialog(payload);
    res.status(200);
    res.send(status_ok);
});

// Handle the /deploybot command
app.post('/deploy', function(req, res, next){
    let payload = data.deploy;
    payload.trigger_id = req.body.trigger_id;
    payload.url = process.env.SUBMIT_DEPLOY_URL;
    payload.dialog.callback_id = uuid.v4();
    postDialog(payload);
    res.status(200);
    res.send(status_ok);
});

// Handle the submit from the createbot command
app.post('/submitcreate', function(req, res, next){
    console.log("---------------submitcreate");
    /*
    Sample set of parameters received in the Submit for /createbot
    {
      type: 'dialog_submission',
      callback_id: 'b96a12fc-3a38-4541-97b9-3f4f4a98979c',
      state: 'Submitted to create bot',
      user_id: 'e1n5uhwkyir48ju5gacuxew7fh',
      channel_id: 'jtut6b7f9jdc8mt3anya9sku6a',
      team_id: 'kzsmo64zkbbcb8jgf1691i4xrc',
      submission: 
        { 
          botname: 'bot2', 
          features: 'repos', 
          platform: 'opt1' 
        },
      cancelled: false 
    }
    */
    if (!req.body.cancelled) {
      // Trigger the repository creation
      // TODO: Invoke Corey's code
      let userBotName = req.body.submission.botname
      let botType = req.body.submission.platform
      const data = require("../mockGithub.json") //Temp Mocked Response

      if (botType == 'opt1'){
        let res = gh.createRepo(userBotName)
        //We don't actually interact with GH yet
        msg = `Bot ${userBotName} created at https://github.ncsu.edu/CSC-510/${userBotName}.git`
        responder.sendMessage(msg, req.body.channel_id);
      }
      
    }

    res.status(200);
    res.send(status_ok);
});

// Handle the submit from the deploybot command
app.post('/submitdeploy', function(req, res, next){
    console.log("---------------submitdeploy");
  /*
    Sample set of parameters received in the Submit for /deploybot
    { 
      type: 'dialog_submission',
      callback_id: 'ab01f610-148c-4eef-a555-f84bae6252dc',
      state: 'Submitted to deploy bot ',
      user_id: 'e1n5uhwkyir48ju5gacuxew7fh',
      channel_id: 'jtut6b7f9jdc8mt3anya9sku6a',
      team_id: 'kzsmo64zkbbcb8jgf1691i4xrc',
      submission:
      {
        botname: 'Bot2',
        repo: 'https://github.ncsu.edu/CSC-510/HW2.git' 
      },
      cancelled: false 
    }
  */
    if (!req.body.cancelled) {
      // Trigger the deploy
      // TODO: Invoke Chris's code

      let userBotName = req.body.submission.botname
      let repo = req.body.submission.repo
      // deployer.startContinerByName(userBotName)  <---- this would run if deploying was live.
      //We don't actually interact with deployment yet
      msg = `Bot ${userBotName} has been deployed.`
      responder.sendMessage(msg, req.body.channel_id);
    }
    res.status(200);
    res.send(status_ok);
});

app.use(function(err, req, res, next){
    res.status(err.status || 500);
    res.send({ error: err.message });
});

app.use(function(req, res){
    res.status(404);
    res.send({ error: "Sorry, can't find that" })
});

async function main() {
  app.listen(port, () => console.log(`Express started on port ${port}!`))
}

async function postDialog(payload){
  const res = await axios.post(process.env.DIALOG_URL, payload, {
      headers: {
          "content-type": "application/json",
      }
  })
  console.log(res)
  return res
}

(async () => 
{
    if (process.env.NODE_ENV != 'test') {
        await main();
    }
})()

module.exports.main = main;
module.exports.app = app;
