# SciPy

**Scope:** Scientific computing, statistics, numerical optimization, linear algebra, integration, differential equations, interpolation, sparse mathematics, signal processing, spatial algorithms, and numerical best practices.

**Companion libraries:** NumPy (`ndarray`), Pandas (`DataFrame`), scikit-learn (estimators), Matplotlib (plots).

## Table of contents

1. [Mental model and installation](#1-mental-model-and-installation)
2. [NumPy interoperability and conventions](#2-numpy-interoperability-and-conventions)
3. [`scipy.stats`: descriptive statistics and distributions](#3-scipystats-descriptive-statistics-and-distributions)
4. [Statistical inference and hypothesis tests](#4-statistical-inference-and-hypothesis-tests)
5. [Resampling, confidence intervals, and density estimation](#5-resampling-confidence-intervals-and-density-estimation)
6. [`scipy.optimize`: scalar and multivariable optimization](#6-scipyoptimize-scalar-and-multivariable-optimization)
7. [Constrained, global, and linear optimization](#7-constrained-global-and-linear-optimization)
8. [Equation solving and parameter estimation](#8-equation-solving-and-parameter-estimation)
9. [`scipy.linalg`: dense linear algebra](#9-scipylinalg-dense-linear-algebra)
10. [`scipy.sparse`: sparse arrays and solvers](#10-scipysparse-sparse-arrays-and-solvers)
11. [`scipy.integrate`: numerical integration](#11-scipyintegrate-numerical-integration)
12. [Ordinary differential equations](#12-ordinary-differential-equations)
13. [`scipy.interpolate`: interpolation and splines](#13-scipyinterpolate-interpolation-and-splines)
14. [`scipy.spatial`: distances and geometry](#14-scipyspatial-distances-and-geometry)
15. [`scipy.signal`: filtering and signal features](#15-scipysignal-filtering-and-signal-features)
16. [`scipy.fft`: Fourier analysis](#16-scipyfft-fourier-analysis)
17. [`scipy.ndimage`: multidimensional image operations](#17-scipyndimage-multidimensional-image-operations)
18. [`scipy.special`: special mathematical functions](#18-scipyspecial-special-mathematical-functions)
19. [Working with Pandas](#19-working-with-pandas)
20. [Numerical reliability, performance, and pitfalls](#20-numerical-reliability-performance-and-pitfalls)
21. [Quick-reference API maps](#21-quick-reference-api-maps)
22. [Exercises with solutions](#22-exercises-with-solutions)
23. [Official resources](#23-official-resources)

---

## 1. Mental model and installation

SciPy supplies tested numerical algorithms for problems that go beyond elementary array arithmetic. NumPy represents and manipulates the data; SciPy provides algorithms acting on it.

```text
Pandas DataFrame / NumPy array
            │
            ▼
Numerical problem formulation
            │
            ▼
SciPy: stats / optimize / linalg / integrate / interpolate / ...
            │
            ▼
Result array, parameter estimate, test result, or solver status
```

| Task | First tool to consider | Why |
|---|---|---|
| Sum, reshape, broadcast arrays | NumPy | Fundamental array operations |
| Join/filter/group tabular data | Pandas | Labeled data manipulation |
| Optimize a mathematical objective | SciPy optimize | Ready-made numerical solvers |
| Calculate a p-value | SciPy stats | Probability distributions and tests |
| Fit predictive classifiers | scikit-learn | ML estimator interface |
| Solve a differential equation | SciPy integrate | Adaptive ODE solvers |
| Analyze frequencies | SciPy signal / fft | Filtering and spectral algorithms |

Install:

```bash
python -m pip install -U numpy scipy pandas matplotlib
```

```python
import numpy as np
import scipy
from scipy import stats, optimize, linalg, integrate

print(scipy.__version__)
print(np.__version__)
```

The `scipy` top-level namespace does **not** duplicate all NumPy functions. Use `numpy` for array creation and basic operations.

## 2. NumPy interoperability and conventions

### 2.1 Shape, dtype, and axis

```python
import numpy as np
from scipy import stats

x = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

print(x.shape)
print(stats.zscore(x, axis=0))
print(stats.zscore(x, axis=1))
```

- `axis=0`: operate down rows, producing a statistic per column.
- `axis=1`: operate across columns, producing a statistic per row.
- `axis=None`: when supported, treat the array as one flattened sample.
- `keepdims=True`: when supported, preserve singleton dimensions for broadcasting.
- Many numerical routines expect floating-point arrays. Integer inputs may be promoted or treated differently depending on algorithm.

### 2.2 Randomness and reproducibility

```python
import numpy as np

rng = np.random.default_rng(42)
observations = rng.normal(loc=10.0, scale=2.0, size=100)
```

Prefer `numpy.random.default_rng()` for modern numerical examples. Some older SciPy functions use a `random_state` argument, while newer interfaces can expose `rng`; check the specific function signature.

### 2.3 Results are often objects, not scalar values

```python
from scipy.optimize import minimize

result = minimize(lambda x: (x[0] - 4) ** 2, x0=[0.0])

print(result.x)
print(result.fun)
print(result.success)
print(result.message)
print(result.nit)
```

Always check `result.success` and termination messages before trusting numerical optimization output.

---

## 3. `scipy.stats`: descriptive statistics and distributions

### 3.1 Descriptive-statistics function map

| API | Purpose | Caveat |
|---|---|---|
| `stats.describe(a)` | Count, extrema, mean, variance, skewness, kurtosis | Variance default differs from `np.var` default |
| `stats.sem(a)` | Standard error of sample mean | Accounts for sample size |
| `stats.zscore(a)` | Standardize observations | Handles `axis`, `nan_policy` |
| `stats.iqr(a)` | Interquartile range | Robust dispersion |
| `stats.trim_mean(a, proportiontocut)` | Trimmed mean | Robustness against extreme values |
| `stats.skew(a)` | Skewness | Distribution asymmetry |
| `stats.kurtosis(a)` | Excess kurtosis by default | Normal distribution has excess kurtosis 0 |
| `stats.mode(a)` | Most frequent value | Tie handling and shape vary by version |
| `stats.rankdata(a)` | Rank observations | Useful for nonparametric statistics |
| `stats.median_abs_deviation(a)` | Median absolute deviation | `scale='normal'` for normal-consistent scale |
| `stats.gmean(a)` | Geometric mean | Typically positive inputs |
| `stats.hmean(a)` | Harmonic mean | Typically positive inputs |

```python
import numpy as np
from scipy import stats

x = np.array([3.0, 4.0, 4.0, 5.0, 100.0])

print(stats.describe(x))
print(stats.iqr(x))
print(stats.trim_mean(x, 0.2))
print(stats.median_abs_deviation(x, scale="normal"))
print(stats.rankdata(x, method="average"))
```

### 3.2 Distribution objects: PDF, CDF, PPF, SF

For a continuous random variable:

- `pdf(x)`: probability **density**; not probability at a single exact value.
- `cdf(x)`: \(P(X \le x)\).
- `sf(x)`: survival function \(P(X > x)\); often more accurate than `1 - cdf(x)` in the tail.
- `ppf(q)`: inverse CDF (quantile); finds x such that `cdf(x)=q`.
- `isf(q)`: inverse survival function.
- `rvs(size=...)`: random draws.
- `mean()`, `var()`, `std()`, `stats()`, `interval()`, `fit()`: summary and fitting methods where supported.

```python
from scipy.stats import norm

print(norm.pdf(0.0, loc=0.0, scale=1.0))
print(norm.cdf(1.96))
print(norm.sf(1.96))
print(norm.ppf(0.975))
print(norm.isf(0.025))
print(norm.interval(0.95))
```

A normal distribution is parameterized by its mean `loc` and standard deviation `scale`.

```python
from scipy import stats

normal = stats.norm(loc=100, scale=15)

print(normal.mean())
print(normal.std())
print(normal.cdf(115))
print(normal.ppf(0.95))
```

### 3.3 Useful continuous and discrete families

| Distribution | API | Example applications |
|---|---|---|
| Normal | `stats.norm` | Gaussian noise, approximate errors |
| Student t | `stats.t` | Heavy-tailed outcomes, small samples |
| Chi-square | `stats.chi2` | Variance tests, goodness-of-fit |
| F | `stats.f` | Ratios of variances, ANOVA |
| Lognormal | `stats.lognorm` | Positive skewed measures |
| Gamma | `stats.gamma` | Waiting times, positive severity |
| Beta | `stats.beta` | Proportions between 0 and 1 |
| Exponential | `stats.expon` | Memoryless waiting times |
| Weibull | `stats.weibull_min` | Reliability / survival analysis |
| Bernoulli | `stats.bernoulli` | Binary event |
| Binomial | `stats.binom` | Success counts in fixed trials |
| Poisson | `stats.poisson` | Event counts |
| Negative binomial | `stats.nbinom` | Overdispersed counts |

Discrete distributions expose `pmf(k)` rather than `pdf(x)`.

```python
from scipy import stats

print(stats.binom.pmf(k=3, n=10, p=0.2))
print(stats.binom.sf(k=2, n=10, p=0.2))
print(stats.poisson.pmf(k=4, mu=3.0))
print(stats.beta.ppf(0.95, a=2, b=5))
```

### 3.4 Distribution fitting

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(5)
sample = rng.normal(loc=7.0, scale=1.5, size=1000)

mean_hat, std_hat = stats.norm.fit(sample)

print(mean_hat, std_hat)
```

Fitted parameters are estimates, not proof that the chosen distribution fits. Check assumptions and goodness-of-fit using held-out data, diagnostic plots, and appropriate tests.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(8)
positive_sample = rng.lognormal(mean=0.6, sigma=0.4, size=500)

shape, loc, scale = stats.lognorm.fit(positive_sample, floc=0)

print(shape, loc, scale)
```

`floc=0` fixes the location parameter at zero; this matters for positive-support distributions.

---

## 4. Statistical inference and hypothesis tests

### 4.1 Choose a test based on the experimental design

| Question | Candidate | Important conditions |
|---|---|---|
| Does one sample mean differ from a constant? | `ttest_1samp` | Independent observations; mean-based inference |
| Do two independent means differ? | `ttest_ind(..., equal_var=False)` | Welch's t-test; independence |
| Does the same subject change? | `ttest_rel` | Paired observations |
| Two independent samples, ranks | `mannwhitneyu` | Interpretation depends on distributional shapes |
| Paired signed differences | `wilcoxon` | Suitable paired differences |
| Compare 3+ means | `f_oneway` | ANOVA assumptions; use robust variants when needed |
| Rank-based 3+ independent groups | `kruskal` | Independent observations |
| Correlation, linear | `pearsonr` | Linear association |
| Correlation, rank monotonic | `spearmanr` | Rank-based association |
| Two categorical variables | `chi2_contingency` | Expected frequency considerations |
| Small 2×2 table | `fisher_exact` | Exact association test |
| Compare empirical distribution with reference | `kstest` | Important parameter-estimation caveats |
| Test normality | `shapiro`, `normaltest` | Large-n sensitivity and small-n limitations |

### 4.2 Independent two-sample Welch t-test

```python
from scipy.stats import ttest_ind

control = [5.1, 4.9, 5.3, 5.0, 5.2]
treatment = [5.9, 6.1, 6.0, 5.8, 6.2]

result = ttest_ind(control, treatment, equal_var=False)

print(result.statistic)
print(result.pvalue)
```

The p-value is the probability, under the null model and assumptions, of observing results at least as extreme as the observed statistic. It is **not** the probability the null hypothesis is true.

### 4.3 Paired observations

```python
from scipy.stats import ttest_rel

before = [100, 95, 105, 110, 102]
after = [97, 93, 100, 107, 100]

result = ttest_rel(before, after)
print(result.statistic, result.pvalue)
```

Pairing matters: independent and paired tests are not interchangeable.

### 4.4 Nonparametric and categorical tests

```python
from scipy.stats import mannwhitneyu, fisher_exact, chi2_contingency

x = [12, 18, 20, 25, 40]
y = [15, 16, 21, 22, 23]

print(mannwhitneyu(x, y, alternative="two-sided"))

contingency = [[12, 5], [4, 11]]
print(fisher_exact(contingency))
print(chi2_contingency(contingency))
```

### 4.5 Correlation and significance

```python
import numpy as np
from scipy.stats import pearsonr, spearmanr

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 5, 4, 7])

print(pearsonr(x, y))
print(spearmanr(x, y))
```

`PearsonRResult.statistic` is Pearson correlation \(r\), and `.pvalue` tests null correlation under the selected assumptions. Rank correlation is appropriate for monotonic patterns not necessarily linear.

### 4.6 Normality tests and limitations

```python
import numpy as np
from scipy.stats import shapiro, normaltest

rng = np.random.default_rng(20)
values = rng.normal(size=150)

print(shapiro(values))
print(normaltest(values))
```

A high p-value is not evidence that data are perfectly normal; a low p-value is not a measure of practical deviation. For very large samples, trivial deviations can become significant.

---

## 5. Resampling, confidence intervals, and density estimation

### 5.1 Bootstrap confidence interval

Bootstrapping repeatedly resamples observations to estimate sampling uncertainty.

```python
import numpy as np
from scipy.stats import bootstrap

rng = np.random.default_rng(1)
values = rng.gamma(shape=2, scale=3, size=100)

result = bootstrap(
    (values,),
    np.mean,
    confidence_level=0.95,
    n_resamples=2000,
    random_state=42,
)

print(result.confidence_interval)
print(result.standard_error)
```

An ordinary bootstrap assumes a suitable resampling structure. For dependent time-series observations, consider block-based resampling instead of independently resampling rows.

### 5.2 Permutation test

```python
import numpy as np
from scipy.stats import permutation_test

left = np.array([1.0, 2.0, 3.0, 4.0])
right = np.array([3.0, 4.0, 5.0, 6.0])

result = permutation_test(
    (left, right),
    lambda a, b: np.mean(a) - np.mean(b),
    permutation_type="independent",
    n_resamples=2000,
    alternative="two-sided",
    random_state=11,
)

print(result.statistic, result.pvalue)
```

Permutation tests depend on **exchangeability** under the null. They do not automatically solve confounding or dependence.

### 5.3 Kernel density estimation (KDE)

```python
import numpy as np
from scipy.stats import gaussian_kde

rng = np.random.default_rng(4)
sample = rng.normal(loc=10, scale=2, size=300)

density = gaussian_kde(sample)
grid = np.linspace(0, 20, 100)

values = density(grid)
print(values.shape)
```

KDE estimates a smooth density, not discrete probabilities. Bandwidth selection strongly affects smoothness; KDE may behave poorly near hard boundaries such as zero.

---

## 6. `scipy.optimize`: scalar and multivariable optimization

### 6.1 Optimization vocabulary

Given \(f(x)\), optimization seeks inputs minimizing or maximizing an objective subject to constraints.

- Objective function: numerical quantity to minimize.
- Decision variables: values the solver can change.
- Gradient / Jacobian: first derivatives used for optimization.
- Hessian: matrix of second derivatives.
- Bounds: limits on individual variables.
- Constraints: restrictions involving multiple variables.
- Local minimum: best within a neighborhood; not necessarily globally best.
- Tolerance: criteria for acceptable convergence.

### 6.2 Scalar minimization

```python
from scipy.optimize import minimize_scalar

result = minimize_scalar(
    lambda x: (x - 3) ** 2 + 5,
    bounds=(0, 10),
    method="bounded",
)

print(result.x)
print(result.fun)
print(result.success)
```

Expected approximate optimum: `x=3`, minimum `5`.

### 6.3 Multivariable minimization

```python
import numpy as np
from scipy.optimize import minimize


def objective(x: np.ndarray) -> float:
    return (x[0] - 2) ** 2 + 3 * (x[1] + 1) ** 2


result = minimize(objective, x0=[0.0, 0.0], method="BFGS")

print(result.x)
print(result.fun)
print(result.success)
```

Expected approximate optimum: `[2, -1]`.

### 6.4 Provide an analytic gradient

```python
import numpy as np
from scipy.optimize import minimize


def objective(x: np.ndarray) -> float:
    return (x[0] - 2) ** 2 + 3 * (x[1] + 1) ** 2


def gradient(x: np.ndarray) -> np.ndarray:
    return np.array([2 * (x[0] - 2), 6 * (x[1] + 1)])


result = minimize(objective, x0=[0.0, 0.0], jac=gradient, method="BFGS")
print(result.x)
```

Providing correct derivatives can reduce optimization cost. Incorrect gradients can produce wrong or unstable results.

### 6.5 Bounds with L-BFGS-B

```python
from scipy.optimize import minimize

result = minimize(
    lambda x: (x[0] - 5) ** 2,
    x0=[0.0],
    bounds=[(0.0, 3.0)],
    method="L-BFGS-B",
)

print(result.x)
```

The unconstrained minimum at 5 is outside the allowed interval, so the constrained optimum is at the boundary 3.

### 6.6 Key optimizer methods

| Algorithm / API | Typical use |
|---|---|
| `minimize(..., method='BFGS')` | Smooth unconstrained problems |
| `minimize(..., method='L-BFGS-B')` | Smooth, bound-constrained problems |
| `minimize(..., method='SLSQP')` | Smooth constrained nonlinear programs |
| `minimize(..., method='trust-constr')` | General constrained problems |
| `minimize(..., method='Nelder-Mead')` | Derivative-free local search |
| `minimize_scalar()` | One decision variable |
| `differential_evolution()` | Global, bounded stochastic search |
| `dual_annealing()` | Global stochastic optimization |
| `least_squares()` | Residual-based nonlinear least squares |
| `curve_fit()` | Convenient nonlinear curve fitting |
| `root()` | Multidimensional roots |
| `root_scalar()` | One-dimensional roots |
| `linprog()` | Linear programming |
| `milp()` | Mixed-integer linear programming |

---

## 7. Constrained, global, and linear optimization

### 7.1 Equality-constrained minimization

Minimize squared distance to a target subject to \(x_0+x_1=1\).

```python
import numpy as np
from scipy.optimize import minimize


def objective(x: np.ndarray) -> float:
    return (x[0] - 0.8) ** 2 + (x[1] - 0.7) ** 2


constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}

result = minimize(
    objective,
    x0=[0.5, 0.5],
    bounds=[(0, 1), (0, 1)],
    constraints=constraints,
    method="SLSQP",
)

print(result.x, result.success)
```

Legacy dictionary constraints are convenient, while `LinearConstraint` and `NonlinearConstraint` provide explicit objects for modern solvers.

### 7.2 Linear programming

`linprog()` **minimizes** \(c^T x\) subject to \(A_{ub}x \le b_{ub}\), \(A_{eq}x=b_{eq}\), and bounds.

```python
from scipy.optimize import linprog

result = linprog(
    c=[-3.0, -2.0],
    A_ub=[[1.0, 1.0], [2.0, 1.0]],
    b_ub=[4.0, 5.0],
    bounds=[(0, None), (0, None)],
    method="highs",
)

print(result.x)
print(-result.fun)
print(result.success)
```

Negative coefficients convert a profit-maximization objective into a minimization objective.

### 7.3 Global optimization

```python
import numpy as np
from scipy.optimize import differential_evolution


def objective(x: np.ndarray) -> float:
    return np.sin(5 * x[0]) + 0.1 * x[0] ** 2


result = differential_evolution(
    objective,
    bounds=[(-4.0, 4.0)],
    seed=42,
)

print(result.x, result.fun)
```

Global optimizers are generally more expensive. Repeated runs or domain-specific checks may still be needed.

---

## 8. Equation solving and parameter estimation

### 8.1 Root finding

```python
from scipy.optimize import root_scalar

result = root_scalar(lambda x: x ** 3 - 2, bracket=[0, 2], method="brentq")

print(result.root)
print(result.converged)
```

`root_scalar()` solves \(f(x)=0\), not \(\min f(x)\).

```python
import numpy as np
from scipy.optimize import root


def equations(x: np.ndarray) -> np.ndarray:
    return np.array([x[0] + x[1] - 3, x[0] - x[1] - 1])


result = root(equations, x0=[0.0, 0.0])
print(result.x)
```

Expected `[2, 1]`.

### 8.2 Nonlinear least squares

```python
import numpy as np
from scipy.optimize import least_squares

x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([1.1, 3.0, 5.2, 7.1])


def residuals(params: np.ndarray) -> np.ndarray:
    slope, intercept = params
    return slope * x + intercept - y


result = least_squares(residuals, x0=[1.0, 0.0])
print(result.x)
```

`least_squares()` minimizes \(\tfrac{1}{2}\sum_i r_i(x)^2\). Use robust losses such as `loss='soft_l1'` when outliers would otherwise dominate.

### 8.3 Nonlinear curve fitting

```python
import numpy as np
from scipy.optimize import curve_fit

x = np.linspace(0, 3, 20)
y = 2.0 * np.exp(-0.8 * x) + 0.5


def decay(x: np.ndarray, amplitude: float, rate: float, offset: float) -> np.ndarray:
    return amplitude * np.exp(-rate * x) + offset


parameters, covariance = curve_fit(
    decay,
    x,
    y,
    p0=[1.0, 0.5, 0.0],
    bounds=([0, 0, -np.inf], [np.inf, np.inf, np.inf]),
)

print(parameters)
print(np.sqrt(np.diag(covariance)))
```

The covariance approximation depends on the model and error assumptions; uncertainty estimates can be unreliable for poorly identified parameters.

### 8.4 Difference: optimization vs roots vs curve fitting

| Problem | Model | API |
|---|---|---|
| Find smallest value | \(\min f(x)\) | `minimize` |
| Solve equality | \(g(x)=0\) | `root`, `root_scalar` |
| Fit model parameters to data | \(\min \sum r_i(\theta)^2\) | `least_squares`, `curve_fit` |
| Enforce linear constraints | \(\min c^T x\) | `linprog` |

---

## 9. `scipy.linalg`: dense linear algebra

### 9.1 Dense matrix function map

| Function | Operation |
|---|---|
| `linalg.solve(A, b)` | Solve linear system \(Ax=b\) |
| `linalg.lstsq(A, b)` | Least-squares solution |
| `linalg.inv(A)` | Inverse of nonsingular matrix |
| `linalg.det(A)` | Determinant |
| `linalg.eig(A)` | Eigenvalues/eigenvectors of general matrix |
| `linalg.eigh(A)` | Eigenvalues/eigenvectors of symmetric/Hermitian matrix |
| `linalg.svd(A)` | Singular value decomposition |
| `linalg.qr(A)` | QR decomposition |
| `linalg.cholesky(A)` | Cholesky factorization |
| `linalg.lu(A)` | LU decomposition |
| `linalg.norm(A)` | Vector/matrix norm |
| `linalg.expm(A)` | Matrix exponential |
| `linalg.logm(A)` | Matrix logarithm |
| `linalg.block_diag(...)` | Block-diagonal matrix construction |

### 9.2 Solve instead of inverting

```python
import numpy as np
from scipy.linalg import solve, inv

A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])

x = solve(A, b)

print(x)
print(np.allclose(A @ x, b))
print(inv(A) @ b)
```

Expected `x = [2, 3]`. Prefer `solve(A,b)` rather than explicitly forming `inv(A) @ b`: it is usually faster and more numerically stable.

### 9.3 Least squares for overdetermined systems

```python
import numpy as np
from scipy.linalg import lstsq

A = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0]])
y = np.array([2.0, 2.9, 4.2])

coefficients, residuals, rank, singular_values = lstsq(A, y)

print(coefficients)
print(rank)
```

### 9.4 Eigenvalues and SVD

```python
import numpy as np
from scipy.linalg import eigh, svd

A = np.array([[2.0, 1.0], [1.0, 2.0]])

eigenvalues, eigenvectors = eigh(A)
U, singular_values, Vh = svd(A)

print(eigenvalues)
print(np.allclose(U @ np.diag(singular_values) @ Vh, A))
```

`eigh()` is for Hermitian/symmetric matrices; it is often preferable to `eig()` for covariance matrices.

### 9.5 Cholesky factorization and covariance

```python
import numpy as np
from scipy.linalg import cholesky, solve_triangular

cov = np.array([[4.0, 1.0], [1.0, 3.0]])
L = cholesky(cov, lower=True)

y = solve_triangular(L, np.array([1.0, 2.0]), lower=True)

print(L)
print(np.allclose(L @ L.T, cov))
print(y)
```

Requires a positive-definite matrix. Nearly singular covariance matrices require extra care.

---

## 10. `scipy.sparse`: sparse arrays and solvers

Sparse structures store only (or primarily) nonzero values, avoiding dense \(n\times n\) storage for sparse problems.

| Format | Strength |
|---|---|
| CSR (`csr_array`) | Fast row slicing, matrix-vector operations |
| CSC (`csc_array`) | Fast column slicing, factorization workflows |
| COO (`coo_array`) | Convenient construction from coordinates |
| LIL (`lil_array`) | Incremental construction |
| DIA (`diags`) | Diagonal/banded matrices |

Prefer modern sparse **array** APIs (`csr_array`, `csc_array`) in new code when possible. Older `csr_matrix` / `csc_matrix` classes remain common in existing libraries.

### 10.1 Sparse array construction

```python
import numpy as np
from scipy.sparse import csr_array, diags

A = csr_array([
    [1.0, 0.0, 0.0],
    [0.0, 2.0, 0.0],
    [0.0, 0.0, 3.0],
])

print(A.nnz)
print(A.toarray())
print((A @ np.array([1.0, 2.0, 3.0])).tolist())

D = diags([1.0, 2.0, 3.0], offsets=0, format="csr")
print(D.toarray())
```

### 10.2 Sparse linear systems

```python
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve, cg

A = diags([2.0, 2.0, 2.0], offsets=0, format="csr")
b = np.array([2.0, 4.0, 6.0])

print(spsolve(A, b))

solution, info = cg(A, b)
print(solution)
print(info)
```

`info == 0` indicates successful convergence for `cg`. Conjugate gradient generally requires a symmetric positive-definite operator.

### 10.3 Leading eigenpairs

```python
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

A = diags([1.0, 2.0, 3.0, 4.0, 5.0], offsets=0, format="csr")

eigenvalues, eigenvectors = eigsh(A, k=2, which="LM")

print(eigenvalues)
print(eigenvectors.shape)
```

Use sparse algorithms when the matrix is sufficiently large and sparse. Converting a huge sparse matrix to dense with `.toarray()` can exhaust memory.

---

## 11. `scipy.integrate`: numerical integration

### 11.1 Integrate a function using `quad`

```python
from scipy.integrate import quad

value, estimated_error = quad(lambda x: x ** 2, 0.0, 2.0)

print(value)
print(estimated_error)
```

Expected value: \(8/3 \approx 2.6667\).

### 11.2 Integrate sampled observations

```python
import numpy as np
from scipy.integrate import trapezoid, simpson, cumulative_trapezoid

x = np.linspace(0.0, 2.0, 101)
y = x ** 2

print(trapezoid(y, x=x))
print(simpson(y, x=x))
print(cumulative_trapezoid(y, x=x, initial=0.0)[-1])
```

| Function | Input | Use |
|---|---|---|
| `quad(f, a, b)` | Callable | Adaptive quadrature |
| `dblquad`, `tplquad` | Callable | 2D and 3D integrals |
| `nquad` | Callable | N-dimensional integration |
| `trapezoid(y, x)` | Samples | Trapezoidal approximation |
| `simpson(y, x)` | Samples | Simpson's rule |
| `cumulative_trapezoid(y, x)` | Samples | Running integral |
| `solve_ivp` | Differential equation | Initial-value ODE solver |

Important: `quad` returns `(integral, error_estimate)`, whereas `trapezoid` returns a numerical integral directly.

---

## 12. Ordinary differential equations

Solve \(dy/dt = -ky\) with \(y(0)=10\).

Analytical solution: \(y(t)=10e^{-kt}\).

```python
import numpy as np
from scipy.integrate import solve_ivp


def derivative(t: float, y: np.ndarray, k: float) -> np.ndarray:
    return -k * y


t_grid = np.linspace(0.0, 5.0, 50)

solution = solve_ivp(
    derivative,
    t_span=(0.0, 5.0),
    y0=[10.0],
    args=(0.8,),
    t_eval=t_grid,
    rtol=1e-8,
    atol=1e-10,
)

print(solution.success)
print(solution.y.shape)
print(solution.y[0, -1])
```

The solver receives `(t, y, *args)`. `solution.t` is the time grid and `solution.y` has shape `(number_of_state_variables, number_of_times)`.

Common solvers: `RK45` (default general nonstiff), `DOP853` (high accuracy nonstiff), `Radau`/`BDF` (often suitable for stiff systems), `LSODA` (automatic stiffness switching).

---

## 13. `scipy.interpolate`: interpolation and splines

Interpolation estimates values **between** observed points; extrapolation estimates **outside** the observed range and may be unstable.

| Function | Best suited to |
|---|---|
| `np.interp` | Simple one-dimensional linear interpolation |
| `interp1d` | Older common interpolation wrapper; considered legacy |
| `CubicSpline` | Smooth cubic interpolation, with derivatives |
| `PchipInterpolator` | Shape-preserving, reduces overshooting |
| `Akima1DInterpolator` | Smooth local interpolation |
| `RegularGridInterpolator` | N-dimensional rectilinear grids |
| `RBFInterpolator` | Scattered multidimensional data |
| `make_interp_spline` | B-spline construction |
| `UnivariateSpline` | Legacy smoothing/interpolating spline |

### 13.1 Cubic spline

```python
import numpy as np
from scipy.interpolate import CubicSpline

x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([0.0, 1.0, 0.0, 2.0])

spline = CubicSpline(x, y)

print(spline(1.5))
print(spline(1.5, 1))
print(spline(1.5, 2))
```

Derivative order 1 returns the slope; derivative order 2 returns the second derivative.

### 13.2 Shape-preserving interpolation

```python
import numpy as np
from scipy.interpolate import PchipInterpolator

x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([0.0, 1.0, 1.2, 1.3])

interpolator = PchipInterpolator(x, y)
print(interpolator(np.linspace(0, 3, 7)))
```

`PchipInterpolator` is often useful for monotone curves where an unconstrained cubic spline could introduce artificial oscillations.

### 13.3 Multi-dimensional regular grid

```python
import numpy as np
from scipy.interpolate import RegularGridInterpolator

x = np.array([0.0, 1.0, 2.0])
y = np.array([0.0, 10.0])
values = x[:, None] + 0.2 * y[None, :]

interpolator = RegularGridInterpolator((x, y), values)
print(interpolator([[0.5, 5.0], [1.5, 7.0]]))
```

### 13.4 Interpolation versus regression

Interpolation fits the observed points exactly (except when using smoothing interpolators). Regression models trends while allowing residuals. Do not use exact interpolation as a substitute for predictive validation.

---

## 14. `scipy.spatial`: distances and geometry

### 14.1 Pairwise distances

```python
import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform

A = np.array([[0.0, 0.0], [1.0, 1.0]])
B = np.array([[1.0, 0.0], [2.0, 2.0]])

print(cdist(A, B, metric="euclidean"))
print(cdist(A, B, metric="cityblock"))
print(squareform(pdist(A)))
```

- `cdist(A, B)`: distances between each row of A and each row of B.
- `pdist(A)`: compressed pairwise distances among rows of A.
- `squareform(...)`: compressed vector ↔ square distance matrix.

### 14.2 KD-tree and nearest-neighbor search

```python
import numpy as np
from scipy.spatial import cKDTree

points = np.array([[0, 0], [1, 1], [5, 5], [10, 10]])
tree = cKDTree(points)

distances, indices = tree.query([[0.5, 0.5]], k=2)

print(distances)
print(indices)
```

Nearest-neighbor performance is sensitive to dimensionality; trees become less advantageous in very high-dimensional settings.

### 14.3 Convex hull

```python
import numpy as np
from scipy.spatial import ConvexHull

points = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0.5, 0.5]])
hull = ConvexHull(points)

print(hull.vertices)
print(hull.volume)
```

In 2D, `hull.volume` represents area and `hull.area` represents perimeter.

---

## 15. `scipy.signal`: filtering and signal features

| Function | Purpose |
|---|---|
| `find_peaks` | Identify local peaks |
| `peak_prominences` | Quantify peak prominence |
| `savgol_filter` | Smooth while preserving local polynomial structure |
| `butter` | Butterworth filter design |
| `sosfilt` | Apply filter using second-order sections |
| `sosfiltfilt` | Forward-backward filtering, approximately zero phase |
| `periodogram` | Estimate power spectral density |
| `welch` | Averaged spectral estimate |
| `resample_poly` | Polyphase resampling |
| `convolve` / `fftconvolve` | Convolution |
| `correlate` | Cross-correlation |

### 15.1 Peak detection

```python
import numpy as np
from scipy.signal import find_peaks

values = np.array([0, 3, 1, 4, 0, 2, 0])

indices, properties = find_peaks(values, prominence=1.0)

print(indices)
print(properties["prominences"])
```

### 15.2 Smooth noisy observations

```python
import numpy as np
from scipy.signal import savgol_filter

rng = np.random.default_rng(9)
x = np.linspace(0, 2 * np.pi, 101)
y = np.sin(x) + rng.normal(scale=0.1, size=x.size)

smoothed = savgol_filter(y, window_length=11, polyorder=3)
print(smoothed.shape)
```

`window_length` must be an appropriate odd positive length for the data; `polyorder < window_length`.

### 15.3 Low-pass Butterworth filtering

```python
import numpy as np
from scipy.signal import butter, sosfiltfilt

sampling_rate = 100.0
t = np.arange(0, 2.0, 1.0 / sampling_rate)
x = np.sin(2 * np.pi * 2 * t) + 0.5 * np.sin(2 * np.pi * 25 * t)

sos = butter(4, 5.0, btype="lowpass", fs=sampling_rate, output="sos")
filtered = sosfiltfilt(sos, x)

print(filtered.shape)
```

Use `sos` representations for good numerical behavior. Forward-backward filtering uses future samples and is not appropriate for a strictly causal real-time process.

---

## 16. `scipy.fft`: Fourier analysis

FFT transforms a discrete signal into frequency components. For real signals, prefer `rfft()` and `rfftfreq()` when only nonnegative frequencies are needed.

```python
import numpy as np
from scipy.fft import rfft, rfftfreq, irfft

fs = 100.0
t = np.arange(0, 1.0, 1.0 / fs)
signal = np.sin(2 * np.pi * 5 * t)

spectrum = rfft(signal)
frequencies = rfftfreq(signal.size, d=1 / fs)

peak_frequency = frequencies[np.argmax(np.abs(spectrum[1:])) + 1]
reconstructed = irfft(spectrum, n=signal.size)

print(peak_frequency)
print(np.allclose(signal, reconstructed))
```

Other methods: `fft`, `ifft`, `fft2`, `ifft2`, `fftn`, `ifftn`, `fftshift`, `next_fast_len`.

Spectral amplitudes depend on normalization, sample count, windowing, and sampling frequency. FFT assumes samples lie on a uniform time grid.

---

## 17. `scipy.ndimage`: multidimensional image operations

Useful routines include `gaussian_filter`, `median_filter`, `sobel`, `laplace`, `zoom`, `rotate`, `shift`, `label`, `binary_erosion`, `binary_dilation`, `binary_opening`, and `binary_closing`.

```python
import numpy as np
from scipy.ndimage import gaussian_filter, sobel, label

image = np.zeros((7, 7), dtype=float)
image[2:5, 2:5] = 1.0

blurred = gaussian_filter(image, sigma=1.0)
edges = sobel(image, axis=0)
regions, count = label(image > 0)

print(blurred.shape)
print(edges.shape)
print(count)
```

`ndimage` operates on arbitrary-dimensional arrays; it is not restricted to photographs.

---

## 18. `scipy.special`: special mathematical functions

| Function | Purpose |
|---|---|
| `expit(x)` | Numerically stable logistic sigmoid |
| `logit(p)` | Inverse sigmoid |
| `softmax(x, axis=...)` | Normalize logit scores into probabilities |
| `logsumexp(x)` | Stable log of sum of exponentials |
| `gamma(x)` | Gamma function |
| `gammaln(x)` | Log-absolute-gamma; avoids huge intermediate values |
| `erf(x)` / `erfc(x)` | Error and complementary error functions |
| `comb(n, k)` | Binomial coefficient |
| `factorial(n)` | Factorial |
| `xlogy(x, y)` | Stable handling of terms like \(x\log(y)\) |

```python
import numpy as np
from scipy.special import expit, logit, softmax, logsumexp, gammaln

z = np.array([-1000.0, 0.0, 1000.0])

print(expit(z))
print(logit(0.8))
print(softmax([1.0, 2.0, 3.0]))
print(logsumexp([1000.0, 1001.0]))
print(gammaln(5.0))
```

For large logits, `logsumexp` is much more stable than evaluating `np.log(np.sum(np.exp(x)))` directly.

---

## 19. Working with Pandas

### 19.1 Columns into numerical functions

```python
import pandas as pd
from scipy import stats

df = pd.DataFrame({
    "segment": ["A", "A", "A", "B", "B", "B"],
    "loss": [1.0, 1.5, 2.1, 2.5, 2.8, 3.0],
})

samples_a = df.loc[df["segment"] == "A", "loss"].to_numpy()
samples_b = df.loc[df["segment"] == "B", "loss"].to_numpy()

result = stats.ttest_ind(samples_a, samples_b, equal_var=False)
print(result.pvalue)
```

### 19.2 Optimize weights to match a target

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

df = pd.DataFrame({
    "scenario_a": [2.0, 3.0, 4.0],
    "scenario_b": [5.0, 2.0, 1.0],
    "target": [3.0, 2.5, 2.0],
})

X = df[["scenario_a", "scenario_b"]].to_numpy()
y = df["target"].to_numpy()


def mse(weights: np.ndarray) -> float:
    return float(np.mean((X @ weights - y) ** 2))


result = minimize(
    mse,
    x0=[0.5, 0.5],
    bounds=[(0, 1), (0, 1)],
    constraints={"type": "eq", "fun": lambda w: np.sum(w) - 1},
    method="SLSQP",
)

print(result.x)
print(result.success)
```

For a probability-of-default or loss-severity project, SciPy can support parameter estimation and optimization, but it does **not** itself provide a complete out-of-the-box credit-risk modeling system.

---

## 20. Numerical reliability, performance, and pitfalls

### 20.1 Condition numbers

```python
import numpy as np

A = np.array([[1.0, 1.0], [1.0, 1.0000001]])

print(np.linalg.cond(A))
```

A high condition number indicates sensitivity to small perturbations. Numerical stability depends on the problem as well as the algorithm.

### 20.2 Numerical tolerance

```python
import numpy as np

actual = np.array([0.1 + 0.2])
expected = np.array([0.3])

print(actual == expected)
print(np.allclose(actual, expected, rtol=1e-7, atol=1e-9))
```

### 20.3 Performance and correctness checklist

1. Check shapes and units before passing data to SciPy.
2. Prefer vectorized residual/objective implementations where possible.
3. Verify feasible bounds and constraints before optimization.
4. Inspect convergence status, residual size, and sensitivity to initial guesses.
5. Scale variables when magnitudes vary greatly.
6. Prefer stable algorithms (`solve` rather than explicit inverse; `logsumexp` rather than raw exponentiation).
7. Avoid densifying huge sparse arrays.
8. Distinguish statistical significance from causal or practical significance.
9. Select tests by sampling design, not solely by p-value.
10. Validate interpolation and extrapolation separately.
11. Use `nan_policy` when supported; check missing values explicitly otherwise.
12. Set reproducible random seeds for randomized algorithms.
13. Beware of in-place mutation if the algorithm may reuse your arrays.
14. Test numerical pipelines on small analytically solvable examples.

### 20.4 Deprecated or legacy practices

- `scipy.interpolate.interp1d` is documented as legacy; prefer targeted modern interpolators in new code.
- `scipy.integrate.trapz`, `cumtrapz`, and `simps` were removed in modern SciPy; use `trapezoid`, `cumulative_trapezoid`, and `simpson`.
- Prefer `scipy.fft` to old `scipy.fftpack` for new work.
- Prefer NumPy for basic `array`, `mean`, `sum`, and other core operations.
- Sparse **arrays** differ from sparse **matrices** in operations such as elementwise multiplication; understand the semantics before migrating.

---

## 21. Quick-reference API maps

### Statistics

```text
stats.describe           Summary sample statistics
stats.sem                Standard error of mean
stats.zscore             Standardize observations
stats.iqr                Interquartile range
stats.trim_mean          Trimmed mean
stats.norm.cdf           Normal cumulative probability
stats.norm.ppf           Normal quantile
stats.binom.pmf          Binomial mass
stats.poisson.pmf        Poisson mass
stats.ttest_ind          Two-sample mean test
stats.ttest_rel          Paired mean test
stats.mannwhitneyu       Independent rank test
stats.pearsonr           Pearson correlation
stats.spearmanr          Spearman rank correlation
stats.chi2_contingency   Categorical association test
stats.fisher_exact       2x2 exact test
stats.bootstrap          Resampling confidence interval
stats.permutation_test   Permutation inference
stats.gaussian_kde       Kernel density estimation
```

### Optimization and linear algebra

```text
optimize.minimize                Multivariable minimization
optimize.minimize_scalar         Scalar minimization
optimize.least_squares           Residual least squares
optimize.curve_fit               Parametric curve fitting
optimize.root                    Nonlinear equation system
optimize.root_scalar             Scalar equation root
optimize.linprog                 Linear programming
optimize.milp                    Mixed-integer linear programming
optimize.differential_evolution  Global bounded optimization
linalg.solve                     Solve Ax=b
linalg.lstsq                     Least-squares system
linalg.eigh                      Symmetric eigenproblem
linalg.svd                       Singular value decomposition
linalg.cholesky                  Positive-definite factorization
sparse.csr_array                 Compressed sparse row array
sparse.linalg.spsolve            Sparse system solution
sparse.linalg.eigsh              Partial symmetric eigendecomposition
```

### Integration, interpolation, spatial, signal

```text
integrate.quad                   Callable 1D integral
integrate.trapezoid              Sampled integral
integrate.simpson                Simpson integration
integrate.cumulative_trapezoid   Running sample integral
integrate.solve_ivp              ODE initial-value solver
interpolate.CubicSpline          Cubic spline
interpolate.PchipInterpolator    Shape-preserving spline
interpolate.RegularGridInterpolator  N-D regular grids
spatial.distance.cdist           Cross-distance matrix
spatial.cKDTree                  Neighbor queries
signal.find_peaks                Local peak detection
signal.savgol_filter             Polynomial smoothing
signal.butter                    IIR filter design
signal.sosfiltfilt               Forward-backward filtering
fft.rfft                         Real-input FFT
ndimage.gaussian_filter          N-D Gaussian smoothing
special.expit                    Logistic sigmoid
special.logsumexp                Stable log-sum-exp
```

---

## 22. Exercises with solutions

### Exercise 1: Probability threshold

For a normal distribution with mean 50 and SD 10, find \(P(X>65)\).

```python
from scipy.stats import norm

probability = norm.sf(65, loc=50, scale=10)
print(probability)
```

### Exercise 2: Constrained portfolio weights

Choose two weights summing to one, both nonnegative, so that the weighted risk target is closest to 4.

```python
import numpy as np
from scipy.optimize import minimize

risk = np.array([2.0, 6.0])

result = minimize(
    lambda w: (risk @ w - 4.0) ** 2,
    x0=[0.2, 0.8],
    bounds=[(0, 1), (0, 1)],
    constraints={"type": "eq", "fun": lambda w: np.sum(w) - 1},
    method="SLSQP",
)

print(result.x)
```

Expected solution near `[0.5, 0.5]`.

### Exercise 3: Approximate a noisy exponential curve

```python
import numpy as np
from scipy.optimize import curve_fit

rng = np.random.default_rng(17)
x = np.linspace(0, 2, 30)
y = 4.0 * np.exp(-1.2 * x) + rng.normal(0, 0.05, x.size)


def f(x: np.ndarray, amplitude: float, decay: float) -> np.ndarray:
    return amplitude * np.exp(-decay * x)


parameters, covariance = curve_fit(f, x, y, p0=[1, 1])
print(parameters)
```

### Exercise 4: Identify the dominant frequency

```python
import numpy as np
from scipy.fft import rfft, rfftfreq

fs = 200.0
t = np.arange(0, 1, 1 / fs)
y = np.sin(2 * np.pi * 17 * t)

freq = rfftfreq(len(y), d=1 / fs)
mag = np.abs(rfft(y))

print(freq[np.argmax(mag[1:]) + 1])
```

Expected: `17.0`.

### Further practice

- Compare Welch t-test and Mann–Whitney U on simulated skewed samples.
- Fit a lognormal distribution to positive loss magnitudes and inspect tail quantiles.
- Compare `CubicSpline` versus `PchipInterpolator` on a monotone series.
- Compare `linalg.solve` versus explicit matrix inversion on an ill-conditioned matrix.
- Optimize a linear program with an additional capacity constraint.
- Integrate an ODE using `RK45` and `BDF`, comparing successful convergence and function evaluations.

---

## 23. Official resources

- [SciPy documentation](https://docs.scipy.org/doc/scipy/)
- [SciPy user guide](https://docs.scipy.org/doc/scipy/tutorial/)
- [SciPy API reference](https://docs.scipy.org/doc/scipy/reference/)
- [NumPy reference](https://numpy.org/doc/stable/reference/)

**Study sequence:** `stats` → `optimize` → `linalg` → `integrate` → `interpolate` → `sparse` → `spatial` → `signal`/`fft` → specialized modules.
