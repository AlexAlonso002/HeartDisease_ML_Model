# -*- coding: utf-8 -*-
"""Project_Final_Training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LGmGYb48Mfz93daNIWT7YNw0ywASJuGL
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
from  sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import torch.optim as optim
import random
import torchvision.datasets as dsets
import torchvision.transforms as transforms #should be used to convert images to pytorch tensors
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset, DataLoader, TensorDataset

device = 'cuda' if torch.cuda.is_available else 'cpu'

"""#Data Preparation"""

df = pd.read_csv("/content/drive/MyDrive/CSCE464/Datasets/ProjectUpdate.csv")
#df = pd.read_csv("/content/drive/MyDrive/GoogleCollabDM/Dataset/ProjectUpdate.csv")

df

x_data = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
x_data

y_data = df[['HeartDisease']]
y_data

x_train, x_test, y_train, y_test = train_test_split(x_data,y_data, test_size = 0.2,random_state=42)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

"""#Shallow: Pytorch model Logistic regression"""

x_train = torch.Tensor(x_train)
x_test = torch.Tensor(x_test)
y_train = torch.Tensor(y_train.to_numpy())
y_test = torch.Tensor(y_test.to_numpy())

class BinaryClassifier(nn.Module):
  def __init__(self):
    super().__init__()
    self.linear = nn.Linear(15, 1)
    self.sigmoid = nn.Sigmoid()

  def forward(self, x):
    return self.sigmoid(self.linear(x))

model = BinaryClassifier()

learning_rate = 0.006208220274456816

x_axis = []
y1_axis = []
y2_axis = []
accuracy = 0

optimizer = optim.Adam(model.parameters(), lr=learning_rate)
#optimizer = optim.SGD(model.parameters(), lr=learning_rate)
print("====Symmary of Model Training====")

for epoch in range(652):
  x = x_train
  y = y_train

  hypothesis = model(x)

  cost = F.binary_cross_entropy(hypothesis, y)

  optimizer.zero_grad()
  cost.backward()
  optimizer.step()

  x_axis.append(epoch)
  y1_axis.append(cost.item())
  y2_axis.append(accuracy)

  if epoch % 10 == 0:
    prediction = hypothesis >= torch.FloatTensor([0.5])
    correct_prediction = prediction.float() == y
    accuracy = correct_prediction.sum() / len(correct_prediction)

    print("Epoch {:4d} Cost: {:.5f} Training Acc: {:.2f}".format(epoch, cost.item(), accuracy*100))

fig, x1 = plt.subplots()
x1.set_xlabel("Epoch")
x1.set_ylabel("Cost")
x1.plot(x_axis, y1_axis, label="Cost")
x1.legend(loc="upper left")

x2 = x1.twinx()
x2.set_ylabel("ACC")
x2.plot(x_axis, y2_axis, color="orange", label="ACC")
x2.legend(loc="upper right")

plt.show()

with torch.no_grad():
  y = model(x_test)
  cost_test = F.binary_cross_entropy(y, y_test)

  prediction = y >= torch.FloatTensor([0.5])
  correct_prediction = prediction.float() == y_test
  accuracy = correct_prediction.sum() / len(correct_prediction)

  print("Cost: {:.2f} Testing Accuracy: {:.2f}".format(cost_test.item(), accuracy*100))

from sklearn.metrics import f1_score, confusion_matrix
confusion_matrix(y_test, prediction)

"""#Medium Deepness

# CNN
"""

x_train = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
y_train = df['HeartDisease']
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)


class Data(Dataset):
  def __init__(self, x, y):
    self.x = torch.FloatTensor(x)
    self.y = torch.LongTensor(y)
    self.len = self.y.shape[0]

  def __getitem__(self, index):
    return self.x[index], self.y[index]

  def __len__(self):
    return self.len

x_train = x_train.values
y_train = y_train.values

x_test = x_test.values
y_test = y_test.values

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(-1, 15, 1)
x_test = x_test.reshape(-1, 15, 1)

print(f"Reshaped x_train: {x_train.shape}")

train = Data(x_train, y_train)
test = Data(x_test, y_test)

train_loader = DataLoader(train, batch_size=100, shuffle=True)
test_loader = DataLoader(test, batch_size=len(test), shuffle=True)

class CNN1(torch.nn.Module):
  def __init__(self):
    super(CNN1, self).__init__()

    self.layer1 = torch.nn.Sequential(
        torch.nn.Conv1d(15, 512, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2),
        nn.Dropout(0.5))



    self.layer2 = torch.nn.Sequential(
        torch.nn.Conv1d(512, 256, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))


    self.layer3 = torch.nn.Sequential(
        torch.nn.Conv1d(256, 128, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))
        #nn.Dropout(0.5))  # Adding dropout



    self.layer4 = torch.nn.Sequential(
        torch.nn.Conv1d(128, 2, kernel_size=1, stride=1, padding=1),
        #torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))


    self.fc = torch.nn.Linear(2 * 1, 2, bias=True)
    torch.nn.init.xavier_uniform_(self.fc.weight)

  def forward(self, x):
    out = self.layer1(x)
    out = self.layer2(out)
    out = self.layer3(out)
    out = self.layer4(out)
    out = out.view(out.size(0), -1)
    out = self.fc(out)
    return out

model = CNN1()
training_epoch = 50
learning_rate = 0.001

#loss = torch.nn.CrossEntropyLoss().to(device)
loss = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

x_axis = []
y_costs = []
y_accs = []

for epoch in range(training_epoch):
    epoch_costs = []
    epoch_accs = []
    for x_train, y_train in train_loader:
        x_train = x_train
        y_train = y_train

        pred = model(x_train)
        cost = loss(pred, y_train)
        epoch_costs.append(cost.item())

        correct_pred = torch.argmax(pred, 1) == y_train
        accuracy = correct_pred.float().mean()
        epoch_accs.append(accuracy.item())

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

    # Calculate mean cost and accuracy for the epoch
    mean_cost = sum(epoch_costs) / len(epoch_costs)
    mean_accuracy = sum(epoch_accs) / len(epoch_accs) * 100

    x_axis.append(epoch)
    y_costs.append(mean_cost)
    y_accs.append(mean_accuracy)

    print(f"Epoch {epoch + 1} / {training_epoch} Cost: {mean_cost:.5f} Training ACC: {mean_accuracy:.2f}%")

fig, ax1 = plt.subplots()

ax1.set_xlabel('Epoch')
ax1.set_ylabel('Cost', color='tab:blue')
ax1.plot(x_axis, y_costs, label="Cost", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Accuracy', color='tab:orange')
ax2.plot(x_axis, y_accs, label="Accuracy", color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

fig.tight_layout()
plt.show()

model.eval()
total = 0
correct = 0

with torch.no_grad():
    for x_test, y_test in test_loader:
        pred = model(x_test)
        correct_pred = torch.argmax(pred, 1) == y_test
        correct += correct_pred.sum().item()
        total += y_test.size(0)

    print("Correct: ", correct)
    print("Total: ", total)

    testing_accuracy = correct / total
    print("Final Testing Accuracy: {:.2f}".format(testing_accuracy*100))

def get_predictions(model, data_loader):
    model.eval()
    predictions = []
    ground_truth = []
    with torch.no_grad():
        for inputs, labels in data_loader:
            #inputs = inputs.to(device)
            #labels = labels.to(device)
            inputs = inputs
            labels = labels
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            predictions.extend(preds.cpu().numpy())
            ground_truth.extend(labels.cpu().numpy())
    return predictions, ground_truth

# Get predictions for test data
test_predictions, test_ground_truth = get_predictions(model, test_loader)

# Calculate confusion matrix
conf_matrix = confusion_matrix(test_ground_truth, test_predictions)

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

"""#MLP

"""

x_train = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
y_train = df['HeartDisease']
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
x_train = x_train.values
y_train = y_train.values

x_test = x_test.values
y_test = y_test.values

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

class Data(Dataset):
  def __init__(self, x, y):
    self.x = torch.FloatTensor(x)
    self.y = torch.LongTensor(y)
    self.len = self.y.shape[0]

  def __getitem__(self, index):
    return self.x[index], self.y[index]

  def __len__(self):
    return self.len

train = Data(x_train, y_train)
test = Data(x_test, y_test)

train_loader = DataLoader(train, batch_size=100, shuffle=True)
test_loader = DataLoader(test, batch_size=len(test), shuffle=True)

linear1 = torch.nn.Linear(15, 300, bias=False)
linear2 = torch.nn.Linear(300, 150, bias=False)
linear3 = torch.nn.Linear(150, 75, bias=False)
linear4 = torch.nn.Linear(75, 2, bias=True)
relu = torch.nn.ReLU()

class MLP(nn.Module):
  def __init__(self):
    super().__init__()
    self.layers = nn.Sequential(
        linear1,
        relu,
        nn.Dropout(0.4),
        linear2,
        relu,
        nn.Dropout(0.2),
        linear3,
        relu,
       #nn.Dropout(0.5),
        linear4,
       # relu,
       # nn.Dropout(0.2),
       # linear5,
        nn.Softmax())
  def forward(self, x):
    return self.layers(x)

model = MLP().to(device)
print(model)

loss = torch.nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
training_epoch = 50

import matplotlib.pyplot as plt

# Assuming you have already defined train_loader, device, model, optimizer, loss, and total_batch

epochs = 50
costs = []
accuracies = []

x_axis = []
y1_axis = []
y2_axis = []

plot_interval = 3

for epoch in range(epochs):
    avg_cost = 0
    total_accuracy = 0
    for idx, data in enumerate(train_loader):
        x_train, y_train = data
        x_train = x_train.to(device)
        y_train = y_train.to(device)


        optimizer.zero_grad()
        pred = model(x_train)
        cost = loss(pred, y_train)

        correct_pred = torch.argmax(pred, 1) == y_train
        accuracy = correct_pred.float().mean()
        total_accuracy += accuracy.item()

        cost.backward()
        optimizer.step()

        # Append values for each batch
        if idx == len(train_loader) - 1 or epoch % plot_interval == 0:
            x_axis.append(epoch + idx / len(train_loader))  # Epoch + fraction of completion of current epoch
            y1_axis.append(cost.item())
            y2_axis.append(accuracy.item())  # Ensure accuracy is converted to a Python float

        avg_cost += cost / len(train_loader)
    avg_accuracy = total_accuracy / len(train_loader)
    costs.append(avg_cost.cpu().detach().numpy())
    accuracies.append(avg_accuracy)
    print("[Epoch:{}] cost = {:.4f} Training ACC: {:.2f}%".format(epoch + 1, avg_cost, avg_accuracy * 100))

# Plotting
fig, x1 = plt.subplots()
x1.set_xlabel("Epoch")
x1.set_ylabel("Cost")
x1.plot(x_axis, y1_axis, label="Cost")
x1.legend(loc="upper left")

x2 = x1.twinx()
x2.set_ylabel("ACC")
x2.plot(x_axis, y2_axis, color="orange", label="ACC")
x2.legend(loc="upper right")

plt.show()

model.eval()
with torch.no_grad():
  for x_test, y_test in test_loader:
    x_test = x_test.to(device)
    y_test = y_test.to(device)

    pred = model(x_test).to(device)
    correct_pred = torch.argmax(pred, 1) == y_test
    accuracy = correct_pred.float().mean()
  print("Final Testing Accuracy: {:.2f}".format(accuracy.item()*100))

def get_predictions(model, data_loader):
    model.eval()
    predictions = []
    ground_truth = []
    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            predictions.extend(preds.cpu().numpy())
            ground_truth.extend(labels.cpu().numpy())
    return predictions, ground_truth

# Get predictions for test data
test_predictions, test_ground_truth = get_predictions(model, test_loader)

# Calculate confusion matrix
conf_matrix = confusion_matrix(test_ground_truth, test_predictions)

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

"""#Deep Learning

#Deep CNN
"""

class Data(Dataset):
  def __init__(self, x, y):
    self.x = torch.FloatTensor(x)
    self.y = torch.LongTensor(y)
    self.len = self.y.shape[0]

  def __getitem__(self, index):
    return self.x[index], self.y[index]

  def __len__(self):
    return self.len

x_train = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
y_train = df['HeartDisease']
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

x_train = x_train.values
y_train = y_train.values

x_test = x_test.values
y_test = y_test.values

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

x_train = x_train.reshape(-1, 15, 1)
x_test = x_test.reshape(-1, 15, 1)

print(f"Reshaped x_train: {x_train.shape}")
class Data(Dataset):
  def __init__(self, x, y):
    self.x = torch.FloatTensor(x)
    self.y = torch.LongTensor(y)
    self.len = self.y.shape[0]

  def __getitem__(self, index):
    return self.x[index], self.y[index]

  def __len__(self):
    return self.len

train = Data(x_train, y_train)
test = Data(x_test, y_test)

train_loader = DataLoader(train, batch_size=100, shuffle=True)
test_loader = DataLoader(test, batch_size=len(test), shuffle=True)

class CNN(torch.nn.Module):
  def __init__(self):
    super(CNN, self).__init__()

    self.layer1 = torch.nn.Sequential(
        #torch.nn.Conv1d(15, 1024, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(15, 512, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2),
        nn.Dropout(0.5))


    self.layer2 = torch.nn.Sequential(
        #torch.nn.Conv1d(1024, 512, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(512, 256, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))


    self.layer3 = torch.nn.Sequential(
        #torch.nn.Conv1d(512, 256, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(256, 128, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))
        #nn.Dropout(0.5))  # Adding dropout

    self.layer4 = torch.nn.Sequential(
        #torch.nn.Conv1d(256, 128, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(128, 64, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))
        #nn.Dropout(0.5))  # Adding dropout

    self.layer5 = torch.nn.Sequential(
        #torch.nn.Conv1d(128, 64, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(64, 32, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))
        #nn.Dropout(0.5))  # Adding dropout

    self.layer6 = torch.nn.Sequential(
        #torch.nn.Conv1d(64, 32, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(32, 16, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))
        #nn.Dropout(0.5))  # Adding dropout

    self.layer7 = torch.nn.Sequential(
        #torch.nn.Conv1d(32, 16, kernel_size=1, stride=1, padding=1),
        torch.nn.Conv1d(16, 8, kernel_size=1, stride=1, padding=1),
        torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2),
        nn.Dropout(0.5))  # Adding dropout


    self.layer8 = torch.nn.Sequential(
        torch.nn.Conv1d(8, 2, kernel_size=1, stride=1, padding=1),
        #torch.nn.ReLU(),
        torch.nn.MaxPool1d(kernel_size=2, stride=2))


    self.fc = torch.nn.Linear(2 * 1, 2, bias=True)
    torch.nn.init.xavier_uniform_(self.fc.weight)

  def forward(self, x):
    out = self.layer1(x)
    out = self.layer2(out)
    out = self.layer3(out)
    out = self.layer4(out)
    out = self.layer5(out)
    out = self.layer6(out)
    out = self.layer7(out)
    out = self.layer8(out)

    out = out.view(out.size(0), -1)  # Flatten the output for the fully connected layer
    out = self.fc(out)
    return out

model = CNN()
training_epoch = 50
learning_rate = 0.001

loss = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

x_axis = []
y_costs = []
y_accs = []

for epoch in range(training_epoch):
    epoch_costs = []
    epoch_accs = []
    for x_train, y_train in train_loader:
        x_train = x_train
        y_train = y_train

        pred = model(x_train)
        cost = loss(pred, y_train)
        epoch_costs.append(cost.item())

        correct_pred = torch.argmax(pred, 1) == y_train
        accuracy = correct_pred.float().mean()
        epoch_accs.append(accuracy.item())

        optimizer.zero_grad()
        cost.backward()
        optimizer.step()

    # Calculate mean cost and accuracy for the epoch
    mean_cost = sum(epoch_costs) / len(epoch_costs)
    mean_accuracy = sum(epoch_accs) / len(epoch_accs) * 100

    x_axis.append(epoch)
    y_costs.append(mean_cost)
    y_accs.append(mean_accuracy)

    print(f"Epoch {epoch + 1} / {training_epoch} Cost: {mean_cost:.5f} Training ACC: {mean_accuracy:.2f}%")

fig, ax1 = plt.subplots()

ax1.set_xlabel('Epoch')
ax1.set_ylabel('Cost', color='tab:blue')
ax1.plot(x_axis, y_costs, label="Cost", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Accuracy', color='tab:orange')
ax2.plot(x_axis, y_accs, label="Accuracy", color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

fig.tight_layout()
plt.show()

model.eval()
total = 0
correct = 0

with torch.no_grad():
    for x_test, y_test in test_loader:
        pred = model(x_test)
        correct_pred = torch.argmax(pred, 1) == y_test
        correct += correct_pred.sum().item()
        total += y_test.size(0)

    testing_accuracy = correct / total
    print("Correct: ", correct)
    print("Total: ", total)

    print("Final Testing Accuracy: {:.2f}".format(testing_accuracy*100))

def get_predictions(model, data_loader):
    model.eval()
    predictions = []
    ground_truth = []
    with torch.no_grad():
        for inputs, labels in data_loader:
            #inputs = inputs.to(device)
            #labels = labels.to(device)
            inputs = inputs
            labels = labels
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            predictions.extend(preds.cpu().numpy())
            ground_truth.extend(labels.cpu().numpy())
    return predictions, ground_truth

# Get predictions for test data
test_predictions, test_ground_truth = get_predictions(model, test_loader)

# Calculate confusion matrix
conf_matrix = confusion_matrix(test_ground_truth, test_predictions)

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

"""#Deep MLP"""

class Data(Dataset):
  def __init__(self, x, y):
    self.x = torch.FloatTensor(x)
    self.y = torch.LongTensor(y)
    self.len = self.y.shape[0]

  def __getitem__(self, index):
    return self.x[index], self.y[index]

  def __len__(self):
    return self.len

x_train = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
y_train = df['HeartDisease']

x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

x_train = x_train.values
y_train = y_train.values

x_test = x_test.values
y_test = y_test.values


scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

train = Data(x_train, y_train)
test = Data(x_test, y_test)

train_loader = DataLoader(train, batch_size=100, shuffle=True)
test_loader = DataLoader(test, batch_size=len(test), shuffle=True)

linear1Deep = torch.nn.Linear(15, 300, bias=False)
linear2Deep = torch.nn.Linear(300, 150, bias=False)
linear3Deep = torch.nn.Linear(150, 75, bias=False)
linear4Deep = torch.nn.Linear(75, 38, bias=False)
linear5Deep = torch.nn.Linear(38, 19, bias=False)
linear6Deep = torch.nn.Linear(19, 2, bias=True)

relu = torch.nn.ReLU()

class DeepMLP(nn.Module):
  def __init__(self):
    super().__init__()
    self.layers = nn.Sequential(
        linear1Deep,
        relu,
        nn.Dropout(0.4),
        linear2Deep,
        relu,
        nn.Dropout(0.2),
        linear3Deep,
        relu,
        linear4Deep,
        relu,
        linear5Deep,
        relu,
        linear6Deep,
        nn.Softmax())
  def forward(self, x):
    return self.layers(x)

DeepModel = DeepMLP().to(device)
print(DeepModel)

DeepLoss = torch.nn.CrossEntropyLoss().to(device)
Deepoptimizer = torch.optim.Adam(DeepModel.parameters(), lr=0.001)

epochs = 50
costs = []
accuracies = []

x_axis = []
y1_axis = []
y2_axis = []

plot_interval = 3

for epoch in range(epochs):
    avg_cost = 0
    total_accuracy = 0
    for idx, data in enumerate(train_loader):
        x_train, y_train = data
        x_train = x_train.to(device)
        y_train = y_train.to(device)


        Deepoptimizer.zero_grad()
        pred = DeepModel(x_train)
        cost = DeepLoss(pred, y_train)

        correct_pred = torch.argmax(pred, 1) == y_train
        accuracy = correct_pred.float().mean()
        total_accuracy += accuracy.item()

        cost.backward()
        Deepoptimizer.step()

        # Append values for each batch
        if idx == len(train_loader) - 1 or epoch % plot_interval == 0:
            x_axis.append(epoch + idx / len(train_loader))
            y1_axis.append(cost.item())
            y2_axis.append(accuracy.item())

        avg_cost += cost / len(train_loader)
    avg_accuracy = total_accuracy / len(train_loader)
    costs.append(avg_cost.cpu().detach().numpy())
    accuracies.append(avg_accuracy)
    print("[Epoch:{}] cost = {:.4f} Training ACC: {:.2f}%".format(epoch + 1, avg_cost, avg_accuracy * 100))

# Plotting
fig, x1 = plt.subplots()
x1.set_xlabel("Epoch")
x1.set_ylabel("Cost")
x1.plot(x_axis, y1_axis, label="Cost")
x1.legend(loc="upper left")

x2 = x1.twinx()
x2.set_ylabel("ACC")
x2.plot(x_axis, y2_axis, color="orange", label="ACC")
x2.legend(loc="upper right")

plt.show()

model.eval()
with torch.no_grad():
  for x_test, y_test in test_loader:
    x_test = x_test.to(device)
    y_test = y_test.to(device)

    pred = DeepModel(x_test).to(device)
    correct_pred = torch.argmax(pred, 1) == y_test
    accuracy = correct_pred.float().mean()
  print("Final Testing Accuracy: {:.2f}".format(accuracy.item()*100))

def get_predictions(model, data_loader):
    DeepModel.eval()
    predictions = []
    ground_truth = []
    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = DeepModel(inputs)
            _, preds = torch.max(outputs, 1)
            predictions.extend(preds.cpu().numpy())
            ground_truth.extend(labels.cpu().numpy())
    return predictions, ground_truth

# Get predictions for test data
test_predictions, test_ground_truth = get_predictions(model, test_loader)

# Calculate confusion matrix
conf_matrix = confusion_matrix(test_ground_truth, test_predictions)

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

"""#Other Modules

#DT
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score,confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

x_train = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
y_train = df['HeartDisease']
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
x_train = x_train.values
y_train = y_train.values

x_test = x_test.values
y_test = y_test.values

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

DT = DecisionTreeClassifier()
DT.fit(x_train,y_train)

y_pred = DT.predict(x_test)
print("Test Acc: ", DT.score(x_test,y_test))
print("Test f1 ", f1_score(y_test,y_pred,average="weighted"))

confusion_matrix(y_test,y_pred)

from sklearn.metrics import classification_report
target_names = ["0","1"]
print(classification_report(y_test,y_pred,target_names=target_names,digits=4))

"""#RF"""

rf = RandomForestClassifier()
rf.fit(x_train,y_train)

importances = rf.feature_importances_
print(importances)

y_pred = rf.predict(x_test)
print("Test Acc: ", rf.score(x_test,y_test))
print("Test f1 ", f1_score(y_test,y_pred,average="weighted"))

confusion_matrix(y_test,y_pred)

target_names = ["0","1"]
print(classification_report(y_test,y_pred,target_names=target_names,digits=4))

"""#Optuna MLP"""

!pip install optuna
import optuna
import numpy as np
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

x_train = df[['Age',"Sex",'RestingBP',"Cholesterol",'FastingBS','MaxHR','ExerciseAngina','Oldpeak','ChestPainType_ATA','ChestPainType_NAP','ChestPainType_TA','RestingECG_Normal','RestingECG_ST','ST_Slope_Flat','ST_Slope_Up']]
y_train = df['HeartDisease']
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
x_train = x_train.values
y_train = y_train.values

x_test = x_test.values
y_test = y_test.values

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

import os
import optuna
from optuna.trial import TrialState
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torchvision import datasets
from torchvision import transforms

DEVICE = torch.device("cpu")
BATCHSIZE = 128
CLASSES = 10
DIR = os.getcwd()
EPOCHS = 10
N_TRAIN_EXAMPLES = BATCHSIZE * 30
N_VALID_EXAMPLES = BATCHSIZE * 10

def define_model(trial):
    # We optimize the number of layers, hidden units and dropout ratio in each layer.
    n_layers = trial.suggest_int("n_layers", 1, 5)
    layers = []

    in_features = 15
    for i in range(n_layers):
        out_features = trial.suggest_int("n_units_l{}".format(i), 4, 128)
        layers.append(nn.Linear(in_features, out_features))
        layers.append(nn.ReLU())
        p = trial.suggest_float("dropout_l{}".format(i), 0.2, 0.5)
        layers.append(nn.Dropout(p))

        in_features = out_features
    layers.append(nn.Linear(in_features, CLASSES))
    layers.append(nn.LogSoftmax(dim=1))

    return nn.Sequential(*layers)


def get_mnist():
    # Load FashionMNIST dataset.
    train_loader = DataLoader(train, batch_size=100, shuffle=True)
    test_loader = DataLoader(test, batch_size=100, shuffle=True)

    return train_loader, test_loader


def objective(trial):
    # Generate the model.
    model = define_model(trial).to(DEVICE)

    # Generate the optimizers.
    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "SGD"])
    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    optimizer = getattr(optim, optimizer_name)(model.parameters(), lr=lr)

    # Get the FashionMNIST dataset.
    train_loader, valid_loader = get_mnist()

    # Training of the model.
    for epoch in range(EPOCHS):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            # Limiting training data for faster epochs.
            if batch_idx * BATCHSIZE >= N_TRAIN_EXAMPLES:
                break

            data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
            data = data.float()
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()

        # Validation of the model.
        model.eval()
        correct = 0
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(valid_loader):
                # Limiting validation data.
                if batch_idx * BATCHSIZE >= N_VALID_EXAMPLES:
                    break
                data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
                data = data.float()
                output = model(data)
                # Get the index of the max log-probability.
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()

        accuracy = correct / min(len(valid_loader.dataset), N_VALID_EXAMPLES)

        trial.report(accuracy, epoch)

        # Handle pruning based on the intermediate value.
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return accuracy


if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100, timeout=600)

    pruned_trials = study.get_trials(deepcopy=False, states=[TrialState.PRUNED])
    complete_trials = study.get_trials(deepcopy=False, states=[TrialState.COMPLETE])

    print("Study statistics: ")
    print("  Number of finished trials: ", len(study.trials))
    print("  Number of pruned trials: ", len(pruned_trials))
    print("  Number of complete trials: ", len(complete_trials))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: ", trial.value)

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))

import torch
import torch.nn as nn
import torch.optim as optim

class SimpleMLP(nn.Module):
    def __init__(self, input_size, output_size, n_units, dropout):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(input_size, n_units,bias=False)
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(n_units, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Parameters
input_size = 15  # Assuming MNIST dataset
output_size = 2    # Assuming 10 classes in the output
n_units = 121       # Number of units in the hidden layer
dropout = 0.27189041823456955  # Dropout probability
lr = 0.0626329711802311  # Learning rate

# Create the model
model = SimpleMLP(input_size, output_size, n_units, dropout)
model.to(device)
# Print the model architecture
print(model)

# Define the optimizer
optimizer = optim.Adam(model.parameters(), lr=lr)

# Define the loss function
criterion = nn.CrossEntropyLoss().to(device)

# Now, you can use this model for training on your dataset.

import torch
import torch.optim as optim
import torch.nn as nn
import matplotlib.pyplot as plt

# Assuming you have already defined train_loader, device, model, optimizer, loss, and total_batch

epochs = 50
costs = []
accuracies = []

x_axis = []
y1_axis = []
y2_axis = []

plot_interval = 3  # Adjust this value to control the spacing between epochs on the plot

for epoch in range(epochs):
    avg_cost = 0
    total_accuracy = 0
    for idx, data in enumerate(train_loader):
        x_train, y_train = data
        x_train = x_train.to(device).float()  # Convert input to float data type
        y_train = y_train.to(device).long()

        optimizer.zero_grad()
        pred = model(x_train)

        if pred.dtype != torch.float:
            pred = pred.float()


        cost = criterion(pred, y_train)  # Using the defined loss function

        correct_pred = torch.argmax(pred, 1) == y_train
        accuracy = correct_pred.float().mean()

        # Move tensors to the same device as model
        cost = cost.to(device)
        accuracy = accuracy.to(device)

        total_accuracy += accuracy.item()

        cost.backward()
        optimizer.step()

        # Append values for each batch
        if idx == len(train_loader) - 1 or epoch % plot_interval == 0:
            x_axis.append(epoch + idx / len(train_loader))  # Epoch + fraction of completion of current epoch
            y1_axis.append(cost.item())
            y2_axis.append(accuracy.item())  # Ensure accuracy is converted to a Python float

        avg_cost += cost / len(train_loader)
    avg_accuracy = total_accuracy / len(train_loader)
    costs.append(avg_cost.cpu().detach().numpy())
    accuracies.append(avg_accuracy)
    print("[Epoch:{}] cost = {:.4f} Training ACC: {:.2f}%".format(epoch + 1, avg_cost, avg_accuracy * 100))

# Plotting
fig, x1 = plt.subplots()
x1.set_xlabel("Epoch")
x1.set_ylabel("Cost")
x1.plot(x_axis, y1_axis, label="Cost")
x1.legend(loc="upper left")

x2 = x1.twinx()
x2.set_ylabel("ACC")
x2.plot(x_axis, y2_axis, color="orange", label="ACC")
x2.legend(loc="upper right")

plt.show()

model.eval()  # Set the model to evaluation mode

test_accuracy = 0

with torch.no_grad():
    for x_test, y_test in test_loader:
        x_test = x_test.to(device).float()  # Convert input to float data type
        y_test = y_test.to(device).long()

        pred = model(x_test)
        correct_pred = torch.argmax(pred, 1) == y_test
        accuracy = correct_pred.float().mean()
        test_accuracy += accuracy.item() * len(x_test)

# Calculate average test accuracy
test_accuracy /= len(test_loader.dataset)
print("Final Testing Accuracy: {:.2f}%".format(test_accuracy * 100))

def get_predictions(model, data_loader):
    model.eval()
    predictions = []
    ground_truth = []
    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs = inputs.float()
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            predictions.extend(preds.cpu().numpy())
            ground_truth.extend(labels.cpu().numpy())
    return predictions, ground_truth

# Get predictions for test data
test_predictions, test_ground_truth = get_predictions(model, test_loader)

# Calculate confusion matrix
conf_matrix = confusion_matrix(test_ground_truth, test_predictions)

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)