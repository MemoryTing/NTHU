## Model Prune
### Model：AlexNet
### Dataset：CIFAR-10
### Goal
Use pytorch to prune module, and try to implement part of network compression.
### Details
Use given prune rate of each layer to get the threshold weight. Set weights whose absolute value is less than threshold to 0.
Then retrain.
### Result of After Pruning
```
conv1.weight         | Nonzeros weight =   19515 /   23232 ( 84.00%) | Total_pruned =    3717 | Shape = (64, 3, 11, 11)
conv1.bias           | Nonzeros weight =      64 /      64 (100.00%) | Total_pruned =       0 | Shape = (64,)
conv2.weight         | Nonzeros weight =  116736 /  307200 ( 38.00%) | Total_pruned =  190464 | Shape = (192, 64, 5, 5)
conv2.bias           | Nonzeros weight =     192 /     192 (100.00%) | Total_pruned =       0 | Shape = (192,)
conv3.weight         | Nonzeros weight =  232243 /  663552 ( 35.00%) | Total_pruned =  431309 | Shape = (384, 192, 3, 3)
conv3.bias           | Nonzeros weight =     384 /     384 (100.00%) | Total_pruned =       0 | Shape = (384,)
conv4.weight         | Nonzeros weight =  327352 /  884736 ( 37.00%) | Total_pruned =  557384 | Shape = (256, 384, 3, 3)
conv4.bias           | Nonzeros weight =     256 /     256 (100.00%) | Total_pruned =       0 | Shape = (256,)
conv5.weight         | Nonzeros weight =  218235 /  589824 ( 37.00%) | Total_pruned =  371589 | Shape = (256, 256, 3, 3)
conv5.bias           | Nonzeros weight =     256 /     256 (100.00%) | Total_pruned =       0 | Shape = (256,)
fc1.weight           | Nonzeros weight =   94372 / 1048576 (  9.00%) | Total_pruned =  954204 | Shape = (4096, 256)
fc1.bias             | Nonzeros weight =    4096 /    4096 (100.00%) | Total_pruned =       0 | Shape = (4096,)
fc2.weight           | Nonzeros weight =  843437 / 16777216 (  5.03%) | Total_pruned = 15933779 | Shape = (4096, 4096)
fc2.bias             | Nonzeros weight =    4096 /    4096 (100.00%) | Total_pruned =       0 | Shape = (4096,)
fc3.weight           | Nonzeros weight =   10240 /   40960 ( 25.00%) | Total_pruned =   30720 | Shape = (10, 4096)
fc3.bias             | Nonzeros weight =      10 /      10 (100.00%) | Total_pruned =       0 | Shape = (10,)
----------------------------------------------------------------------
Alive: 1871484, Pruned weight: 18473166, Total: 20344650, Compression rate :      10.87x  ( 90.80% pruned)
```