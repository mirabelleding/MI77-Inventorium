# Stochastic Processes

Mathematical foundations, stochastic calculus, numerical simulation, and Python implementations.

## Contents

1. [Probability foundations](#1-probability-foundations)
2. [What is a stochastic process?](#2-what-is-a-stochastic-process)
3. [Dependence, stationarity, and noise](#3-dependence-stationarity-and-noise)
4. [Discrete processes: random walks and Markov chains](#4-discrete-processes-random-walks-and-markov-chains)
5. [Poisson processes and random arrivals](#5-poisson-processes-and-random-arrivals)
6. [Brownian motion and its mathematical properties](#6-brownian-motion-and-its-mathematical-properties)
7. [Fractional Brownian motion and long memory](#7-fractional-brownian-motion-and-long-memory)
8. [Filtrations, martingales, and stopping times](#8-filtrations-martingales-and-stopping-times)
9. [Stochastic integration and Itô's lemma](#9-stochastic-integration-and-itos-lemma)
10. [Stochastic differential equations](#10-stochastic-differential-equations)
11. [Important diffusion models](#11-important-diffusion-models)
12. [Numerical simulation with Python](#12-numerical-simulation-with-python)
13. [Monte Carlo estimation and validation](#13-monte-carlo-estimation-and-validation)
14. [Applications and modelling decisions](#14-applications-and-modelling-decisions)
15. [Worked mathematical exercises](#15-worked-mathematical-exercises)
16. [Notation and terminology](#16-notation-and-terminology)

---

## 1. Probability foundations

### 1.1 Random variables and probability spaces

A probability space is a triple

$$
(\Omega,\mathcal F,\mathbb P),
$$

where:

- $\Omega$ is the set of possible outcomes (the **sample space**).
- $\mathcal F$ is a collection of measurable events.
- $\mathbb P$ assigns probabilities to events.

A random variable $X:\Omega\to\mathbb R$ maps an outcome to a number. Its cumulative distribution function (CDF) is

$$
F_X(x)=\mathbb P(X\le x).
$$

For a continuous random variable with density $f_X$:

$$
F_X(x)=\int_{-\infty}^{x}f_X(u)\,du,
\qquad
\mathbb P(a<X\le b)=\int_a^b f_X(x)\,dx.
$$

The density itself is **not** the probability of a particular exact value: for a continuous distribution, $\mathbb P(X=x)=0$.

### 1.2 Expected value, variance, and covariance

For a discrete $X$:

$$
\mathbb E[X]=\sum_x x\,\mathbb P(X=x).
$$

For a continuous $X$:

$$
\mathbb E[X]=\int_{-\infty}^{\infty}x f_X(x)\,dx.
$$

Variance measures spread around the mean:

$$
\operatorname{Var}(X)
=\mathbb E[(X-\mathbb E[X])^2]
=\mathbb E[X^2]-(\mathbb E[X])^2.
$$

Covariance and correlation measure linear association:

$$
\operatorname{Cov}(X,Y)
=\mathbb E[(X-\mathbb E[X])(Y-\mathbb E[Y])],
$$

$$
\rho_{X,Y}
=\frac{\operatorname{Cov}(X,Y)}{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}}.
$$

Useful identities:

$$
\mathbb E[aX+b]=a\mathbb E[X]+b,
$$

$$
\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X),
$$

$$
\operatorname{Var}(X+Y)
=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y).
$$

If $X$ and $Y$ are independent and have finite second moments, their covariance is zero. **The converse is generally false.** For *jointly Gaussian* variables, however, zero covariance implies independence.

### 1.3 The normal distribution

$$
X\sim\mathcal N(\mu,\sigma^2)
$$

means $X$ is normally distributed with mean $\mu$ and **variance** $\sigma^2$ (not standard deviation $\sigma^2$).

$$
f_X(x)=\frac{1}{\sigma\sqrt{2\pi}}
\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right].
$$

If $Z\sim\mathcal N(0,1)$, then $X=\mu+\sigma Z$ has distribution $\mathcal N(\mu,\sigma^2)$.

**Example — instrument error.** A sensor measures $25.0$ °C with independent errors $\varepsilon\sim\mathcal N(0,0.2^2)$. An observation can be represented as $Y=25.0+\varepsilon$.

```python
import numpy as np

rng = np.random.default_rng(42)
measurements = 25.0 + rng.normal(loc=0.0, scale=0.2, size=10_000)

print(type(measurements))       # <class 'numpy.ndarray'>
print(measurements.shape)      # (10000,)
print(measurements.mean())     # Approximately 25.0
print(measurements.var())      # Approximately 0.04
```

### 1.4 Conditional expectation

$\mathbb E[X\mid Y]$ is the expected value of $X$ given the information supplied by $Y$; it is usually **itself a random variable** (a function of $Y$).

The **law of total expectation** is

$$
\mathbb E[X]=\mathbb E\!\left[\mathbb E[X\mid Y]\right].
$$

The **law of total variance** is

$$
\operatorname{Var}(X)
=\mathbb E[\operatorname{Var}(X\mid Y)]
+\operatorname{Var}(\mathbb E[X\mid Y]).
$$

These formulas repeatedly appear in Markov processes, Bayesian filtering, and stochastic modelling.

---

## 2. What is a stochastic process?

A **stochastic process** is a family of random variables indexed by a parameter, often time:

$$
\boxed{\{X_t:t\in T\}.}
$$

For every fixed $t$, $X_t$ is a random variable. For every fixed outcome $\omega$, the mapping $t\mapsto X_t(\omega)$ is a **sample path** (or *trajectory*).

This gives two complementary views:

| View | Question | Example |
|---|---|---|
| Distribution at a fixed time | What are the possible values of $X_5$? | Temperature at 5 p.m. |
| Sample path | How does $X_t$ evolve as time changes? | One day's temperature curve |

### 2.1 Classification by index and state space

| Time/index | State space | Example |
|---|---|---|
| Discrete | Discrete | Weather states observed daily; Markov chain |
| Discrete | Continuous | Daily sensor readings; Gaussian random walk |
| Continuous | Discrete | Number of arrivals up to time $t$; Poisson process |
| Continuous | Continuous | Brownian motion; Ornstein–Uhlenbeck process |

**Discrete time does not mean discrete values.** The index $n\in\{0,1,2,\ldots\}$ can be discrete even when each $X_n$ is real-valued.

### 2.2 Finite-dimensional distributions

A process is characterized by joint distributions of the form

$$
\mathbb P(X_{t_1}\le x_1,\ldots,X_{t_k}\le x_k).
$$

Knowing only the individual distribution of each $X_t$ is insufficient to describe the process: dependence *between times* matters.

For example, two processes might have $X_t\sim\mathcal N(0,1)$ at every time, yet one consists of independent samples and the other is highly correlated.

---

## 3. Dependence, stationarity, and noise

### 3.1 Autocovariance and autocorrelation

Define the mean and covariance functions:

$$
m(t)=\mathbb E[X_t],
\qquad
C(s,t)=\operatorname{Cov}(X_s,X_t).
$$

For a discrete-time process, the autocorrelation at lag $k$ compares $X_n$ with $X_{n+k}$.

For a **weakly stationary** process (constant finite mean and covariance depending only on lag):

$$
\gamma(k)=\operatorname{Cov}(X_n,X_{n+k}),
\qquad
\rho(k)=\frac{\gamma(k)}{\gamma(0)}.
$$

**Strict stationarity** means every joint distribution remains unchanged under a common shift in time. Strict stationarity is stronger than weak stationarity in general. A strictly stationary process with finite second moments is weakly stationary.

### 3.2 Gaussian versus white noise

These adjectives answer **different questions**:

- **Gaussian:** What probability distribution describes the variables? (Normal.)
- **White:** What is the dependence/frequency structure? (Uncorrelated in time, with a flat spectral density under the stationary idealization.)

For discrete Gaussian white noise:

$$
\varepsilon_n\overset{\mathrm{iid}}{\sim}\mathcal N(0,\sigma^2),
\qquad
\operatorname{Cov}(\varepsilon_n,\varepsilon_m)=0\quad(n\ne m).
$$

But white noise need not be Gaussian. For example, independent random signs $\varepsilon_n\in\{-1,+1\}$ with equal probabilities form non-Gaussian white noise.

Also, a Gaussian process need not be white: its values can be correlated across time.

In continuous-time stochastic calculus, **ideal white noise** is formalized as a generalized random process (informally the derivative of Brownian motion), not an ordinary function with finite values at every instant.

### 3.3 Why noise has colors: frequency analysis

A frequency-domain description uses the **power spectral density** (PSD), $S(f)$. For stationary processes, the Wiener–Khinchin relationship links PSD and autocovariance through a Fourier transform.

A common colored-noise convention is

$$
\boxed{S(f)\propto f^{-\beta},\qquad f>0.}
$$

| Color | $\beta$ | Approximate PSD | Relative emphasis |
|---|---:|---|---|
| Violet (purple) | $-2$ | $f^2$ | Strongly high frequency |
| Blue | $-1$ | $f$ | High frequency |
| White | $0$ | Constant | Equal power per unit frequency |
| Pink | $1$ | $1/f$ | Low frequency |
| Red / brown | $2$ | $1/f^2$ | Strongly low frequency |

**Important qualifications:** These are power-law conventions over a specified frequency range. Unbounded ideal $1/f$ or $1/f^2$ spectra are problematic near $f=0$ for finite-variance stationary processes; real simulations have finite resolution, filtering, and/or cutoffs. **Brownian motion is nonstationary**, so its common $1/f^2$ description should not be mistaken for the ordinary stationary PSD of $W_t$.

### 3.4 Generating colored noise with the FFT

The discrete Fourier transform decomposes a finite sequence into frequency components. To target $S(f)\propto f^{-\beta}$, scale the **amplitude** by $f^{-\beta/2}$ because power is proportional to squared amplitude.

```python
import numpy as np

def colored_noise(beta: float, n: int, seed: int = 42) -> np.ndarray:
    """Periodic finite-length colored-noise approximation; unit sample SD."""
    if n < 2:
        raise ValueError("n must be >= 2")

    rng = np.random.default_rng(seed)
    white = rng.standard_normal(n)
    frequencies = np.fft.rfftfreq(n, d=1.0)
    spectrum = np.fft.rfft(white)

    weights = np.zeros_like(frequencies)
    positive = frequencies > 0
    weights[positive] = frequencies[positive] ** (-beta / 2)
    spectrum *= weights       # DC frequency deliberately set to zero

    samples = np.fft.irfft(spectrum, n=n)
    return samples / samples.std()

white  = colored_noise(beta=0,  n=4096)
pink   = colored_noise(beta=1,  n=4096)
red    = colored_noise(beta=2,  n=4096)
blue   = colored_noise(beta=-1, n=4096)
violet = colored_noise(beta=-2, n=4096)

print(pink.shape)  # (4096,)
print(type(pink))  # <class 'numpy.ndarray'>
```

This produces a **finite, periodic approximation** with a low-frequency cutoff, not an exact continuous-time noise model. Zeroing the DC component also forces a zero sample mean.

### 3.5 Autocorrelation in Python

```python
def lag_correlation(values: np.ndarray, lag: int) -> float:
    if not 0 < lag < len(values):
        raise ValueError("lag must be between 1 and len(values) - 1")
    return float(np.corrcoef(values[:-lag], values[lag:])[0, 1])

print(lag_correlation(white, 1))  # Typically near 0
print(lag_correlation(red, 1))    # Typically strongly positive
```

Do not infer a stochastic model from the visual appearance of one path alone. Compare sample autocorrelations, histograms, estimated spectra, and theoretical properties across repeated simulations.

---

## 4. Discrete processes: random walks and Markov chains

### 4.1 Random walk

Let $\varepsilon_1,\varepsilon_2,\ldots$ be independent increments with mean zero and variance $\sigma^2$. Define

$$
X_n=X_0+\sum_{k=1}^{n}\varepsilon_k.
$$

Then

$$
\mathbb E[X_n]=X_0,
\qquad
\operatorname{Var}(X_n)=n\sigma^2.
$$

**Derivation:** Linearity of expectation gives $\mathbb E[\sum\varepsilon_k]=\sum\mathbb E[\varepsilon_k]=0$. Independence makes all cross-covariances zero, so $\operatorname{Var}(\sum\varepsilon_k)=\sum\operatorname{Var}(\varepsilon_k)=n\sigma^2$.

For a simple symmetric random walk, each increment is $+1$ or $-1$ with probability $1/2$.

```python
rng = np.random.default_rng(7)
steps = rng.choice([-1, 1], size=20)
position = np.r_[0, np.cumsum(steps)]

print(position.shape)  # (21,)
```

The increments are independent; the *positions* are dependent because they contain previous increments.

### 4.2 Markov property

A process is **Markov** when, given the present state, earlier states provide no additional information about the distribution of its future:

$$
\mathbb P(X_{n+1}=j\mid X_n=i,X_{n-1},\ldots)
=\mathbb P(X_{n+1}=j\mid X_n=i).
$$

For a time-homogeneous finite-state Markov chain, transition probabilities form a matrix $P$:

$$
P_{ij}=\mathbb P(X_{n+1}=j\mid X_n=i),
\qquad \sum_jP_{ij}=1.
$$

**Example — machine operating states:**

$$
P=\begin{pmatrix}
0.95&0.05\\
0.30&0.70
\end{pmatrix}
$$

State 0 is *working*; state 1 is *failed*. A working machine has a 5% chance of failing next period; a failed machine has a 30% chance of returning to service.

Starting in state 0, the row-vector probability distribution after $n$ steps is $\boldsymbol\pi_n=\boldsymbol\pi_0P^n$.

```python
P = np.array([[0.95, 0.05], [0.30, 0.70]])
pi0 = np.array([1.0, 0.0])

pi1 = pi0 @ P
pi2 = pi0 @ np.linalg.matrix_power(P, 2)

print(pi1)  # [0.95 0.05]
print(pi2)  # [0.9175 0.0825]
```

A stationary distribution $\boldsymbol\pi$ satisfies $\boldsymbol\pi P=\boldsymbol\pi$ and $\sum_i\pi_i=1$. Whether it exists uniquely and attracts other distributions depends on properties of the chain.

---

## 5. Poisson processes and random arrivals

A homogeneous **Poisson process** $N_t$ counts events arriving at constant rate $\lambda>0$, with:

1. $N_0=0$.
2. Independent increments.
3. $N_t-N_s\sim\operatorname{Poisson}(\lambda(t-s))$ for $t>s$.

Consequently,

$$
\mathbb P(N_t=k)=e^{-\lambda t}\frac{(\lambda t)^k}{k!},
\qquad
\mathbb E[N_t]=\operatorname{Var}(N_t)=\lambda t.
$$

### 5.1 Waiting times

The time $T_1$ to the first event has an exponential distribution:

$$
\mathbb P(T_1>t)=\mathbb P(N_t=0)=e^{-\lambda t},
$$

so

$$
T_1\sim\operatorname{Exponential}(\lambda),
\qquad \mathbb E[T_1]=\frac1\lambda.
$$

The exponential distribution has the **memoryless** property:

$$
\mathbb P(T>s+t\mid T>s)=\mathbb P(T>t).
$$

**Example — telescope detections.** If a detector records events at a mean rate of 3 per minute, the probability of observing no events during the next 2 minutes is $e^{-6}$.

```python
rng = np.random.default_rng(42)

counts = rng.poisson(lam=3 * 2, size=10_000)
waiting_times = rng.exponential(scale=1 / 3, size=10_000)

print(counts.shape)         # (10000,)
print(waiting_times.shape)  # (10000,)
```

NumPy's `exponential` uses **scale** $=1/\lambda$, not rate $\lambda$.

### 5.2 Compound Poisson processes

If each arrival produces a random amount $Y_i$, a **compound Poisson process** is

$$
J_t=\sum_{i=1}^{N_t}Y_i.
$$

If the $Y_i$ are identically distributed and independent of the Poisson count, with finite second moments:

$$
\mathbb E[J_t]=\lambda t\,\mathbb E[Y],
\qquad
\operatorname{Var}(J_t)=\lambda t\,\mathbb E[Y^2].
$$

This models discrete jumps such as insurance claims, packet arrivals, or bursts of radiation. The variance involves $\mathbb E[Y^2]$, **not merely** $\operatorname{Var}(Y)$.

---

## 6. Brownian motion and its mathematical properties

A **standard Brownian motion** (Wiener process) $W_t$ satisfies:

1. $W_0=0$.
2. It has independent increments.
3. $W_t-W_s\sim\mathcal N(0,t-s)$ for $0\le s<t$.
4. Its sample paths are continuous almost surely.

### 6.1 Distribution, mean, and variance

By setting $s=0$:

$$
W_t\sim\mathcal N(0,t),
\quad
\mathbb E[W_t]=0,
\quad
\operatorname{Var}(W_t)=t.
$$

The standard deviation is $\sqrt t$, not $t$.

### 6.2 Brownian covariance: derivation

Take $0\le s\le t$ and split the future value into a present value plus a future increment:

$$
W_t=W_s+(W_t-W_s).
$$

Because $W_t-W_s$ is independent of $W_s$ and both have mean zero,

$$
\begin{aligned}
\operatorname{Cov}(W_s,W_t)
&=\mathbb E[W_sW_t]\\
&=\mathbb E[W_s^2]
 +\mathbb E[W_s(W_t-W_s)]\\
&=s+0=s.
\end{aligned}
$$

By symmetry,

$$
\boxed{\operatorname{Cov}(W_s,W_t)=\min(s,t).}
$$

**Consequences:** Brownian *levels* are correlated and nonstationary, while Brownian increments over disjoint time intervals are independent.

### 6.3 Why Brownian paths are not differentiable

Consider a difference quotient:

$$
\frac{W_{t+h}-W_t}{h}
\sim\mathcal N\!\left(0,\frac{1}{h}\right),\qquad h>0.
$$

Its variance diverges as $h\downarrow0$. This is an intuition for why an ordinary derivative fails. In fact, Brownian sample paths are **almost surely nowhere differentiable**. Continuity does not imply differentiability.

### 6.4 Quadratic variation: a central derivation

Partition $[0,T]$ into $n$ equal intervals, $\Delta t=T/n$, and define

$$
Q_n=\sum_{i=1}^n (W_{t_i}-W_{t_{i-1}})^2.
$$

Since $\Delta W_i\sim\mathcal N(0,\Delta t)$,

$$
\mathbb E[(\Delta W_i)^2]=\Delta t
\quad\Longrightarrow\quad
\mathbb E[Q_n]=n\Delta t=T.
$$

For a zero-mean Gaussian $Z$ with variance $v$, $\mathbb E[Z^4]=3v^2$; therefore $\operatorname{Var}(Z^2)=2v^2$. Independence gives

$$
\operatorname{Var}(Q_n)
=n\cdot2(\Delta t)^2
=\frac{2T^2}{n}\longrightarrow0.
$$

Thus $Q_n\to T$ in mean square (and hence in probability) along these partitions. The quadratic variation is written

$$
\boxed{[W]_T=T.}
$$

This is the source of the formal Itô-calculus mnemonic

$$
(dW_t)^2=dt,
\qquad dt\,dW_t=0,
\qquad(dt)^2=0.
$$

These are **rules of stochastic differential bookkeeping**, not ordinary algebraic identities between infinitesimals.

### 6.5 Brownian scaling

For $c>0$,

$$
\widetilde W_t=\frac{1}{\sqrt c}W_{ct}
$$

is again standard Brownian motion in distribution. This explains why Brownian fluctuations scale with $\sqrt{\Delta t}$.

### 6.6 Simulating Brownian paths

```python
import numpy as np

def brownian_paths(
    t_end: float = 1.0,
    steps: int = 252,
    paths: int = 1_000,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    if t_end <= 0 or steps <= 0 or paths <= 0:
        raise ValueError("t_end, steps, and paths must be positive")

    rng = np.random.default_rng(seed)
    dt = t_end / steps
    dW = rng.normal(0.0, np.sqrt(dt), size=(paths, steps))
    W = np.concatenate(
        [np.zeros((paths, 1)), np.cumsum(dW, axis=1)],
        axis=1,
    )
    time = np.linspace(0.0, t_end, steps + 1)
    return time, W

time, W = brownian_paths()
print(time.shape)  # (253,)
print(W.shape)     # (1000, 253)
print(W[:, 0].mean())  # 0.0
```

Here `W[:, -1]` gives 1,000 simulated terminal values; `W[0, :]` gives one entire path. The simulated grid-point distributions are exact for Brownian motion, although connecting points with straight lines does **not** reconstruct the true continuous path between grid points.

---

## 7. Fractional Brownian motion and long memory

Fractional Brownian motion $B_t^H$ is a centered Gaussian process with **Hurst parameter** $0<H<1$ and covariance

$$
\boxed{
\mathbb E[B_s^HB_t^H]
=\frac12\left(s^{2H}+t^{2H}-|t-s|^{2H}\right).
}
$$

It is self-similar: $B_{ct}^H$ and $c^HB_t^H$ have the same finite-dimensional distributions.

For $H=1/2$, fractional Brownian motion is standard Brownian motion. For $H\ne1/2$, its nonoverlapping increments are generally correlated.

### 7.1 Fractional Gaussian noise

The discrete increments

$$
G_n^H=B_{n+1}^H-B_n^H
$$

form **fractional Gaussian noise** (fGn), a stationary Gaussian process with lag-$k$ covariance

$$
\boxed{
\gamma_H(k)
=\frac12\left(|k+1|^{2H}-2|k|^{2H}+|k-1|^{2H}\right).
}
$$

| Hurst exponent | Increment dependence | Interpretation |
|---|---|---|
| $H<1/2$ | Negative lag correlations | Anti-persistent increments |
| $H=1/2$ | Independent increments | Ordinary Brownian motion |
| $H>1/2$ | Positive lag correlations | Persistent increments; long-range dependence |

For large $k$, $\gamma_H(k)\sim H(2H-1)k^{2H-2}$. When $H>1/2$, these positive correlations decay so slowly that their sum diverges: a mathematical definition of long-range dependence.

**Caution:** These are statistical tendencies, not deterministic claims that an upward step must be followed by another upward step. An estimated Hurst exponent alone does not prove a particular physical mechanism or predictive financial advantage.

---

## 8. Filtrations, martingales, and stopping times

### 8.1 Filtrations: growing information

A **filtration** is an increasing family of information sets:

$$
\mathcal F_s\subseteq\mathcal F_t,\qquad s\le t.
$$

Informally, $\mathcal F_t$ represents everything observable up to time $t$. A process is **adapted** if $X_t$ is known from $\mathcal F_t$: its current value cannot require future information.

### 8.2 Martingales

An integrable adapted process $M_t$ is a martingale when

$$
\boxed{\mathbb E[M_t\mid\mathcal F_s]=M_s,\qquad s\le t.}
$$

This is a conditional-expectation statement, not a claim that every path is constant or that the process has no fluctuations.

**Example 1 — Brownian motion is a martingale.** Since the future increment is independent of past information and has mean zero,

$$
\mathbb E[W_t\mid\mathcal F_s]
=\mathbb E[W_s+(W_t-W_s)\mid\mathcal F_s]
=W_s.
$$

**Example 2 — $W_t^2-t$ is a martingale.** Using the same decomposition,

$$
\begin{aligned}
\mathbb E[W_t^2\mid\mathcal F_s]
&=W_s^2+\mathbb E[(W_t-W_s)^2]\\
&=W_s^2+(t-s).
\end{aligned}
$$

Therefore $\mathbb E[W_t^2-t\mid\mathcal F_s]=W_s^2-s$.

### 8.3 Stopping times

A random time $\tau$ is a **stopping time** if, by time $t$, it is possible to determine whether $\tau\le t$ using information available up to $t$.

Example: the first time a temperature sensor exceeds a threshold,

$$
\tau=\inf\{t\ge0:X_t\ge a\}.
$$

Martingale stopping theorems have important integrability and boundedness conditions. It is **not** universally valid to substitute an arbitrary unbounded stopping time into martingale identities.

---

## 9. Stochastic integration and Itô's lemma

### 9.1 Why ordinary integration is insufficient

An expression such as

$$
\int_0^T H_t\,dW_t
$$

is an **Itô stochastic integral** when $H_t$ is suitably adapted and integrable. Unlike an ordinary Riemann integral, the integrator $W_t$ has unbounded variation along almost every path.

For an appropriate square-integrable $H$:

$$
\mathbb E\!\left[\int_0^T H_t\,dW_t\right]=0,
$$

and the **Itô isometry** gives

$$
\boxed{
\mathbb E\!\left[\left(\int_0^T H_t\,dW_t\right)^2\right]
=\mathbb E\!\left[\int_0^T H_t^2\,dt\right].
}
$$

The isometry connects a stochastic integral's variance with an ordinary time integral.

### 9.2 Itô's lemma: derivation intuition

Suppose

$$
dX_t=\mu(t,X_t)\,dt+\sigma(t,X_t)\,dW_t
$$

and $f(t,x)$ has sufficient derivatives. A second-order Taylor expansion gives

$$
df\approx f_t\,dt+f_x\,dX+\tfrac12f_{xx}(dX)^2.
$$

Using $(dW)^2=dt$ and discarding higher-order terms:

$$
(dX)^2=(\mu\,dt+\sigma\,dW)^2\rightsquigarrow\sigma^2\,dt.
$$

Thus **Itô's lemma** is

$$
\boxed{
df(t,X_t)
=\left(f_t+\mu f_x+\frac12\sigma^2f_{xx}\right)dt
+\sigma f_x\,dW_t.
}
$$

All derivatives are evaluated at $(t,X_t)$. The extra $\tfrac12\sigma^2 f_{xx}$ term is absent from the ordinary chain rule; it arises from Brownian quadratic variation.

### 9.3 Worked example: $f(W_t)=W_t^2$

Let $f(x)=x^2$. Then $f_x=2x$, $f_{xx}=2$, and with $dW_t=0\,dt+1\,dW_t$:

$$
d(W_t^2)=2W_t\,dW_t+dt.
$$

Integrating:

$$
\boxed{W_T^2=2\int_0^T W_t\,dW_t+T.}
$$

Compare ordinary calculus, where the $+T$ correction would not appear.

### 9.4 Worked example: derive geometric Brownian motion

Suppose an asset or growing population follows

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t,
\qquad S_0>0.
$$

Apply Itô's lemma to $f(S)=\log S$:

$$
f'(S)=\frac1S,
\qquad f''(S)=-\frac1{S^2}.
$$

Therefore

$$
\begin{aligned}
d\log S_t
&=\frac1{S_t}dS_t
+\frac12\left(-\frac1{S_t^2}\right)\sigma^2S_t^2dt\\
&=\left(\mu-\frac{\sigma^2}{2}\right)dt+\sigma\,dW_t.
\end{aligned}
$$

Integrate from 0 to $t$:

$$
\log S_t-\log S_0
=\left(\mu-\frac{\sigma^2}{2}\right)t+\sigma W_t.
$$

Exponentiating yields the **exact solution**:

$$
\boxed{
S_t=S_0\exp\!\left[
\left(\mu-\frac{\sigma^2}{2}\right)t+\sigma W_t
\right].
}
$$

The $-\sigma^2/2$ adjustment is the Itô correction. Under this constant-parameter model, $\mathbb E[S_t]=S_0e^{\mu t}$, not $S_0e^{(\mu-\sigma^2/2)t}$.

### 9.5 Itô versus Stratonovich

There are multiple stochastic integration conventions. In one dimension, under standard smoothness conditions, the **Stratonovich** equation

$$
dX_t=a(t,X_t)\,dt+b(t,X_t)\circ dW_t
$$

corresponds to the **Itô** equation

$$
dX_t=\left[a(t,X_t)+\tfrac12b(t,X_t)\frac{\partial b}{\partial x}(t,X_t)\right]dt+b(t,X_t)\,dW_t.
$$

Stratonovich integrals obey a classical-looking chain rule, while Itô integrals obey Itô's lemma. Their drift coefficients must be adjusted when translating between conventions. Multidimensional conversion requires the corresponding vector/Jacobian correction.

---

## 10. Stochastic differential equations

A one-dimensional Itô stochastic differential equation (SDE) takes the form

$$
\boxed{dX_t=\mu(t,X_t)\,dt+\sigma(t,X_t)\,dW_t.}
$$

- $\mu$: **drift**, the local deterministic trend.
- $\sigma$: **diffusion coefficient**, the local size of random fluctuations.
- $W_t$: driving Brownian motion.
- $X_0$: initial condition.

The differential notation abbreviates an integral equation:

$$
X_t=X_0+\int_0^t\mu(s,X_s)\,ds+\int_0^t\sigma(s,X_s)\,dW_s.
$$

This distinction matters: $dW_t/dt$ is not an ordinary time derivative.

### 10.1 Drift and diffusion from small increments

For small $h>0$, approximately:

$$
\mathbb E[X_{t+h}-X_t\mid X_t=x]\approx\mu(t,x)h,
$$

$$
\operatorname{Var}(X_{t+h}-X_t\mid X_t=x)\approx\sigma^2(t,x)h.
$$

Notice that **variance**, not standard deviation, scales linearly with $h$; standard deviation scales as $\sqrt h$.

### 10.2 Existence and uniqueness

One standard sufficient set of conditions for a well-behaved strong solution is that drift and diffusion satisfy suitable global Lipschitz and linear-growth bounds in the state variable. Not all important models satisfy these simple sufficient conditions everywhere: some require specialized arguments, boundary conditions, or numerical methods.

### 10.3 Multidimensional SDEs

For a vector state $\mathbf X_t\in\mathbb R^d$ and $m$ Brownian drivers:

$$
d\mathbf X_t=\boldsymbol\mu(t,\mathbf X_t)dt+B(t,\mathbf X_t)d\mathbf W_t,
$$

where $B$ is a $d\times m$ matrix. The instantaneous covariance of the random increment is approximately

$$
\operatorname{Cov}(\Delta\mathbf X_t\mid\mathbf X_t)
\approx BB^\mathsf T\Delta t.
$$

This is useful for coupled physical systems and correlated risk factors.

---

## 11. Important diffusion models

### 11.1 Arithmetic Brownian motion

$$
dX_t=\mu\,dt+\sigma\,dW_t.
$$

Exact solution:

$$
X_t=X_0+\mu t+\sigma W_t.
$$

Therefore $X_t\sim\mathcal N(X_0+\mu t,\sigma^2t)$. Unlike geometric Brownian motion, this process may be negative.

### 11.2 Geometric Brownian motion (GBM)

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t.
$$

For deterministic $S_0>0$, the exact solution above gives

$$
\mathbb E[S_t]=S_0e^{\mu t},
$$

$$
\operatorname{Var}(S_t)
=S_0^2e^{2\mu t}(e^{\sigma^2t}-1).
$$

$S_t$ is lognormally distributed and remains strictly positive for every finite $t$ almost surely. A basic GBM model does **not** reproduce volatility clustering, jumps, or every feature of observed asset prices.

### 11.3 Ornstein–Uhlenbeck (OU) process

$$
\boxed{dX_t=\theta(m-X_t)dt+\sigma\,dW_t,\qquad\theta>0.}
$$

Here $m$ is the long-run level and $\theta$ controls mean reversion.

**Deriving the solution.** Rewrite the SDE as

$$
dX_t+\theta X_tdt=\theta m\,dt+\sigma\,dW_t.
$$

Multiply by the integrating factor $e^{\theta t}$ and apply the product rule (the factor is deterministic, so there is no additional quadratic-covariation term):

$$
d(e^{\theta t}X_t)=\theta me^{\theta t}dt+\sigma e^{\theta t}dW_t.
$$

Integrating and rearranging:

$$
\boxed{
X_t=m+(X_0-m)e^{-\theta t}
+\sigma\int_0^t e^{-\theta(t-s)}\,dW_s.
}
$$

Take expectations. The Itô integral has mean zero:

$$
\boxed{\mathbb E[X_t]=m+(X_0-m)e^{-\theta t}.}
$$

Use the Itô isometry for the variance (with deterministic $X_0$):

$$
\begin{aligned}
\operatorname{Var}(X_t)
&=\sigma^2\int_0^t e^{-2\theta(t-s)}ds\\
&=\boxed{\frac{\sigma^2}{2\theta}(1-e^{-2\theta t})}.
\end{aligned}
$$

As $t\to\infty$, its mean approaches $m$ and variance approaches $\sigma^2/(2\theta)$. Starting from the appropriate stationary Gaussian distribution yields a stationary OU process.

**Applications:** physical velocity under friction, noisy temperature regulation, mean-reverting biological measurements, and interest-rate models.

### 11.4 Cox–Ingersoll–Ross (CIR) process

$$
dX_t=\kappa(\theta-X_t)dt+\sigma\sqrt{X_t}\,dW_t.
$$

Its stochastic volatility shrinks as $X_t$ approaches zero. With nonnegative initial state and standard parameter restrictions, the continuous-time CIR solution stays nonnegative. In the standard strictly positive parameter setting, the **Feller condition** $2\kappa\theta\ge\sigma^2$ ensures the zero boundary is unattainable when started above zero.

**Numerical caution:** A naive Euler–Maruyama step can become negative even when the exact process cannot; specialized exact-transition or positivity-preserving schemes are often preferable.

### 11.5 Comparing the models

| Model | Drift | Diffusion | Typical behavior |
|---|---|---|---|
| Arithmetic Brownian | $\mu$ | $\sigma$ | Additive fluctuations |
| GBM | $\mu X$ | $\sigma X$ | Multiplicative growth; positivity |
| OU | $\theta(m-X)$ | $\sigma$ | Mean reversion; real-valued |
| CIR | $\kappa(\theta-X)$ | $\sigma\sqrt X$ | Mean reversion; nonnegative exact solution |

---

## 12. Numerical simulation with Python

### 12.1 Euler–Maruyama method

For time grid $t_n=n\Delta t$, draw Brownian increments

$$
\Delta W_n=\sqrt{\Delta t}\,Z_n,
\qquad Z_n\overset{\mathrm{iid}}{\sim}\mathcal N(0,1).
$$

The Euler–Maruyama discretization is

$$
\boxed{
X_{n+1}=X_n+\mu(t_n,X_n)\Delta t
+\sigma(t_n,X_n)\sqrt{\Delta t}\,Z_n.
}
$$

**Why $\sqrt{\Delta t}$?** Because $\operatorname{Var}(\Delta W)=\Delta t$; scaling a standard normal by $\sqrt{\Delta t}$ produces that variance.

```python
from collections.abc import Callable
import numpy as np

def euler_maruyama(
    drift: Callable[[float, np.ndarray], np.ndarray],
    diffusion: Callable[[float, np.ndarray], np.ndarray],
    x0: float,
    t_end: float,
    steps: int,
    paths: int,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate scalar Itô SDEs with vectorized independent paths."""
    if t_end <= 0 or steps <= 0 or paths <= 0:
        raise ValueError("t_end, steps, and paths must be positive")

    rng = np.random.default_rng(seed)
    dt = t_end / steps
    time = np.linspace(0, t_end, steps + 1)
    result = np.empty((paths, steps + 1), dtype=float)
    result[:, 0] = x0

    for n in range(steps):
        x = result[:, n]
        dW = np.sqrt(dt) * rng.standard_normal(paths)
        result[:, n + 1] = (
            x + drift(time[n], x) * dt
              + diffusion(time[n], x) * dW
        )

    return time, result

# Noisy return of an object to its natural equilibrium level.
theta, equilibrium, sigma = 1.5, 20.0, 0.8
time, X = euler_maruyama(
    drift=lambda t, x: theta * (equilibrium - x),
    diffusion=lambda t, x: sigma * np.ones_like(x),
    x0=15.0,
    t_end=2.0,
    steps=500,
    paths=10_000,
)

print(time.shape)  # (501,)
print(X.shape)     # (10000, 501)
print(X[:, -1].mean())  # Near 20 + (15 - 20) * exp(-1.5 * 2)
```

This simple implementation assumes scalar states, compatible vectorized coefficient functions, and independent Brownian drivers across paths. It deliberately does not handle jump SDEs, correlated multidimensional drivers, boundary constraints, or adaptive time stepping.

### 12.2 Simulating an exact OU transition

For $\theta>0$ and a fixed step $\Delta t$, the OU transition conditional on $X_n=x$ is Gaussian:

$$
X_{n+1}=m+(x-m)e^{-\theta\Delta t}
+\sigma\sqrt{\frac{1-e^{-2\theta\Delta t}}{2\theta}}\,Z_n.
$$

```python
def ou_exact_paths(
    x0: float, mean: float, theta: float, sigma: float,
    t_end: float, steps: int, paths: int, seed: int = 42,
) -> np.ndarray:
    if theta <= 0 or t_end <= 0 or steps <= 0 or paths <= 0 or sigma < 0:
        raise ValueError("Invalid OU simulation parameters")

    rng = np.random.default_rng(seed)
    dt = t_end / steps
    decay = np.exp(-theta * dt)
    innovation_sd = sigma * np.sqrt((1 - decay**2) / (2 * theta))

    result = np.empty((paths, steps + 1))
    result[:, 0] = x0
    for n in range(steps):
        result[:, n + 1] = (
            mean + (result[:, n] - mean) * decay
            + innovation_sd * rng.standard_normal(paths)
        )
    return result
```

The **exact transition method** gives the correct distribution at grid points; Euler–Maruyama only approximates it. Exact simulation is possible for some processes (e.g. Brownian motion, constant-coefficient GBM, OU), but not every SDE.

### 12.3 Milstein method

For a one-dimensional Itô SDE with sufficiently smooth state-dependent diffusion $b(x)$, the Milstein method adds a correction:

$$
X_{n+1}=X_n+a(X_n)\Delta t+b(X_n)\Delta W_n
+\frac12b(X_n)b'(X_n)\left[(\Delta W_n)^2-\Delta t\right].
$$

For GBM, $b(x)=\sigma x$ and $b'(x)=\sigma$, so the correction is

$$
\frac12\sigma^2 X_n\left[(\Delta W_n)^2-\Delta t\right].
$$

### 12.4 Strong versus weak convergence

Two distinct notions of numerical accuracy:

| Convergence | Focus | Representative error |
|---|---|---|
| Strong | Individual simulated paths, using coupled Brownian motion | $\mathbb{E}[\lvert X_T-\widehat{X}_T\rvert]$ |
| Weak | Expected statistics of the distribution | $\lvert\mathbb{E}[g(X_T)]-\mathbb{E}[g(\widehat{X}_T)]\rvert$ |

Under standard regularity assumptions, Euler–Maruyama has **strong order $1/2$** and **weak order 1**; scalar Milstein typically has **strong order 1** with suitable smoothness. These are asymptotic results, not universal guarantees for arbitrary coefficients or discontinuous payoffs.

### 12.5 Random-number-generator design

`np.random.default_rng(seed)` creates an independent, explicit `numpy.random.Generator`. Prefer passing a generator or seed explicitly to a simulation function instead of silently relying on global random state.

For fair solver comparisons, drive both methods with **the same Brownian increments** (coupled paths). Separately seeded simulations do not isolate numerical discretization error.

---

## 13. Monte Carlo estimation and validation

### 13.1 Estimating an expectation

Suppose $Y_1,\ldots,Y_N$ are independent, identically distributed observations. Monte Carlo estimates $\mathbb E[Y]$ with

$$
\widehat\mu_N=\frac1N\sum_{i=1}^N Y_i.
$$

The **standard error** is estimated by

$$
\widehat{\mathrm{SE}}(\widehat\mu_N)=\frac{s_Y}{\sqrt N},
$$

where $s_Y$ is the sample standard deviation. Under suitable central-limit assumptions, an approximate 95% confidence interval is

$$
\widehat\mu_N\pm1.96\frac{s_Y}{\sqrt N}.
$$

This interval describes Monte Carlo **sampling uncertainty**, not the time-discretization bias of a numerical SDE solver.

```python
terminal = X[:, -1]  # Terminal states from the OU Euler simulation
estimate = float(terminal.mean())
se = float(terminal.std(ddof=1) / np.sqrt(len(terminal)))
ci_95 = (estimate - 1.96 * se, estimate + 1.96 * se)

print(type(ci_95))  # <class 'tuple'>
print(len(ci_95))   # 2
```

### 13.2 Validating an OU simulation

For deterministic initial state $x_0$:

$$
m_T=m+(x_0-m)e^{-\theta T},
\qquad
v_T=\frac{\sigma^2}{2\theta}(1-e^{-2\theta T}).
$$

Compare the simulation against both formulas:

```python
T = 2.0
target_mean = equilibrium + (15.0 - equilibrium) * np.exp(-theta * T)
target_var = sigma**2 / (2 * theta) * (1 - np.exp(-2 * theta * T))

print("theory mean:", target_mean)
print("sample mean:", X[:, -1].mean())
print("theory variance:", target_var)
print("sample variance:", X[:, -1].var())
```

Interpret differences carefully:

1. **Monte Carlo error:** finite number of paths, usually of order $N^{-1/2}$ for means.
2. **Discretization error:** finite time step, governed by the numerical scheme.
3. **Model error:** mismatch between the SDE assumptions and real data.
4. **Implementation error:** incorrect scaling, indexing, parameterization, or random generation.

### 13.3 Diagnostics for stochastic models

| Diagnostic | What it checks | Typical concern |
|---|---|---|
| Mean and variance over time | Moment formulas | Wrong drift or diffusion |
| Autocorrelation of increments | Temporal dependence | Independence assumption fails |
| Histogram / Q–Q plot | Marginal distribution | Heavy tails or skew |
| Distribution of holding times | Arrival process | Non-Poisson events |
| Sample-path boundary checks | State constraints | Negative simulated CIR values |
| Error versus time-step size | Numerical convergence | Discretization bias |
| Error versus path count | Monte Carlo convergence | Insufficient sampling |

**Variance reduction:** Antithetic variates, control variates, importance sampling, and stratification can improve Monte Carlo efficiency when used appropriately. Faster computation is not achieved merely by reducing sample count without accounting for increased uncertainty.

---

## 14. Applications and modelling decisions

| Application | Possible process | Why it fits | Main caveat |
|---|---|---|---|
| Molecule diffusing in a fluid | Brownian motion | Random cumulative displacement | Interactions and boundaries may matter |
| Temperature around a thermostat setting | OU | Fluctuation around an equilibrium | Assumes approximately linear restoring force |
| Calls arriving at a help desk | Poisson process | Random event counts | Real rates may change by hour |
| Equipment working/failed states | Markov chain | Discrete transitions | History dependence may violate Markov property |
| Insurance claim amounts over time | Compound Poisson | Random arrivals with random sizes | Claim sizes or arrivals may depend on each other |
| Simplified continuously compounding growth | GBM | Multiplicative changes | Constant volatility and continuous paths are restrictive |
| Long-memory signals | Fractional Gaussian noise | Correlated stationary increments | Estimating $H$ can be fragile |
| Synthetic audio or image textures | Colored noise | Controls relative frequencies | A spectral slope does not define every perceptual feature |

### 14.1 Questions that determine the model

- Does time evolve in discrete steps or continuously?
- Are observations counts, categories, or real-valued measurements?
- Are increments independent? Are values mean-reverting?
- Must the process stay positive, bounded, or integer-valued?
- Are jumps possible? Is variance approximately constant?
- Are parameters fixed, time-varying, or state-dependent?
- Is the goal to reproduce the distribution, individual paths, forecasts, or analytical properties?

Avoid conflating a **model's mathematical tractability** with **evidence that it represents the observed system well**.

---

## 15. Worked mathematical exercises

### Exercise 1 — Sum of independent normal variables

Let $X\sim\mathcal N(2,4)$ and $Y\sim\mathcal N(3,9)$ be independent. Find the distribution of $X+Y$.

**Solution:** Independent normal variables have a normal sum, with means and variances adding:

$$
X+Y\sim\mathcal N(2+3,4+9)=\boxed{\mathcal N(5,13)}.
$$

The standard deviation is $\sqrt{13}$, **not** $2+3$.

### Exercise 2 — Covariance of Brownian values

Find $\operatorname{Cov}(W_2,W_5)$ and $\operatorname{Corr}(W_2,W_5)$.

**Solution:** $\operatorname{Cov}(W_2,W_5)=\min(2,5)=2$. The variances are 2 and 5, so

$$
\operatorname{Corr}(W_2,W_5)=\frac{2}{\sqrt{2}\sqrt5}=\boxed{\sqrt{\frac25}}.
$$

### Exercise 3 — Why drift is not the same as expected log growth

For GBM $dS_t=\mu S_tdt+\sigma S_tdW_t$, derive $\mathbb E[\log(S_t/S_0)]$.

**Solution:** Apply Itô's lemma to $\log S_t$:

$$
\log\frac{S_t}{S_0}
=\left(\mu-\tfrac12\sigma^2\right)t+\sigma W_t.
$$

Since $\mathbb E[W_t]=0$:

$$
\boxed{\mathbb E[\log(S_t/S_0)]=(\mu-\sigma^2/2)t.}
$$

This differs from $\log(\mathbb E[S_t]/S_0)=\mu t$ because $\mathbb E[\log S_t]\ne\log\mathbb E[S_t]$ in general.

### Exercise 4 — Recover a Poisson waiting-time probability

Events arrive at rate $\lambda=2$ per hour. What is the probability of waiting longer than half an hour for the next event?

**Solution:** With an exponential waiting time $T$,

$$
\mathbb P(T>0.5)=e^{-2(0.5)}=\boxed{e^{-1}\approx0.3679}.
$$

### Exercise 5 — Identify the source of an Itô correction

For $dX_t=\sigma\,dW_t$ and $f(x)=x^3$, find $d(X_t^3)$.

**Solution:** $f'(x)=3x^2$ and $f''(x)=6x$. Itô's lemma gives

$$
\boxed{d(X_t^3)=3\sigma X_t^2dW_t+3\sigma^2X_tdt.}
$$

The second term comes from quadratic variation; the ordinary chain rule misses it.

### Exercise 6 — Predict stationary OU variance

An OU process has $\theta=2$, $m=10$, and $\sigma=4$. What is its stationary variance?

**Solution:**

$$
\boxed{\lim_{t\to\infty}\operatorname{Var}(X_t)=\frac{\sigma^2}{2\theta}=\frac{16}{4}=4.}
$$

Its stationary standard deviation is $2$.

---

## 16. Notation and terminology

| Symbol / term | Meaning |
|---|---|
| $\Omega$ | Sample space |
| $\mathcal F$ | Collection of measurable events |
| $\mathbb P$ | Probability measure |
| $X_t$ | Random variable indexed by time $t$ |
| $X_t(\omega)$ | Value along one sample path |
| $\mathbb E[X]$ | Expected value |
| $\operatorname{Var}(X)$ | Variance |
| $\operatorname{Cov}(X,Y)$ | Covariance |
| $\rho(k)$ | Autocorrelation at lag $k$ |
| $S(f)$ | Power spectral density |
| $\mathcal F_t$ | Information available up to time $t$ |
| $W_t$ | Standard Brownian motion / Wiener process |
| $\Delta W$ | Brownian increment, variance $\Delta t$ |
| $dW_t$ | Stochastic differential notation, not an ordinary derivative |
| $\mu(t,x)$ | Drift coefficient of an SDE |
| $\sigma(t,x)$ | Diffusion coefficient of an SDE |
| $H$ | Hurst parameter of fractional Brownian motion |
| $[W]_T$ | Quadratic variation of Brownian motion over $[0,T]$ |
| *Adapted* | Process value uses only currently available information |
| *Martingale* | Conditional expected future value equals present value |
| *Markov* | Conditional future law depends only on the present state |
| *Stationary* | Appropriate distributional properties unchanged by shifting time |
| *Strong numerical error* | Accuracy of coupled individual sample paths |
| *Weak numerical error* | Accuracy of expected test functions/statistics |

### Essential relationships

$$
\begin{aligned}
\text{Independent increments} &\not\Rightarrow \text{independent process levels},\\
\text{Gaussian} &\not\Leftrightarrow \text{white},\\
\text{Continuous paths} &\not\Rightarrow \text{differentiable paths},\\
\text{Markov} &\not\Leftrightarrow \text{martingale},\\
\text{Exact model simulation} &\ne \text{discretized numerical solution}.
\end{aligned}
$$

The mathematical chain linking the major topics is:

$$
\text{Random variables}
\;\longrightarrow\;
\text{Stochastic processes}
\;\longrightarrow\;
\text{Brownian motion}
\;\longrightarrow\;
\text{Itô integration}
\;\longrightarrow\;
\text{SDEs and numerical solvers}.
$$
