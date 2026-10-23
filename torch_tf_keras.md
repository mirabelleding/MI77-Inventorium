# PyTorch, TensorFlow & Keras

**Scope:** Deep learning fundamentals; comparative framework architecture; PyTorch tensors, autograd, models, data loaders and training; TensorFlow tensors, `GradientTape`, `tf.function` and `tf.data`; Keras 3 multi-backend APIs, model-building, callbacks, training and saving; CNNs, recurrent models, attention, reproducibility, deployment, and performance.

**Version note:** Target modern PyTorch 2.x, TensorFlow 2.x, and **Keras 3**. Certain acceleration and deployment APIs depend on hardware, operating system, and versions. Examples are CPU-compatible unless they explicitly select a supported accelerator. TensorFlow is a framework; Keras 3 is a high-level API that can use TensorFlow, PyTorch, or JAX as its backend (and supports an OpenVINO inference-only backend).

## Table of contents

1. [What each library does](#1-what-each-library-does)
2. [Framework architecture and comparison](#2-framework-architecture-and-comparison)
3. [Installation, environments, and versions](#3-installation-environments-and-versions)
4. [Neural network mathematics and terminology](#4-neural-network-mathematics-and-terminology)
5. [Tensor shapes, batches, and model inputs](#5-tensor-shapes-batches-and-model-inputs)
6. [PyTorch: tensor fundamentals](#6-pytorch-tensor-fundamentals)
7. [PyTorch: autograd and computational graphs](#7-pytorch-autograd-and-computational-graphs)
8. [PyTorch: modules and model construction](#8-pytorch-modules-and-model-construction)
9. [PyTorch: datasets and loaders](#9-pytorch-datasets-and-loaders)
10. [PyTorch: losses, optimizers, and schedulers](#10-pytorch-losses-optimizers-and-schedulers)
11. [PyTorch: complete training and evaluation loop](#11-pytorch-complete-training-and-evaluation-loop)
12. [PyTorch: devices, precision, and performance](#12-pytorch-devices-precision-and-performance)
13. [PyTorch: persistence, compilation, and distributed concepts](#13-pytorch-persistence-compilation-and-distributed-concepts)
14. [TensorFlow: tensors and variables](#14-tensorflow-tensors-and-variables)
15. [TensorFlow: automatic differentiation](#15-tensorflow-automatic-differentiation)
16. [TensorFlow: graph execution and `tf.function`](#16-tensorflow-graph-execution-and-tffunction)
17. [TensorFlow: `tf.data` input pipelines](#17-tensorflow-tfdata-input-pipelines)
18. [TensorFlow: complete low-level training loop](#18-tensorflow-complete-low-level-training-loop)
19. [TensorFlow: performance and distribution](#19-tensorflow-performance-and-distribution)
20. [Keras 3: backend model and `keras.ops`](#20-keras-3-backend-model-and-kerasops)
21. [Keras: `Sequential` and Functional APIs](#21-keras-sequential-and-functional-apis)
22. [Keras: model subclassing and custom layers](#22-keras-model-subclassing-and-custom-layers)
23. [Keras: `compile`, `fit`, `evaluate`, and `predict`](#23-keras-compile-fit-evaluate-and-predict)
24. [Keras: callbacks, metrics, and regularization](#24-keras-callbacks-metrics-and-regularization)
25. [Keras: saving, loading, and exporting](#25-keras-saving-loading-and-exporting)
26. [The same neural network in all three styles](#26-the-same-neural-network-in-all-three-styles)
27. [Convolutional neural networks](#27-convolutional-neural-networks)
28. [Sequences, recurrent networks, and attention](#28-sequences-recurrent-networks-and-attention)
29. [Training concepts and failure modes](#29-training-concepts-and-failure-modes)
30. [NumPy, Pandas, and scikit-learn interoperability](#30-numpy-pandas-and-scikit-learn-interoperability)
31. [API maps: PyTorch](#31-api-maps-pytorch)
32. [API maps: TensorFlow](#32-api-maps-tensorflow)
33. [API maps: Keras](#33-api-maps-keras)
34. [Decision guide and common pitfalls](#34-decision-guide-and-common-pitfalls)
35. [Practice exercises with solutions](#35-practice-exercises-with-solutions)
36. [Official documentation and learning path](#36-official-documentation-and-learning-path)
---

## 1. What each library does

| Tool | Primary abstraction | Main advantage |
|---|---|---|
| PyTorch | `torch.Tensor`, `torch.nn.Module` | Flexible tensor/autograd/model control |
| TensorFlow | `tf.Tensor`, `tf.Variable`, `tf.Module` | Tensor computation, graph execution, ML infrastructure |
| Keras 3 | `keras.Layer`, `keras.Model` | Higher-level reusable model and training APIs |

**Important:** These are not simply three interchangeable packages. PyTorch and TensorFlow are complete tensor/autograd frameworks. Keras is a framework-agnostic high-level interface that can delegate computation to different backends.

```text
                 Your model code
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
  Native PyTorch  Native TensorFlow  Keras 3 APIs
         │             │             │
         │             │       ┌─────┼─────┐
         │             │       ▼     ▼     ▼
         │             │     Torch   TF   JAX
         ▼             ▼             ▼
       Tensor operations, automatic differentiation,
       optimized kernels, device execution
```

Keras can train on PyTorch and TensorFlow backends, but native framework code may provide more direct access to low-level backend features.

---

## 2. Framework architecture and comparison

| Feature | PyTorch | TensorFlow | Keras 3 |
|---|---|---|---|
| Tensor class | `torch.Tensor` | `tf.Tensor` | Backend tensor through Keras API |
| Trainable state | `nn.Parameter` | `tf.Variable` | `add_weight()` in `Layer` |
| Model interface | `nn.Module` | `tf.Module`, `tf.keras.Model` | `keras.Model` |
| Derivatives | `backward()`, `autograd.grad()` | `tf.GradientTape()` | Handled by backend; built-in `fit()` |
| Training control | Explicit by default | Explicit or Keras | High-level by default; customizable |
| Data pipelines | `Dataset`, `DataLoader` | `tf.data.Dataset` | Can consume several compatible input pipelines |
| Save common model state | `state_dict()` | Checkpoints / SavedModel | `.keras` format |
| Compile for optimization | `torch.compile` | `tf.function` / XLA options | Backend-dependent |
| Production | PyTorch serving/export ecosystem | TensorFlow serving/edge ecosystem | Backend/export dependent |

**Use PyTorch** for explicit gradients, custom model engineering, and many modern deep-learning workflows. **Use TensorFlow** when TensorFlow-native pipelines, serving, or distribution are central. **Use Keras** for concise model construction, training, and rapid experimentation. No framework is universally fastest.

---

## 3. Installation, environments, and versions

### 3.1 Packages

```bash
python -m pip install torch torchvision torchaudio
python -m pip install tensorflow
python -m pip install keras
```

PyTorch GPU installation varies by CUDA/ROCm/platform. Use the official installation selector for accelerator-specific packages. TensorFlow GPU availability is likewise operating-system- and accelerator-dependent.

### 3.2 Verify versions

```python
import torch

print(torch.__version__)
print(torch.cuda.is_available())
```

```python
import tensorflow as tf

print(tf.__version__)
print(tf.config.list_physical_devices("GPU"))
```

```python
import keras

print(keras.__version__)
print(keras.backend.backend())
```

### 3.3 Keras backend selection

**In a new Python process, before importing Keras:**

```python
import os

os.environ["KERAS_BACKEND"] = "torch"

import keras

print(keras.backend.backend())
```

Alternative valid values for training include `"tensorflow"` and `"jax"`. Switching backend settings after importing Keras in a running process is not a reliable migration strategy; restart the process/kernel.

---

## 4. Neural network mathematics and terminology

### 4.1 Linear layer

For a row-wise feature matrix:

\[
Z = XW^T + b
\]

If `X` has shape `(batch, in_features)` and `W` has shape `(out_features, in_features)`, `Z` has shape `(batch, out_features)`.

### 4.2 Activation functions

| Function | Definition / role |
|---|---|
| ReLU | `max(0, x)`; simple nonlinearity |
| LeakyReLU | Small nonzero negative slope |
| GELU | Smooth nonlinearity common in transformers |
| Sigmoid | Maps real numbers into `(0, 1)` |
| Tanh | Maps into `(-1, 1)` |
| Softmax | Turns a vector of scores into a distribution over classes |
| SiLU / Swish | `x * sigmoid(x)` |

### 4.3 Forward pass, loss, gradients, optimizer

```text
Input X
  │
  ▼
Model f(X; θ)
  │
  ▼
Predictions
  │
  ▼
Loss L(predictions, target)
  │
  ▼
Automatic differentiation ∂L/∂θ
  │
  ▼
Optimizer updates θ
```

Gradient descent:

\[
\theta_{t+1}=\theta_t-\eta\nabla_\theta L(\theta_t)
\]

- `θ`: trainable weights and biases.
- `η`: learning rate.
- `epoch`: one pass through training examples.
- `batch`: subset of training examples processed per update.
- `iteration`/`step`: typically one parameter update.
- `loss`: optimization objective.
- `metric`: evaluation quantity, not necessarily differentiable.

### 4.4 Recommended outputs and losses

| Task | Network output | Training loss | Prediction interpretation |
|---|---|---|---|
| Regression | `(..., 1)` raw real values | MSE/MAE/Huber | Numeric output |
| Binary classification | `(..., 1)` logit | BCE with logits | Sigmoid then threshold |
| Multiclass classification | `(..., C)` logits | Cross-entropy from logits | Softmax then argmax |
| Multilabel classification | `(..., C)` independent logits | BCE with logits | Sigmoid per class |

Do **not** apply sigmoid before `BCEWithLogitsLoss` or softmax before `CrossEntropyLoss`; these losses incorporate numerically stable activation handling.

---

## 5. Tensor shapes, batches, and model inputs

| Data type | Common shape convention |
|---|---|
| Tabular MLP input | `(batch, features)` |
| Binary regression target | `(batch, 1)` |
| Multiclass label IDs | `(batch,)` |
| PyTorch image (channels-first) | `(batch, channels, height, width)` |
| TensorFlow/Keras image (usually channels-last) | `(batch, height, width, channels)` |
| Sequence | `(batch, time, features)` |
| Attention token embeddings | `(batch, sequence_length, embedding_dim)` |

A model predicting one continuous target per sample should generally receive the target in compatible shape `(batch, 1)`, preventing accidental broadcasting of `(batch,)` against `(batch, 1)`.

```python
import torch

X = torch.randn(32, 10)
y = torch.randn(32, 1)

print(X.shape)
print(y.shape)
```

---

# Part I — PyTorch

## 6. PyTorch: tensor fundamentals

### 6.1 Tensor creation

```python
import numpy as np
import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
y = torch.zeros((2, 3))
z = torch.ones((2, 3))
r = torch.randn((2, 3))
i = torch.arange(0, 10, 2)

print(x.dtype)
print(x.shape)
print(y.shape, z.shape, r.shape)
print(i)
```

More creation functions: `torch.empty`, `torch.full`, `torch.linspace`, `torch.eye`, `torch.rand`, `torch.randint`, `torch.zeros_like`, `torch.ones_like`, `torch.randn_like`.

### 6.2 NumPy bridge

```python
import numpy as np
import torch

array = np.array([1.0, 2.0, 3.0], dtype=np.float32)
tensor = torch.from_numpy(array)

print(tensor)
print(tensor.numpy())
```

`torch.from_numpy` often shares CPU memory with the NumPy array. Use `.clone()` or appropriate copying when isolation is required; `.numpy()` normally requires a CPU tensor that is detached from autograd.

### 6.3 Tensor shape operations

| Method | What it does |
|---|---|
| `.reshape(...)` | Change shape; may copy if necessary |
| `.view(...)` | Reinterpret compatible contiguous layout |
| `.flatten(start_dim=...)` | Collapse dimensions |
| `.unsqueeze(dim)` | Insert size-1 dimension |
| `.squeeze(dim)` | Remove size-1 dimension |
| `.transpose(dim0, dim1)` | Swap two axes |
| `.permute(...)` | Reorder all axes |
| `.movedim(source, destination)` | Relocate selected axis |
| `.expand(...)` | Broadcast view (not actual replicated storage) |
| `.repeat(...)` | Repeat elements physically |
| `.contiguous()` | Request contiguous storage |
| `torch.stack(...)` | Create new axis by stacking |
| `torch.cat(...)` | Concatenate existing axis |

```python
import torch

x = torch.arange(24).reshape(2, 3, 4)

print(x[:, 1, ::2])
print(x.permute(2, 0, 1).shape)
print(x.flatten(start_dim=1).shape)
print(x.unsqueeze(0).shape)
print(torch.stack([x, x], dim=0).shape)
```

### 6.4 Broadcasting and matrix multiplication

```python
import torch

X = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
mean = torch.tensor([1.0, 3.0])
W = torch.tensor([[2.0], [1.0]])

print(X - mean)
print(X @ W)
print(torch.matmul(X, W))
```

`*` is elementwise multiplication; `@` is matrix multiplication.

### 6.5 Dtype and device

```python
import torch

x = torch.tensor([1.0, 2.0], dtype=torch.float32)

print(x.float())
print(x.double())
print(x.device)
print(x.to(dtype=torch.float64).dtype)
```

`torch.float32` is a common training dtype. `float64` may help numerical precision but typically costs memory and computation. Mixed precision can accelerate supported hardware workloads.

---

## 7. PyTorch: autograd and computational graphs

### 7.1 Basic derivative

```python
import torch

x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x

y.backward()

print(y.item())
print(x.grad.item())
```

Expected gradient: `8.0` because \(d(x^2+2x)/dx=2x+2\).

### 7.2 Gradients for vectors and scalar losses

```python
import torch

w = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
loss = (w ** 2).sum()

loss.backward()

print(w.grad)
```

Expected gradient `[2, 4, 6]`.

### 7.3 `autograd.grad()` without reading `.grad`

```python
import torch

x = torch.tensor([2.0, 3.0], requires_grad=True)
y = (x ** 3).sum()

gradient = torch.autograd.grad(y, x)[0]

print(gradient)
```

### 7.4 Chain rule and backpropagation

If \(y=f(g(x))\), autodiff applies the chain rule \(dy/dx=(df/dg)(dg/dx)\) through the recorded computation graph. Gradients flow through differentiable operations on tensors that require gradients.

### 7.5 Gradient accumulation

```python
import torch

w = torch.tensor(2.0, requires_grad=True)

(w ** 2).backward()
print(w.grad)

(w ** 3).backward()
print(w.grad)

w.grad.zero_()
print(w.grad)
```

Gradients **accumulate** by default; optimizers do not clear them unless told to.

### 7.6 Evaluation contexts

```python
import torch

x = torch.randn(3, requires_grad=True)

with torch.no_grad():
    y = x ** 2

with torch.inference_mode():
    z = x * 3

print(y.requires_grad)
print(z.requires_grad)
```

`inference_mode` can offer additional inference optimizations, but has stricter behavior than `no_grad` for tensors subsequently used in autograd computations.

### 7.7 Common autograd pitfalls

- In-place operations can invalidate saved tensors needed for backward computation.
- `.item()` extracts a Python number and breaks the gradient path.
- `.detach()` disconnects a tensor from the autograd graph.
- `torch.no_grad()` disables gradient recording in the block.
- Calling `.backward()` twice through the same graph may require `retain_graph=True`, but often the better answer is to recompute the forward pass.
- Non-leaf tensors ordinarily do not retain `.grad` unless `.retain_grad()` is called.

---

## 8. PyTorch: modules and model construction

### 8.1 `nn.Module`

A module encapsulates learnable parameters, child layers, forward computation, and state serialization.

```python
import torch
from torch import nn


class MLP(nn.Module):

    def __init__(self, input_features: int, hidden_units: int = 32):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_features, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


model = MLP(input_features=10)

print(model)
print(model(torch.randn(5, 10)).shape)
```

### 8.2 `nn.Parameter` and buffers

```python
import torch
from torch import nn


class Affine(nn.Module):

    def __init__(self):
        super().__init__()
        self.scale = nn.Parameter(torch.ones(1))
        self.register_buffer("offset", torch.zeros(1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.scale * x + self.offset


model = Affine()

print(dict(model.named_parameters()).keys())
print(dict(model.named_buffers()).keys())
```

A `Parameter` is trainable by default; buffers are tracked state but not optimizer parameters by default.

### 8.3 Inspect model architecture

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 2))

print(list(model.parameters()))
print(dict(model.named_modules()).keys())
print(model.state_dict().keys())
print(sum(p.numel() for p in model.parameters()))
```

### 8.4 `train()` versus `eval()`

`model.train()` puts relevant layers such as dropout and batch normalization into training mode. `model.eval()` sets evaluation mode. Neither automatically disables gradients, so pair evaluation with `torch.no_grad()` or `torch.inference_mode()`.

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(5, 5), nn.Dropout(0.5))

model.train()
train_output = model(torch.ones(2, 5))

model.eval()
with torch.inference_mode():
    eval_output = model(torch.ones(2, 5))

print(train_output.shape, eval_output.shape)
```

### 8.5 Important layer families

| Layer | Purpose |
|---|---|
| `nn.Linear` | Fully connected mapping |
| `nn.Conv1d`, `nn.Conv2d`, `nn.Conv3d` | Convolution |
| `nn.MaxPool2d`, `nn.AvgPool2d` | Pooling |
| `nn.BatchNorm1d`, `nn.BatchNorm2d` | Batch normalization |
| `nn.LayerNorm` | Per-sample layer normalization |
| `nn.Dropout` | Stochastic regularization |
| `nn.Embedding` | Integer index → dense vector |
| `nn.LSTM`, `nn.GRU`, `nn.RNN` | Recurrent sequence layers |
| `nn.MultiheadAttention` | Attention |
| `nn.TransformerEncoder` | Transformer encoder stack |
| `nn.Sequential`, `nn.ModuleList`, `nn.ModuleDict` | Composition and module registration |

`ModuleList` registers nested layers but does not itself define forward composition; you still implement iteration in `forward`.

---

## 9. PyTorch: datasets and loaders

### 9.1 TensorDataset and DataLoader

```python
import torch
from torch.utils.data import TensorDataset, DataLoader

X = torch.randn(100, 8)
y = torch.randn(100, 1)

dataset = TensorDataset(X, y)
loader = DataLoader(dataset, batch_size=16, shuffle=True)

for features, targets in loader:
    print(features.shape, targets.shape)
    break
```

### 9.2 Custom dataset

```python
import torch
from torch.utils.data import Dataset


class TabularDataset(Dataset):

    def __init__(self, X: torch.Tensor, y: torch.Tensor):
        self.X = X
        self.y = y

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.X[index], self.y[index]


dataset = TabularDataset(torch.randn(20, 4), torch.randint(0, 2, (20,)))
print(dataset[0])
```

### 9.3 `DataLoader` parameters

| Parameter | Purpose |
|---|---|
| `batch_size` | Number of examples per minibatch |
| `shuffle` | Shuffle sample indices each epoch |
| `num_workers` | Multiprocess loading workers |
| `pin_memory` | Pinned CPU memory, often useful for GPU transfer |
| `drop_last` | Drop incomplete final batch |
| `collate_fn` | Combine individual samples into a batch |
| `sampler` | Explicit sampling policy |
| `persistent_workers` | Keep worker processes across epochs |

For small or platform-constrained projects, start with `num_workers=0`. Worker spawning behavior differs across operating systems; multiprocess loading often needs a guarded Python script entry point.

### 9.4 Train/validation dataset split

```python
import torch
from torch.utils.data import TensorDataset, random_split

X = torch.randn(100, 5)
y = torch.randn(100, 1)

dataset = TensorDataset(X, y)
train_set, validation_set = random_split(
    dataset,
    [80, 20],
    generator=torch.Generator().manual_seed(42),
)

print(len(train_set), len(validation_set))
```

For time series, do not use random splitting when it violates chronology.

---

## 10. PyTorch: losses, optimizers, and schedulers

### 10.1 Loss API map

| Loss | Task |
|---|---|
| `nn.MSELoss()` | Regression; squared error |
| `nn.L1Loss()` | Regression; absolute error |
| `nn.SmoothL1Loss()` | Robust-ish regression |
| `nn.HuberLoss()` | Huber regression |
| `nn.BCEWithLogitsLoss()` | Binary/multilabel classification from logits |
| `nn.CrossEntropyLoss()` | Multiclass classification from logits |
| `nn.NLLLoss()` | Negative log-likelihood on log-probabilities |
| `nn.KLDivLoss()` | KL divergence formulation |
| `nn.CosineEmbeddingLoss()` | Cosine similarity learning |
| `nn.TripletMarginLoss()` | Metric learning |

### 10.2 Binary versus multiclass shapes

Binary:

```python
import torch
from torch import nn

logits = torch.tensor([[0.3], [-1.1], [1.5]])
target = torch.tensor([[1.0], [0.0], [1.0]])

loss = nn.BCEWithLogitsLoss()(logits, target)
probs = torch.sigmoid(logits)

print(loss.item())
print(probs)
```

Multiclass:

```python
import torch
from torch import nn

logits = torch.tensor([[1.0, 2.0, 0.0], [2.0, 0.0, 1.0]])
labels = torch.tensor([1, 0], dtype=torch.long)

loss = nn.CrossEntropyLoss()(logits, labels)
probabilities = torch.softmax(logits, dim=1)

print(loss.item())
print(probabilities)
```

### 10.3 Optimizers

| Optimizer | Idea |
|---|---|
| `torch.optim.SGD` | Stochastic gradient descent, optionally momentum |
| `torch.optim.Adam` | Adaptive first/second moments |
| `torch.optim.AdamW` | Adam with decoupled weight decay |
| `torch.optim.RMSprop` | Adaptive learning-rate approach |
| `torch.optim.Adagrad` | Cumulative adaptive step sizes |
| `torch.optim.LBFGS` | Quasi-Newton optimization; closure-based |

```python
import torch
from torch import nn

model = nn.Linear(4, 1)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

print(optimizer.param_groups[0]["lr"])
```

### 10.4 Learning-rate schedulers

| Scheduler | Role |
|---|---|
| `StepLR` | Reduce LR every specified epoch count |
| `MultiStepLR` | Reduce LR at milestones |
| `ExponentialLR` | Exponential decay |
| `CosineAnnealingLR` | Cosine schedule |
| `ReduceLROnPlateau` | Adjust LR when monitored metric stagnates |
| `OneCycleLR` | Per-step one-cycle policy |
| `LambdaLR` | User-specified schedule |

```python
import torch
from torch import nn

model = nn.Linear(4, 1)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

for epoch in range(12):
    optimizer.step()
    scheduler.step()

print(scheduler.get_last_lr())
```

The scheduler update frequency (per epoch or per batch) depends on scheduler. In real training, `optimizer.step()` must follow computed gradients; the snippet illustrates the LR schedule only.

---

## 11. PyTorch: complete training and evaluation loop

This is a standalone synthetic **binary classification** example. The network outputs logits; targets have shape `(batch, 1)` and dtype `float32`.

```python
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


torch.manual_seed(42)
rng = np.random.default_rng(42)

X_np = rng.normal(size=(800, 10)).astype(np.float32)
logits_np = X_np[:, :3] @ np.array([1.5, -2.0, 0.8], dtype=np.float32)
p_np = 1 / (1 + np.exp(-logits_np))
y_np = rng.binomial(1, p_np).astype(np.float32).reshape(-1, 1)

X = torch.from_numpy(X_np)
y = torch.from_numpy(y_np)

train_dataset = TensorDataset(X[:640], y[:640])
validation_dataset = TensorDataset(X[640:], y[640:])

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
validation_loader = DataLoader(validation_dataset, batch_size=64)

model = nn.Sequential(
    nn.Linear(10, 32),
    nn.ReLU(),
    nn.Linear(32, 1),
)

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)

for epoch in range(20):
    model.train()
    running_loss = 0.0

    for features, target in train_loader:
        optimizer.zero_grad()
        prediction_logits = model(features)
        loss = criterion(prediction_logits, target)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * features.size(0)

    model.eval()
    correct = 0
    total = 0

    with torch.inference_mode():
        for features, target in validation_loader:
            probabilities = torch.sigmoid(model(features))
            predictions = (probabilities >= 0.5).float()
            correct += (predictions == target).sum().item()
            total += target.numel()

    print(epoch + 1, running_loss / len(train_dataset), correct / total)
```

The data is synthetic and independently generated by row; for real time-dependent data, use chronological splits. This loop shows the essential framework responsibilities: data loading, gradient clearing, forward pass, loss, backward pass, parameter update, and separate inference mode.

### 11.1 Why weight training loss by batch size?

`running_loss += loss.item() * features.size(0)` correctly accumulates mean batch loss by sample count, even when the last batch is smaller. Dividing by `len(train_dataset)` produces the sample-weighted epoch mean for per-example losses.

### 11.2 Gradient clipping

```python
import torch
from torch import nn

model = nn.Linear(4, 1)
loss = (model(torch.randn(8, 4)) ** 2).mean()

loss.backward()

total_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
print(total_norm)
```

Clipping can mitigate exploding gradients, particularly in recurrent or deep networks. It does not cure incorrect loss functions or severe scaling issues.

---

## 12. PyTorch: devices, precision, and performance

### 12.1 CPU/GPU/MPS device selection

```python
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

x = torch.randn(3, 4, device=device)
print(device, x.device)
```

`mps` is Apple Metal acceleration on supported macOS hardware. It is not an iPad GPU execution backend for standard PyTorch scripts.

### 12.2 Move model and batch together

```python
import torch
from torch import nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = nn.Linear(5, 2).to(device)
features = torch.randn(4, 5).to(device)

print(model(features).device)
```

Mixing CPU input tensors and GPU model parameters generally causes a device mismatch error.

### 12.3 Automatic mixed precision (CUDA example)

```python
import torch
from torch import nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = nn.Linear(4, 1).to(device)
optimizer = torch.optim.Adam(model.parameters())
x = torch.randn(8, 4, device=device)
y = torch.randn(8, 1, device=device)

with torch.autocast(device_type=device.type, enabled=device.type == "cuda"):
    loss = nn.MSELoss()(model(x), y)

loss.backward()
optimizer.step()
```

For CUDA float16 training at scale, `torch.amp.GradScaler` is often important to prevent underflow. The simple snippet uses autocasting only to illustrate the context manager. Do not assume every operation is safe or faster under lower precision.

### 12.4 `torch.compile`

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(10, 20), nn.ReLU(), nn.Linear(20, 1))

compiled = torch.compile(model)
print(compiled(torch.randn(4, 10)).shape)
```

Compilation can speed steady-state execution, but the first call incurs tracing/compilation overhead. It is not always beneficial for very small models, rapidly changing shapes, or unsupported operation patterns. TorchScript is no longer the recommended actively developed compiler path for new general-purpose PyTorch optimization projects.

---

## 13. PyTorch: persistence, compilation, and distributed concepts

### 13.1 Model state dict

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(3, 8), nn.ReLU(), nn.Linear(8, 1))

torch.save(model.state_dict(), "model_weights.pt")

restored = nn.Sequential(nn.Linear(3, 8), nn.ReLU(), nn.Linear(8, 1))
restored.load_state_dict(torch.load("model_weights.pt", map_location="cpu", weights_only=True))
restored.eval()

print(restored(torch.randn(2, 3)).shape)
```

This saves parameters and registered buffers, **not** the Python architecture definition. Recreate compatible module structure before loading.

### 13.2 Checkpoint optimizer state and epoch

```python
import torch
from torch import nn

model = nn.Linear(5, 1)
optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)

checkpoint = {
    "epoch": 10,
    "model_state": model.state_dict(),
    "optimizer_state": optimizer.state_dict(),
}

torch.save(checkpoint, "checkpoint.pt")

restored = torch.load("checkpoint.pt", map_location="cpu", weights_only=True)
model.load_state_dict(restored["model_state"])
optimizer.load_state_dict(restored["optimizer_state"])
```

For faithful training resumes, also consider saving scheduler state, mixed-precision scaler state, RNG states, and data-sampler position.

### 13.3 Distributed training overview

- **Data parallelism:** replicate a model across workers and process different minibatches.
- **Model parallelism:** distribute parameters and operations across devices.
- **`DistributedDataParallel` (DDP):** synchronizes gradients across processes; generally preferred to legacy `DataParallel` for multi-GPU training.
- **FSDP and other sharding:** partition model state to reduce per-device memory.
- **`torch.distributed`** provides communication and parallel training infrastructure.

Most introductory models do not require distributed training.

---

# Part II — TensorFlow

## 14. TensorFlow: tensors and variables

### 14.1 Tensor operations

```python
import tensorflow as tf

x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
y = tf.ones((2, 2))

print(x.shape)
print(tf.matmul(x, y))
print(tf.reduce_mean(x))
print(tf.reshape(x, (4,)))
```

### 14.2 `tf.Tensor` versus `tf.Variable`

`tf.Tensor` represents an immutable tensor value. `tf.Variable` stores mutable state, commonly trainable model parameters.

```python
import tensorflow as tf

weight = tf.Variable([1.0, 2.0])
weight.assign([3.0, 4.0])
weight.assign_add([1.0, 1.0])

print(weight.numpy())
```

### 14.3 NumPy interoperability

```python
import numpy as np
import tensorflow as tf

array = np.array([1.0, 2.0, 3.0], dtype=np.float32)
tensor = tf.convert_to_tensor(array)

print(tensor.numpy())
print(tf.cast(tensor, tf.float64))
```

`tensor.numpy()` is available for eager tensors; tensors inside compiled graph contexts cannot always be converted to NumPy during tracing/execution.

### 14.4 Indexing and shape operations

```python
import tensorflow as tf

x = tf.reshape(tf.range(24), (2, 3, 4))

print(x[:, 1, ::2])
print(tf.transpose(x, perm=(2, 0, 1)).shape)
print(tf.expand_dims(x, axis=0).shape)
print(tf.concat([x, x], axis=0).shape)
print(tf.stack([x, x], axis=0).shape)
```

---

## 15. TensorFlow: automatic differentiation

### 15.1 `tf.GradientTape`

```python
import tensorflow as tf

x = tf.Variable(3.0)

with tf.GradientTape() as tape:
    y = x ** 2 + 2 * x

gradient = tape.gradient(y, x)

print(y.numpy())
print(gradient.numpy())
```

### 15.2 Multiple trainable variables

```python
import tensorflow as tf

w = tf.Variable(2.0)
b = tf.Variable(1.0)

with tf.GradientTape() as tape:
    y = (w * 3.0 + b - 10.0) ** 2

gradients = tape.gradient(y, [w, b])

print([g.numpy() for g in gradients])
```

### 15.3 Higher-order derivatives

```python
import tensorflow as tf

x = tf.Variable(2.0)

with tf.GradientTape() as outer:
    with tf.GradientTape() as inner:
        y = x ** 3
    first = inner.gradient(y, x)

second = outer.gradient(first, x)

print(first.numpy())
print(second.numpy())
```

Expected first derivative at 2 = 12; second derivative at 2 = 12.

### 15.4 GradientTape rules

- A tape records operations performed in its context.
- Trainable `tf.Variable` objects are watched automatically by default.
- Other tensors may require `tape.watch(tensor)`.
- A nonpersistent tape normally supports only one call to `gradient`.
- Some operations are nondifferentiable or have undefined gradients.
- Higher-order derivatives require nested tapes or a suitably persistent tape.

---

## 16. TensorFlow: graph execution and `tf.function`

### 16.1 Eager versus traced function

```python
import tensorflow as tf


@tf.function
def f(x: tf.Tensor) -> tf.Tensor:
    return x ** 2 + 3 * x


print(f(tf.constant([1.0, 2.0])))
```

`@tf.function` traces Python-defined computation into reusable TensorFlow graphs where possible. This can optimize execution, but introduces graph semantics and potential retracing when input signatures vary.

### 16.2 Input signature

```python
import tensorflow as tf


@tf.function(input_signature=[tf.TensorSpec(shape=(None, 4), dtype=tf.float32)])
def predict_sum(x: tf.Tensor) -> tf.Tensor:
    return tf.reduce_sum(x, axis=1)


print(predict_sum(tf.ones((3, 4))))
```

Input signatures help specify allowable shapes/dtypes and control retracing.

### 16.3 `tf.cond` and `tf.while_loop`

```python
import tensorflow as tf

x = tf.constant(5)

y = tf.cond(x > 3, lambda: x * 2, lambda: x - 2)

print(y)
```

Use graph-native control flow when ordinary Python branching behaves unexpectedly under tracing. `tf.function`'s AutoGraph conversion can handle supported Python structures, but not all arbitrary Python side effects.

### 16.4 Retracing and Python side effects

Tracing may capture Python values and run Python code differently from eager execution. Avoid relying on `print()` side effects inside traced functions; `tf.print()` is graph compatible. Repeated tracing can be expensive.

---

## 17. TensorFlow: `tf.data` input pipelines

### 17.1 From tensors to batched datasets

```python
import tensorflow as tf

X = tf.random.normal((100, 8))
y = tf.random.uniform((100, 1))

dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(buffer_size=100, seed=42).batch(16).prefetch(tf.data.AUTOTUNE)

for features, targets in dataset.take(1):
    print(features.shape, targets.shape)
```

### 17.2 `map`, `cache`, `repeat`, `prefetch`

```python
import tensorflow as tf

values = tf.data.Dataset.range(10)

processed = (
    values
    .map(lambda x: tf.cast(x, tf.float32) ** 2)
    .batch(4)
    .prefetch(tf.data.AUTOTUNE)
)

for batch in processed:
    print(batch.numpy())
```

### 17.3 Important dataset methods

| API | Purpose |
|---|---|
| `Dataset.from_tensor_slices` | Slices tensors into samples |
| `Dataset.from_generator` | Build dataset from Python generator |
| `.map()` | Transform elements |
| `.filter()` | Keep matching elements |
| `.shuffle()` | Shuffle within buffer |
| `.batch()` | Combine samples |
| `.padded_batch()` | Batch variable-length records with padding |
| `.cache()` | Cache dataset results |
| `.prefetch()` | Overlap input work with model work |
| `.repeat()` | Repeat samples/dataset |
| `.take()` / `.skip()` | Select prefix / omit prefix |
| `.interleave()` | Interleave from multiple streams |
| `.apply()` | Apply dataset transformation |

Caching/shuffling/prefetching must respect memory and independence requirements. Repeating a dataset indefinitely requires control over steps per epoch.

---

## 18. TensorFlow: complete low-level training loop

This example trains a binary classifier using `tf.Variable`-managed Keras layer weights and a TensorFlow-native `GradientTape` loop.

```python
import numpy as np
import tensorflow as tf

rng = np.random.default_rng(42)
X = rng.normal(size=(500, 6)).astype(np.float32)
logits = X[:, 0] * 1.5 - X[:, 1] * 2.0
y = rng.binomial(1, 1 / (1 + np.exp(-logits))).astype(np.float32).reshape(-1, 1)

dataset = tf.data.Dataset.from_tensor_slices((X, y)).shuffle(500, seed=42).batch(32)

model = tf.keras.Sequential([
    tf.keras.Input(shape=(6,)),
    tf.keras.layers.Dense(24, activation="relu"),
    tf.keras.layers.Dense(1),
])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)

for epoch in range(10):
    metric = tf.keras.metrics.Mean()

    for features, target in dataset:
        with tf.GradientTape() as tape:
            predictions = model(features, training=True)
            loss = loss_fn(target, predictions)

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))
        metric.update_state(loss)

    print(epoch + 1, float(metric.result()))
```

`tf.keras` is TensorFlow's Keras integration. For new backend-agnostic Keras code, prefer direct `import keras` and `keras.ops` rather than mixing TensorFlow operations into custom Keras 3 layers.

---

## 19. TensorFlow: performance and distribution

### 19.1 Device inspection

```python
import tensorflow as tf

print(tf.config.list_physical_devices())
print(tf.config.list_physical_devices("GPU"))
```

### 19.2 Mixed precision (when hardware supports it)

```python
import tensorflow as tf

print(tf.keras.mixed_precision.global_policy())
```

A globally enabled mixed precision policy affects model layers and numeric behavior; confirm hardware support and loss/output dtype considerations before enabling it in production.

### 19.3 Distribution strategies

| Tool | Purpose |
|---|---|
| `tf.distribute.MirroredStrategy` | Synchronous multi-GPU on one machine |
| `tf.distribute.MultiWorkerMirroredStrategy` | Multiworker synchronized training |
| `tf.distribute.TPUStrategy` | TPU training |
| `tf.function` | Graph tracing and execution |
| `tf.data` | Optimized input loading |
| `tf.saved_model.save` | TensorFlow SavedModel serialization |

```python
import tensorflow as tf

strategy = tf.distribute.get_strategy()

print(strategy.num_replicas_in_sync)
```

Distributed training is a systems concern in addition to a model concern: data sharding, gradient reductions, recovery, and reproducibility become important.

---

# Part III — Keras 3

## 20. Keras 3: backend model and `keras.ops`

### 20.1 Keras is not exclusively TensorFlow

```text
keras.Model, keras.layers.*, keras.losses.*,
keras.optimizers.*, keras.metrics.*, keras.ops.*
                    │
                    ▼
       Selected backend at import time
             │       │       │
             ▼       ▼       ▼
         TensorFlow PyTorch  JAX
```

Keras 3 also supports an OpenVINO inference-only backend. Model portability depends on avoiding backend-specific calls in custom components and on feature compatibility.

### 20.2 Backend-agnostic tensor operations

```python
import keras
from keras import ops

x = ops.convert_to_tensor([[1.0, 2.0], [3.0, 4.0]])

print(ops.sum(x, axis=1))
print(ops.mean(x))
print(ops.matmul(x, ops.transpose(x)))
```

### 20.3 `keras.ops` reference map

| Function | Meaning |
|---|---|
| `ops.convert_to_tensor` | Create backend tensor |
| `ops.shape` | Tensor shape |
| `ops.reshape` | Reshape |
| `ops.transpose` | Permute axes |
| `ops.concatenate` | Concatenate |
| `ops.stack` | Add stack axis |
| `ops.sum`, `ops.mean` | Reductions |
| `ops.matmul` | Matrix multiplication |
| `ops.einsum` | Einstein summation |
| `ops.exp`, `ops.log`, `ops.sqrt` | Elementwise functions |
| `ops.softmax`, `ops.sigmoid` | Activations |
| `ops.binary_crossentropy` | Binary cross entropy |
| `ops.categorical_crossentropy` | Multiclass cross entropy |

### 20.4 Write a portable custom layer

```python
import keras
from keras import layers, ops


class SquareActivation(layers.Layer):

    def call(self, inputs):
        return ops.square(inputs)


model = keras.Sequential([
    keras.Input(shape=(4,)),
    layers.Dense(8),
    SquareActivation(),
    layers.Dense(1),
])

print(model.summary())
```

For portability, use `keras.ops` in custom `call` implementations instead of assuming tensors are `torch.Tensor` or `tf.Tensor`.

---

## 21. Keras: `Sequential` and Functional APIs

### 21.1 Sequential model

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(10,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(16, activation="relu"),
    layers.Dense(1),
])

model.summary()
```

Best when layers form a single linear stack.

### 21.2 Functional model

```python
import keras
from keras import layers

inputs = keras.Input(shape=(10,), name="features")
x = layers.Dense(32, activation="relu")(inputs)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(1, name="prediction")(x)

model = keras.Model(inputs=inputs, outputs=outputs)
model.summary()
```

The Functional API creates computational graphs that can branch, merge, reuse layers, or expose multiple outputs.

### 21.3 Multiple input branches

```python
import keras
from keras import layers

numeric_input = keras.Input(shape=(5,), name="numeric")
category_input = keras.Input(shape=(1,), dtype="int32", name="category")

numeric_features = layers.Dense(16, activation="relu")(numeric_input)
category_embedding = layers.Embedding(input_dim=20, output_dim=4)(category_input)
category_features = layers.Flatten()(category_embedding)

joined = layers.Concatenate()([numeric_features, category_features])
output = layers.Dense(1, activation="sigmoid")(joined)

model = keras.Model(
    inputs={"numeric": numeric_input, "category": category_input},
    outputs=output,
)

model.summary()
```

A feature's integer category IDs must lie in the embedding layer's valid range `[0, input_dim)`.

### 21.4 When to choose each model API

| API | Use |
|---|---|
| `keras.Sequential` | Simple single-path network |
| `keras.Model(inputs, outputs)` | Branching, shared layers, multiple inputs/outputs |
| Subclass `keras.Model` | Highly customized architecture/control flow |

---

## 22. Keras: model subclassing and custom layers

### 22.1 Custom dense-like layer

```python
import keras
from keras import layers, ops


class AffineLayer(layers.Layer):

    def __init__(self, units: int):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        self.kernel = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="glorot_uniform",
            trainable=True,
        )
        self.bias = self.add_weight(
            shape=(self.units,),
            initializer="zeros",
            trainable=True,
        )

    def call(self, inputs):
        return ops.matmul(inputs, self.kernel) + self.bias


layer = AffineLayer(3)
print(layer(ops.ones((2, 4))).shape)
```

A `Layer` tracks its weights when created through `add_weight()` or registered sublayers. Do not create fresh trainable weights on every forward `call`.

### 22.2 Subclass a whole model

```python
import keras
from keras import layers


class Regressor(keras.Model):

    def __init__(self, hidden_units: int = 32):
        super().__init__()
        self.hidden = layers.Dense(hidden_units, activation="relu")
        self.output_layer = layers.Dense(1)

    def call(self, inputs, training: bool = False):
        x = self.hidden(inputs)
        return self.output_layer(x)


model = Regressor(hidden_units=16)
print(model(keras.ops.ones((5, 8))).shape)
```

For saving/loading a portable custom class with full reconstruction, implement appropriate serialization configuration and registration where needed; built-in Functional/Sequential models are easier to serialize without custom code.

---

## 23. Keras: `compile`, `fit`, `evaluate`, and `predict`

### 23.1 Regression example

```python
import numpy as np
import keras
from keras import layers

rng = np.random.default_rng(42)
X = rng.normal(size=(300, 10)).astype("float32")
y = (2 * X[:, 0] - X[:, 1] + 0.1 * rng.normal(size=300)).astype("float32")

model = keras.Sequential([
    keras.Input(shape=(10,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(1),
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss="mse",
    metrics=["mae"],
)

history = model.fit(X, y, batch_size=32, epochs=10, validation_split=0.2, verbose=0)

print(history.history.keys())
print(model.evaluate(X[:20], y[:20], verbose=0))
print(model.predict(X[:3], verbose=0))
```

### 23.2 Binary classification and output-layer choices

**Version A — explicit sigmoid output:**

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(10,)),
    layers.Dense(24, activation="relu"),
    layers.Dense(1, activation="sigmoid"),
])

model.compile(
    optimizer="adam",
    loss=keras.losses.BinaryCrossentropy(from_logits=False),
    metrics=[keras.metrics.BinaryAccuracy()],
)
```

**Version B — raw logits output:**

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(10,)),
    layers.Dense(24, activation="relu"),
    layers.Dense(1),
])

model.compile(
    optimizer="adam",
    loss=keras.losses.BinaryCrossentropy(from_logits=True),
    metrics=[keras.metrics.BinaryAccuracy(threshold=0.0)],
)
```

**Important:** When the output is raw logits, `BinaryAccuracy(threshold=0.0)` uses the correct decision boundary in logit space. Ordinary `BinaryAccuracy()` defaults to a threshold of `0.5` and is suitable for sigmoid probabilities, not raw logits.

### 23.3 Multiclass classification with integer labels

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(12,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(4),
])

model.compile(
    optimizer="adam",
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)
```

For one-hot encoded labels, use `CategoricalCrossentropy`, not `SparseCategoricalCrossentropy`.

### 23.4 Keras metrics and return types

`model.fit()` returns a `History` object, usually with `.history` mapping epoch metrics to lists. `model.evaluate()` returns loss and configured metrics. `model.predict()` returns model predictions, not automatically calibrated class probabilities unless the model output is defined to be probabilities.

---

## 24. Keras: callbacks, metrics, and regularization

### 24.1 Key callbacks

| Callback | Purpose |
|---|---|
| `EarlyStopping` | End training when monitor stops improving |
| `ModelCheckpoint` | Save best/current model |
| `ReduceLROnPlateau` | Lower learning rate on plateau |
| `LearningRateScheduler` | User-specified schedule |
| `TensorBoard` | Training logs |
| `CSVLogger` | Append epoch metrics to CSV |
| `TerminateOnNaN` | Stop on invalid loss |
| `BackupAndRestore` | Recovery of certain interrupted runs |

### 24.2 Early stopping and checkpointing

```python
import keras

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
    ),
    keras.callbacks.ModelCheckpoint(
        filepath="best_model.keras",
        monitor="val_loss",
        save_best_only=True,
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
    ),
]
```

Use callbacks as `model.fit(..., validation_data=(X_val, y_val), callbacks=callbacks)` after constructing/compiling a model. Validation data should respect the real prediction task, especially chronology.

### 24.3 Regularization layers and penalties

```python
import keras
from keras import layers, regularizers

model = keras.Sequential([
    keras.Input(shape=(20,)),
    layers.Dense(64, activation="relu", kernel_regularizer=regularizers.l2(1e-4)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(1),
])
```

- `Dropout`: active during training, inactive at standard inference.
- `BatchNormalization`: maintains batch-dependent running statistics and behaves differently between training and inference.
- L1/L2 regularizers: add penalties to the objective.
- Early stopping: prevents continued fitting beyond monitored improvements.

### 24.4 Custom callback class

```python
import keras


class LearningRateLog(keras.callbacks.Callback):

    def on_epoch_end(self, epoch: int, logs: dict | None = None):
        print(epoch + 1, float(self.model.optimizer.learning_rate))
```

---

## 25. Keras: saving, loading, and exporting

### 25.1 Native Keras 3 format

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(4,)),
    layers.Dense(8, activation="relu"),
    layers.Dense(1),
])

model.save("model.keras")
restored = keras.models.load_model("model.keras")

print(restored.summary())
```

Keras 3 uses `.keras` as its recommended model-saving format. Saving a model in this format is different from exporting a TensorFlow SavedModel for serving.

### 25.2 Export a TensorFlow serving artifact

For a Keras model on a supported backend/export setup:

```python
model.export("saved_model_artifact", format="tf_saved_model")
```

TensorFlow SavedModel is intended for deployment and serving workflows. Keras 3 `keras.models.load_model()` does **not** directly reload TensorFlow SavedModel as a normal Keras model; use the `.keras` format for portable editable model reloads, or appropriate inference wrappers/export tooling for SavedModel.

### 25.3 Keras 2 to Keras 3 migration traps

- Use `import keras` for standalone multi-backend Keras 3 code.
- Set backend before import.
- Replace `tf.*` calls in portable custom layers with `keras.ops.*` equivalents where possible.
- Keras 3 `model.save()` should use `.keras` (or supported legacy `.h5`), not a bare SavedModel directory.
- For a TensorFlow SavedModel export, call `model.export()`.
- Legacy custom objects may require migration or registered serialization.
- TensorFlow's `tf.keras` integration is tied to installed TensorFlow/Keras compatibility; use one coherent environment.

---

## 26. The same neural network in all three styles

Target architecture: input width 10 → hidden 32/ReLU → output 1 raw logit.

### 26.1 Native PyTorch

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Linear(10, 32),
    nn.ReLU(),
    nn.Linear(32, 1),
)

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

X = torch.randn(64, 10)
y = torch.randint(0, 2, (64, 1)).float()

optimizer.zero_grad()
loss = criterion(model(X), y)
loss.backward()
optimizer.step()

print(loss.item())
```

### 26.2 Native TensorFlow training

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.Input(shape=(10,)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1),
])

optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)

X = tf.random.normal((64, 10))
y = tf.cast(tf.random.uniform((64, 1), maxval=2, dtype=tf.int32), tf.float32)

with tf.GradientTape() as tape:
    loss = loss_fn(y, model(X, training=True))

gradients = tape.gradient(loss, model.trainable_variables)
optimizer.apply_gradients(zip(gradients, model.trainable_variables))

print(float(loss))
```

### 26.3 Keras 3 high-level training

```python
import numpy as np
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(10,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(1),
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss=keras.losses.BinaryCrossentropy(from_logits=True),
)

X = np.random.default_rng(42).normal(size=(64, 10)).astype("float32")
y = np.random.default_rng(43).integers(0, 2, size=(64, 1)).astype("float32")

model.fit(X, y, epochs=3, batch_size=16, verbose=0)
print(model.predict(X[:3], verbose=0))
```

These are the **same architecture family**, not identical parameters, training paths, or guaranteed equal outputs. Framework initializers, RNG states, and numerical backends differ.

---

## 27. Convolutional neural networks

### 27.1 CNN concepts

A 2D convolution applies trainable local filters over spatial dimensions. Pooling reduces spatial resolution. Convolution has shared weights across positions.

PyTorch typically works with `(N,C,H,W)` by default; Keras/TensorFlow commonly use `(N,H,W,C)` by default. Converting axis order correctly is essential.

### 27.2 PyTorch CNN

```python
import torch
from torch import nn

model = nn.Sequential(
    nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(kernel_size=2),
    nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((1, 1)),
    nn.Flatten(),
    nn.Linear(16, 10),
)

images = torch.randn(8, 1, 28, 28)
logits = model(images)

print(logits.shape)
```

### 27.3 Keras CNN

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.Conv2D(8, 3, padding="same", activation="relu"),
    layers.MaxPooling2D(pool_size=2),
    layers.Conv2D(16, 3, padding="same", activation="relu"),
    layers.GlobalAveragePooling2D(),
    layers.Dense(10),
])

print(model.summary())
```

### 27.4 Computer vision task map

| Problem | Common building blocks |
|---|---|
| Image classification | CNN, vision transformer |
| Object detection | Backbone + localization/classification head |
| Semantic segmentation | Encoder-decoder / U-Net-like structure |
| Image embedding | CNN or transformer backbone with projection head |
| Transfer learning | Pretrained feature extractor and task-specific head |

For transfer learning, freeze an appropriate feature backbone initially, then optionally unfreeze with a lower learning rate. Pretrained normalization and image preprocessing must match the model's training recipe.

---

## 28. Sequences, recurrent networks, and attention

### 28.1 PyTorch LSTM

```python
import torch
from torch import nn

lstm = nn.LSTM(
    input_size=6,
    hidden_size=16,
    num_layers=2,
    batch_first=True,
)

sequence = torch.randn(4, 12, 6)
outputs, (hidden, cell) = lstm(sequence)

print(outputs.shape)
print(hidden.shape)
print(cell.shape)
```

With `batch_first=True`, input and output sequence dimensions are `(batch, time, features)`. Hidden state convention remains `(num_layers * num_directions, batch, hidden_size)`.

### 28.2 Keras LSTM

```python
import keras
from keras import layers

model = keras.Sequential([
    keras.Input(shape=(12, 6)),
    layers.LSTM(16),
    layers.Dense(1),
])

model.summary()
```

### 28.3 GRU versus LSTM

- `LSTM`: recurrent gating with memory cell and hidden state.
- `GRU`: simpler gated recurrent unit with fewer gating structures.
- Both model sequences with learned recurrent dynamics.
- Transformers increasingly dominate many text tasks, but recurrence remains useful for some sequences and constraints.

### 28.4 Attention intuition

Scaled dot-product attention:

\[
\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

- Queries (`Q`) indicate what each position seeks.
- Keys (`K`) indicate what positions can match.
- Values (`V`) supply information combined by attention weights.

### 28.5 PyTorch multihead attention

```python
import torch
from torch import nn

attention = nn.MultiheadAttention(embed_dim=32, num_heads=4, batch_first=True)

X = torch.randn(2, 10, 32)
outputs, weights = attention(X, X, X)

print(outputs.shape)
print(weights.shape)
```

The example uses **self-attention** (`Q=K=V=X`). For autoregressive attention, you must apply suitable causal masking; without it, positions can attend to future inputs.

### 28.6 Keras multihead attention

```python
import keras
from keras import layers

X = keras.ops.ones((2, 10, 32))

attention = layers.MultiHeadAttention(num_heads=4, key_dim=8)
outputs = attention(query=X, value=X, key=X)

print(outputs.shape)
```

### 28.7 Transformer encoder in PyTorch

```python
import torch
from torch import nn

layer = nn.TransformerEncoderLayer(
    d_model=32,
    nhead=4,
    dim_feedforward=64,
    batch_first=True,
)

model = nn.TransformerEncoder(layer, num_layers=2)

sequence = torch.randn(3, 20, 32)
print(model(sequence).shape)
```

Transformers usually require appropriate position information, masks, and task-specific pooling/output heads. A plain attention stack alone does not define a complete language model.

---

## 29. Training concepts and failure modes

### 29.1 Loss curves

| Pattern | Possible interpretation | Potential response |
|---|---|---|
| Training loss stays flat | Bad LR, bug, weak signal | Inspect gradients/labels/features |
| Train loss falls; validation rises | Overfitting or validation mismatch | Regularize, stop early, check split |
| Both losses high | Underfitting, optimization issues | Improve model, features, optimization |
| NaN/Inf loss | Instability, invalid values | Check scale, loss, gradients, LR |
| Large generalization gap | Capacity, leakage, distribution shift | Improve validation and regularization |

### 29.2 Important hyperparameters

- Learning rate: controls update size; often more influential than architecture details.
- Batch size: affects memory, gradient noise, and number of updates.
- Epoch count: controls duration of training.
- Weight decay/L1/L2: regularization.
- Dropout rate: stochastic regularization strength.
- Hidden width/depth: model capacity.
- Activation: affects nonlinearity and gradient flow.
- Optimizer and scheduler: affect convergence path.

### 29.3 Initialization and normalization

- Glorot/Xavier initialization is often suited to tanh-like layers.
- He/Kaiming initialization is commonly used for ReLU-like networks.
- Batch norm depends on running statistics and train/eval behavior.
- Layer norm is often preferred in transformer blocks.
- Scaling tabular features before a neural network can improve optimization.

### 29.4 Classification targets and leakage

A raw probability prediction should not be treated as calibrated solely because it was produced by sigmoid or softmax. For probability-sensitive applications, evaluate reliability on held-out periods and consider separate calibration procedures.

### 29.5 Reproducibility

```python
import random
import numpy as np
import torch

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
```

These seeds improve repeatability but do not guarantee bitwise identical execution across different hardware, accelerator kernels, or library versions.

---

## 30. NumPy, Pandas, and scikit-learn interoperability

### 30.1 Pandas to PyTorch

```python
import numpy as np
import pandas as pd
import torch

frame = pd.DataFrame({
    "age": [25, 35, 45],
    "income": [50_000.0, 75_000.0, 90_000.0],
})

X = torch.tensor(frame.to_numpy(dtype=np.float32))

print(X.shape)
```

Categorical features must be encoded or embedded; datetime/nullable object columns generally cannot be passed directly as floating tensor input.

### 30.2 scikit-learn preprocessing + PyTorch

```python
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler

X_train = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
X_test = np.array([[4.0, 40.0]])

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)

print(train_tensor.shape)
print(test_tensor.shape)
```

Do not fit preprocessors on test features in ways that leak test distribution information into training.

### 30.3 Tensor conversion compared

| Operation | PyTorch | TensorFlow | Keras |
|---|---|---|---|
| Create | `torch.tensor(a)` | `tf.convert_to_tensor(a)` | `keras.ops.convert_to_tensor(a)` |
| To NumPy | `x.detach().cpu().numpy()` | `x.numpy()` in eager mode | Backend-dependent conversion; use Keras ops when portable |
| Matmul | `a @ b`, `torch.matmul` | `tf.matmul` | `keras.ops.matmul` |
| Reshape | `x.reshape(...)` | `tf.reshape(x, ...)` | `keras.ops.reshape(x, ...)` |
| Sum | `x.sum(dim=...)` | `tf.reduce_sum(..., axis=...)` | `keras.ops.sum(..., axis=...)` |

### 30.4 Sklearn vs neural network interfaces

| Workflow stage | scikit-learn | PyTorch | Keras |
|---|---|---|---|
| Define model | `LogisticRegression()` | `nn.Module` | `keras.Model` |
| Train | `.fit(X, y)` | Custom optimizer loop | `.fit(X, y)` |
| Predict | `.predict(X)` | `model(X)` plus postprocessing | `.predict(X)` |
| Preprocess | `Pipeline` | External or model-internal transforms | Layers / external pipelines |
| Evaluate | `sklearn.metrics` | Custom metric computations | `.evaluate()` / metrics |
| Tune | `GridSearchCV` etc. | External libraries / custom | Keras tooling / external search |

---

## 31. API maps: PyTorch

### Tensor operations

```text
torch.tensor             Create tensor from data
torch.as_tensor          Convert or reuse data without forcing copy
torch.from_numpy         Share NumPy CPU memory where supported
torch.zeros / ones       Fixed-value tensors
torch.rand / randn       Random samples
torch.arange / linspace  Numeric sequences
torch.reshape            Reshape tensor
torch.stack / cat        Stack or concatenate
torch.transpose          Swap dimensions
torch.permute            Rearrange dimensions
torch.matmul / mm        Matrix multiplication
torch.einsum             Einstein summation
torch.mean / sum         Reductions
torch.max / argmax       Maximum / index
torch.where              Conditional selection
torch.clamp              Clip elements
torch.softmax            Softmax probabilities
torch.sigmoid            Logistic activation
torch.logsumexp          Stable log-sum-exp
torch.linalg.solve       Linear system
torch.linalg.svd         Singular value decomposition
```

### Autograd, model, training

```text
tensor.requires_grad_          Enable gradient tracking
tensor.backward                Backpropagate scalar loss
torch.autograd.grad            Request explicit gradients
tensor.grad                    Accumulated gradient attribute
tensor.detach                  Disconnect from graph
torch.no_grad                  Disable gradient recording
torch.inference_mode           Inference-mode optimization
nn.Module                      Base trainable model abstraction
nn.Sequential                  Ordered module composition
nn.ModuleList                  Registered list of submodules
nn.Parameter                   Trainable parameter registration
nn.Linear                      Fully connected layer
nn.Conv2d                      2D convolution
nn.BatchNorm2d                 Batch normalization
nn.LayerNorm                   Layer normalization
nn.Dropout                     Stochastic dropout
nn.Embedding                   Index embedding
nn.LSTM / GRU                  Recurrent modules
nn.MultiheadAttention          Multi-head attention
nn.CrossEntropyLoss            Multiclass logit loss
nn.BCEWithLogitsLoss           Binary logit loss
nn.MSELoss                     Squared error
optim.SGD / Adam / AdamW        Optimizers
optim.lr_scheduler.StepLR      Learning rate scheduler
nn.utils.clip_grad_norm_       Gradient norm clipping
DataLoader                     Minibatch iteration
TensorDataset                  Tensor-backed dataset
model.state_dict               Parameter/buffer state
model.load_state_dict          Restore parameter/buffer state
torch.save / load              Serialization
torch.compile                  Optional compilation
```

### Common inspection methods

```python
import torch
from torch import nn

model = nn.Sequential(nn.Linear(3, 4), nn.ReLU(), nn.Linear(4, 1))

print(type(model))
print(list(model.named_children()))
print(list(model.named_parameters()))
print(model.state_dict().keys())
print(sum(p.numel() for p in model.parameters()))
```

---

## 32. API maps: TensorFlow

```text
tf.constant                    Immutable tensor
tf.Variable                    Mutable trainable state
tf.convert_to_tensor           Convert data to tensor
tf.cast                        Change dtype
tf.reshape                     Change shape
tf.transpose                   Rearrange axes
tf.expand_dims / squeeze       Insert/remove singleton axes
tf.concat / stack              Merge tensors
tf.matmul                      Matrix multiplication
tf.einsum                      Einstein summation
tf.reduce_sum / mean           Reductions
tf.where                       Conditional selection
tf.gather                      Gather indexed values
tf.boolean_mask                Boolean indexed selection
tf.math.sigmoid / softmax       Activation functions
tf.linalg.solve                Linear system
tf.GradientTape                Automatic differentiation
tf.function                    Trace into TensorFlow function
tf.TensorSpec                  Specify symbolic tensor shape/dtype
tf.data.Dataset                Dataset pipeline
tf.data.AUTOTUNE               Dataset runtime performance tuning
tf.keras.layers.Dense          Dense neural network layer
tf.keras.layers.Conv2D         Image convolution
tf.keras.Model                 Keras model integration
tf.keras.optimizers.Adam       Adam optimizer
tf.distribute.MirroredStrategy Multi-GPU synchronous strategy
tf.saved_model.save            TensorFlow SavedModel export
tf.config.list_physical_devices Inspect available devices
```

---

## 33. API maps: Keras

### Models, layers, training

```text
keras.Input                        Functional model input
keras.Sequential                   Linear-stack network
keras.Model                        Functional or subclassed model
keras.layers.Layer                 Custom layer foundation
keras.layers.Dense                 Dense transformation
keras.layers.Conv1D / Conv2D       Convolutional layers
keras.layers.MaxPooling2D          Spatial pooling
keras.layers.BatchNormalization    Batch norm
keras.layers.LayerNormalization    Layer norm
keras.layers.Dropout               Dropout
keras.layers.Embedding             Embedding
keras.layers.LSTM / GRU            Recurrent layers
keras.layers.MultiHeadAttention    Attention
keras.layers.Concatenate          Merge multiple tensors
keras.layers.Add                  Elementwise merge
keras.optimizers.Adam / AdamW      Optimizers
keras.losses.MeanSquaredError      Regression loss
keras.losses.BinaryCrossentropy   Binary loss
keras.losses.CategoricalCrossentropy One-hot multiclass loss
keras.losses.SparseCategoricalCrossentropy Integer multiclass loss
keras.metrics.BinaryAccuracy      Binary accuracy
keras.metrics.AUC                 ROC/PR-related AUC configurations
keras.metrics.MeanAbsoluteError   Regression MAE
model.compile                     Configure train procedure
model.fit                         Train
model.evaluate                    Evaluate
model.predict                     Predict
model.summary                     Summarize architecture
model.save                        Save .keras archive
keras.models.load_model           Reload supported model files
model.export                      Export serving artifact
```

### Callbacks and ops

```text
keras.callbacks.EarlyStopping       Stop on monitored plateau
keras.callbacks.ModelCheckpoint     Save best model
keras.callbacks.ReduceLROnPlateau   Reduce learning rate
keras.callbacks.TensorBoard         TensorBoard training logs
keras.callbacks.CSVLogger           CSV epoch logs
keras.callbacks.TerminateOnNaN      Stop on NaN loss
keras.ops.convert_to_tensor         Backend tensor creation
keras.ops.matmul                    Matrix multiplication
keras.ops.reshape                   Reshape
keras.ops.sum / mean                Reductions
keras.ops.sigmoid / softmax         Activations
keras.ops.concatenate / stack       Merge tensors
keras.ops.einsum                    Einstein summation
keras.ops.binary_crossentropy      Binary cross entropy
keras.backend.backend              Current backend name
```

---

## 34. Decision guide and common pitfalls

### 34.1 Framework decision matrix

| If you need... | First consider |
|---|---|
| Explicit gradient and training-loop control | PyTorch |
| Rapid standard model prototyping | Keras 3 |
| TensorFlow data/serving/graph infrastructure | TensorFlow |
| One higher-level API across backend families | Keras 3 |
| Custom transformer/LLM research model | Often PyTorch |
| Familiar `fit`/`predict` training interface | Keras |
| Tabular classification with limited data | Often scikit-learn first |

### 34.2 Important traps

| Issue | Consequence | Better approach |
|---|---|---|
| Sigmoid before BCE-with-logits | Incorrect double sigmoid | Pass raw logits |
| Softmax before PyTorch cross entropy | Redundant transformation, poorer loss semantics | Pass logits |
| Wrong label dtype for `CrossEntropyLoss` | Error or wrong loss expectations | Integer class IDs, `torch.long` |
| `(batch,)` targets against `(batch,1)` outputs | Broadcast mismatch/wrong loss | Match shapes |
| Not calling `optimizer.zero_grad()` | Unexpected gradient accumulation | Clear gradients each step |
| Forgetting `model.eval()` | Dropout/BN behavior wrong | Set evaluation mode |
| Assuming `eval()` turns off autograd | Extra gradient graph/memory | Use `inference_mode()` |
| In-place changes to autograd intermediates | Backprop errors | Avoid unsafe in-place ops |
| CPU model + GPU data | Device mismatch | Move model and batch together |
| Switching Keras backend after import | Stale backend state | Restart and configure before import |
| Using TF ops in portable Keras custom layers | Backend lock-in | Prefer `keras.ops` |
| `model.save("directory")` in Keras 3 | Not a valid SavedModel save path | Use `.keras` or `.export()` |
| Preprocessing fit on all data | Leakage | Fit transforms on training only |
| Random splits on temporal data | Future leakage | Chronological validation |
| Comparing train loss with test score only | Cannot diagnose generalization well | Track train/validation/test separately |
| Assuming accelerator always faster | Small-model overhead may dominate | Benchmark representative workloads |
| Loading untrusted serialized objects | Deserialization security risk | Trust and validate artifacts |

### 34.3 Interpreting model output

For binary classification with raw logits \(z\), apply sigmoid:

\[
P(Y=1|x)=\sigma(z)=\frac{1}{1+e^{-z}}
\]

For multiclass logits \(z_i\), apply softmax:

\[
P(Y=i|x)=\frac{e^{z_i}}{\sum_j e^{z_j}}
\]

These are model-produced scores interpreted as probabilities; they may require **empirical calibration** before use in decisions sensitive to absolute risk.

---

## 35. Practice exercises with solutions

### Exercise 1: Verify autograd against the analytical derivative

For \(f(x)=x^3-4x^2+2x\), compute its gradient at \(x=2\).

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x ** 3 - 4 * x ** 2 + 2 * x

y.backward()

print(x.grad.item())
```

Analytical derivative: \(3x^2-8x+2\), so at 2 the result is `-2.0`.

### Exercise 2: Tensor shape manipulation

Convert an image batch from channels-last `(N,H,W,C)` to channels-first `(N,C,H,W)`.

```python
import torch

images = torch.randn(8, 32, 32, 3)
converted = images.permute(0, 3, 1, 2)

print(converted.shape)
```

Expected shape `(8, 3, 32, 32)`.

### Exercise 3: Correct binary loss

```python
import torch
from torch import nn

logits = torch.tensor([[2.0], [-2.0], [0.0]])
targets = torch.tensor([[1.0], [0.0], [1.0]])

loss = nn.BCEWithLogitsLoss()(logits, targets)
probabilities = torch.sigmoid(logits)
predicted = (probabilities >= 0.5).float()

print(loss.item())
print(predicted)
```

### Exercise 4: Portability with Keras ops

```python
import keras
from keras import ops


class NormalizedProduct(keras.layers.Layer):

    def call(self, inputs):
        left, right = inputs
        product = ops.matmul(left, right)
        return product / (1 + ops.abs(product))


layer = NormalizedProduct()
a = ops.ones((2, 3))
b = ops.ones((3, 4))

print(layer((a, b)).shape)
```

### Exercise 5: Implement a basic linear model manually in PyTorch

```python
import torch
from torch import nn


torch.manual_seed(3)
X = torch.linspace(-2, 2, 100).reshape(-1, 1)
y = 3 * X + 1

model = nn.Linear(1, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
criterion = nn.MSELoss()

for _ in range(200):
    optimizer.zero_grad()
    loss = criterion(model(X), y)
    loss.backward()
    optimizer.step()

print(model.weight.item())
print(model.bias.item())
```

Expected trained weight near 3 and intercept near 1.

### Further exercises

1. Write a custom `nn.Module` with two hidden layers, LayerNorm, and dropout.
2. Write a PyTorch training function accepting a model, data loader, loss, and optimizer, returning mean epoch loss.
3. Convert a saved NumPy data matrix into a `TensorDataset`; compare `shuffle=True` and chronological iterators.
4. Train a Keras model using both a TensorFlow backend and a PyTorch backend in **separate processes** and compare metrics, not exact weights.
5. Write a TensorFlow `tf.function` with an input signature for a batch of tabular observations.
6. Explain why validation loss may differ between train and evaluation modes with dropout.
7. Add early stopping to a Keras model and save only the best `.keras` checkpoint.
8. Draw a tensor shape trace through Conv2D → pooling → flatten → dense.
9. Explain why attention without causal masking would leak future tokens in next-token prediction.
10. Explore a pretrained model with the official library that supplies the weights; preserve its preprocessing requirements.

---

## 36. Official documentation and learning path

### Official guides

- [PyTorch documentation](https://docs.pytorch.org/docs/stable/index.html)
- [PyTorch beginner tutorials](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
- [PyTorch DataLoader tutorial](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)
- [PyTorch compile documentation](https://docs.pytorch.org/docs/stable/generated/torch.compile.html)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [TensorFlow Automatic Differentiation](https://www.tensorflow.org/guide/autodiff)
- [TensorFlow `tf.function` guide](https://www.tensorflow.org/guide/function)
- [TensorFlow `tf.data` guide](https://www.tensorflow.org/guide/data)
- [Keras 3 documentation](https://keras.io/)
- [Keras 3 multi-backend overview](https://keras.io/keras_3/)
- [Keras built-in training guide](https://keras.io/guides/training_with_built_in_methods/)
- [Keras 3 migration guide](https://keras.io/guides/migrating_to_keras_3/)

### Suggested progression

1. Tensor algebra and shapes (`NumPy` first, then `torch.Tensor`).
2. Autograd and the chain rule.
3. Implement a linear model from scratch.
4. Write a PyTorch `nn.Module` and full optimization loop.
5. Use `Dataset` and `DataLoader` with genuine train/validation splits.
6. Understand loss functions, logits, and probability calibration.
7. Implement the same model with Keras `Sequential` and Functional APIs.
8. Learn TensorFlow `GradientTape` and `tf.data` to understand backend-level counterparts.
9. Explore CNNs, recurrent models, and attention.
10. Add persistence, device placement, profiling, and production validation.

**Core takeaway:** PyTorch exposes explicit tensor/autograd training mechanics; TensorFlow exposes a rich tensor/graph/data infrastructure; Keras 3 standardizes convenient high-level model construction and training across supported backends.
