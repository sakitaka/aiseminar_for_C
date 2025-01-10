import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import cv2
from  utils import preprocess
import time
import sys


def take_picture():
     camera =cv2.VideoCapture(0)
     re, img =camera.read()
     img =cv2.resize(img, dsize =(224,224))
     return img


categories=["can", "pet"]
model = torchvision.models.alexnet(pretrained=True)
model.classifier[-1] = torch.nn.Linear(4096, len(categories))


# model = torchvision.models.resnet18(pretrained=True)
# model.fc = torch.nn.Linear(512, len(categories))


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
model.to(device)

# gosa
criterion = nn.CrossEntropyLoss()

# optimizer
optimizer = optim.Adam(model.parameters(), lr = 5*10**-4)


#data import
image_size = 224
mean = (0.485, 0.456, 0.406)
std = (0.229, 0.224, 0.225)
data_transform = {
    "train": transforms.Compose([
        transforms.RandomResizedCrop(
            image_size, scale=(0.5, 1.0)
        ),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(degrees=[-15, 15]),
        transforms.ToTensor(),
        transforms.Normalize(mean,std),
        #transforms.RandomErasing(0.5),
        ]),
    "val": transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean,std)
        ])
}


train_dataset = torchvision.datasets.ImageFolder(root = "./data/train", transform=data_transform["train"])
val_dataset = torchvision.datasets.ImageFolder(root = "./data/val", transform=data_transform["val"])


BATCH_SIZE = 8

trainloader = torch.utils.data.DataLoader(train_dataset, batch_size = BATCH_SIZE, shuffle = True)

valloader = torch.utils.data.DataLoader(val_dataset, batch_size = BATCH_SIZE, shuffle = False)

EPOCHS = 10

for epoch in range(EPOCHS):
    running_loss = 0.0

    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        inputs =inputs.to(device)
        labels = labels.to(device)
        outputs = model(inputs)
        optimizer.zero_grad()
        loss = criterion(outputs,labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        if True:
            print("now{}epoch,{}cycle,loss:{}".format(epoch,i+1, running_loss/100))
            running_loss = 0.0
torch.save(model,"model_weight_res.pth")

test_loss = 0
correct = 0
for i, data in enumerate(valloader,0):
    inputs, labels = data
    inputs = inputs.to(device)
    labels = labels.to(device)
    outputs = model(inputs)
    test_loss += criterion(outputs, labels).item()

    pred = outputs.argmax(dim=1, keepdim=True)

    correct += pred.eq(labels.view_as(pred)).sum().item()

print("test_loss{}".format(test_loss/len(valloader)))
print("accuracy{}".format(correct/len(val_dataset)))

while True:
    s = input("press enter after putting can:")
    if s == "q":break
    img =take_picture()
    cv2.imwrite("image.jpeg",img)
    preprocessed = preprocess(img)
    output = model(preprocessed)
    output = torch.nn.functional.softmax(output, dim =1).detach().cpu().numpy().flatten()
    category_index = output.argmax()
    #print(output)
    if category_index == 0:
        print("can")
    else:
        print("pet")

