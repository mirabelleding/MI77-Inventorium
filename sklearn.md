# Scikit-learn (`sklearn`)

**Scope:** Estimator architecture, supervised learning, unsupervised learning, data preparation, pipelines, feature engineering, validation, hyperparameter tuning, model evaluation, inspection, calibration, and production-minded practices.

## Table of contents

1. [Mental model and setup](#1-mental-model-and-setup)
2. [Estimator API and object architecture](#2-estimator-api-and-object-architecture)
3. [Data representation and splitting](#3-data-representation-and-splitting)
4. [Preprocessing and scaling](#4-preprocessing-and-scaling)
5. [Missing data and categorical encoding](#5-missing-data-and-categorical-encoding)
6. [Pipelines and column-specific transformations](#6-pipelines-and-column-specific-transformations)
7. [Feature engineering and feature selection](#7-feature-engineering-and-feature-selection)
8. [Linear regression family](#8-linear-regression-family)
9. [Linear classifiers and probability estimates](#9-linear-classifiers-and-probability-estimates)
10. [Decision trees and ensembles](#10-decision-trees-and-ensembles)
11. [Support vector machines and nearest neighbors](#11-support-vector-machines-and-nearest-neighbors)
12. [Naive Bayes, discriminant analysis, and Gaussian processes](#12-naive-bayes-discriminant-analysis-and-gaussian-processes)
13. [Clustering](#13-clustering)
14. [Dimensionality reduction](#14-dimensionality-reduction)
15. [Anomaly detection and novelty detection](#15-anomaly-detection-and-novelty-detection)
16. [Model evaluation: classification](#16-model-evaluation-classification)
17. [Model evaluation: regression](#17-model-evaluation-regression)
18. [Cross-validation strategies](#18-cross-validation-strategies)
19. [Hyperparameter search](#19-hyperparameter-search)
20. [Probability calibration and threshold selection](#20-probability-calibration-and-threshold-selection)
21. [Model inspection and interpretation](#21-model-inspection-and-interpretation)
22. [Class imbalance, weights, and metadata](#22-class-imbalance-weights-and-metadata)
23. [Custom estimators and streaming updates](#23-custom-estimators-and-streaming-updates)
24. [Model persistence, reproducibility, and deployment](#24-model-persistence-reproducibility-and-deployment)
25. [Complete end-to-end examples](#25-complete-end-to-end-examples)
26. [Common mistakes and debugging](#26-common-mistakes-and-debugging)
27. [Comprehensive API reference tables](#27-comprehensive-api-reference-tables)
28. [Exercises and solutions](#28-exercises-and-solutions)
29. [Official resources](#29-official-resources)

---

## 1. Mental model and setup

Scikit-learn provides implementations of classical machine learning algorithms and the surrounding workflow: preprocessing → feature engineering → fitting → tuning → prediction → evaluation.

```text
Raw data
   │
   ▼
Train / validation / test split
   │
   ▼
Preprocessing fitted ONLY on training fold
   │
   ▼
Estimator.fit(X_train, y_train)
   │
   ├─────────── Cross-validation / hyperparameter search
   │
   ▼
Estimator.predict(X_test)
   │
   ▼
Metrics, calibration, diagnostics, deployment
```

| Library | Central object | Task |
|---|---|---|
| NumPy | `ndarray` | Numerical arrays |
| Pandas | `DataFrame` | Tabular data processing |
| SciPy | Numerical solvers and distributions | Numerical mathematics |
| Scikit-learn | Estimator | Classical ML workflows |
| PyTorch | `Tensor`, `nn.Module` | Differentiable neural models |

Install and inspect:

```bash
python -m pip install -U scikit-learn numpy pandas scipy matplotlib
```

```python
import sklearn

print(sklearn.__version__)
sklearn.show_versions()
```

Most scikit-learn estimators work with NumPy arrays and Pandas DataFrames. Many algorithms require numeric finite features, with specialized estimators supporting missing values or other inputs.

---

## 2. Estimator API and object architecture

### 2.1 The shared estimator contract

| Method | Meaning | Typical objects |
|---|---|---|
| `fit(X, y)` | Learn parameters | Predictors / transformers |
| `predict(X)` | Return predicted label or numeric response | Predictors |
| `predict_proba(X)` | Return class probability estimates | Probabilistic classifiers |
| `decision_function(X)` | Return decision score/margin | Some classifiers |
| `transform(X)` | Transform features | Transformers |
| `fit_transform(X, y=None)` | Fit transformer then transform | Transformers |
| `inverse_transform(X)` | Reverse transformation where possible | Some transformers |
| `fit_predict(X)` | Fit and return labels/predictions | Certain clusterers, etc. |
| `score(X, y)` | Default estimator score | Many estimators |
| `get_params(deep=True)` | Get constructor/config parameters | Estimators |
| `set_params(**params)` | Configure estimator parameters | Estimators |

Not all estimators implement every method. The meaning of `score` varies: regression often uses \(R^2\), classification often uses accuracy, and unsupervised models use other definitions.

```python
from sklearn.linear_model import Ridge

model = Ridge(alpha=2.0)

print(model.get_params()["alpha"])
model.set_params(alpha=0.5)
print(model.get_params()["alpha"])
```

### 2.2 Parameters versus learned attributes

Constructor parameters are normally exposed as `alpha`, `max_depth`, `C`, etc. Learned attributes usually end with `_`:

```python
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1.0], [2.0], [3.0]])
y = np.array([2.0, 4.0, 6.0])

model = LinearRegression(fit_intercept=True)
model.fit(X, y)

print(model.coef_)
print(model.intercept_)
print(model.n_features_in_)
```

`coef_` appears after fitting; `fit_intercept` is a configuration parameter.

### 2.3 Cloning and model identity

```python
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression

original = LogisticRegression(C=0.5)
copy = clone(original)

print(copy.get_params()["C"])
print(copy is original)
```

`clone()` reconstructs an **unfitted** estimator with the same parameters; it is not a copy of learned fitted state.

### 2.4 Inspection of available estimators

```python
from sklearn.utils.discovery import all_estimators

classifiers = all_estimators(type_filter="classifier")

print(len(classifiers))
print(classifiers[:5])
```

Older scikit-learn versions also exposed `all_estimators` through `sklearn.utils`; the module path has evolved, so check your installed version.

---

## 3. Data representation and splitting

### 3.1 The `X` and `y` convention

- `X`: feature matrix, shape `(n_samples, n_features)`.
- `y`: target vector, usually shape `(n_samples,)`.
- Rows represent observations; columns represent features.
- Class labels may be strings or integers for many classifiers.

```python
import pandas as pd

frame = pd.DataFrame({
    "age": [25, 34, 45, 53],
    "income": [45_000, 61_000, 83_000, 95_000],
    "defaulted": [0, 0, 1, 0],
})

X = frame[["age", "income"]]
y = frame["defaulted"]

print(X.shape)
print(y.shape)
```

### 3.2 Train/test split for classification

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print(X_train.shape, X_test.shape)
```

`stratify=y` preserves approximate class proportions; it is not suitable for all designs, especially chronological data or grouped subjects.

### 3.3 Data leakage

Leakage occurs when information unavailable at prediction time influences model training or feature preparation. Example: fitting a scaler using the full dataset before splitting. The correct approach is to split first and put transformations into a `Pipeline`, ensuring fold-specific fitting during cross-validation.

### 3.4 Dataset generators

| Utility | Purpose |
|---|---|
| `make_classification` | Synthetic supervised classification data |
| `make_regression` | Synthetic regression data |
| `make_blobs` | Gaussian clusters |
| `make_moons` | Nonlinear two-class geometry |
| `load_iris` | Small classification example |
| `load_wine` | Classification example |
| `load_diabetes` | Regression example |
| `load_breast_cancer` | Binary classification example |

```python
from sklearn.datasets import make_classification, make_regression

X_class, y_class = make_classification(
    n_samples=500,
    n_features=12,
    n_informative=5,
    random_state=0,
)

X_reg, y_reg = make_regression(
    n_samples=500,
    n_features=8,
    noise=5,
    random_state=0,
)
```

---

## 4. Preprocessing and scaling

### 4.1 Scaling methods compared

| Transformer | Mathematical intuition | Use |
|---|---|---|
| `StandardScaler` | `(x - mean) / std` | Standardization for linear/SVM/NN models |
| `MinMaxScaler` | Rescale to target interval | Bounded feature scaling |
| `RobustScaler` | Median and quantile-based scale | Outlier-heavy data |
| `MaxAbsScaler` | Divide by max absolute value | Sparse-friendly scaling |
| `Normalizer` | Normalize each sample row | Cosine-related workflows |
| `QuantileTransformer` | Rank/quantile-based mapping | Strongly nonnormal marginals |
| `PowerTransformer` | Yeo–Johnson or Box–Cox | Skewed features |
| `Binarizer` | Threshold numeric features | Binary feature creation |
| `KBinsDiscretizer` | Discretize continuous variables | Binning |

### 4.2 Standardization

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0]])

scaler = StandardScaler()
Z = scaler.fit_transform(X)

print(scaler.mean_)
print(scaler.scale_)
print(Z)
print(scaler.inverse_transform(Z))
```

### 4.3 Robust and quantile scaling

```python
import numpy as np
from sklearn.preprocessing import RobustScaler, QuantileTransformer

X = np.array([[1.0], [2.0], [3.0], [100.0]])

print(RobustScaler().fit_transform(X).ravel())
print(QuantileTransformer(n_quantiles=4, random_state=42).fit_transform(X).ravel())
```

Quantile transforms can distort distances and extrapolate poorly outside fitted ranges. Apply them only when appropriate for the model and problem.

### 4.4 Feature scaling versus target scaling

`StandardScaler` normally transforms **features**. To transform the target and automatically invert predictions, consider `TransformedTargetRegressor`.

```python
import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(1)
X = rng.normal(size=(100, 3))
y = 100 + X @ np.array([1.0, 2.0, 3.0])

model = TransformedTargetRegressor(
    regressor=Ridge(),
    transformer=StandardScaler(),
)

model.fit(X, y)
print(model.predict(X[:3]))
```

---

## 5. Missing data and categorical encoding

### 5.1 Imputation

| Transformer | Purpose |
|---|---|
| `SimpleImputer` | Replace missing values using mean/median/most-frequent/constant |
| `KNNImputer` | Neighbor-based imputation |
| `IterativeImputer` | Iterative multivariate imputation, experimental |
| `MissingIndicator` | Add flags for missingness |

```python
import numpy as np
from sklearn.impute import SimpleImputer

X = np.array([[1.0, np.nan], [2.0, 10.0], [np.nan, 20.0]])

imputer = SimpleImputer(strategy="median", add_indicator=True)
X_clean = imputer.fit_transform(X)

print(X_clean)
```

For `IterativeImputer`, importing `sklearn.experimental.enable_iterative_imputer` remains necessary in versions where that feature is experimental.

### 5.2 One-hot encoding

```python
import numpy as np
from sklearn.preprocessing import OneHotEncoder

X = np.array([["east"], ["west"], ["east"]], dtype=object)

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoded = encoder.fit_transform(X)

print(encoder.get_feature_names_out())
print(encoded)
print(encoder.transform([["north"]]))
```

`handle_unknown='ignore'` prevents an error for unseen categories and outputs all zeros for that feature's encoded columns.

### 5.3 Ordinal encoding

```python
from sklearn.preprocessing import OrdinalEncoder

encoder = OrdinalEncoder(
    categories=[["low", "medium", "high"]],
    handle_unknown="use_encoded_value",
    unknown_value=-1,
)

print(encoder.fit_transform([["low"], ["high"], ["medium"]]))
```

Ordinal encoding implies an order; use one-hot for nominal categories unless the model and encoding assumptions warrant another choice.

### 5.4 Label encoding

```python
from sklearn.preprocessing import LabelEncoder

labels = ["cat", "dog", "dog", "bird"]

encoder = LabelEncoder()
encoded = encoder.fit_transform(labels)

print(encoded)
print(encoder.classes_)
print(encoder.inverse_transform(encoded))
```

`LabelEncoder` is designed for target labels (`y`), not as the default encoding method for feature columns.

---

## 6. Pipelines and column-specific transformations

### 6.1 Why pipelines matter

Pipelines ensure each transformation is **fitted only on the training data within each cross-validation split**, helping prevent data leakage. They also give you one estimator exposing `fit`, `predict`, and `score`.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000),
)

print(model.named_steps.keys())
```

### 6.2 Explicit names with `Pipeline`

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

model = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
    ("regressor", Ridge(alpha=1.0)),
])

print(model.get_params()["regressor__alpha"])
model.set_params(regressor__alpha=2.5)
```

Double underscores (`step__parameter`) address nested constructor parameters.

### 6.3 Real mixed DataFrame pipeline

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

X = pd.DataFrame({
    "income": [40_000, 60_000, None, 80_000, 55_000, 72_000],
    "age": [25, 30, 45, 38, None, 50],
    "region": ["east", "west", "east", "north", "west", "north"],
})
y = [0, 0, 1, 0, 1, 1]

numeric = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])

categorical = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric, ["income", "age"]),
    ("categorical", categorical, ["region"]),
])

model = Pipeline([
    ("prepare", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000)),
])

model.fit(X, y)
print(model.predict(X.iloc[:2]))
print(model.named_steps["prepare"].get_feature_names_out())
```

### 6.4 Column selection helpers

```python
import pandas as pd
from sklearn.compose import make_column_selector

X = pd.DataFrame({
    "age": [25, 30],
    "region": ["east", "west"],
})

numeric_columns = make_column_selector(dtype_include="number")(X)
category_columns = make_column_selector(dtype_include="object")(X)

print(numeric_columns)
print(category_columns)
```

### 6.5 Pandas output support

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

X = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [10.0, 20.0, 30.0]})

scaler = StandardScaler().set_output(transform="pandas")

print(scaler.fit_transform(X))
```

Not all transformations or sparse-output configurations support DataFrame outputs equally; one-hot encoding may need `sparse_output=False` in a pandas-output pipeline.

### 6.6 FeatureUnion and FunctionTransformer

```python
import numpy as np
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import FunctionTransformer, StandardScaler

X = np.array([[1.0, 2.0], [3.0, 4.0]])

features = FeatureUnion([
    ("original", FunctionTransformer(validate=False)),
    ("scaled", StandardScaler()),
])

print(features.fit_transform(X))
```

---

## 7. Feature engineering and feature selection

### 7.1 Polynomial expansion

```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures

X = np.array([[2.0, 3.0]])

transformer = PolynomialFeatures(degree=2, include_bias=False)

print(transformer.fit_transform(X))
print(transformer.get_feature_names_out())
```

Expected features: `x0`, `x1`, `x0^2`, `x0 x1`, `x1^2`.

### 7.2 Spline features

```python
import numpy as np
from sklearn.preprocessing import SplineTransformer

X = np.linspace(0.0, 1.0, 8).reshape(-1, 1)

transformer = SplineTransformer(n_knots=4, degree=3)
print(transformer.fit_transform(X).shape)
```

### 7.3 Univariate selection

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif

X, y = make_classification(
    n_samples=200,
    n_features=20,
    n_informative=5,
    random_state=42,
)

selector = SelectKBest(score_func=f_classif, k=5)
X_selected = selector.fit_transform(X, y)

print(X_selected.shape)
print(selector.get_support(indices=True))
```

### 7.4 Recursive feature elimination

```python
from sklearn.datasets import make_regression
from sklearn.feature_selection import RFE
from sklearn.linear_model import Ridge

X, y = make_regression(n_samples=120, n_features=10, random_state=1)

selector = RFE(estimator=Ridge(), n_features_to_select=4)
selector.fit(X, y)

print(selector.support_)
print(selector.ranking_)
```

### 7.5 Model-based selection

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

X, y = make_classification(n_samples=150, n_features=12, random_state=3)

selector = SelectFromModel(
    RandomForestClassifier(n_estimators=100, random_state=3),
    threshold="median",
)

print(selector.fit_transform(X, y).shape)
```

Never perform supervised feature selection on all data before cross-validation. Put the selector inside the pipeline.

| Method | Trade-off |
|---|---|
| `VarianceThreshold` | Very fast, unsupervised |
| `SelectKBest` | Fast univariate tests; ignores feature interactions |
| `RFE` / `RFECV` | More expensive; accounts for estimator effects |
| `SelectFromModel` | Uses coefficients or importances |
| `SequentialFeatureSelector` | Wrapper selection, potentially expensive |

---

## 8. Linear regression family

### 8.1 Models and penalties

| Estimator | Core idea |
|---|---|
| `LinearRegression` | Ordinary least squares |
| `Ridge` | L2-regularized regression |
| `Lasso` | L1 regularization; may zero coefficients |
| `ElasticNet` | Mixture of L1 and L2 penalties |
| `RidgeCV` / `LassoCV` / `ElasticNetCV` | Cross-validated regularization |
| `HuberRegressor` | Robust regression to outliers |
| `QuantileRegressor` | Conditional quantile regression |
| `SGDRegressor` | Iterative linear regression with SGD |
| `PoissonRegressor` | Generalized linear model for nonnegative counts |
| `GammaRegressor` | GLM for positive skewed outcomes |
| `TweedieRegressor` | Tweedie-family GLM |
| `RANSACRegressor` | Robust sample-consensus regression |

### 8.2 Ridge versus Lasso

```python
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

rng = np.random.default_rng(42)
X = rng.normal(size=(150, 5))
y = 2 * X[:, 0] - X[:, 1] + rng.normal(scale=0.2, size=150)

models = {
    "ols": LinearRegression(),
    "ridge": Ridge(alpha=1.0),
    "lasso": Lasso(alpha=0.05),
    "elastic": ElasticNet(alpha=0.05, l1_ratio=0.5),
}

for name, model in models.items():
    model.fit(X, y)
    print(name, np.round(model.coef_, 3))
```

For squared-error regression, Ridge penalizes \(\sum_j\beta_j^2\), Lasso penalizes \(\sum_j|\beta_j|\), and ElasticNet combines both. Regularization strength interacts with feature scale; scaling is usually important.

### 8.3 Quantile regression

```python
from sklearn.datasets import make_regression
from sklearn.linear_model import QuantileRegressor

X, y = make_regression(n_samples=100, n_features=3, noise=10, random_state=4)

model = QuantileRegressor(quantile=0.9, alpha=0.1, solver="highs")
model.fit(X, y)

print(model.predict(X[:4]))
```

A 0.9 conditional quantile is different from the conditional mean. Quantile models can help estimate an upper conditional outcome, subject to model and calibration assumptions.

---

## 9. Linear classifiers and probability estimates

| Estimator | Concept |
|---|---|
| `LogisticRegression` | Linear logistic probability model |
| `SGDClassifier` | Efficient iterative linear classifier |
| `RidgeClassifier` | Ridge-based classification |
| `Perceptron` | Linear online classification |
| `PassiveAggressiveClassifier` | Margin-oriented online classifier |

### 9.1 Logistic regression

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=500, n_features=8, random_state=5)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=5
)

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
model.fit(X_train, y_train)

print(model.predict(X_test[:3]))
print(model.predict_proba(X_test[:3]))
print(model.score(X_test, y_test))
```

### 9.2 Decision scores versus probabilities

```python
scores = model.decision_function(X_test[:3])
probabilities = model.predict_proba(X_test[:3])

print(scores)
print(probabilities)
```

- `decision_function`: model score / logit / margin depending on model.
- `predict_proba`: estimated class probabilities **when supported**.
- `classes_`: ordering of probability columns.

### 9.3 Understanding `C`

For `LogisticRegression`, **smaller `C` means stronger regularization**. This is the inverse direction from Ridge's `alpha` parameter.

```python
from sklearn.linear_model import LogisticRegression

regularized = LogisticRegression(C=0.1)
less_regularized = LogisticRegression(C=10.0)
```

---

## 10. Decision trees and ensembles

### 10.1 Main estimator map

| Estimator | Method |
|---|---|
| `DecisionTreeClassifier` / `DecisionTreeRegressor` | Single decision tree |
| `RandomForestClassifier` / `RandomForestRegressor` | Bagged trees with feature randomness |
| `ExtraTreesClassifier` / `ExtraTreesRegressor` | Extremely randomized tree ensemble |
| `BaggingClassifier` / `BaggingRegressor` | Bootstrap ensemble of base estimators |
| `AdaBoostClassifier` / `AdaBoostRegressor` | Adaptive boosting |
| `GradientBoostingClassifier` / `GradientBoostingRegressor` | Sequential boosted trees |
| `HistGradientBoostingClassifier` / `HistGradientBoostingRegressor` | Histogram-based gradient boosting |
| `VotingClassifier` / `VotingRegressor` | Combine predictions |
| `StackingClassifier` / `StackingRegressor` | Learn combination of base models |

### 10.2 Decision trees

```python
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier, export_text

X, y = make_classification(n_samples=100, n_features=4, random_state=2)

model = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=2)
model.fit(X, y)

print(model.feature_importances_)
print(export_text(model, max_depth=2))
```

Depth limits and minimum leaf sizes provide important regularization for trees.

### 10.3 Random forests

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

X, y = make_classification(n_samples=400, n_features=8, random_state=2)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=3,
    random_state=2,
    n_jobs=-1,
)

model.fit(X, y)

print(model.predict_proba(X[:3]))
print(model.feature_importances_)
```

### 10.4 Histogram gradient boosting

```python
from sklearn.datasets import make_regression
from sklearn.ensemble import HistGradientBoostingRegressor

X, y = make_regression(n_samples=800, n_features=12, random_state=3)

model = HistGradientBoostingRegressor(
    max_iter=200,
    learning_rate=0.05,
    max_leaf_nodes=15,
    random_state=3,
)

model.fit(X, y)
print(model.predict(X[:4]))
```

Histogram-based gradient boosting is often useful for medium-to-large tabular datasets. Exact behavior, feature support, and performance vary by model and version.

### 10.5 Bias, variance, and ensembling

- A deep single tree may have low bias but high variance.
- Bagging often reduces variance by averaging diverse estimators.
- Boosting sequentially fits corrections and can reduce bias; regularization remains essential.
- Ensemble feature importances based on impurity can be biased toward high-cardinality features; compare against permutation importance on held-out data.

---

## 11. Support vector machines and nearest neighbors

### 11.1 SVM estimator map

| Estimator | Use |
|---|---|
| `SVC` | Kernel classification |
| `LinearSVC` | Linear margin classification |
| `SVR` | Kernel regression |
| `LinearSVR` | Linear support vector regression |
| `OneClassSVM` | Novelty detection |

```python
from sklearn.datasets import make_moons
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

X, y = make_moons(n_samples=300, noise=0.2, random_state=42)

model = make_pipeline(
    StandardScaler(),
    SVC(kernel="rbf", C=2.0, gamma="scale"),
)

model.fit(X, y)
print(model.predict(X[:5]))
```

For SVMs, scale sensitivity can be substantial. `SVC(probability=True)` can produce probabilities, but involves extra calibration cost and its probabilities may disagree with the sign of a decision score near the threshold.

### 11.2 Nearest neighbors

```python
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

X, y = make_classification(n_samples=100, n_features=5, random_state=1)

classifier = KNeighborsClassifier(n_neighbors=5, weights="distance")
classifier.fit(X, y)
print(classifier.predict(X[:3]))

neighbors = NearestNeighbors(n_neighbors=3).fit(X)
distances, indices = neighbors.kneighbors(X[:2])

print(distances)
print(indices)
```

Nearest-neighbor methods are sensitive to feature scales and frequently degrade in very high-dimensional spaces.

---

## 12. Naive Bayes, discriminant analysis, and Gaussian processes

| Estimator | Typical use |
|---|---|
| `GaussianNB` | Continuous features under Gaussian class-conditional assumption |
| `MultinomialNB` | Counts, nonnegative discrete features |
| `BernoulliNB` | Binary feature occurrence |
| `ComplementNB` | Text classification in imbalanced settings |
| `LinearDiscriminantAnalysis` | Generative linear classifier / dimension reduction |
| `QuadraticDiscriminantAnalysis` | Class-specific covariance decision boundaries |
| `GaussianProcessRegressor` | Probabilistic flexible regression with uncertainty |
| `GaussianProcessClassifier` | Gaussian-process classification |

```python
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

X, y = load_iris(return_X_y=True)

for model in [GaussianNB(), LinearDiscriminantAnalysis()]:
    model.fit(X, y)
    print(type(model).__name__, model.score(X, y))
```

Gaussian processes can supply posterior uncertainty, but scaling to many training samples can be expensive. They are not a universal replacement for gradient boosting on large tabular data.

---

## 13. Clustering

### 13.1 Major clustering algorithms

| Algorithm | Mechanism | Key considerations |
|---|---|---|
| `KMeans` | Centroid partitioning | Requires `n_clusters`; favors compact groups |
| `MiniBatchKMeans` | Incremental centroid updates | Larger datasets |
| `DBSCAN` | Density-connected groups | Identifies noise, sensitive to `eps` |
| `HDBSCAN` | Hierarchical density clustering | Density-varying structure; availability version-dependent |
| `AgglomerativeClustering` | Hierarchical merges | Linkage and distance metric |
| `SpectralClustering` | Graph-spectrum partitioning | Graph construction, scaling |
| `GaussianMixture` | Probabilistic mixture model | Soft assignments, distributional assumptions |
| `Birch` | Hierarchical subclustering | Large datasets |

### 13.2 K-means

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.7, random_state=42)

model = KMeans(n_clusters=3, n_init=10, random_state=42)
labels = model.fit_predict(X)

print(model.cluster_centers_)
print(model.inertia_)
print(labels[:10])
```

`inertia_` is within-cluster squared distance to centroids. Smaller inertia always results when enough additional clusters are added, so it is not sufficient to select cluster count alone.

### 13.3 DBSCAN

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler

X, _ = make_moons(n_samples=300, noise=0.07, random_state=42)
X = StandardScaler().fit_transform(X)

labels = DBSCAN(eps=0.3, min_samples=5).fit_predict(X)

print(set(labels))
```

Label `-1` designates points considered noise. Unlike KMeans, DBSCAN does not require preselecting a number of clusters.

### 13.4 Clustering scores

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score, adjusted_rand_score

X, true_labels = make_blobs(n_samples=200, centers=3, random_state=11)
predicted = KMeans(n_clusters=3, n_init=10, random_state=11).fit_predict(X)

print(silhouette_score(X, predicted))
print(adjusted_rand_score(true_labels, predicted))
```

`silhouette_score` assesses separation/compactness given features and a distance notion. `adjusted_rand_score` compares predicted group assignments with reference labels while adjusting for chance; cluster labels need not have the same numeric IDs.

---

## 14. Dimensionality reduction

| Transformer | Key role |
|---|---|
| `PCA` | Orthogonal directions of maximal variance |
| `IncrementalPCA` | Batched PCA updates |
| `TruncatedSVD` | SVD on sparse/count data without centering |
| `NMF` | Nonnegative additive factorization |
| `FastICA` | Independent component decomposition |
| `KernelPCA` | Nonlinear kernel embedding |
| `FactorAnalysis` | Latent-variable covariance structure |
| `TSNE` | Visualization-oriented nonlinear embedding |
| `Isomap` | Manifold embedding |

### 14.1 PCA

```python
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_wine(return_X_y=True)

model = make_pipeline(StandardScaler(), PCA(n_components=2))
Z = model.fit_transform(X)

print(Z.shape)
print(model.named_steps["pca"].explained_variance_ratio_)
```

PCA captures directions of feature variance, not necessarily directions most predictive of a target. Scaling can dramatically change PCA results.

### 14.2 Truncated SVD

```python
import numpy as np
from scipy.sparse import csr_array
from sklearn.decomposition import TruncatedSVD

X = csr_array(np.array([
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
], dtype=float))

model = TruncatedSVD(n_components=2, random_state=42)
Z = model.fit_transform(X)

print(Z.shape)
```

### 14.3 NMF

```python
import numpy as np
from sklearn.decomposition import NMF

X = np.array([
    [1.0, 0.0, 2.0],
    [0.0, 2.0, 1.0],
    [2.0, 1.0, 0.0],
])

model = NMF(n_components=2, init="random", random_state=1, max_iter=1000)
W = model.fit_transform(X)
H = model.components_

print(W.shape, H.shape)
print(W @ H)
```

NMF requires nonnegative data and produces an approximate factorization.

---

## 15. Anomaly detection and novelty detection

| Estimator | Technique |
|---|---|
| `IsolationForest` | Random isolation-based anomaly scoring |
| `LocalOutlierFactor` | Local density deviations |
| `OneClassSVM` | Boundary around typical observations |
| `EllipticEnvelope` | Robust covariance Gaussian-style envelope |

```python
import numpy as np
from sklearn.ensemble import IsolationForest

rng = np.random.default_rng(0)
normal = rng.normal(size=(100, 2))
anomalies = np.array([[6.0, 6.0], [-7.0, -5.0]])
X = np.vstack([normal, anomalies])

model = IsolationForest(contamination=0.02, random_state=0)
labels = model.fit_predict(X)
scores = model.decision_function(X)

print(labels[-2:])
print(scores[-2:])
```

Many outlier detectors return `+1` for normal/inlier and `-1` for anomaly/outlier. Larger `decision_function` values generally indicate more normal-looking points, but score conventions vary across methods.

For `LocalOutlierFactor`, standard use is `fit_predict` on training data. Use `novelty=True` when you need to score unseen observations, and avoid interpreting its in-sample and novelty modes as identical.

---

## 16. Model evaluation: classification

### 16.1 Confusion matrix

For binary labels 0 and 1:

```text
                 Predicted 0      Predicted 1
Actual 0         TN               FP
Actual 1         FN               TP
```

\[
\mathrm{Precision}=\frac{TP}{TP+FP},\quad
\mathrm{Recall}=\frac{TP}{TP+FN}
\]

\[
\mathrm{Specificity}=\frac{TN}{TN+FP},\quad
F_1=2\frac{PR}{P+R}
\]

### 16.2 Common classification metrics

| Function | Interprets |
|---|---|
| `accuracy_score` | Overall correct fraction |
| `balanced_accuracy_score` | Mean recall across classes |
| `precision_score` | Positive prediction precision |
| `recall_score` | Sensitivity / recall |
| `f1_score` | Harmonic mean precision and recall |
| `fbeta_score` | Custom relative recall weight |
| `confusion_matrix` | Counts by actual/predicted class |
| `classification_report` | Precision, recall, F1, support |
| `roc_auc_score` | Ranking across decision thresholds |
| `average_precision_score` | PR-curve summary |
| `log_loss` | Probabilistic cross-entropy |
| `brier_score_loss` | Squared probability error (binary) |
| `matthews_corrcoef` | Correlation-like classification score |
| `cohen_kappa_score` | Chance-adjusted categorical agreement |

```python
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
)

y_true = [0, 0, 0, 1, 1, 1]
y_pred = [0, 0, 1, 1, 0, 1]

print(accuracy_score(y_true, y_pred))
print(balanced_accuracy_score(y_true, y_pred))
print(precision_score(y_true, y_pred))
print(recall_score(y_true, y_pred))
print(f1_score(y_true, y_pred))
print(confusion_matrix(y_true, y_pred))
print(classification_report(y_true, y_pred))
```

### 16.3 ROC AUC, average precision, and log loss

```python
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss

y_true = [0, 0, 1, 1]
probabilities = [0.1, 0.4, 0.35, 0.9]

print(roc_auc_score(y_true, probabilities))
print(average_precision_score(y_true, probabilities))
print(log_loss(y_true, probabilities))
```

AUC measures ranking, not calibration. A model can have good ROC AUC but poorly calibrated probabilities.

### 16.4 Multiclass averaging

- `average='micro'`: pool contributions across classes.
- `average='macro'`: unweighted average of per-class scores.
- `average='weighted'`: average weighted by class supports.
- `average=None`: return per-class metrics where supported.

```python
from sklearn.metrics import f1_score

y_true = [0, 1, 2, 0, 1, 2]
y_pred = [0, 2, 2, 0, 1, 1]

print(f1_score(y_true, y_pred, average="macro"))
print(f1_score(y_true, y_pred, average="weighted"))
```

### 16.5 Display helpers

```python
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay
```

These helpers use fitted estimators or arrays, with display classes such as `.from_estimator()` and `.from_predictions()`.

---

## 17. Model evaluation: regression

| Metric | Lower / higher is better? | Notes |
|---|---|---|
| `mean_absolute_error` | Lower | Absolute error in response units |
| `mean_squared_error` | Lower | Squares large errors |
| `root_mean_squared_error` | Lower | Error in response units |
| `median_absolute_error` | Lower | Robust median absolute error |
| `mean_absolute_percentage_error` | Lower | Undefined-like behavior near zero, handled with finite large values |
| `r2_score` | Higher | Fraction of baseline variation explained |
| `explained_variance_score` | Higher | Explained variation; differs from R² under bias |
| `mean_pinball_loss` | Lower | Quantile regression loss |
| `mean_poisson_deviance` | Lower | Count response deviance |
| `mean_gamma_deviance` | Lower | Positive response deviance |

```python
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    r2_score,
    mean_pinball_loss,
)

y_true = [3.0, 5.0, 2.5, 7.0]
y_pred = [2.8, 5.3, 2.1, 6.5]

print(mean_absolute_error(y_true, y_pred))
print(mean_squared_error(y_true, y_pred))
print(root_mean_squared_error(y_true, y_pred))
print(r2_score(y_true, y_pred))
print(mean_pinball_loss(y_true, y_pred, alpha=0.9))
```

Never interpret a good training-set \(R^2\) as adequate evidence of generalization. Always evaluate out-of-sample.

---

## 18. Cross-validation strategies

### 18.1 Choose the splitter to match the data-generating process

| Splitter | Typical design |
|---|---|
| `KFold` | General independent samples |
| `StratifiedKFold` | Preserve classification class proportions |
| `RepeatedKFold` | Repeated random-fold validation |
| `GroupKFold` | Never split the same group across folds |
| `StratifiedGroupKFold` | Respect groups and approximate class balance |
| `LeaveOneGroupOut` | Entire group held out |
| `TimeSeriesSplit` | Chronological train → future validation |
| `ShuffleSplit` | Multiple random train/test partitions |
| `StratifiedShuffleSplit` | Stratified random partitions |

### 18.2 Cross-validation and scores

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc")

print(scores)
print(scores.mean(), scores.std())
```

### 18.3 Several metrics at once

```python
from sklearn.model_selection import cross_validate

results = cross_validate(
    model,
    X,
    y,
    cv=cv,
    scoring={"auc": "roc_auc", "accuracy": "accuracy", "f1": "f1"},
    return_train_score=True,
)

print(results.keys())
print(results["test_auc"].mean())
```

### 18.4 Group-aware validation

```python
import numpy as np
from sklearn.model_selection import GroupKFold

X = np.arange(24).reshape(12, 2)
y = np.array([0, 1] * 6)
groups = np.repeat([10, 20, 30, 40], 3)

for train_idx, valid_idx in GroupKFold(n_splits=4).split(X, y, groups):
    print(set(groups[train_idx]).intersection(set(groups[valid_idx])))
```

Each intersection should be empty. Useful when multiple observations come from the same person, account, station, entity, or customer.

### 18.5 Time series validation

```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

X = np.arange(18).reshape(-1, 1)

for train_idx, test_idx in TimeSeriesSplit(n_splits=3, gap=1).split(X):
    print(train_idx, test_idx)
```

`TimeSeriesSplit` assumes a suitable order and often roughly equal time spacing for comparable fold durations. A `gap` helps prevent proximity leakage, but **it does not automatically enforce arbitrary information publication lags** or prevent leakage from feature engineering performed before splitting.

### 18.6 Out-of-fold predictions

```python
from sklearn.model_selection import cross_val_predict
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))

out_of_fold = cross_val_predict(model, X, y, cv=5, method="predict_proba")
print(out_of_fold.shape)
```

`cross_val_predict` produces out-of-fold predictions, but the aggregated metric based on those predictions is not in general identical to the mean cross-validation score.

---

## 19. Hyperparameter search

### 19.1 Grid search

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipeline = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=2000)),
])

search = GridSearchCV(
    pipeline,
    param_grid={
        "model__C": [0.01, 0.1, 1.0, 10.0],
        "model__class_weight": [None, "balanced"],
    },
    scoring="roc_auc",
    cv=5,
    n_jobs=-1,
)

search.fit(X_train, y_train)

print(search.best_params_)
print(search.best_score_)
print(search.best_estimator_.score(X_test, y_test))
```

`best_score_` is the mean cross-validation **selection metric** on the training portion. The example's final `.score` is estimator default accuracy, not AUC; calculate held-out AUC explicitly when comparing like-for-like.

### 19.2 Randomized search

```python
from scipy.stats import loguniform
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC

search = RandomizedSearchCV(
    SVC(),
    param_distributions={
        "C": loguniform(1e-3, 1e3),
        "gamma": loguniform(1e-4, 1e1),
    },
    n_iter=20,
    cv=3,
    random_state=42,
)

search.fit(X_train, y_train)
print(search.best_params_)
```

This assumes `X_train, y_train` from the previous section; in a production workflow, include scaling inside the searched pipeline for SVMs.

### 19.3 Read search results

```python
import pandas as pd

results = pd.DataFrame(search.cv_results_)

print(results[["rank_test_score", "mean_test_score", "params"]].head())
```

### 19.4 Nested cross-validation

When reporting an unbiased comparison of tuning procedures, use **outer** cross-validation folds for evaluation and **inner** folds for hyperparameter selection. Reporting only `search.best_score_` tends to overstate performance if it is also used for final model assessment.

### 19.5 Successive halving

`HalvingGridSearchCV` and `HalvingRandomSearchCV` are experimental in some releases and require enabling their experimental module before import. Always verify version-specific status and resource settings.

---

## 20. Probability calibration and threshold selection

### 20.1 Probability calibration

Accurate ranking does not ensure accurate probabilities. If predictions are interpreted as risk probabilities, calibration deserves separate evaluation.

```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=800, n_features=10, random_state=7)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=7
)

model = CalibratedClassifierCV(
    RandomForestClassifier(n_estimators=100, random_state=7),
    method="sigmoid",
    cv=3,
)

model.fit(X_train, y_train)
probabilities = model.predict_proba(X_test)[:, 1]

print(brier_score_loss(y_test, probabilities))
```

Calibration must be learned from data that do not leak into the corresponding base predictions. `CalibratedClassifierCV` handles this through cross-validation when configured for CV fitting.

### 20.2 Threshold selection

```python
import numpy as np
from sklearn.metrics import precision_score, recall_score

y_true = np.array([0, 0, 1, 1, 0, 1])
p = np.array([0.05, 0.3, 0.4, 0.8, 0.6, 0.9])

for threshold in [0.3, 0.5, 0.7]:
    predicted = (p >= threshold).astype(int)
    print(threshold, precision_score(y_true, predicted), recall_score(y_true, predicted))
```

Optimize thresholds on a validation set or within a valid cross-validation design, never on the final untouched test set.

### 20.3 Threshold-vs-calibration distinction

- **Calibration:** does predicted 0.20 correspond to approximately 20% observed frequency?
- **Discrimination:** do risky cases receive higher scores than less risky cases?
- **Decision threshold:** at which estimated probability do you take action, given business costs?

---

## 21. Model inspection and interpretation

### 21.1 Permutation feature importance

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=500, n_features=8, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)

result = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10,
    random_state=42,
    scoring="accuracy",
)

print(result.importances_mean)
print(result.importances_std)
```

Permutation importance measures score degradation after shuffling one feature. Strongly correlated features can obscure one another's importance.

### 21.2 Partial dependence and ICE

```python
from sklearn.inspection import PartialDependenceDisplay

PartialDependenceDisplay.from_estimator(model, X_test, features=[0, 1], kind="average")
```

Partial dependence averages a model's predictions over a feature grid. It can evaluate unrealistic feature combinations when predictors are strongly correlated; it is **not** a causal effect estimate.

### 21.3 Reading coefficients

For a logistic regression, a unit change in feature \(x_j\) changes log-odds by the coefficient \(\beta_j\), conditional on the remaining variables *in that model*. Exponentiating the coefficient yields an odds ratio, but interpretation is affected by preprocessing and feature correlation.

```python
import numpy as np

beta = 0.4
print(np.exp(beta))
```

---

## 22. Class imbalance, weights, and metadata

### 22.1 Built-in class weights

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

logistic = LogisticRegression(class_weight="balanced")
forest = RandomForestClassifier(class_weight="balanced", random_state=42)
```

Balanced weighting is not equivalent to adjusting the decision threshold or calibrating probabilities. Class weighting can influence probability calibration.

### 22.2 Sample weights

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X = np.array([[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]])
y = np.array([0, 0, 0, 1, 1, 1])
weights = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])

model = LogisticRegression()
model.fit(X, y, sample_weight=weights)
print(model.coef_)
```

### 22.3 Metadata routing

Modern scikit-learn supports opt-in routing of metadata such as `sample_weight` through supported meta-estimators. It is still evolving; check the routing guide and the specific estimator's `set_fit_request()` and related interfaces.

```python
import sklearn
from sklearn.linear_model import LogisticRegression

sklearn.set_config(enable_metadata_routing=True)

model = LogisticRegression().set_fit_request(sample_weight=True)
print(model.get_metadata_routing())

sklearn.set_config(enable_metadata_routing=False)
```

For a pipeline with several consumers, each relevant component must appropriately request or decline the metadata. Routing is not needed for ordinary calls with only `X` and `y`.

---

## 23. Custom estimators and streaming updates

### 23.1 Custom transformer

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ClipFeatures(TransformerMixin, BaseEstimator):

    def __init__(self, lower: float = -5.0, upper: float = 5.0):
        self.lower = lower
        self.upper = upper

    def fit(self, X: np.ndarray, y: np.ndarray | None = None):
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        return np.clip(np.asarray(X), self.lower, self.upper)


transformer = ClipFeatures(lower=0.0, upper=3.0)
print(transformer.fit_transform([[-2, 1, 7]]))
print(transformer.get_params())
```

This follows key conventions: constructor arguments are stored as attributes with the same names; `fit` returns `self`; `transform` returns transformed features. For production-quality custom estimators, consider feature-name support, validation, `n_features_in_`, fitted-state checks, estimator tags, and `check_estimator`.

### 23.2 Incremental learning

```python
import numpy as np
from sklearn.linear_model import SGDClassifier

X1 = np.array([[0.0], [1.0], [2.0], [3.0]])
y1 = np.array([0, 0, 1, 1])
X2 = np.array([[0.5], [2.5], [1.5], [3.5]])
y2 = np.array([0, 1, 0, 1])

model = SGDClassifier(loss="log_loss", random_state=0)
model.partial_fit(X1, y1, classes=np.array([0, 1]))
model.partial_fit(X2, y2)

print(model.predict([[2.7]]))
```

`partial_fit` is not universally available; an incremental estimator updates its state on batches, and results depend on batch order and hyperparameters. `warm_start=True` is not synonymous with `partial_fit`.

---

## 24. Model persistence, reproducibility, and deployment

### 24.1 Persist a fitted pipeline

```python
import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X, y)

joblib.dump(model, "iris_pipeline.joblib")
restored = joblib.load("iris_pipeline.joblib")

print(restored.predict(X[:3]))
```

**Security warning:** pickle/joblib-based loading can execute arbitrary code. Never load untrusted model files. Persist version information and make sure training/serving environments are compatible; cross-version deserialization is not guaranteed.

### 24.2 Reproducibility checklist

1. Record training data snapshot and feature schema.
2. Set `random_state` for stochastic components where supported.
3. Fit preprocessing inside cross-validation folds.
4. Keep a final untouched test set.
5. Save evaluation metrics, subgroup diagnostics, and chosen threshold.
6. Persist dependencies and model parameters.
7. Check drift, calibration, and operational failure cases after deployment.
8. Avoid treating model outputs as causal explanations.

---

## 25. Complete end-to-end examples

### 25.1 Classification with Pandas and mixed features

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

rng = np.random.default_rng(42)
n = 600

X = pd.DataFrame({
    "income": rng.normal(70_000, 20_000, n),
    "utilization": rng.uniform(0, 1, n),
    "region": rng.choice(["east", "west", "north"], n),
})

logits = -2.0 - 0.000015 * (X["income"] - 70_000) + 4.0 * X["utilization"]
p = 1 / (1 + np.exp(-logits))
y = pd.Series(rng.binomial(1, p), name="target")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

numeric_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])

categorical_pipeline = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])

prep = ColumnTransformer([
    ("numeric", numeric_pipeline, ["income", "utilization"]),
    ("categorical", categorical_pipeline, ["region"]),
])

model = Pipeline([
    ("features", prep),
    ("classifier", LogisticRegression(max_iter=2000)),
])

model.fit(X_train, y_train)

predicted = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print(roc_auc_score(y_test, probabilities))
print(classification_report(y_test, predicted))
```

This is a synthetic classification example, not a validated credit risk model. Actual PD systems require strong time-based validation, representativeness analysis, calibration, monitoring, and governance.

### 25.2 Regression with feature scaling, search, and error evaluation

```python
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_regression(
    n_samples=1000,
    n_features=20,
    n_informative=8,
    noise=15,
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ("scale", StandardScaler()),
    ("ridge", Ridge()),
])

search = GridSearchCV(
    pipeline,
    {"ridge__alpha": [0.01, 0.1, 1, 10, 100]},
    cv=5,
    scoring="neg_root_mean_squared_error",
    n_jobs=-1,
)

search.fit(X_train, y_train)
predicted = search.predict(X_test)

print(search.best_params_)
print(mean_absolute_error(y_test, predicted))
print(root_mean_squared_error(y_test, predicted))
print(r2_score(y_test, predicted))
```

### 25.3 Feature selection inside cross-validation

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=300,
    n_features=30,
    n_informative=6,
    random_state=42,
)

pipeline = Pipeline([
    ("select", SelectKBest(score_func=f_classif, k=10)),
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=2000)),
])

print(cross_val_score(pipeline, X, y, cv=5, scoring="roc_auc"))
```

### 25.4 Time-aware workflow concept

For genuine chronological data, maintain an explicit feature timestamp and target-outcome timestamp. Ensure all predictors are available as of prediction time. Prefer expanding or rolling-origin validation with a suitable gap/embargo to match label maturity and operational lags.

---

## 26. Common mistakes and debugging

| Mistake | Why it matters | Better practice |
|---|---|---|
| Fit scaler before train/test split | Leakage | Fit inside `Pipeline` |
| Tune on test set | Selection bias | Reserve test for final assessment |
| Use shuffled CV for forward prediction | Temporal leakage | Time-ordered splitter |
| Split multiple rows from same customer across folds | Group leakage | `GroupKFold` |
| Use accuracy on rare-positive problem | Dominant class masks failures | PR, recall, precision, cost metrics |
| Interpret ROC AUC as calibration | Ranking ≠ absolute probability quality | Brier score/calibration curves |
| Use `LabelEncoder` on nominal feature columns | Artificial ordering | `OneHotEncoder` |
| Ignore unknown categories at deployment | Transform failure | `handle_unknown='ignore'` or suited strategy |
| Compare `.score()` values across estimator types | Different default metrics | Explicit scoring |
| Omit feature scaling for RBF SVM | Distorted distance geometry | Standardize within pipeline |
| Fit supervised selector before CV | Outcome leakage | Feature selector in pipeline |
| Assume `predict_proba` is always present | Not all estimators support it | Check interface / calibration |
| Trust impurity importance causally | Correlation and cardinality biases | Held-out permutation + domain checks |
| Confuse `C` and `alpha` | Opposite regularization interpretation | Check estimator objective |
| Refit final model on test data | Invalid evaluation | Keep test untouched |
| Load unknown pickle/joblib model | Code execution risk | Trusted artifacts only |

### 26.1 Inspect fitted pipeline internals

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
import numpy as np

X = np.arange(20, dtype=float).reshape(10, 2)
y = np.arange(10, dtype=float)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("ridge", Ridge()),
])

pipeline.fit(X, y)

print(pipeline.named_steps["scaler"].mean_)
print(pipeline.named_steps["ridge"].coef_)
print(pipeline.get_params()["ridge__alpha"])
```

---

## 27. Comprehensive API reference tables

### Data, preprocessing, composition

```text
model_selection.train_test_split          Holdout split
model_selection.KFold                    K-fold splitter
model_selection.StratifiedKFold          Class-preserving K-fold
model_selection.GroupKFold               Nonoverlapping groups
model_selection.TimeSeriesSplit          Ordered splits
model_selection.cross_val_score         Single-metric CV
model_selection.cross_validate          Multi-metric CV
model_selection.cross_val_predict       Out-of-fold predictions
model_selection.GridSearchCV            Exhaustive parameter combinations
model_selection.RandomizedSearchCV      Sample parameter combinations
pipeline.Pipeline                       Sequential preprocessing + estimator
pipeline.make_pipeline                  Auto-named pipeline
pipeline.FeatureUnion                   Horizontal combination of features
compose.ColumnTransformer              Column-specific transformations
compose.make_column_transformer         Constructor convenience
compose.make_column_selector            Column selection helper
compose.TransformedTargetRegressor      Transform regression target
preprocessing.StandardScaler            Mean/std scaling
preprocessing.RobustScaler              Median/quantile scaling
preprocessing.MinMaxScaler              Interval scaling
preprocessing.MaxAbsScaler              Absolute-max scaling
preprocessing.Normalizer                Row vector normalization
preprocessing.QuantileTransformer       Rank-quantile mapping
preprocessing.PowerTransformer          Distributional power transforms
preprocessing.OneHotEncoder             Nominal feature encoding
preprocessing.OrdinalEncoder            Ordered category encoding
preprocessing.LabelEncoder              Target label encoding
preprocessing.PolynomialFeatures        Polynomial and interaction features
preprocessing.SplineTransformer         Basis spline features
preprocessing.FunctionTransformer       Wrap custom transformation
impute.SimpleImputer                     Simple missing-value fill
impute.KNNImputer                        Neighbor-based fill
impute.MissingIndicator                  Missingness flags
```

### Models

```text
linear_model.LinearRegression            OLS
linear_model.Ridge / RidgeCV             L2 regression
linear_model.Lasso / LassoCV             L1 regression
linear_model.ElasticNet / ElasticNetCV   Mixed L1/L2 regression
linear_model.LogisticRegression          Logistic classifier
linear_model.SGDClassifier               Incremental linear classifier
linear_model.SGDRegressor                Incremental linear regressor
linear_model.HuberRegressor              Robust regression
linear_model.QuantileRegressor           Quantile regression
linear_model.PoissonRegressor            Poisson GLM
linear_model.GammaRegressor              Gamma GLM
tree.DecisionTreeClassifier              Classification tree
tree.DecisionTreeRegressor               Regression tree
ensemble.RandomForestClassifier         Bagged forest classifier
ensemble.RandomForestRegressor          Bagged forest regressor
ensemble.ExtraTreesClassifier           Randomized trees
ensemble.HistGradientBoostingClassifier Histogram boosted classifier
ensemble.HistGradientBoostingRegressor  Histogram boosted regressor
ensemble.GradientBoostingClassifier     Gradient boosting
ensemble.VotingClassifier               Ensemble voting
ensemble.StackingClassifier             Stacked models
svm.SVC / svm.SVR                       Kernel SVMs
svm.LinearSVC / svm.LinearSVR           Linear SVMs
neighbors.KNeighborsClassifier          KNN classifier
neighbors.KNeighborsRegressor           KNN regressor
naive_bayes.GaussianNB                  Gaussian Naive Bayes
naive_bayes.MultinomialNB               Count-based Naive Bayes
gaussian_process.GaussianProcessRegressor Probabilistic GP regression
```

### Unsupervised and evaluation

```text
cluster.KMeans                           Centroid partitioning
cluster.MiniBatchKMeans                  Batched K-means
cluster.DBSCAN                           Density clustering
cluster.AgglomerativeClustering         Hierarchical clustering
mixture.GaussianMixture                 Gaussian mixture
decomposition.PCA                        Principal components
decomposition.TruncatedSVD               Sparse-friendly SVD
decomposition.NMF                        Nonnegative factorization
decomposition.FastICA                    Independent components
ensemble.IsolationForest                Anomaly detection
neighbors.LocalOutlierFactor            Local density outliers
metrics.accuracy_score                  Accuracy
metrics.balanced_accuracy_score         Class-balanced accuracy
metrics.precision_score                 Precision
metrics.recall_score                    Recall
metrics.f1_score                        F1
metrics.confusion_matrix                Confusion matrix
metrics.roc_auc_score                   ROC AUC
metrics.average_precision_score         PR summary
metrics.log_loss                        Cross-entropy
metrics.brier_score_loss                Brier score
metrics.mean_absolute_error             MAE
metrics.mean_squared_error              MSE
metrics.root_mean_squared_error         RMSE
metrics.r2_score                        R²
metrics.silhouette_score                Cluster compactness/separation
metrics.adjusted_rand_score            Cluster agreement
inspection.permutation_importance       Held-out feature importance
inspection.PartialDependenceDisplay     Partial dependence / ICE
calibration.CalibratedClassifierCV      Probability calibration
feature_selection.SelectKBest           Univariate feature selection
feature_selection.RFE / RFECV           Recursive feature elimination
feature_selection.SelectFromModel       Model importance selection
feature_selection.SequentialFeatureSelector Stepwise selection
```

### Useful estimator attributes

```text
estimator.classes_                Known target labels (classifiers)
estimator.n_features_in_          Number of input features
estimator.feature_names_in_       Input feature names, when available
estimator.coef_                   Learned coefficients, supported models
estimator.intercept_              Learned intercept, supported models
estimator.feature_importances_    Learned importance, supported trees
transformer.get_feature_names_out() Names after transformation
pipeline.named_steps             Estimators by pipeline step name
search.best_params_              Best hyperparameter combination
search.best_estimator_           Best refitted estimator
search.best_score_               Cross-validated selection score
search.cv_results_               All tuning results
```

---

## 28. Exercises and solutions

### Exercise 1: Compare two classifiers fairly

Train a scaled logistic regression and a random forest on the same stratified train/test split, then compare held-out ROC AUC.

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=700, n_features=12, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=0
)

models = {
    "logistic": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    "forest": RandomForestClassifier(n_estimators=200, random_state=0),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    p = model.predict_proba(X_test)[:, 1]
    print(name, roc_auc_score(y_test, p))
```

### Exercise 2: Choose a threshold based on recall

```python
import numpy as np
from sklearn.metrics import precision_recall_curve

y_true = np.array([0, 1, 0, 1, 1, 0, 0, 1])
p = np.array([0.1, 0.9, 0.2, 0.55, 0.7, 0.4, 0.3, 0.6])

precision, recall, thresholds = precision_recall_curve(y_true, p)

valid = np.flatnonzero(recall[:-1] >= 0.75)
chosen = thresholds[valid[-1]]

print(chosen)
print((p >= chosen).astype(int))
```

This exercise optimizes against the same tiny data used to illustrate scores, not a correct real-world held-out evaluation design. In practice, threshold selection uses validation predictions.

### Exercise 3: Prevent feature-selection leakage

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

X, y = make_classification(n_samples=250, n_features=40, random_state=42)

model = make_pipeline(
    SelectKBest(f_classif, k=10),
    LogisticRegression(max_iter=1000),
)

print(cross_val_score(model, X, y, cv=5, scoring="roc_auc"))
```

### Additional practice

- Compare KFold vs StratifiedKFold when the positive class is rare.
- Construct a `ColumnTransformer` with missing numerical values and new categorical levels at inference time.
- Compare Ridge, ElasticNet, RandomForestRegressor, and HistGradientBoostingRegressor on the same held-out dataset.
- Evaluate calibration curves for a random forest before and after sigmoid calibration.
- Implement a custom transformer supporting feature names and validate it inside a pipeline.
- Explain why group-level and time-level leakage can persist even when preprocessing is correctly pipelined.

---

## 29. Official resources

- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Scikit-learn API Reference](https://scikit-learn.org/stable/api/index.html)
- [Common Pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)
- [Metadata Routing](https://scikit-learn.org/stable/metadata_routing.html)
- [Developing Scikit-learn Estimators](https://scikit-learn.org/stable/developers/develop.html)

**Suggested study order:** estimator protocol → leakage/splitting → preprocessing → pipelines → linear models → ensembles → metrics → cross-validation → hyperparameter search → calibration/interpretation → unsupervised methods → custom estimators and deployment.
