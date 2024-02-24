!pip install syft==0.2.0a2
!pip install "pillow<7"
import random
import syft as sy
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets
from torchvision import transforms



class Arguments():
    def __init__(self):
        self.batch_size = 128
        self.test_batch_size = 1000
        self.epochs = 1
        self.lr = 0.01
        self.momentum = 0.5
        self.no_cuda = True
        self.seed = 200387223 ## TODO change seed to your studentID inside the class Arguments (line 17)
        self.log_interval = 30
        self.save_model = False

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4*4*50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4*4*50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def train(args, model, device, federated_train_loader, optimizer, epoch, participates):
    model.train()  # <-- initial training
    for batch_idx, (data, target) in enumerate(federated_train_loader): # <-- now it is a distributed dataset
        if target.location.id in participates:
            model.send(data.location) # <-- NEW: send the model to the right location
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            model.get() # <-- NEW: get the model back
            if batch_idx % args.log_interval == 0:
                loss = loss.get() # <-- NEW: get the loss back
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * args.batch_size, len(federated_train_loader) * args.batch_size,
                    100. * batch_idx / len(federated_train_loader), loss.item()))



def test(args, model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item() # sum up batch loss
            pred = output.argmax(1, keepdim=True) # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\n    Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


### main function

args = Arguments()
use_cuda = not args.no_cuda and torch.cuda.is_available()
torch.manual_seed(args.seed)
device = torch.device("cuda" if use_cuda else "cpu")
kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}

hook = sy.TorchHook(torch)  # <-- NEW: hook PyTorch ie add extra functionalities to support Federated Learning

## create 10 node workers  and assign node id---- ##
nodes = []
for i in range(10):
    nodes.append(sy.VirtualWorker(hook, id="node"+str(i)))  # <-- NEW: define remote worker

## distribute data across nodes
federated_train_loader = sy.FederatedDataLoader( # <-- this is now a FederatedDataLoader
    datasets.MNIST('./data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ]))
    .federate((nodes)), ## TODO: pass the worker nodes you created here to distribute the data
    batch_size=args.batch_size, shuffle=True, **kwargs)

## test dataset is always same at the central server
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=False, transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=args.test_batch_size, shuffle=True, **kwargs)

## Part A of the problem
## TODO: Vary the number of nodes that will participate in the federated learning
for x in [ 3, 5, 7, 10 ]:

    #reinitialize weights ... or reset model before each new experiment
    model = Net().to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr)

    args.epochs = 3 # N epochs is fixed

    ## TODO: select 'x' number of random  node ids that will be passed to the training function; these nodes will particiapte in the federated learning
    # iteratively create different size node_list
    nodes_id = []
    while len(nodes_id) < x:
       index = random.randint(0,9)
       if nodes[index] not in nodes_id:
         nodes_id.append(nodes[index])

    print("# of Epochs", 3, ", # of Nodes", x)
    for epoch in range(1, args.epochs + 1):
        print("  Epochs #", epoch)
        train(args, model, device, federated_train_loader, optimizer, epoch,  nodes_id )
        test(args, model, device, test_loader)



## Part B of the problem
## TODO: Vary the number of epochs to train the global model
for n in [3, 5, 10]:

    #reinitialize weights ... or reset model before each new experiment
    model = Net().to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr)

    nodes_id = [] # initialize empty list
    args.epochs = n # number of Epochs

    ## TODO: select random 5 node ids that will be passed to the training function; these nodes will particiapte in the federated learning
    nodes_id = []
    while len(nodes_id) < 5:
       index = random.randint(0,9)
       if nodes[index] not in nodes_id:
         nodes_id.append(nodes[index])


    print("# of Epochs", n, ", # of Nodes", 5)
    for epoch in range(1, args.epochs + 1):
        print("  Epochs #", epoch)
        train(args, model, device, federated_train_loader, optimizer, epoch, nodes_id )
        test(args, model, device, test_loader)
