# **EAS 595 Fundamental of Artificial Intelligence**

# Dhruv Patel(#50321707)

# Project 2
"""

import torch
import numpy as np
import pandas as pd
from torch.autograd import Variable
import torch.nn.functional as F
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
import os
import torch as th
from torch import nn, optim

"""# 1.Extract features values and Image Ids from the data:"""

data = pd.read_csv('data_csv.csv')
data.head()

cols = data.columns
cols.shape

x_data = data[cols[2:32]]
x_data.head()

x_data.shape

"""Encoding M and B into number(0 and 1)"""

y_data = data[cols[1]]
le = LabelEncoder()
y_data = np.array(le.fit_transform(y_data))
print(y_data)
y_data[:5], le.classes_

y_data.shape, x_data.values.shape

from sklearn.preprocessing import StandardScaler
from torch.autograd import Variable
import torch.utils.data as data_utils
import torch.nn.init as init

"""# 2.Apply feature scaling technique:"""

scaler = StandardScaler()
transformed = scaler.fit_transform(x_data)

# train = data_utils.TensorDataset(torch.from_numpy(transformed).float(),
#                                  torch.from_numpy(y_data.float())
# # transformed
# print(torch.from_numpy(x_data))
print(transformed)
print(x_data)

"""Converting into Tensor"""

x_data = Variable(torch.from_numpy(transformed))
y_data = Variable(torch.from_numpy(y_data))

print(type(x_data))
print(type(y_data))

"""# 3.Data Partitioning:"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size = 0.8)

"""## Create the model class"""

input_dim = 30
output_dim = 1

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.l1 = torch.nn.Linear(input_dim,output_dim)        
        self.sigmoid = torch.nn.Sigmoid()
        
    def forward(self, x):
      y_pred = self.sigmoid(self.l1(x))
      return y_pred
    
model = Model()

print(model)

x_train.float().size(), y_train.float().size(),x_test.float().size(), y_test.float().size()

"""# 4.Create Logisitic Regression Architecture using Pytorch library:

Instantiate the Loss Class:
We use the cross-entropy to compute the loss.
"""

criterion = torch.nn.BCELoss(reduction='sum')

"""Instatnitate the Optimizer Class:
The optimizer will be the learning algorithm we use. In this case, we will use the Stochastic Gradient Descent.
"""

optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

"""Train the Model"""

print(x_data)
print(x_data.float())
#y_data.view(-1,1) # flatten the y_data sets

for epochs in range(1000):
    y_pred = model(x_train.float())
    loss = criterion(y_pred, y_train.view(-1,1).float())
    print('Epoch',epochs,'Loss:',loss.item())
    optimizer.zero_grad()
    loss.backward(retain_graph=True)
    optimizer.step()

x_train.data[0]

model.double().forward(x_test.data[25]) > 0.5, y_test[25]
model.double().forward(x_test.data[55]) > 0.5, y_test[55]
pred = model.double().forward(x_test) > 0.5
pred.numpy()[:5]
a = pred.numpy()
b = y_test.numpy()
pred.numpy().reshape(-1).shape, y_data.numpy().shape

"""Here is the confusion matrix of test data.
From confusion matrix, 38(TP) targets are Malign and 1(FP) Malign is considered as Benign. And 69(TN) targets are benign and 6(FN) Benign is considered as Malign.
"""

import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
c = confusion_matrix(a,b)
sns.heatmap(c, annot=True, xticklabels=le.classes_, yticklabels=le.classes_);

"""By using PyTorch Library, we get accuracy of 94%.

It is 86% correctly classified and it predicts 97% corrected value(True Positive/Negative, False Positive/ Negative).

There 1000 integration(epochs) in LogisticRegression library.
"""

print(classification_report(a,b))

"""# 5.Connect to the workers of the hospitals for training:"""

!pip install torch==1.3.0 torchvision==0.4.1

!pip install tf-encrypted

! URL="https://github.com/openmined/PySyft.git" && FOLDER="PySyft" && if [ ! -d $FOLDER ]; then git clone -b dev --single-branch $URL; else (cd $FOLDER && git pull $URL && cd ..); fi;

!cd PySyft; python setup.py install  > /dev/null

import os
import sys
module_path = os.path.abspath(os.path.join('./PySyft'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
!pip install --upgrade --force-reinstall lz4
!pip install --upgrade --force-reinstall websocket
!pip install --upgrade --force-reinstall websockets
!pip install --upgrade --force-reinstall zstd
!conda install

import syft as sy
hook = sy.TorchHook(th)

"""## Generate Virtual Workers"""

ECMC = sy.VirtualWorker(hook, id="ECMC")
BuffaloGeneral = sy.VirtualWorker(hook, id="BuffaloGeneral")

"""# 6.Send the data to the workers of the hospitals for training:"""

data_ECMC_train = x_train[0:227].send(ECMC)
target_ECMC_train = y_train[0:227].send(ECMC)

data_BuffaloGeneral_train = x_train[228:455].send(BuffaloGeneral).float()
target_BuffaloGeneral_train = y_train[228:455].send(BuffaloGeneral).float()
x_test.shape, y_test.shape

data_ECMC_test = x_test[0:227].send(ECMC)
target_ECMC_test = y_test[0:227].send(ECMC)
data_BuffaloGeneral_test = x_test[228:455].send(BuffaloGeneral).float()
target_BuffaloGeneral_test = y_test[228:455].send(BuffaloGeneral).float()

datasets_train = [(data_ECMC_train,target_ECMC_train), (data_BuffaloGeneral_train,target_BuffaloGeneral_train)]
_data_train, _target_train = datasets_train

"""## 7. Training and Testeing the Fadared Logistic Regression Model"""

def train():

  model = Model()
  opt = torch.optim.SGD(params=model.parameters(), lr=0.1)
  criterion = torch.nn.BCELoss(reduction='sum')
  for iter in range(1000):

    for _data, _target in datasets_train:

      # send model to the data
      model = model.send(_data.location)

      # do normal training
      opt.zero_grad()
      pred = model(_data.float())
      _loss = criterion(pred, _target.view(-1,1).float())
      _loss.backward()
      opt.step()

      # get smarter model back
      model = model.get()
      target_value = _target
      print(_loss.get())

train()

datasets_test = [(data_ECMC_test,target_ECMC_test), (data_BuffaloGeneral_test,target_BuffaloGeneral_test)]
datasets_test

def test():
    
    test_loss = 0
    for _data, _target in datasets_test:
      # send model to the data
      model = model.send(_data.location)
      y_pred = model(_data)
      test_loss += F.mse_loss(y_pred.view(-1), _target, reduction='sum').item()
      prediction = y_pred.data.max(1, keepdim=True)[1]
      # getting back the model
      model = model.get()
    test_loss /= len(test_loader.dataset)
    print('Test set: Average loss: {:.4f}'.format(test_loss))
    print(prediction)

test()
for epoch in range(10):

    federated_model = train()
    test()

"""## 8.Results"""

def accuracy_calc(y,y_pred):
    #True Positive --> Actual = 1, Predicted = 1
    #True Negative --> Actual = 0, Predicted = 0
    #False Positive--> Actual = 1, Predicted = 0
    #False Negative--> Actual = 0, Predicted = 1
    c_matrix=confusion_matrix(y, np.round(y_pred))
    tp=c_matrix[1][1]
    fn=c_matrix[1][0]
    fp=c_matrix[0][1]
    tn=c_matrix[0][0]
    accuracy=(tp+tn)/(tp+tn+fp+fn)
    precision=tp/(tp+fp)
    recall=tp/(tp+fn)
    return c_matrix,accuracy,precision,recall

"""Accuaracy, Precision, Recall"""

c_matrix,accuracy,precision,recall=accuracy_calc(_target_value,prediction)
print('-->Accuracy:',accuracy)
print('-->Precision:',precision)
print('-->Recall:',recall)

"""Confusion Matrix"""

print('-->Confusion Matrix of Test data')
print(np.transpose(c_matrix))
