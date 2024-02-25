const { func } = require('assert-plus');
const Client = require('mattermost-client');

let host = "chat.robotcodelab.com"
let group = "CSC510-S22"
let bot_name = "celebrimbot";
let client = new Client(host, group, {});

const helpMessage = `# Celebrimbot Help Page
| **Command**  | **Description**  |
| ------------ | ------------ |
| !help   |  opens Celebrimbot help page |
| / createBot  | Prompts you with a form to create a bot|
| / deployBot  | Prompts you with a form to deploy a bot|
`

async function main()
{
    let request = await client.tokenLogin(process.env.TEAMBOTTOKEN);
    client.on('message', function(msg)
    {
        if( hears(msg, "!help"))
        {
          let channel = msg.broadcast.channel_id;
            sendHelpMessage(channel)
        }
    });
}

function hears(msg, text)
{
    if( msg.data.sender_name == bot_name) return false;
    if( msg.data.post )
    {
        let post = JSON.parse(msg.data.post);
        if( post.message.indexOf(text) >= 0)
        {
            return true;
        }
    }
    return false;
}

async function sendMessage(msg, channel_id)
{
    client.postMessage(msg, channel_id);
}

async function sendHelpMessage(channel_id)
{
    client.postMessage(helpMessage, channel_id);
}

(async () => 
{
    if (process.env.NODE_ENV != 'test') {
        await main();
    }
})()


module.exports.sendMessage = sendMessage;
module.exports.main = main;
