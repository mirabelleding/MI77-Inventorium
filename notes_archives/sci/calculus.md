# Calculus & Mathematical Methods — Comprehensive Study Notes

Limits, continuity, differentiation, integration, infinite series, multivariable calculus, vector calculus, optimization, differential equations, linear algebra connections, probability, and numerical methods.

## Contents

**Part I — Single-variable calculus**

1. [Mathematical language and functions](#1-mathematical-language-and-functions)
2. [Limits: intuition, algebra, and rigorous definitions](#2-limits-intuition-algebra-and-rigorous-definitions)
3. [Continuity, asymptotes, and important theorems](#3-continuity-asymptotes-and-important-theorems)
4. [Sequences and their convergence](#4-sequences-and-their-convergence)
5. [Derivatives from first principles](#5-derivatives-from-first-principles)
6. [Differentiation rules and their derivations](#6-differentiation-rules-and-their-derivations)
7. [Implicit, logarithmic, inverse, and parametric differentiation](#7-implicit-logarithmic-inverse-and-parametric-differentiation)
8. [Geometry and applications of derivatives](#8-geometry-and-applications-of-derivatives)
9. [Mean value theorems, approximation, and L'Hôpital's rule](#9-mean-value-theorems-approximation-and-lhôpitals-rule)
10. [Integration, Riemann sums, and the Fundamental Theorem](#10-integration-riemann-sums-and-the-fundamental-theorem)
11. [Integration techniques and improper integrals](#11-integration-techniques-and-improper-integrals)
12. [Infinite series, convergence tests, and Taylor expansions](#12-infinite-series-convergence-tests-and-taylor-expansions)
13. [Parametric curves and polar coordinates](#13-parametric-curves-and-polar-coordinates)

**Part II — Multivariable calculus and geometry**

14. [Partial derivatives and total differentials](#14-partial-derivatives-and-total-differentials)
15. [Gradient, chain rules, Jacobian, and Hessian](#15-gradient-chain-rules-jacobian-and-hessian)
16. [Multivariable optimization and Lagrange multipliers](#16-multivariable-optimization-and-lagrange-multipliers)
17. [Multiple integrals and coordinate transformations](#17-multiple-integrals-and-coordinate-transformations)
18. [Vector calculus: fields, circulation, and flux](#18-vector-calculus-fields-circulation-and-flux)

**Part III — Differential equations and related mathematics**

19. [Ordinary differential equations (ODEs)](#19-ordinary-differential-equations-odes)
20. [Partial differential equations (PDEs)](#20-partial-differential-equations-pdes)
21. [Linear algebra and matrix calculus connections](#21-linear-algebra-and-matrix-calculus-connections)
22. [Probability, covariance, and calculus in statistics](#22-probability-covariance-and-calculus-in-statistics)
23. [Numerical methods, approximation, and error](#23-numerical-methods-approximation-and-error)

**Part IV — Reference and review**

24. [Formula and theorem reference](#24-formula-and-theorem-reference)
25. [Worked problems with solutions](#25-worked-problems-with-solutions)

---

# Part I — Single-variable calculus

## 1. Mathematical language and functions

### Functions, domains, and ranges

A **function** $f:A\to B$ assigns exactly one output $f(x)\in B$ to each input $x\in A$. The **domain** is the set of permitted inputs. The **image** is the set of outputs that are actually attained; it can be smaller than the declared codomain $B$.

For $f(x)=\sqrt{x-2}$ over the real numbers, the domain is $[2,\infty)$ and the range is $[0,\infty)$.

| Property | Definition | Example |
|---|---|---|
| Even | $f(-x)=f(x)$ | $x^2$, $\cos x$ |
| Odd | $f(-x)=-f(x)$ | $x^3$, $\sin x$ |
| Periodic | $f(x+T)=f(x)$ for some $T>0$ | $\sin x$ with $T=2\pi$ |
| Increasing | $x_1<x_2\Rightarrow f(x_1)\le f(x_2)$ | $e^x$ |
| Strictly increasing | $x_1<x_2\Rightarrow f(x_1)<f(x_2)$ | $x^3$ |
| Injective | Different inputs cannot have the same output | $e^x$ on $\mathbb R$ |
| Surjective | Every element of the codomain is attained | $x^3:\mathbb R\to\mathbb R$ |
| Bijective | Both injective and surjective | $e^x:\mathbb R\to(0,\infty)$ |

An inverse function $f^{-1}$ exists on the full declared codomain when $f$ is bijective. Do not confuse **inverse function** $f^{-1}(x)$ with **reciprocal** $1/f(x)$.

### The central notations

| Notation | Meaning |
|---|---|
| $\lim_{x\to a}f(x)$ | Limit as $x$ approaches $a$ |
| $f'(x)$, $df/dx$ | First derivative with respect to $x$ |
| $f''(x)$ | Second derivative |
| $\partial f/\partial x$ | Partial derivative of a multivariable function |
| $\nabla f$ | Gradient vector |
| $\int_a^b f(x)\,dx$ | Definite integral |
| $\sum_{n=1}^{\infty}a_n$ | Infinite series |
| $\mathbb R$, $\mathbb R^n$ | Real numbers; $n$-dimensional real space |
| $f\in C^k$ | $f$ has continuous derivatives through order $k$ |

**Important:** $dy/dx$ is derivative notation, not a ratio of independently defined finite changes. In many substitutions and differential equations it behaves algebraically like a ratio; the justification comes from the chain rule and differential calculus.

### Common functions and transformations

- $f(x)+c$ shifts the graph vertically by $c$.
- $f(x-c)$ shifts the graph horizontally to the right by $c$.
- $c\,f(x)$ scales the vertical coordinates.
- $f(cx)$ changes the horizontal scale.
- $f(g(x))$ is **composition**, not multiplication.

Examples:

$$
f(x)=x^2,\qquad g(x)=\sin x
$$

$$
(f\circ g)(x)=\sin^2x,\qquad (g\circ f)(x)=\sin(x^2).
$$

These are different functions; their derivatives are also different.

---

## 2. Limits: intuition, algebra, and rigorous definitions

### A limit is about approaching, not necessarily attaining

The statement

$$
\lim_{x\to a}f(x)=L
$$

means that values of $f(x)$ can be made arbitrarily close to $L$ by taking $x$ sufficiently close to $a$, with $x\ne a$. The value $f(a)$ may be different or undefined.

For example,

$$
f(x)=\frac{x^2-1}{x-1}
$$

is undefined at $x=1$. But when $x\ne1$,

$$
\frac{(x-1)(x+1)}{x-1}=x+1,
$$

so $\lim_{x\to1}f(x)=2$. This is a **removable discontinuity**.

### One-sided limits

$$
\lim_{x\to a^-}f(x)
\qquad\text{and}\qquad
\lim_{x\to a^+}f(x)
$$

are limits from the left and right. A finite two-sided limit exists exactly when both one-sided limits exist and agree.

For $f(x)=|x|/x$ (defined when $x\ne0$), the left limit at zero is $-1$ and the right limit is $+1$; the two-sided limit does not exist.

### The formal epsilon–delta definition

Saying $\lim_{x\to a}f(x)=L$ means:

> For every $\varepsilon>0$, there exists $\delta>0$ such that
> $0<|x-a|<\delta$ implies $|f(x)-L|<\varepsilon$.

Here $\varepsilon$ controls how close the **output** must be to $L$, while $\delta$ controls how close the **input** must be to $a$. The proof must work for *every* positive $\varepsilon$, however small.

**Proof example: $\lim_{x\to a}x^2=a^2$.**

We want $|x^2-a^2|<\varepsilon$. Factor:

$$
|x^2-a^2|=|x-a||x+a|.
$$

First require $|x-a|<1$. Then

$$
|x+a|\le |x-a|+2|a|<1+2|a|.
$$

It is sufficient to choose

$$
\delta=\min\left(1,\frac{\varepsilon}{2|a|+1}\right).
$$

Whenever $0<|x-a|<\delta$,

$$
|x^2-a^2|<\delta(2|a|+1)\le\varepsilon.
$$

That proves the limit. Notice that $\delta$ is permitted to depend on both $\varepsilon$ and the point $a$.

### Limit laws

If $\lim f=L$ and $\lim g=M$ at the same point, then

$$
\lim(f+g)=L+M,\qquad
\lim(fg)=LM,\qquad
\lim\frac{f}{g}=\frac{L}{M}\quad(M\ne0).
$$

Polynomial limits can therefore be evaluated by substitution. Rational functions can also be evaluated by substitution **when the denominator's limit is nonzero**.

Do not apply the quotient law when both numerator and denominator approach zero; simplify or use a justified indeterminate-form technique.

### Squeeze theorem

If $g(x)\le f(x)\le h(x)$ near $a$, and both outer functions approach $L$, then $f(x)$ also approaches $L$.

Example:

$$
-x^2\le x^2\sin(1/x)\le x^2\qquad(x\ne0).
$$

Both bounds approach zero, so

$$
\lim_{x\to0}x^2\sin(1/x)=0.
$$

The inner sine oscillates infinitely often; the shrinking factor $x^2$ makes the product converge.

### Two fundamental trigonometric limits

With angles measured in **radians**:

$$
\lim_{x\to0}\frac{\sin x}{x}=1,
\qquad
\lim_{x\to0}\frac{1-\cos x}{x}=0.
$$

The first is the central limit used to derive the derivative of sine. The analogous limit $(1-\cos x)/x^2=1/2$ follows from $1-\cos x=2\sin^2(x/2)$.

### Limits at infinity and asymptotes

- $\lim_{x\to\infty}f(x)=L$ indicates a right-hand horizontal asymptote $y=L$.
- If $f(x)\to\pm\infty$ as $x\to a^\pm$, the line $x=a$ is a vertical asymptote from that side.
- A limit equal to $+\infty$ is **not** convergence to a finite real number.

For the rational function $(3x^2+1)/(x^2-4x)$, division by $x^2$ shows that the limit as $x\to\pm\infty$ is $3$.

---

## 3. Continuity, asymptotes, and important theorems

### Continuity at a point

A function is continuous at $x=a$ when:

1. $f(a)$ is defined.
2. $\lim_{x\to a}f(x)$ exists.
3. $\lim_{x\to a}f(x)=f(a)$.

An ordinary polynomial is continuous everywhere. A quotient of continuous functions is continuous wherever the denominator does not vanish.

Common discontinuities:

| Type | Illustration | Feature |
|---|---|---|
| Removable | $(x^2-1)/(x-1)$ at $x=1$ | Finite common limit, missing or incorrect value |
| Jump | $f(x)=-1$ for $x<0$, $+1$ for $x\ge0$ | One-sided limits disagree |
| Infinite | $1/x$ at $x=0$ | Unbounded near the point |
| Oscillatory | $\sin(1/x)$ at $x=0$ | No single limiting output |

### Intermediate Value Theorem (IVT)

If $f$ is continuous on $[a,b]$ and $c$ lies between $f(a)$ and $f(b)$, then there is some $t\in[a,b]$ with $f(t)=c$.

**Root existence example.** Let $f(x)=x^3-x-1$. Since $f(1)=-1$ and $f(2)=5$, the IVT guarantees at least one root in $(1,2)$.

The theorem proves **existence**, not the number of roots or an explicit formula.

### Extreme Value Theorem (EVT)

A continuous real-valued function on a **closed, bounded interval** $[a,b]$ attains both its absolute minimum and maximum.

The hypotheses matter. For $f(x)=x$ on $(0,1)$, neither 0 nor 1 is attained, so there is no absolute minimum or maximum.

### Continuity versus differentiability

Differentiability at $a$ implies continuity at $a$, but the reverse need not hold.

Proof: If $f'(a)$ exists, then

$$
f(x)-f(a)=\frac{f(x)-f(a)}{x-a}(x-a)\longrightarrow f'(a)\cdot0=0.
$$

Thus $\lim_{x\to a}f(x)=f(a)$.

Counterexample to the converse: $f(x)=|x|$ is continuous at zero, but its left derivative is $-1$ and its right derivative is $+1$.

---

## 4. Sequences and their convergence

A sequence $(a_n)$ is a function whose inputs are positive integers. Its convergence is defined by

$$
a_n\to L\quad\Longleftrightarrow\quad
\forall\varepsilon>0\;\exists N\;\forall n\ge N:
|a_n-L|<\varepsilon.
$$

**Proof that $a_n=1/n$ converges to zero.**

Given $\varepsilon>0$, choose an integer $N>1/\varepsilon$. For every $n\ge N$,

$$
\left|\frac1n-0\right|=\frac1n\le\frac1N<\varepsilon.
$$

Contrast:

- $1/n\to0$: convergent sequence.
- $n\to+\infty$: divergent in the real-number sense.
- $(-1)^n$: bounded but divergent because it oscillates between two values.
- $(-1)^n/n\to0$: convergent despite alternating signs.

### Monotone convergence theorem for sequences

Every bounded monotone real sequence converges.

The theorem rests on the **completeness of the real numbers**: an increasing sequence bounded above converges to the supremum of its terms.

**Geometric example:** $a_n=1-2^{-n}$ increases and remains below 1, so it converges; its limit is 1.

### Cauchy sequences

A sequence is **Cauchy** when its terms eventually become arbitrarily close *to one another*:

$$
\forall\varepsilon>0\;\exists N\;\forall m,n\ge N:
|a_m-a_n|<\varepsilon.
$$

In $\mathbb R$, a sequence is Cauchy **if and only if** it converges. In a general metric space, this equivalence requires completeness.

Convergence of a **series** $\sum a_n$ is a different question: it means the sequence of partial sums $s_N=\sum_{n=1}^{N}a_n$ converges. A series can diverge even if $a_n\to0$.

---

## 5. Derivatives from first principles

### Secant lines become tangent lines

Over a finite interval from $x$ to $x+h$, the average rate of change is

$$
\frac{\Delta y}{\Delta x}
=\frac{f(x+h)-f(x)}{h}.
$$

The derivative is the limiting slope as the interval shrinks:

$$
\boxed{f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}}.
$$

If this limit is finite, the function is differentiable at $x$. Physically, if $f(t)$ is position, $f'(t)$ is instantaneous velocity and $f''(t)$ is acceleration.

### Deriving the derivative of $x^2$

$$
\begin{aligned}
\frac{d}{dx}x^2
&=\lim_{h\to0}\frac{(x+h)^2-x^2}{h}\\
&=\lim_{h\to0}\frac{2xh+h^2}{h}\\
&=\lim_{h\to0}(2x+h)\\
&=2x.
\end{aligned}
$$

We did **not** substitute $h=0$ into the original $0/0$ fraction. We simplified for nonzero $h$ first, then took the limit.

### Deriving the power rule for positive integer powers

Using the binomial theorem:

$$
(x+h)^n=x^n+nx^{n-1}h+\binom n2x^{n-2}h^2+\cdots+h^n.
$$

Subtract $x^n$, divide by $h$, and let $h\to0$. Every term except the first remaining one contains a positive power of $h$ and vanishes:

$$
\boxed{\frac{d}{dx}x^n=nx^{n-1}}.
$$

For arbitrary real $n$ on $x>0$, the rule follows from $x^n=e^{n\ln x}$ and the chain rule.

### Geometric meaning of the tangent-line equation

At $x=a$, the tangent line is

$$
y=f(a)+f'(a)(x-a).
$$

For $f(x)=x^2$ at $a=3$, the point is $(3,9)$ and slope is 6:

$$
y=9+6(x-3)=6x-9.
$$

The tangent line is also the **first-order local approximation** to a smooth function.

---

## 6. Differentiation rules and their derivations

### Essential differentiation table

| Function $f(x)$ | Derivative $f'(x)$ | Conditions / notes |
|---|---|---|
| $c$ | $0$ | Constant |
| $x^n$ | $nx^{n-1}$ | At points where the power is differentiable |
| $e^x$ | $e^x$ | All real $x$ |
| $a^x$ | $a^x\ln a$ | $a>0$ |
| $\ln x$ | $1/x$ | $x>0$ |
| $\ln|x|$ | $1/x$ | $x\ne0$ |
| $\sin x$ | $\cos x$ | Radians |
| $\cos x$ | $-\sin x$ | Radians |
| $\tan x$ | $\sec^2x$ | Where $\tan x$ exists |
| $\cot x$ | $-\csc^2x$ | Where defined |
| $\sec x$ | $\sec x\tan x$ | Where defined |
| $\csc x$ | $-\csc x\cot x$ | Where defined |
| $\arcsin x$ | $1/\sqrt{1-x^2}$ | $|x|<1$ |
| $\arccos x$ | $-1/\sqrt{1-x^2}$ | $|x|<1$ |
| $\arctan x$ | $1/(1+x^2)$ | All real $x$ |
| $\sinh x$ | $\cosh x$ | Hyperbolic sine |
| $\cosh x$ | $\sinh x$ | Hyperbolic cosine |
| $\tanh x$ | $\operatorname{sech}^2x$ | Hyperbolic tangent |

### Sum and constant multiple

$$
(f+g)'=f'+g',\qquad(cf)'=cf'.
$$

These follow immediately from splitting the difference quotient and applying limit laws.

### Product rule — derived

Insert and subtract $f(x+h)g(x)$:

$$
\begin{aligned}
&(fg)'(x)\\
&=\lim_{h\to0}\frac{f(x+h)g(x+h)-f(x)g(x)}{h}\\
&=\lim_{h\to0}\left[
f(x+h)\frac{g(x+h)-g(x)}{h}
+g(x)\frac{f(x+h)-f(x)}{h}\right]\\
&=f(x)g'(x)+f'(x)g(x).
\end{aligned}
$$

The final equality uses continuity of differentiable $f$ to replace $f(x+h)$ by $f(x)$ in the limit.

$$
\boxed{(fg)'=f'g+fg'}.
$$

**Example:** for $f(x)=x^2\sin x$,

$$
f'(x)=2x\sin x+x^2\cos x.
$$

### Quotient rule — derived

Write $f/g=f\cdot g^{-1}$. By the product and chain rules,

$$
(g^{-1})'=-g^{-2}g'.
$$

Hence, where $g\ne0$,

$$
\boxed{\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}}.
$$

Example:

$$
\frac{d}{dx}\frac{x}{1+x^2}
=\frac{1-x^2}{(1+x^2)^2}.
$$

### Chain rule — derived conceptually

For a composition $y=f(g(x))$, changing $x$ by $\Delta x$ changes $u=g(x)$ by $\Delta u$, which in turn changes $y$ by $\Delta y$.

When $\Delta u\ne0$,

$$
\frac{\Delta y}{\Delta x}
=\frac{\Delta y}{\Delta u}\frac{\Delta u}{\Delta x}.
$$

Taking limits suggests

$$
\boxed{\frac{d}{dx}f(g(x))=f'(g(x))g'(x)}.
$$

A fully rigorous proof uses the fact that differentiability implies the local approximation $f(u+\Delta u)-f(u)=f'(u)\Delta u+o(\Delta u)$, which also handles $\Delta u=0$.

**Example 1 — power of a function:**

$$
\frac{d}{dx}(3x^2+1)^5=5(3x^2+1)^4(6x).
$$

**Example 2 — nested trigonometric function:**

$$
\frac{d}{dx}\sin(x^2)=2x\cos(x^2).
$$

**Example 3 — exponential composition:**

$$
\frac{d}{dx}e^{\sin x}=e^{\sin x}\cos x.
$$

**Common mistake:** the derivative of $\sin(x^2)$ is **not** $\cos(x^2)$. The inner derivative $2x$ is required.

### Deriving the derivative of $\sin x$

Use the identity $\sin(x+h)=\sin x\cos h+\cos x\sin h$:

$$
\begin{aligned}
\frac{d}{dx}\sin x
&=\lim_{h\to0}\frac{\sin(x+h)-\sin x}{h}\\
&=\sin x\lim_{h\to0}\frac{\cos h-1}{h}
+\cos x\lim_{h\to0}\frac{\sin h}{h}\\
&=0+\cos x=\cos x.
\end{aligned}
$$

This derivation explains why **radians** are indispensable to the standard derivative formula.

### Deriving the derivative of an inverse function

If $y=f^{-1}(x)$, then $f(y)=x$. Differentiate both sides:

$$
f'(y)y'=1,\qquad
\boxed{(f^{-1})'(x)=\frac1{f'(f^{-1}(x))}}.
$$

Example: set $y=\arctan x$, so $\tan y=x$. Then

$$
\sec^2y\,y'=1,\qquad y'=\frac1{1+\tan^2y}=\frac1{1+x^2}.
$$

---

## 7. Implicit, logarithmic, inverse, and parametric differentiation

### Implicit differentiation

Not every curve is naturally given by $y=f(x)$. For a circle,

$$
x^2+y^2=R^2.
$$

Treat $y$ as a differentiable function of $x$ locally. Differentiating:

$$
2x+2y\frac{dy}{dx}=0
\quad\Rightarrow\quad
\boxed{\frac{dy}{dx}=-\frac xy}.
$$

This formula applies where $y\ne0$; at the leftmost/rightmost points the circle has a vertical tangent and $y$ is not locally a differentiable function of $x$.

### General implicit-function formula

For $F(x,y)=0$ with $F_y\ne0$ near a point, differentiation gives

$$
F_x+F_y\frac{dy}{dx}=0
\quad\Rightarrow\quad
\boxed{\frac{dy}{dx}=-\frac{F_x}{F_y}}.
$$

The condition $F_y\ne0$ is part of the local guarantee given by the implicit function theorem; one cannot blindly divide by $F_y$ when it vanishes.

### Logarithmic differentiation

For products, quotients, and variable exponents, take logarithms first.

Example for $x>0$:

$$
y=x^x,\qquad \ln y=x\ln x.
$$

Differentiate:

$$
\frac{y'}y=\ln x+1
\quad\Rightarrow\quad
\boxed{y'=x^x(\ln x+1)}.
$$

More generally, for positive differentiable $u(x)$,

$$
\frac{d}{dx}u(x)^{v(x)}
=u(x)^{v(x)}
\left(v'(x)\ln u(x)+v(x)\frac{u'(x)}{u(x)}\right).
$$

### Parametric differentiation

When $x=x(t)$ and $y=y(t)$, where $dx/dt\ne0$,

$$
\frac{dy}{dx}=\frac{dy/dt}{dx/dt}.
$$

For a unit circle parameterization $x=\cos t$, $y=\sin t$,

$$
\frac{dy}{dx}=\frac{\cos t}{-\sin t}=-\cot t,
$$

where $\sin t\ne0$. This agrees with implicit differentiation of $x^2+y^2=1$.

For the second derivative, **differentiate with respect to $t$ and divide by $dx/dt$ again**:

$$
\frac{d^2y}{dx^2}
=\frac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt}.
$$

Do not simply divide $d^2y/dt^2$ by $d^2x/dt^2$.

---

## 8. Geometry and applications of derivatives

### Increasing, decreasing, and critical points

If $f'(x)>0$ throughout an interval, $f$ is strictly increasing there. If $f'(x)<0$, it is strictly decreasing. This conclusion follows from the Mean Value Theorem.

A **critical point** of $f$ is a point in its domain where $f'(x)=0$ or $f'$ does not exist. Critical points are candidates for local extrema, **not guarantees**.

Example: $f(x)=x^3-3x$.

$$
f'(x)=3x^2-3=3(x-1)(x+1).
$$

The critical points are $x=-1$ and $x=1$:

| Interval | Sign of $f'$ | Behaviour |
|---|---|---|
 $(-\infty,-1)$ | Positive | Increasing |
 $(-1,1)$ | Negative | Decreasing |
 $(1,\infty)$ | Positive | Increasing |

Thus $x=-1$ is a local maximum and $x=1$ is a local minimum. The values are $f(-1)=2$ and $f(1)=-2$.

**Counterexample:** $f(x)=x^3$ has $f'(0)=0$ but no extremum at zero; the function continues increasing on both sides.

### Second derivative: concavity and convexity

The second derivative describes how the **slope** changes:

- $f''(x)>0$: the graph bends upward (**convex**, or “concave up” in elementary calculus).
- $f''(x)<0$: the graph bends downward (**concave**, or “concave down”).
- $f''(x)=0$: the test is inconclusive by itself.

For $f(x)=x^2$,

$$
f'(x)=2x,\qquad f''(x)=2>0,
$$

so the function is strictly convex everywhere.

For $f(x)=-x^2$, $f''(x)=-2<0$, so it is strictly concave everywhere.

**Inflection point:** a point where concavity *changes*. For $f(x)=x^3$,

$$
f''(x)=6x,
$$

which changes from negative to positive at zero; hence $(0,0)$ is an inflection point.

But $f(x)=x^4$ has $f''(0)=0$ without changing concavity. Merely solving $f''=0$ does not prove an inflection point.

### Second-derivative test

At a stationary point $a$ with $f'(a)=0$:

| Condition | Conclusion |
|---|---|
 $f''(a)>0$ | Strict local minimum |
 $f''(a)<0$ | Strict local maximum |
 $f''(a)=0$ | Inconclusive |

Examples:

- $f(x)=x^2$: $f''(0)=2$, local minimum.
- $f(x)=-x^2$: $f''(0)=-2$, local maximum.
- $f(x)=x^4$: $f''(0)=0$, still a minimum.
- $f(x)=x^3$: $f''(0)=0$, neither a minimum nor maximum.

### Convexity from tangent lines and chords

A differentiable function on an interval is convex if its graph lies **above every tangent line**:

$$
f(y)\ge f(x)+f'(x)(y-x).
$$

Equivalently, for $0\le t\le1$,

$$
f(tx+(1-t)y)\le tf(x)+(1-t)f(y).
$$

The inequality says that the graph lies **below the chord** joining two points on it. These two descriptions are compatible: chords above the graph, tangent lines below it.

For a twice-differentiable function on an interval, $f''\ge0$ implies convexity. A positive second derivative everywhere is sufficient for strict convexity, but is not necessary (consider $x^4$ at zero).

### Optimization on a closed interval

To find an **absolute** maximum or minimum of a continuous function on $[a,b]$:

1. Find critical points in $(a,b)$.
2. Evaluate the function at those points.
3. Evaluate it at endpoints $a$ and $b$.
4. Compare all candidates.

**Example:** $f(x)=x(4-x)$ on $[0,4]$.

$$
f'(x)=4-2x=0\quad\Rightarrow\quad x=2.
$$

At $x=0,2,4$ the function values are $0,4,0$. The absolute maximum is 4 at $x=2$.

### Related rates

When several physical quantities depend on time, differentiate an equation connecting them.

**Expanding circle:** $A=\pi r^2$ with radius $r(t)$. By the chain rule:

$$
\frac{dA}{dt}=2\pi r\frac{dr}{dt}.
$$

If $r=3$ meters and $dr/dt=0.2$ meters/second, then $dA/dt=1.2\pi$ square meters/second.

Always include units: derivatives carry units of **output per input**, whereas correlations are dimensionless.

### Linearization and differentials

For a differentiable function near $x=a$:

$$
f(a+h)=f(a)+f'(a)h+o(h).
$$

The approximation $f(a+h)\approx f(a)+f'(a)h$ is **linearization**. We write the first-order differential as $dy=f'(x)\,dx$.

Example: estimate $\sqrt{4.1}$ using $f(x)=\sqrt{x}$ at $a=4$:

$$
\sqrt{4.1}\approx2+\frac1{2\sqrt4}(0.1)=2.025.
$$

The true value is approximately 2.024846. The small discrepancy comes from the neglected nonlinear terms.

---

## 9. Mean value theorems, approximation, and L'Hôpital's rule

### Rolle's theorem

If $f$ is continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a)=f(b)$, then there exists $c\in(a,b)$ such that $f'(c)=0$.

**Reason:** By the Extreme Value Theorem, $f$ attains maximum and minimum values. If it is not constant, at least one of those extrema occurs inside the interval. At a differentiable interior extremum, the derivative is zero (Fermat's theorem). If constant, every interior derivative is zero.

### Mean Value Theorem (MVT)

If $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, there exists $c\in(a,b)$ satisfying

$$
\boxed{f'(c)=\frac{f(b)-f(a)}{b-a}}.
$$

Some instantaneous slope equals the slope of the secant line across the whole interval.

**Short proof from Rolle:** Define the secant line

$$
\ell(x)=f(a)+\frac{f(b)-f(a)}{b-a}(x-a).
$$

Set $g(x)=f(x)-\ell(x)$. Then $g(a)=g(b)=0$. Rolle supplies a point with $g'(c)=0$, so $f'(c)-\ell'(c)=0$, proving the result.

**Example:** $f(x)=x^2$ on $[1,3]$. The secant slope is $(9-1)/(3-1)=4$. Since $f'(x)=2x$, $c=2$ satisfies the theorem.

### Consequences of the MVT

- If $f'(x)=0$ everywhere on an interval, $f$ is constant.
- If $f'(x)>0$ everywhere, $f$ is strictly increasing.
- If $|f'(x)|\le M$, then $|f(b)-f(a)|\le M|b-a|$ (a Lipschitz bound).
- If two functions have the same derivative on an interval, they differ by a constant.

### L'Hôpital's rule

For an indeterminate quotient of form $0/0$ or $\infty/\infty$, under the rule's differentiability, nonzero-denominator-derivative, and limit hypotheses:

$$
\lim_{x\to a}\frac{f(x)}{g(x)}
=\lim_{x\to a}\frac{f'(x)}{g'(x)}
$$

provided the right-hand limit exists as a finite or infinite extended limit.

**Example:**

$$
\lim_{x\to0}\frac{e^x-1}{x}
=\lim_{x\to0}\frac{e^x}{1}=1.
$$

**Example requiring two applications:**

$$
\begin{aligned}
\lim_{x\to0}\frac{1-\cos x}{x^2}
&=\lim_{x\to0}\frac{\sin x}{2x}\\
&=\lim_{x\to0}\frac{\cos x}{2}
=\frac12.
\end{aligned}
$$

**Important restrictions:**

- Do not apply directly to an expression of form $0\cdot\infty$, $\infty-\infty$, $1^\infty$, $0^0$, or $\infty^0$. Transform it into a suitable quotient first.
- Differentiate the **numerator and denominator separately**; do not use the quotient rule on their ratio.
- The rule is not a substitute for verifying that the necessary indeterminate form and hypotheses hold.

For $x\ln x$ as $x\to0^+$, write $\ln x/(1/x)$. Then derivatives give $(1/x)/(-1/x^2)=-x\to0$.

### Taylor's theorem as a refinement of linearization

The linear approximation at $a$ is $f(a)+f'(a)(x-a)$. Taylor's theorem adds curvature and higher-order information:

$$
f(x)=\sum_{k=0}^{n}\frac{f^{(k)}(a)}{k!}(x-a)^k+R_n(x).
$$

If $f$ has enough derivatives, the Lagrange remainder has the form

$$
R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}
$$

for some $\xi$ between $a$ and $x$.

**Where do the coefficients come from?** Suppose a polynomial $P_n(x)=c_0+c_1(x-a)+\cdots+c_n(x-a)^n$ should have the same derivatives as $f$ through order $n$ at $a$.

- $P_n(a)=c_0=f(a)$.
- $P_n'(a)=c_1=f'(a)$.
- $P_n''(a)=2!c_2=f''(a)$.
- In general, $P_n^{(k)}(a)=k!c_k=f^{(k)}(a)$.

Therefore $c_k=f^{(k)}(a)/k!$.

Example at $a=0$:

$$
e^x\approx1+x+\frac{x^2}{2}+\frac{x^3}{6}.
$$

At $x=0.1$, the cubic approximation is $1.1051667$, close to $e^{0.1}\approx1.1051702$.

The remainder theorem lets us **bound** errors instead of merely hoping the approximation is close.

---

## 10. Integration, Riemann sums, and the Fundamental Theorem

### Two related ideas: antiderivatives and accumulation

An **indefinite integral** represents a family of antiderivatives:

$$
\int f(x)\,dx=F(x)+C
\quad\text{when }F'(x)=f(x).
$$

A **definite integral** accumulates signed area (or more generally, a quantity such as mass, work, or probability):

$$
\int_a^b f(x)\,dx.
$$

Unlike an indefinite integral, a definite integral produces a **number** when its limits and integrand are specified.

### Riemann sums: where the integral comes from

Partition $[a,b]$ into $n$ subintervals of width $\Delta x=(b-a)/n$, choose a sample point $x_i^*$ in each subinterval, and compute

$$
\sum_{i=1}^n f(x_i^*)\Delta x.
$$

If these sums converge to a common value as the maximum subinterval width tends to zero, that value is the definite integral.

**Derivation of $\int_0^1x^2\,dx$.**

Use right endpoints $x_i=i/n$ and $\Delta x=1/n$:

$$
\begin{aligned}
\int_0^1x^2\,dx
&=\lim_{n\to\infty}\sum_{i=1}^{n}\left(\frac in\right)^2\frac1n\\
&=\lim_{n\to\infty}\frac1{n^3}\sum_{i=1}^{n}i^2\\
&=\lim_{n\to\infty}\frac{n(n+1)(2n+1)}{6n^3}\\
&=\frac13.
\end{aligned}
$$

This explains integration as a limit of finite approximations rather than merely a reverse-derivative trick.

### Fundamental Theorem of Calculus (FTC), Part I

If $f$ is continuous and $F(x)=\int_a^x f(t)\,dt$, then

$$
\boxed{F'(x)=f(x)}.
$$

**Reason:** $F(x+h)-F(x)=\int_x^{x+h}f(t)\,dt$. Divide by $h$. By continuity, the average value of $f$ on that shrinking interval approaches $f(x)$.

For a variable upper limit $g(x)$, combine with the chain rule:

$$
\frac{d}{dx}\int_a^{g(x)}f(t)\,dt=f(g(x))g'(x).
$$

Example:

$$
\frac{d}{dx}\int_0^{x^2}\sin t\,dt=2x\sin(x^2).
$$

### FTC, Part II

If $F'=f$ on $[a,b]$ and $f$ is continuous, then

$$
\boxed{\int_a^bf(x)\,dx=F(b)-F(a)}.
$$

The theorem links the seemingly different concepts of **accumulation** and **instantaneous change**.

Example:

$$
\int_1^3 2x\,dx=[x^2]_1^3=9-1=8.
$$

### Properties of definite integrals

$$
\int_a^b(cf+dg)\,dx
=c\int_a^bf\,dx+d\int_a^bg\,dx
$$

$$
\int_a^bf\,dx=-\int_b^af\,dx,\qquad
\int_a^c f\,dx=\int_a^b f\,dx+\int_b^c f\,dx.
$$

If $f\ge0$, its definite integral is nonnegative. If $f$ takes negative values, the integral counts *signed* area, not the sum of absolute geometric areas; the latter uses $\int|f(x)|\,dx$.

### Average value and physical meaning

The average value of an integrable function on $[a,b]$ is

$$
f_{\mathrm{avg}}=\frac1{b-a}\int_a^bf(x)\,dx.
$$

If $v(t)$ is velocity, $\int_{t_0}^{t_1}v(t)\,dt$ is net displacement. If $|v(t)|$ is speed, $\int |v(t)|\,dt$ is distance traveled.

### Essential antiderivatives

| Integrand | Antiderivative | Conditions |
|---|---|---|
| $x^n$ | $x^{n+1}/(n+1)+C$ | $n\ne-1$, where defined |
| $1/x$ | $\ln|x|+C$ | $x\ne0$ on an interval |
| $e^x$ | $e^x+C$ | All real |
| $a^x$ | $a^x/\ln a+C$ | $a>0$, $a\ne1$ |
| $\sin x$ | $-\cos x+C$ | All real |
| $\cos x$ | $\sin x+C$ | All real |
| $\sec^2x$ | $\tan x+C$ | Where defined |
| $1/(1+x^2)$ | $\arctan x+C$ | All real |
| $1/\sqrt{1-x^2}$ | $\arcsin x+C$ | $|x|<1$ |

**Remember the constant $C$:** differentiation removes constants, so indefinite integration cannot recover a unique original constant.

---

## 11. Integration techniques and improper integrals

### Substitution — reverse chain rule

If $u=g(x)$ and $du=g'(x)\,dx$, then

$$
\int f(g(x))g'(x)\,dx=\int f(u)\,du.
$$

**Example:** $\int 2x\cos(x^2)\,dx$.

Set $u=x^2$, so $du=2x\,dx$:

$$
\int2x\cos(x^2)\,dx=\int\cos u\,du=\sin u+C
=\sin(x^2)+C.
$$

For definite integrals, change the limits too:

$$
\int_0^1 2x e^{x^2}\,dx
=\int_{u=0}^{u=1}e^u\,du=e-1.
$$

### Integration by parts — derived from the product rule

Starting with $(uv)'=u'v+uv'$ and integrating:

$$
uv=\int u'v\,dx+\int uv'\,dx.
$$

Rearrange:

$$
\boxed{\int u\,dv=uv-\int v\,du}.
$$

**Example:** $\int x e^x\,dx$.

Choose $u=x$, $dv=e^x\,dx$; then $du=dx$ and $v=e^x$:

$$
\int xe^x\,dx=xe^x-\int e^x\,dx=e^x(x-1)+C.
$$

Choose $u$ so that differentiating it simplifies the remaining integral; this is a heuristic, not a theorem.

### Partial fractions

For a proper rational function with a factorable denominator, decompose into simpler pieces.

Example:

$$
\frac1{x^2-1}=\frac1{(x-1)(x+1)}
=\frac12\frac1{x-1}-\frac12\frac1{x+1}.
$$

Thus

$$
\int\frac{dx}{x^2-1}
=\frac12\ln|x-1|-\frac12\ln|x+1|+C
$$

on any interval avoiding the singularities $x=\pm1$. For an improper definite integral crossing a pole, analyze one-sided integrals; do not simply cancel divergent terms.

### Trigonometric identities and substitutions

Useful identities:

$$
\sin^2x+\cos^2x=1,\quad
1+\tan^2x=\sec^2x,\quad
\sin^2x=\frac{1-\cos2x}{2}.
$$

Example:

$$
\int\sin^2x\,dx
=\frac12\int(1-\cos2x)\,dx
=\frac x2-\frac{\sin2x}{4}+C.
$$

For square roots:

| Expression | Common substitution | Identity |
|---|---|---|
| $\sqrt{a^2-x^2}$ | $x=a\sin\theta$ | $1-\sin^2\theta=\cos^2\theta$ |
| $\sqrt{a^2+x^2}$ | $x=a\tan\theta$ | $1+\tan^2\theta=\sec^2\theta$ |
| $\sqrt{x^2-a^2}$ | $x=a\sec\theta$ | $\sec^2\theta-1=\tan^2\theta$ |

The substitution domain and signs must be handled carefully; expressions such as $\sqrt{\cos^2\theta}$ equal $|\cos\theta|$, not automatically $\cos\theta$.

### Improper integrals

An integral is **improper** if its interval is unbounded or the integrand becomes unbounded on the interval.

$$
\int_1^\infty f(x)\,dx
=\lim_{R\to\infty}\int_1^R f(x)\,dx.
$$

Example:

$$
\int_1^\infty\frac{dx}{x^2}
=\lim_{R\to\infty}\left(1-\frac1R\right)=1.
$$

### The $p$-integral test

For $p\in\mathbb R$:

$$
\int_1^\infty x^{-p}\,dx
\begin{cases}
\text{converges},&p>1,\\
\text{diverges},&p\le1.
\end{cases}
$$

For $p\ne1$:

$$
\int_1^R x^{-p}\,dx
=\frac{R^{1-p}-1}{1-p}.
$$

As $R\to\infty$, the expression is finite precisely when $1-p<0$, i.e. $p>1$. For $p=1$, the integral is $\ln R\to\infty$.

**Different endpoint, different threshold:**

$$
\int_0^1 x^{-p}\,dx
\begin{cases}
\text{converges},&p<1,\\
\text{diverges},&p\ge1.
\end{cases}
$$

### Comparison of integrals

For nonnegative functions with $0\le f(x)\le g(x)$ sufficiently far out:

- If $\int_a^\infty g(x)\,dx$ converges, then so does $\int_a^\infty f(x)\,dx$.
- If $\int_a^\infty f(x)\,dx$ diverges, then so does $\int_a^\infty g(x)\,dx$.

For signed integrands, positive-function comparisons alone are insufficient; consider absolute convergence and cancellations.

---

## 12. Infinite series, convergence tests, and Taylor expansions

### Sequence versus series

A **sequence** is $a_1,a_2,\ldots$. A **series** is the formal sum

$$
\sum_{n=1}^{\infty}a_n
=\lim_{N\to\infty}\sum_{n=1}^{N}a_n.
$$

The series converges only if its **partial sums** have a finite limit.

The necessary condition $a_n\to0$ is **not sufficient** for a series to converge.

### Geometric series — derivation

For ratio $r$ and $r\ne1$, let

$$
S_N=a+ar+\cdots+ar^{N-1}.
$$

Subtract $rS_N$:

$$
(1-r)S_N=a-ar^N
\quad\Rightarrow\quad
S_N=a\frac{1-r^N}{1-r}.
$$

If $|r|<1$, then $r^N\to0$:

$$
\boxed{\sum_{n=0}^\infty ar^n=\frac{a}{1-r}\quad(|r|<1)}.
$$

Example: $1/2+1/4+1/8+\cdots=1$.

If $|r|\ge1$ and $a\ne0$, the infinite geometric series does not converge.

### Harmonic series — why it diverges

The terms of

$$
1+\frac12+\frac13+\frac14+\cdots
$$

approach zero, but the series diverges.

Group terms:

$$
1+\frac12
+\left(\frac13+\frac14\right)
+\left(\frac15+\cdots+\frac18\right)
+\cdots.
$$

Each block after the first contains increasingly many terms, but its sum is at least $1/2$. There are infinitely many such blocks, so the partial sums cannot remain bounded.

### Convergence-test reference

| Test | Main idea | Conditions and conclusion |
|---|---|---|
| Term / divergence test | Inspect $\lim a_n$ | If not zero (or not existing), $\sum a_n$ diverges; zero alone proves nothing |
| Geometric | $\sum ar^n$ | Converges for $|r|<1$ |
| $p$-series | $\sum 1/n^p$ | Converges for $p>1$ |
| Integral test | Compare to $\int f(x)\,dx$ | $a_n=f(n)$ with $f$ positive, continuous, decreasing eventually |
| Direct comparison | Bound by another nonnegative series | Convergence from a larger convergent majorant; divergence from a smaller divergent minorant |
| Limit comparison | $\lim a_n/b_n=c$ | $0<c<\infty$ for eventually positive terms implies same convergence |
| Ratio test | $L=\lim|a_{n+1}/a_n|$ | $L<1$: absolute convergence; $L>1$: divergence; $L=1$: inconclusive |
| Root test | $L=\limsup|a_n|^{1/n}$ | $L<1$: absolute convergence; $L>1$: divergence; $L=1$: inconclusive |
| Alternating series test | Alternating signs and shrinking magnitudes | If $b_n\downarrow0$, $\sum(-1)^nb_n$ converges |

### Ratio test: a worked example

For $\sum_{n=0}^\infty x^n/n!$, put $a_n=x^n/n!$:

$$
\left|\frac{a_{n+1}}{a_n}\right|
=\frac{|x|}{n+1}\longrightarrow0.
$$

Therefore this series converges absolutely for **every real $x$**. It is the exponential series.

### Absolute versus conditional convergence

If $\sum|a_n|$ converges, then $\sum a_n$ converges **absolutely**.

The alternating harmonic series

$$
1-\frac12+\frac13-\frac14+\cdots=\ln2
$$

converges by the alternating series test, but the sum of absolute values is the divergent harmonic series. This is **conditional convergence**.

Absolute convergence is more robust: rearranging the terms preserves the sum. A conditionally convergent real series may change value under a suitable rearrangement.

### Power series and radius of convergence

A power series centered at $a$ has the form

$$
\sum_{n=0}^\infty c_n(x-a)^n.
$$

There is a radius $R\in[0,\infty]$ such that the series converges absolutely for $|x-a|<R$ and diverges for $|x-a|>R$. **Endpoints must be tested separately**.

Example:

$$
\sum_{n=0}^\infty x^n=\frac1{1-x}
\qquad(|x|<1).
$$

At $x=1$ it becomes $1+1+\cdots$; at $x=-1$ it oscillates. Neither endpoint converges.

### Taylor and Maclaurin series

Taylor series about $x=a$:

$$
\sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n.
$$

Maclaurin is the special case $a=0$.

| Function | Maclaurin expansion | Convergence |
|---|---|---|
| $e^x$ | $1+x+x^2/2!+x^3/3!+\cdots$ | All real $x$ |
| $\sin x$ | $x-x^3/3!+x^5/5!-\cdots$ | All real $x$ |
| $\cos x$ | $1-x^2/2!+x^4/4!-\cdots$ | All real $x$ |
| $1/(1-x)$ | $1+x+x^2+\cdots$ | $|x|<1$ |
| $\ln(1+x)$ | $x-x^2/2+x^3/3-\cdots$ | $-1<x\le1$ |
| $\arctan x$ | $x-x^3/3+x^5/5-\cdots$ | $|x|\le1$ |

**Derivation of the sine series coefficients:** at $x=0$, the derivatives of $\sin x$ cycle through $\sin,\cos,-\sin,-\cos$. Their values are $0,1,0,-1,0,1,\ldots$; placing these in $f^{(n)}(0)/n!$ gives the alternating odd-power expansion.

### Taylor series may fail to reproduce a smooth function

Infinite differentiability alone does **not** imply equality with the Taylor series.

The function

$$
f(x)=
\begin{cases}
e^{-1/x^2},&x\ne0,\\
0,&x=0
\end{cases}
$$

has every derivative equal to zero at zero, so its Maclaurin series is identically zero, while $f(x)>0$ elsewhere. The additional condition needed is that the Taylor remainders tend to zero.

### Taylor approximation error

For $e^x$ on $[0,0.1]$, the third-degree Taylor remainder obeys

$$
|R_3(0.1)|\le\frac{e^{0.1}}{4!}(0.1)^4
\approx4.61\times10^{-6}.
$$

This is a guaranteed upper bound on the error, not the error itself.

---

## 13. Parametric curves and polar coordinates

### Parametric curves

A planar curve can be described by $x=x(t)$ and $y=y(t)$. Different parameterizations may trace the same geometric curve at different speeds or in different directions.

For a particle path $\mathbf r(t)=(x(t),y(t))$:

- Velocity: $\mathbf v(t)=(x'(t),y'(t))$.
- Speed: $\|\mathbf v(t)\|=\sqrt{x'(t)^2+y'(t)^2}$.
- Acceleration: $\mathbf a(t)=(x''(t),y''(t))$.

The arc length from $t=a$ to $t=b$ is

$$
L=\int_a^b\sqrt{[x'(t)]^2+[y'(t)]^2}\,dt.
$$

**Why?** Over a short time interval, the displacement is approximately $\mathbf r'(t)\Delta t$; summing its magnitude and taking a limit yields the integral.

### Polar coordinates

$$
x=r\cos\theta,\qquad y=r\sin\theta,\qquad r^2=x^2+y^2.
$$

The same point can have multiple polar descriptions; in particular $(r,\theta)$ and $(r,\theta+2\pi)$ represent the same location.

For a polar curve $r=r(\theta)$, arc length is

$$
L=\int_{\alpha}^{\beta}
\sqrt{r(\theta)^2+[r'(\theta)]^2}\,d\theta.
$$

**Derivation:** $x'=r'\cos\theta-r\sin\theta$ and $y'=r'\sin\theta+r\cos\theta$; squaring and adding cancels the cross terms, leaving $x'^2+y'^2=r'^2+r^2$.

The area swept by a nonnegative radial curve with a suitable nonoverlapping angular description is

$$
A=\frac12\int_{\alpha}^{\beta}r(\theta)^2\,d\theta.
$$

This follows from the area of a thin circular sector, approximately $\tfrac12r^2\Delta\theta$.

For $r=R$ and $0\le\theta\le2\pi$, the formula returns $\pi R^2$.

---

# Part II — Multivariable calculus and geometry

## 14. Partial derivatives and total differentials

### Why partial differentiation exists

A one-variable function $y=f(x)$ has one independent input. A multivariable function, such as temperature

$$
T=T(x,y,z,t),
$$

depends on **location** $(x,y,z)$ and **time** $t$. Temperature may change when we move east, move upward, or wait, and those changes need not be identical.

The partial derivative isolates the change in one variable **while holding the other independent variables fixed**.

For $f(x,y)$:

$$
\boxed{
\frac{\partial f}{\partial x}(x,y)
=\lim_{h\to0}\frac{f(x+h,y)-f(x,y)}{h}
}
$$

$$
\boxed{
\frac{\partial f}{\partial y}(x,y)
=\lim_{h\to0}\frac{f(x,y+h)-f(x,y)}{h}
}
$$

The symbol $\partial$ (curly d) signals a **partial derivative**, as distinct from the ordinary derivative $d/dx$ of a one-variable function.

### Worked example: differentiate with respect to each input

Let

$$
f(x,y)=x^2y+\sin(xy).
$$

Differentiate with respect to $x$, treating $y$ as a constant:

$$
\boxed{f_x=2xy+y\cos(xy)}.
$$

Differentiate with respect to $y$, treating $x$ as a constant:

$$
\boxed{f_y=x^2+x\cos(xy)}.
$$

Why the $y$ in the first cosine term? Because the chain rule gives

$$
\frac{\partial}{\partial x}\sin(xy)
=\cos(xy)\frac{\partial(xy)}{\partial x}=y\cos(xy).
$$

Similarly, differentiation with respect to $y$ produces $x\cos(xy)$.

**Numeric example at $(x,y)=(1,2)$:**

$$
f_x(1,2)=4+2\cos2,\qquad f_y(1,2)=1+\cos2.
$$

These are the slopes of two different cross-sections of the same surface.

### Geometric interpretation

The graph $z=f(x,y)$ is a surface.

- Fix $y=y_0$ and vary $x$: the resulting cross-section has slope $f_x(x,y_0)$.
- Fix $x=x_0$ and vary $y$: the cross-section has slope $f_y(x_0,y)$.

**Partial derivatives are not the entire story:** a simultaneous change in $x$ and $y$ combines both effects.

### Second-order and mixed partial derivatives

Differentiate again:

$$
f_{xx}=\frac{\partial^2f}{\partial x^2},\qquad
f_{yy}=\frac{\partial^2f}{\partial y^2},
$$

$$
f_{xy}=\frac{\partial}{\partial y}(f_x),\qquad
f_{yx}=\frac{\partial}{\partial x}(f_y).
$$

For the example $f=x^2y+\sin(xy)$:

$$
f_{xy}=2x+\cos(xy)-xy\sin(xy),
$$

$$
f_{yx}=2x+\cos(xy)-xy\sin(xy).
$$

The mixed partial derivatives agree.

**Clairaut's / Schwarz's theorem:** If the relevant second partial derivatives are continuous in a neighborhood of a point, then $f_{xy}=f_{yx}$ there. The continuity hypothesis is a convenient sufficient condition; mixed partials need not agree without appropriate regularity.

### Total change versus partial change

For small changes $\Delta x,\Delta y$, a differentiable $f$ obeys

$$
f(x+\Delta x,y+\Delta y)
=f(x,y)+f_x\Delta x+f_y\Delta y
+o\left(\sqrt{\Delta x^2+\Delta y^2}\right).
$$

The linear part is the **total differential**:

$$
\boxed{df=f_x\,dx+f_y\,dy}.
$$

Example:

$$
V(r,h)=\pi r^2h
$$

is the volume of a cylinder. Its differential is

$$
dV=2\pi rh\,dr+\pi r^2\,dh.
$$

Thus a small radius change and a small height change have separate first-order effects; radius appears twice because area scales quadratically with it.

### Differentiation along a path

Suppose $x=x(t)$, $y=y(t)$ and $z(t)=f(x(t),y(t))$. Both inputs now depend on time. The ordinary derivative is

$$
\boxed{
\frac{dz}{dt}
=f_x\frac{dx}{dt}+f_y\frac{dy}{dt}
}.
$$

For $f=x^2y$, $x(t)=t^2$, and $y(t)=\sin t$:

$$
z(t)=t^4\sin t,
$$

$$
\frac{dz}{dt}=4t^3\sin t+t^4\cos t.
$$

The multivariable chain rule gives the same result:

$$
f_xx'(t)+f_yy'(t)
=(2xy)(2t)+(x^2)(\cos t)
=4t^3\sin t+t^4\cos t.
$$

### Why partial derivatives alone do not guarantee differentiability

This is a subtle but important multivariable distinction.

Define

$$
f(x,y)=
\begin{cases}
\dfrac{xy}{x^2+y^2},&(x,y)\ne(0,0),\\
0,&(x,y)=(0,0).
\end{cases}
$$

Along the $x$-axis ($y=0$), $f(x,0)=0$, so $f_x(0,0)=0$. Similarly $f_y(0,0)=0$.

Yet along $y=x\ne0$:

$$
f(x,x)=\frac{x^2}{2x^2}=\frac12.
$$

This does not approach $f(0,0)=0$. The function is **not even continuous** at the origin, so it cannot be differentiable there.

In multiple dimensions:

- Existence of partial derivatives at a point does **not** imply continuity.
- Differentiability implies continuity.
- Continuity of all first partial derivatives **in a neighborhood** is a standard sufficient condition for differentiability.

### Ordinary derivative, partial derivative, and PDE

Do not conflate these terms:

| Term | What it is |
|---|---|
| Ordinary derivative $dy/dx$ | Differentiate a one-variable function |
| Partial derivative $\partial f/\partial x$ | Differentiate with respect to one independent variable, holding others fixed |
| Total derivative $df/dt$ | Account for all dependencies on $t$ |
| ODE | Equation involving ordinary derivatives of an unknown function |
| PDE | Equation involving partial derivatives of an unknown function of several variables |

For example, $u_t=\alpha u_{xx}$ is a **partial differential equation** about a function $u(x,t)$; neither $u_t$ nor $u_{xx}$ is an ordinary derivative.

---

## 15. Gradient, chain rules, Jacobian, and Hessian

### The gradient

For a scalar function $f:\mathbb R^n\to\mathbb R$, the gradient is the vector of first partial derivatives:

$$
\boxed{
\nabla f=
\begin{pmatrix}
\partial f/\partial x_1\\
\vdots\\
\partial f/\partial x_n
\end{pmatrix}
}.
$$

For $f(x,y)=x^2+3xy+y^2$:

$$
\nabla f(x,y)=
\begin{pmatrix}
2x+3y\\
3x+2y
\end{pmatrix}.
$$

The gradient points in the direction of **steepest local increase** when interpreted with the standard Euclidean inner product.

### Directional derivative — derived

Move from $\mathbf x$ a short distance $h$ along a unit vector $\mathbf u$:

$$
D_{\mathbf u}f(\mathbf x)
=\lim_{h\to0}\frac{f(\mathbf x+h\mathbf u)-f(\mathbf x)}h.
$$

If $f$ is differentiable,

$$
\boxed{D_{\mathbf u}f=\nabla f\cdot\mathbf u}.
$$

**Why the gradient gives steepest ascent:** By Cauchy–Schwarz,

$$
\nabla f\cdot\mathbf u
\le\|\nabla f\|\,\|\mathbf u\|
=\|\nabla f\|.
$$

Equality occurs when $\mathbf u$ is aligned with the gradient (assuming $\nabla f\ne0$). Thus the maximum directional derivative is $\|\nabla f\|$.

At a stationary point where $\nabla f=0$, all first-order directional derivatives vanish, but this alone does not tell us whether the point is a minimum, maximum, or saddle.

### Level sets and tangent planes

A **level set** in two dimensions is $f(x,y)=c$. Along a path $\mathbf r(t)$ staying on the level set,

$$
0=\frac d{dt}f(\mathbf r(t))
=\nabla f(\mathbf r(t))\cdot\mathbf r'(t).
$$

Therefore $\nabla f$ is perpendicular to the tangent direction of a regular level curve.

For a surface $z=f(x,y)$, the tangent plane at $(a,b,f(a,b))$ is

$$
z=f(a,b)+f_x(a,b)(x-a)+f_y(a,b)(y-b).
$$

This is the multivariable version of single-variable linearization.

### The Jacobian matrix

For a vector-valued map $\mathbf F:\mathbb R^n\to\mathbb R^m$ with components $F_1,\ldots,F_m$, its Jacobian is the $m\times n$ matrix

$$
\boxed{
J_{\mathbf F}=
\begin{pmatrix}
\partial F_1/\partial x_1&\cdots&\partial F_1/\partial x_n\\
\vdots&&\vdots\\
\partial F_m/\partial x_1&\cdots&\partial F_m/\partial x_n
\end{pmatrix}
}.
$$

Rows correspond to outputs, columns to inputs. The Jacobian is the best local **linear transformation**:

$$
\mathbf F(\mathbf x+\mathbf h)
=\mathbf F(\mathbf x)+J_{\mathbf F}(\mathbf x)\mathbf h+o(\|\mathbf h\|).
$$

**Example:** Let

$$
\mathbf F(x,y)=(x^2-y^2,\ 2xy).
$$

Then

$$
J_{\mathbf F}=
\begin{pmatrix}
2x&-2y\\
2y&2x
\end{pmatrix},
\qquad
\det J_{\mathbf F}=4(x^2+y^2).
$$

Its determinant is nonzero except at the origin, so the map is locally invertible away from zero by the inverse function theorem. This does **not** mean the map is globally one-to-one.

### Multivariable chain rule in matrix form

For $\mathbf G:\mathbb R^k\to\mathbb R^n$ and $\mathbf F:\mathbb R^n\to\mathbb R^m$,

$$
\boxed{J_{\mathbf F\circ\mathbf G}
=J_{\mathbf F}(\mathbf G(\mathbf x))J_{\mathbf G}(\mathbf x)}.
$$

The order of matrix multiplication matters: the derivative of the **outer map** is multiplied by the derivative of the **inner map**.

In machine learning, repeated application of this rule is the core of **backpropagation**.

### The Hessian matrix

For scalar $f:\mathbb R^n\to\mathbb R$, the Hessian collects second partial derivatives:

$$
\boxed{
H_f=
\begin{pmatrix}
f_{x_1x_1}&\cdots&f_{x_1x_n}\\
\vdots&&\vdots\\
f_{x_nx_1}&\cdots&f_{x_nx_n}
\end{pmatrix}
}.
$$

For a $C^2$ function the Hessian is symmetric, by equality of mixed partial derivatives.

**Example:** $f(x,y)=x^2+xy+2y^2$:

$$
H_f=
\begin{pmatrix}
2&1\\
1&4
\end{pmatrix}.
$$

Since $2>0$ and $\det H_f=8-1=7>0$, this Hessian is **positive definite**. Thus the quadratic function is strictly convex and its only stationary point, $(0,0)$, is its unique global minimum.

### Second-order Taylor approximation in multiple variables

For twice continuously differentiable $f$ and a small vector increment $\mathbf h$:

$$
f(\mathbf x+\mathbf h)
=f(\mathbf x)+\nabla f(\mathbf x)^\top\mathbf h
+\frac12\mathbf h^\top H_f(\mathbf x)\mathbf h
+o(\|\mathbf h\|^2).
$$

The gradient describes first-order change; the quadratic form $\mathbf h^\top H\mathbf h$ describes local curvature.

### Implicit differentiation with several variables

If $F(x,y,z)=0$ defines $z=z(x,y)$ locally and $F_z\ne0$, then

$$
\boxed{z_x=-\frac{F_x}{F_z},\qquad z_y=-\frac{F_y}{F_z}}.
$$

For the sphere $F=x^2+y^2+z^2-R^2=0$:

$$
z_x=-\frac{x}{z},\qquad z_y=-\frac{y}{z}
$$

where $z\ne0$. This describes local height slopes of a spherical surface.

---

## 16. Multivariable optimization and Lagrange multipliers

### Unconstrained stationary points

For differentiable $f(x,y)$, an interior local extremum must satisfy

$$
\nabla f(x,y)=\mathbf0.
$$

This is necessary but generally not sufficient.

**Example:** $f(x,y)=x^2-y^2$ has gradient $(2x,-2y)$, which vanishes at $(0,0)$. But along $y=0$, $f=x^2\ge0$; along $x=0$, $f=-y^2\le0$. The origin is a **saddle**, not a maximum or minimum.

### Second-derivative test in two dimensions

At a stationary point, let

$$
D=f_{xx}f_{yy}-(f_{xy})^2=\det H_f.
$$

| Test | Classification |
|---|---|
| $D>0$ and $f_{xx}>0$ | Strict local minimum |
| $D>0$ and $f_{xx}<0$ | Strict local maximum |
| $D<0$ | Saddle point |
| $D=0$ | Inconclusive |

In higher dimensions, look at the **eigenvalues of the symmetric Hessian**:

- All positive: positive definite, strict local minimum.
- All negative: negative definite, strict local maximum.
- Mixed positive and negative: indefinite, saddle.
- Any zero eigenvalues: the second-order test may be inconclusive.

### Constrained optimization: the geometric idea

Suppose we want to optimize $f(x,y)$ subject to the equality constraint $g(x,y)=c$.

At a regular constrained extremum, feasible motion is tangent to the constraint curve. Since the objective cannot improve to first order along those tangent directions, $\nabla f$ must be **normal** to the constraint.

But $\nabla g$ is also normal to the constraint. The two gradients must therefore be parallel:

$$
\boxed{\nabla f=\lambda\nabla g}.
$$

This is the method of **Lagrange multipliers**. The scalar $\lambda$ is a multiplier describing the local sensitivity of the optimum to a constraint relaxation under suitable regularity.

### Worked Lagrange-multiplier example

Maximize and minimize $f(x,y)=xy$ on the unit circle $x^2+y^2=1$.

Set $g(x,y)=x^2+y^2$ and solve

$$
\begin{cases}
y=2\lambda x,\\
x=2\lambda y,\\
x^2+y^2=1.
\end{cases}
$$

Since $x$ and $y$ cannot both be zero, multiply the first two equations to obtain $xy=4\lambda^2xy$. More directly, the equations imply $x^2=y^2$, so $y=\pm x$.

- If $y=x$, then $2x^2=1$, and $xy=+1/2$.
- If $y=-x$, then $2x^2=1$, and $xy=-1/2$.

Thus:

$$
\boxed{\max xy=\frac12,\qquad \min xy=-\frac12}.
$$

The circle is compact and $xy$ is continuous, so these extrema exist; the candidate comparison identifies them.

**Independent verification:** from $(x-y)^2\ge0$ and $x^2+y^2=1$,

$$
1-2xy\ge0\quad\Rightarrow\quad xy\le\frac12.
$$

Similarly $(x+y)^2\ge0$ implies $xy\ge-1/2$. Equality is attainable.

### Multiple constraints

For equality constraints $g_1(\mathbf x)=c_1,\ldots,g_k(\mathbf x)=c_k$ and sufficiently regular independent constraint gradients:

$$
\nabla f=\lambda_1\nabla g_1+\cdots+\lambda_k\nabla g_k.
$$

Inequality-constrained optimization leads to **Karush–Kuhn–Tucker (KKT)** conditions, incorporating feasibility, multiplier signs, and complementary slackness. KKT conditions require appropriate constraint qualifications; they are not automatically sufficient without additional assumptions such as convexity.

### Convex optimization and global guarantees

For a differentiable convex function on a convex domain, any stationary point in the interior is a **global minimum**.

Proof sketch: convexity gives

$$
f(y)\ge f(x)+\nabla f(x)^\top(y-x).
$$

If $\nabla f(x)=0$, then $f(y)\ge f(x)$ for all feasible $y$.

This explains why optimization over convex objectives is especially tractable: local minima do not hide worse-than-global solutions.

### Gradient descent and Newton's method

**Gradient descent:**

$$
\mathbf x_{k+1}=\mathbf x_k-\eta\nabla f(\mathbf x_k).
$$

The step moves opposite the steepest-ascent direction. Step size $\eta$ matters: too large can overshoot or diverge; too small can converge slowly.

**Newton's method for optimization** uses local quadratic curvature:

$$
\mathbf x_{k+1}
=\mathbf x_k-H_f(\mathbf x_k)^{-1}\nabla f(\mathbf x_k),
$$

assuming the Hessian is invertible. In practice, Newton steps may need damping or safeguards, especially away from convex regions.

---

## 17. Multiple integrals and coordinate transformations

### Double integrals

A double integral accumulates values over a two-dimensional region $D$:

$$
\iint_D f(x,y)\,dA.
$$

Interpretations include:

- Volume beneath $z=f(x,y)$ when $f\ge0$.
- Mass of a thin plate with surface density $f(x,y)$.
- Probability over a region if $f$ is a joint probability density.

**Fubini's theorem** permits an appropriate double integral to be evaluated as iterated one-dimensional integrals (for example, for continuous functions on rectangles):

$$
\int_a^b\int_c^d f(x,y)\,dy\,dx.
$$

For a nonrectangular domain, the inner integration bounds may depend on the outer variable.

### Example: a triangular region

Let $D=\{(x,y):0\le x\le1,\ 0\le y\le x\}$. Then

$$
\begin{aligned}
\iint_D(x+y)\,dA
&=\int_0^1\int_0^x(x+y)\,dy\,dx\\
&=\int_0^1\left(x^2+\frac{x^2}{2}\right)\,dx\\
&=\frac32\cdot\frac13=\frac12.
\end{aligned}
$$

If the integration order is reversed, the same region becomes $0\le y\le1$ and $y\le x\le1$:

$$
\int_0^1\int_y^1(x+y)\,dx\,dy=\frac12.
$$

Changing integration order is often the key to simplifying a difficult domain.

### Why changing coordinates introduces a Jacobian

For a differentiable transformation $(u,v)\mapsto(x(u,v),y(u,v))$, a tiny rectangle of side lengths $du,dv$ becomes approximately a parallelogram.

Its area is scaled by the absolute determinant of the local linear transformation:

$$
\boxed{
dA=\left|\det\frac{\partial(x,y)}{\partial(u,v)}\right|\,du\,dv
}.
$$

The determinant represents **local area scaling**; in three dimensions it represents volume scaling.

### Polar-coordinate Jacobian — derived

With $x=r\cos\theta$, $y=r\sin\theta$,

$$
J=
\begin{pmatrix}
\cos\theta&-r\sin\theta\\
\sin\theta&r\cos\theta
\end{pmatrix}.
$$

Its determinant is

$$
\det J=r(\cos^2\theta+\sin^2\theta)=r.
$$

Therefore:

$$
\boxed{dA=r\,dr\,d\theta}.
$$

**Common mistake:** forgetting the factor $r$ when converting a double integral to polar coordinates.

### Polar example: integrate over a disk

Over the disk $x^2+y^2\le R^2$, calculate $\iint_D(x^2+y^2)\,dA$:

$$
\begin{aligned}
\iint_D(x^2+y^2)\,dA
&=\int_0^{2\pi}\int_0^R r^2\cdot r\,dr\,d\theta\\
&=\int_0^{2\pi}\frac{R^4}{4}\,d\theta\\
&=\frac{\pi R^4}{2}.
\end{aligned}
$$

### Triple integrals

A triple integral accumulates throughout a volume:

$$
\iiint_V f(x,y,z)\,dV.
$$

For density $\rho(x,y,z)$, total mass is $M=\iiint_V\rho\,dV$.

| Coordinates | Transformation | Volume element |
|---|---|---|
| Cartesian | $(x,y,z)$ | $dx\,dy\,dz$ |
| Cylindrical | $x=r\cos\theta$, $y=r\sin\theta$, $z=z$ | $r\,dr\,d\theta\,dz$ |
| Spherical | $x=\rho\sin\phi\cos\theta$, $y=\rho\sin\phi\sin\theta$, $z=\rho\cos\phi$ | $\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$ |

Here $\phi$ is measured downward from the positive $z$-axis; other textbooks sometimes swap the roles of $\phi$ and $\theta$.

### Recovering the volume of a sphere

For a sphere of radius $R$:

$$
\begin{aligned}
V
&=\int_0^{2\pi}\int_0^\pi\int_0^R
\rho^2\sin\phi\,d\rho\,d\phi\,d\theta\\
&=\left(2\pi\right)\left(2\right)\left(\frac{R^3}{3}\right)
=\frac{4\pi R^3}{3}.
\end{aligned}
$$

---

## 18. Vector calculus: fields, circulation, and flux

### Scalar fields and vector fields

A **scalar field** assigns one number to each location, such as temperature $T(x,y,z)$.

A **vector field** assigns a vector to each location, such as fluid velocity $\mathbf F(x,y,z)=(P,Q,R)$.

The operators gradient, divergence, and curl encode different aspects of spatial change:

| Operator | Input | Output | Interpretation |
|---|---|---|---|
| Gradient $\nabla f$ | Scalar field | Vector field | Direction and magnitude of steepest increase |
| Divergence $\nabla\cdot\mathbf F$ | Vector field | Scalar field | Local net outward flux density |
| Curl $\nabla\times\mathbf F$ | 3D vector field | Vector field | Local rotational tendency |
| Laplacian $\nabla^2f$ | Scalar field | Scalar field | Sum of second spatial derivatives |

In Cartesian coordinates:

$$
\nabla\cdot\mathbf F=P_x+Q_y+R_z.
$$

$$
\nabla\times\mathbf F=
\begin{pmatrix}
R_y-Q_z\\
P_z-R_x\\
Q_x-P_y
\end{pmatrix}.
$$

$$
\nabla^2f=f_{xx}+f_{yy}+f_{zz}.
$$

### Divergence versus curl: a physical interpretation

- Positive **divergence**: the field behaves locally like a source, with more outward than inward flux through a tiny volume.
- Negative divergence: local sink-like behaviour.
- Nonzero **curl**: local circulation or spinning tendency.

A vector field can have zero divergence and nonzero curl, or vice versa.

### Line integrals

For a scalar field $f$ along a curve $C$, the arc-length integral is

$$
\int_C f\,ds
=\int_a^b f(\mathbf r(t))\|\mathbf r'(t)\|\,dt.
$$

For a vector field $\mathbf F$, the circulation/work integral is

$$
\int_C\mathbf F\cdot d\mathbf r
=\int_a^b\mathbf F(\mathbf r(t))\cdot\mathbf r'(t)\,dt.
$$

The two integrals have different meanings: the scalar integral weights path length, while the vector integral accounts for the **direction** of travel.

### Conservative fields and potential functions

If $\mathbf F=\nabla\phi$ for a potential function $\phi$, then along a path from $A$ to $B$,

$$
\int_C\mathbf F\cdot d\mathbf r=\phi(B)-\phi(A).
$$

Hence the integral is path-independent, and the integral around any closed loop is zero. On suitable simply connected domains, a continuously differentiable vector field with zero curl is conservative; domain topology matters.

### Green's theorem — plane circulation and area

For a positively oriented simple closed curve $C$ bounding a suitable planar region $D$:

$$
\boxed{
\oint_C P\,dx+Q\,dy
=\iint_D(Q_x-P_y)\,dA
}.
$$

This relates circulation around the **boundary** to curl throughout the **interior**.

**Worked example:** take $\mathbf F=(-y,x)$ around the unit circle counterclockwise.

Parameterize $C$ by $\mathbf r(t)=(\cos t,\sin t)$, $0\le t\le2\pi$:

$$
\mathbf F(\mathbf r(t))=(-\sin t,\cos t),
\qquad \mathbf r'(t)=(-\sin t,\cos t).
$$

Therefore $\mathbf F\cdot\mathbf r'=1$ and the circulation is $2\pi$.

By Green's theorem, $Q_x-P_y=1-(-1)=2$, and

$$
\iint_D2\,dA=2\pi,
$$

matching the direct calculation.

### Stokes' theorem — circulation in three dimensions

For a surface $S$ with boundary $C$ and compatible orientations:

$$
\boxed{
\oint_C\mathbf F\cdot d\mathbf r
=\iint_S(\nabla\times\mathbf F)\cdot\mathbf n\,dS
}.
$$

Stokes generalizes Green's theorem: circulation around a boundary equals curl flux through any suitable spanning surface.

### Divergence theorem — flux through a closed surface

For a solid volume $V$ with outward-oriented boundary surface $\partial V$:

$$
\boxed{
\iint_{\partial V}\mathbf F\cdot\mathbf n\,dS
=\iiint_V\nabla\cdot\mathbf F\,dV
}.
$$

**Example:** $\mathbf F=(x,y,z)$ and $V$ is the unit ball. Since $\nabla\cdot\mathbf F=3$,

$$
\iiint_V3\,dV
=3\left(\frac{4\pi}{3}\right)=4\pi.
$$

The outward flux across the unit sphere is therefore $4\pi$. This can also be seen directly: on the unit sphere, $\mathbf F=\mathbf n$, so $\mathbf F\cdot\mathbf n=1$, and the sphere's area is $4\pi$.

### The common structure

The three great integral theorems are versions of a single organizing principle: **accumulated local derivatives over an interior correspond to a quantity measured on its boundary**.

- Fundamental Theorem of Calculus: derivative on an interval ↔ endpoint values.
- Green: planar curl over a region ↔ circulation around its boundary.
- Stokes: surface curl flux ↔ circulation around its boundary.
- Divergence: divergence in a volume ↔ flux through its closed boundary.

---

# Part III — Differential equations and related mathematics

## 19. Ordinary differential equations (ODEs)

### What is a differential equation?

A differential equation relates an unknown function to one or more of its derivatives.

An **ordinary differential equation** has derivatives with respect to a single independent variable:

$$
\frac{dy}{dt}=ky
$$

or

$$
y''+4y=0.
$$

The **order** is the highest derivative appearing. The first equation is first order, the second is second order.

An **initial-value problem (IVP)** specifies the ODE and values such as $y(0)=y_0$, or for a second-order equation, $y(0)$ and $y'(0)$. A **boundary-value problem** specifies conditions at different points, such as $y(0)=0$ and $y(L)=1$.

### Separable differential equations

An ODE of the form

$$
\frac{dy}{dx}=g(x)h(y)
$$

can be separated (where $h(y)\ne0$):

$$
\frac{dy}{h(y)}=g(x)\,dx.
$$

Integrate both sides, then solve for $y$ if possible.

**Exponential growth / decay derivation:**

$$
\frac{dy}{dt}=ky.
$$

For $y\ne0$:

$$
\frac{dy}{y}=k\,dt
\quad\Rightarrow\quad
\ln|y|=kt+C.
$$

Exponentiation yields

$$
\boxed{y(t)=Ce^{kt}},
$$

where allowing $C=0$ restores the equilibrium solution omitted when dividing by $y$.

- $k>0$: exponential growth.
- $k<0$: exponential decay.
- Half-life for decay: $t_{1/2}=\ln2/|k|$.

### Logistic equation — a nonlinear separable ODE

$$
\frac{dP}{dt}=rP\left(1-\frac PK\right),
$$

where $r>0$ is the intrinsic rate and $K>0$ is carrying capacity.

For a non-equilibrium solution with $P\ne0,K$, separate:

$$
\frac{dP}{P(1-P/K)}=r\,dt.
$$

Since

$$
\frac1{P(1-P/K)}
=\frac1P+\frac1{K-P},
$$

integrating (remember the minus sign from $d(K-P)=-dP$) gives

$$
\ln|P|-\ln|K-P|=rt+C.
$$

Solving:

$$
\boxed{P(t)=\frac{K}{1+A e^{-rt}}}
$$

with $A=K/P(0)-1$ for a positive initial population. The equilibrium solutions $P\equiv0$ and $P\equiv K$ should be checked separately.

At small $P$ relative to $K$, growth is approximately exponential. As $P\to K$, the growth rate approaches zero.

### First-order linear ODEs and integrating factors

The standard form is

$$
y'+p(x)y=q(x).
$$

We want to make the left side the derivative of a product. Multiply by an unknown factor $\mu(x)$:

$$
\mu y'+\mu p y=\mu q.
$$

But $(\mu y)'=\mu y'+\mu' y$, so require $\mu'=\mu p$. Therefore

$$
\frac{\mu'}{\mu}=p
\quad\Rightarrow\quad
\boxed{\mu(x)=e^{\int p(x)\,dx}}.
$$

Then

$$
(\mu y)'=\mu q,
\qquad
\boxed{y=\frac{\int\mu q\,dx+C}{\mu}}.
$$

**Example:** solve $y'+2y=6$.

Here $\mu=e^{2x}$. Hence

$$
(e^{2x}y)'=6e^{2x},
$$

$$
e^{2x}y=3e^{2x}+C,
\quad
\boxed{y=3+Ce^{-2x}}.
$$

The solution approaches the equilibrium value 3 as $x\to\infty$.

### Exact differential equations

An equation

$$
M(x,y)\,dx+N(x,y)\,dy=0
$$

is **exact** if there is a potential $\Phi$ satisfying $\Phi_x=M$ and $\Phi_y=N$. Then its solutions lie on level curves $\Phi(x,y)=C$.

On a simply connected region, if the functions and partials are sufficiently smooth, $M_y=N_x$ is a criterion for exactness.

Example:

$$
(2xy+1)\,dx+x^2\,dy=0.
$$

Since $M_y=2x=N_x$, integrate $M$ with respect to $x$:

$$
\Phi(x,y)=x^2y+x+h(y).
$$

Match $\Phi_y=x^2+h'(y)$ to $N=x^2$, giving $h'(y)=0$. Thus

$$
\boxed{x^2y+x=C}.
$$

### Second-order linear ODEs with constant coefficients

Consider

$$
a y''+b y'+c y=0\qquad(a\ne0).
$$

Try an exponential solution $y=e^{rx}$. Substitution gives

$$
(ar^2+br+c)e^{rx}=0.
$$

Since $e^{rx}\ne0$, the **characteristic equation** is

$$
\boxed{ar^2+br+c=0}.
$$

| Roots | General real solution |
|---|---|
| Distinct real $r_1,r_2$ | $C_1e^{r_1x}+C_2e^{r_2x}$ |
| Repeated real $r$ | $(C_1+C_2x)e^{rx}$ |
| Complex $\alpha\pm i\beta$ | $e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)$ |

**Why a repeated root needs $xe^{rx}$:** One exponential provides only one independent solution; the reduction-of-order method supplies a second independent solution proportional to $xe^{rx}$.

### Harmonic oscillator

An undamped spring–mass system satisfies

$$
m y''+ky=0.
$$

Let $\omega=\sqrt{k/m}$. The characteristic roots are $\pm i\omega$, so

$$
\boxed{y(t)=A\cos(\omega t)+B\sin(\omega t)}.
$$

The amplitude and phase are determined by initial displacement and velocity.

With damping $c y'$ added, $m y''+c y'+ky=0$ can be underdamped, critically damped, or overdamped depending on the sign of $c^2-4mk$.

### Nonhomogeneous equations and resonance

For

$$
a y''+b y'+cy=g(x),
$$

the general solution is

$$
y=y_{\mathrm{homogeneous}}+y_{\mathrm{particular}}.
$$

**Example:** $y''+y=\sin x$. Since $\sin x$ already solves the homogeneous equation, a particular solution proportional just to $\sin x$ cannot work. Try $y_p=Ax\cos x$:

$$
(Ax\cos x)''+Ax\cos x=-2A\sin x.
$$

Choosing $A=-1/2$ gives

$$
y=C_1\cos x+C_2\sin x-\frac x2\cos x.
$$

The extra $x$ factor is the algebraic signal of **resonance**.

### Existence and uniqueness: why an ODE may have many solutions

For $y'=F(t,y)$ and $y(t_0)=y_0$, continuity of $F$ and a local Lipschitz condition in $y$ give a locally unique solution (Picard–Lindelöf theorem).

Without uniqueness hypotheses, multiple solutions may share one initial value.

Example for $y\ge0$:

$$
y'=2\sqrt{y},\qquad y(0)=0.
$$

Both $y\equiv0$ and $y=t^2$ for $t\ge0$ satisfy the differential equation and the same initial condition; delayed-start solutions also exist. Thus specifying an initial value does not *always* ensure uniqueness.

---

## 20. Partial differential equations (PDEs)

### From partial derivatives to PDEs

A PDE relates a function of **two or more independent variables** to its partial derivatives.

For a spatially varying temperature $u(x,t)$:

- $u_t=\partial u/\partial t$ measures change with time at fixed position.
- $u_x=\partial u/\partial x$ measures spatial gradient at fixed time.
- $u_{xx}=\partial^2u/\partial x^2$ measures spatial curvature.

The simplest classical PDEs:

| Equation | Model | Meaning |
|---|---|---|
| $u_t=\alpha u_{xx}$ | Heat equation | Diffusion / smoothing |
| $u_{tt}=c^2u_{xx}$ | Wave equation | Propagation / oscillation |
| $u_{xx}+u_{yy}=0$ | Laplace equation | Steady-state potential / equilibrium |
| $u_{xx}+u_{yy}=f(x,y)$ | Poisson equation | Potential with a source term |
| $u_t+cu_x=0$ | Transport / advection equation | Profile translating at speed $c$ |

Classical second-order linear PDEs are often categorized as **elliptic** (Laplace), **parabolic** (heat), or **hyperbolic** (wave). These labels reflect structural properties of their highest-order derivatives and the qualitative phenomena they model.

### Order, linearity, and coefficients

The **order** of a PDE is its highest derivative order.

- $u_t+cu_x=0$ is first order.
- $u_t=\alpha u_{xx}$ is second order because of $u_{xx}$.
- $u_t=\alpha u_{xx}$ is linear in $u$ and its derivatives.
- $u_t=uu_x$ is nonlinear because it multiplies the unknown $u$ by a derivative of itself.

For a second-order PDE in two spatial variables written as

$$
A u_{xx}+2B u_{xy}+C u_{yy}+\text{lower-order terms}=0,
$$

the sign of $B^2-AC$ (under nondegeneracy assumptions) identifies an elliptic ($<0$), parabolic ($=0$), or hyperbolic ($>0$) principal part. The time-dependent heat equation is a standard parabolic evolution equation, not merely a two-spatial-variable equation of this form.

### Deriving the heat equation from conservation

Consider a thin uniform rod. Let

- $u(x,t)$ = temperature,
- $\rho$ = mass density,
- $c_p$ = specific heat capacity,
- $k$ = thermal conductivity,
- $q(x,t)$ = heat flux per unit cross-sectional area.

**Fourier's law** says that heat flows from hotter regions toward colder regions:

$$
q=-k\,u_x.
$$

For a short rod segment $[x,x+\Delta x]$ of cross-sectional area $A$, stored thermal energy is approximately $\rho c_p A\Delta x\,u$. Energy conservation gives

$$
\rho c_p A\Delta x\,u_t
=Aq(x,t)-Aq(x+\Delta x,t).
$$

Divide by $A\Delta x$ and take $\Delta x\to0$:

$$
\rho c_p u_t=-q_x.
$$

With constant $k$ and $q=-ku_x$:

$$
\rho c_p u_t=ku_{xx}.
$$

Define **thermal diffusivity** $\alpha=k/(\rho c_p)$:

$$
\boxed{u_t=\alpha u_{xx}}.
$$

This derivation requires simplifying assumptions: one-dimensional conduction, uniform material properties, and no internal heat sources.

**With varying conductivity** $k(x)$, the correct form is $\rho c_p u_t=\partial_x(k(x)u_x)$, not simply $k(x)u_{xx}$; the product rule creates an additional term.

### Heat equation: boundary and initial conditions

A PDE alone usually does not specify a unique physical solution. For a rod $0<x<L$, we may prescribe:

- **Initial condition:** $u(x,0)=f(x)$, the starting temperature profile.
- **Dirichlet boundary conditions:** $u(0,t)=u(L,t)=0$, fixed endpoint temperatures.
- **Neumann conditions:** $u_x(0,t)=u_x(L,t)=0$, zero heat flux at the endpoints.
- **Robin conditions:** combinations such as $u_x+h u=0$, modeling heat exchange with surroundings.

The number and type of conditions depend on the PDE and domain. For example, a second-order-in-time wave equation generally needs **both** initial displacement and initial velocity.

### Separation of variables: a full worked heat-equation derivation

Solve

$$
u_t=\alpha u_{xx},\quad0<x<L,\ t>0,
$$

with $u(0,t)=u(L,t)=0$.

**Step 1 — try a product solution.**

Assume $u(x,t)=X(x)T(t)$. Substitute:

$$
X(x)T'(t)=\alpha X''(x)T(t).
$$

Divide wherever $XT\ne0$:

$$
\frac{T'}{\alpha T}=\frac{X''}{X}.
$$

The left side depends only on $t$; the right depends only on $x$. For the equality to hold for all $x,t$, each side must equal the **same constant**. Choose $-\lambda$:

$$
X''+\lambda X=0,\qquad T'+\alpha\lambda T=0.
$$

**Step 2 — apply endpoint conditions.**

$X(0)=X(L)=0$. Nonzero solutions exist for the discrete eigenvalues

$$
\lambda_n=\left(\frac{n\pi}{L}\right)^2,\qquad n=1,2,3,\ldots
$$

with eigenfunctions

$$
X_n(x)=\sin\left(\frac{n\pi x}{L}\right).
$$

**Step 3 — solve the time equation.**

$$
T_n(t)=e^{-\alpha\lambda_n t}
=e^{-\alpha(n\pi/L)^2t}.
$$

**Step 4 — combine modes.**

Each separated solution has the form

$$
u_n(x,t)=A_n\sin\left(\frac{n\pi x}{L}\right)
e^{-\alpha(n\pi/L)^2t}.
$$

By linearity, appropriate sums of modes are also solutions:

$$
\boxed{
u(x,t)=\sum_{n=1}^{\infty}b_n
\sin\left(\frac{n\pi x}{L}\right)
e^{-\alpha(n\pi/L)^2t}
}.
$$

The initial profile $f(x)=u(x,0)$ determines the Fourier sine coefficients

$$
b_n=\frac2L\int_0^L f(x)\sin\left(\frac{n\pi x}{L}\right)\,dx.
$$

**Interpretation:** each spatial pattern decays exponentially, and higher-frequency modes decay faster because the exponent contains $n^2$. Heat diffusion smooths fine-scale variation rapidly.

### Single-mode heat equation example

If the initial temperature is already one sine mode,

$$
u(x,0)=\sin(\pi x/L),
$$

the solution is simply

$$
\boxed{
u(x,t)=\sin(\pi x/L)\,e^{-\alpha\pi^2t/L^2}
}.
$$

Check directly:

$$
u_t=-\frac{\alpha\pi^2}{L^2}u,
\qquad
u_{xx}=-\frac{\pi^2}{L^2}u,
$$

so indeed $u_t=\alpha u_{xx}$. It satisfies both endpoint conditions and the prescribed initial profile.

### Deriving the wave equation

For a taut string with tension $T$ and mass per unit length $\mu$, let $u(x,t)$ be its small transverse displacement.

Over a short segment of length $\Delta x$, the net transverse tension force is approximately

$$
T\,[u_x(x+\Delta x,t)-u_x(x,t)]
\approx T\,u_{xx}\Delta x.
$$

Newton's law says mass $\mu\Delta x$ times transverse acceleration $u_{tt}$ equals this force:

$$
\mu\Delta x\,u_{tt}=T\,u_{xx}\Delta x.
$$

Cancel $\Delta x$ and define $c^2=T/\mu$:

$$
\boxed{u_{tt}=c^2u_{xx}}.
$$

This derivation assumes small transverse slopes and approximately constant tension.

### Travelling-wave solutions

Both

$$
u(x,t)=f(x-ct)
\qquad\text{and}\qquad
u(x,t)=g(x+ct)
$$

solve the one-dimensional wave equation for sufficiently smooth $f,g$.

**Why:** for $u=f(x-ct)$, the chain rule gives $u_{tt}=c^2f''(x-ct)$ and $u_{xx}=f''(x-ct)$.

Thus profiles can propagate to the right or left without changing shape in the idealized model.

For a fixed string, separated solutions have spatial sine modes and oscillatory time factors:

$$
u_n(x,t)=\sin(n\pi x/L)
\left[A_n\cos(cn\pi t/L)+B_n\sin(cn\pi t/L)\right].
$$

**Heat versus wave:** heat modes decay; ideal wave modes oscillate.

### Laplace's equation and steady state

For constant thermal diffusivity and no sources, a time-independent heat profile satisfies $u_t=0$. Thus

$$
\boxed{u_{xx}=0}
$$

in one spatial dimension, or

$$
\boxed{u_{xx}+u_{yy}=0}
$$

in two dimensions. The latter is **Laplace's equation**.

Solutions are called **harmonic functions**. They satisfy striking properties such as the mean-value property: for suitable interior disks, a harmonic function's value at the center equals its average over the boundary circle.

### Advection versus diffusion

**Pure transport:**

$$
u_t+cu_x=0
\quad\Rightarrow\quad
u(x,t)=f(x-ct).
$$

The profile translates without smoothing.

**Pure diffusion:**

$$
u_t=\alpha u_{xx}.
$$

The profile smooths over time.

**Advection–diffusion:**

$$
u_t+cu_x=\alpha u_{xx}
$$

combines transport and smoothing. Similar equations arise in contaminant transport, fluid dynamics, and population models.

### Fourier series and orthogonality

The separated sine modes are orthogonal on $[0,L]$:

$$
\int_0^L
\sin\left(\frac{m\pi x}{L}\right)
\sin\left(\frac{n\pi x}{L}\right)\,dx
=\begin{cases}
0,&m\ne n,\\
L/2,&m=n.
\end{cases}
$$

This is why multiplying a Fourier sine series by one basis function and integrating isolates its coefficient.

Conceptually, a Fourier series is a decomposition into **orthogonal oscillatory patterns**, analogous to resolving a vector into components along orthogonal axes.

### PDEs beyond the introductory examples

| PDE / equation family | Common application |
|---|---|
| Navier–Stokes | Fluid motion, nonlinear conservation of momentum |
| Schrödinger | Quantum mechanical evolution |
| Black–Scholes | Option-pricing model under its assumptions |
| Reaction–diffusion | Chemical reactions, biological pattern formation |
| Maxwell's equations | Electromagnetic fields |
| Poisson / Laplace | Electrostatic and gravitational potentials |

These models often require additional mathematics—functional analysis, numerical discretization, boundary conditions, and sometimes weak/distributional solutions—because classical smooth solutions may not always exist.

---

## 21. Linear algebra and matrix calculus connections

### Vectors, dot products, and norms

For $\mathbf x,\mathbf y\in\mathbb R^n$:

$$
\mathbf x\cdot\mathbf y
=\sum_{i=1}^n x_i y_i,
\qquad
\|\mathbf x\|_2=\sqrt{\sum_{i=1}^n x_i^2}.
$$

The dot product measures alignment; the Euclidean norm measures length.

$$
\mathbf x\cdot\mathbf y
=\|\mathbf x\|\|\mathbf y\|\cos\theta.
$$

**Cauchy–Schwarz inequality:**

$$
|\mathbf x\cdot\mathbf y|\le\|\mathbf x\|\,\|\mathbf y\|.
$$

One proof considers the nonnegative quadratic $\|\mathbf x-t\mathbf y\|^2\ge0$ for every real $t$. Its discriminant must be nonpositive, giving $(\mathbf x\cdot\mathbf y)^2\le\|\mathbf x\|^2\|\mathbf y\|^2$.

This inequality also explains why Pearson correlation cannot exceed 1 in absolute value.

### Matrix multiplication as composition of linear maps

If $A:\mathbb R^n\to\mathbb R^m$ and $B:\mathbb R^k\to\mathbb R^n$, then

$$
A(B\mathbf x)=(AB)\mathbf x.
$$

The product $AB$ represents **first applying $B$, then $A$**. In general $AB\ne BA$.

The transpose $A^\top$ reverses the dimensions and satisfies $(AB)^\top=B^\top A^\top$.

### Eigenvalues and eigenvectors

An eigenvector $\mathbf v\ne0$ satisfies

$$
A\mathbf v=\lambda\mathbf v.
$$

The transformation scales $\mathbf v$ without changing its direction (up to sign).

The characteristic equation $\det(A-\lambda I)=0$ determines eigenvalues.

For

$$
A=
\begin{pmatrix}
2&0\\
0&5
\end{pmatrix},
$$

the coordinate-axis vectors are eigenvectors with eigenvalues 2 and 5.

For real symmetric matrices, the spectral theorem guarantees an orthonormal eigenbasis and real eigenvalues.

### Quadratic forms, Hessians, and definiteness

A quadratic form is

$$
q(\mathbf x)=\mathbf x^\top A\mathbf x.
$$

Only the symmetric part $(A+A^\top)/2$ affects this scalar value.

If $A$ is symmetric:

| Eigenvalues of $A$ | Quadratic form | Meaning |
|---|---|---|
| All $>0$ | $\mathbf x^\top A\mathbf x>0$ for $\mathbf x\ne0$ | Positive definite |
| All $\ge0$ | $\mathbf x^\top A\mathbf x\ge0$ | Positive semidefinite |
| All $<0$ | Strictly negative away from zero | Negative definite |
| Mixed signs | Can be positive or negative | Indefinite |

At a stationary point of a smooth function, the Hessian quadratic form captures second-order curvature in every direction.

### Matrix derivatives

Let $f(\mathbf x)=\mathbf b^\top\mathbf x$. Then

$$
\nabla_{\mathbf x}f=\mathbf b.
$$

For $q(\mathbf x)=\mathbf x^\top A\mathbf x$:

$$
\boxed{\nabla_{\mathbf x}q=(A+A^\top)\mathbf x}.
$$

If $A$ is symmetric, this simplifies to $2A\mathbf x$.

**Derivation in components:**

$$
q=\sum_{i,j}x_iA_{ij}x_j.
$$

Differentiate with respect to $x_k$. Terms where $i=k$ contribute $\sum_j A_{kj}x_j$; terms where $j=k$ contribute $\sum_i x_iA_{ik}$. Combining yields the $k$th entry of $(A+A^\top)\mathbf x$.

### Deriving ordinary least squares

Given a design matrix $X\in\mathbb R^{n\times p}$ and target $\mathbf y$, minimize

$$
L(\boldsymbol\beta)=\|X\boldsymbol\beta-\mathbf y\|_2^2.
$$

Expand:

$$
L=\boldsymbol\beta^\top X^\top X\boldsymbol\beta
-2\mathbf y^\top X\boldsymbol\beta+\mathbf y^\top\mathbf y.
$$

Differentiate:

$$
\nabla_\beta L=2X^\top X\boldsymbol\beta-2X^\top\mathbf y.
$$

Setting the gradient to zero yields the **normal equations**:

$$
\boxed{X^\top X\boldsymbol\beta=X^\top\mathbf y}.
$$

If $X$ has full column rank, $X^\top X$ is invertible and

$$
\boldsymbol\beta=(X^\top X)^{-1}X^\top\mathbf y.
$$

In numerical computation, solving via QR or SVD is generally preferable to explicitly forming the inverse; it is more stable, especially when the columns are nearly linearly dependent.

---

## 22. Probability, covariance, and calculus in statistics

### Probability densities and integration

For a continuous random variable $X$ with density $f_X$:

$$
P(a\le X\le b)=\int_a^b f_X(x)\,dx,
\qquad
\int_{-\infty}^{\infty}f_X(x)\,dx=1.
$$

The density itself need not be at most 1; probability is the **area** under the density over an interval.

### Expected values and variance

$$
E[X]=\int_{-\infty}^{\infty}x f_X(x)\,dx,
$$

$$
\operatorname{Var}(X)
=E[(X-E[X])^2]
=E[X^2]-(E[X])^2.
$$

**Derivation of the shortcut:** Expand $(X-\mu)^2=X^2-2\mu X+\mu^2$ and take expectations:

$$
E[X^2]-2\mu E[X]+\mu^2=E[X^2]-\mu^2.
$$

### Covariance and Pearson correlation

$$
\operatorname{Cov}(X,Y)
=E[(X-E[X])(Y-E[Y])]
=E[XY]-E[X]E[Y].
$$

$$
\boxed{
\rho_{X,Y}
=\frac{\operatorname{Cov}(X,Y)}
{\sigma_X\sigma_Y}
}.
$$

Covariance has units equal to the product of the variables' units; Pearson correlation is dimensionless. The bound $|\rho|\le1$ follows from Cauchy–Schwarz.

**Sample Pearson coefficient** for paired observations $(x_i,y_i)$:

$$
r=
\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}
{\sqrt{\sum_i(x_i-\bar x)^2\,\sum_i(y_i-\bar y)^2}}.
$$

Factors of $1/(n-1)$ in sample covariance and standard deviations cancel.

### Pearson, Spearman, and Kendall: different associations

| Measure | Based on | Detects |
|---|---|---|
| Pearson $r$ / $\rho$ | Centered numerical values | Linear association |
| Spearman $\rho_s$ | Pearson correlation of ranks | Monotonic rank association |
| Kendall $\tau$ | Concordant versus discordant pairs | Agreement in pairwise ordering |

For observations without ties:

$$
\tau=\frac{C-D}{\binom n2}.
$$

With ties, Kendall's **tau-b** uses a denominator adjusted for pairs tied only in one variable; blindly applying the no-ties formula can give a misleading magnitude.

### A deterministic relation can have zero correlation

Suppose $X$ has a distribution symmetric about zero and $Y=X^2$. Then

$$
\operatorname{Cov}(X,X^2)
=E[X^3]-E[X]E[X^2]=0,
$$

because the odd moments $E[X]$ and $E[X^3]$ vanish (assuming the relevant moments exist).

Yet $Y$ is entirely determined by $X$. Thus **uncorrelated does not generally imply independent**.

For jointly Gaussian random variables, zero covariance *does* imply independence—an important special property, not a general rule.

### Variance and covariance of sums

For constants $a,b$:

$$
\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X).
$$

For two random variables:

$$
\boxed{
\operatorname{Var}(X+Y)
=\operatorname{Var}(X)+\operatorname{Var}(Y)
+2\operatorname{Cov}(X,Y)
}.
$$

If $X$ and $Y$ are independent, covariance is zero and the variances add. The converse does not generally hold.

### Change of variables: calculus inside probability

If $Y=g(X)$ for a differentiable **one-to-one** transformation with inverse, densities transform as

$$
\boxed{
f_Y(y)
=f_X(g^{-1}(y))
\left|\frac{d}{dy}g^{-1}(y)\right|
}.
$$

The derivative factor is a one-dimensional Jacobian. It preserves total probability when the coordinate scale changes.

If $g$ is not one-to-one, sum contributions over all inverse branches.

**Example:** If $X$ is uniform on $[0,1]$ and $Y=X^2$, then $x=\sqrt y$ and $dx/dy=1/(2\sqrt y)$:

$$
f_Y(y)=\frac1{2\sqrt y}\quad(0<y<1).
$$

Check normalization:

$$
\int_0^1\frac1{2\sqrt y}\,dy=[\sqrt y]_0^1=1.
$$

### Law of Large Numbers and Central Limit Theorem

For independent identically distributed observations $X_1,\ldots,X_n$ with finite mean $\mu$, the sample mean $\bar X_n$ converges to $\mu$ under the usual Law of Large Numbers conditions.

If the variance $\sigma^2$ is finite and positive, the classical CLT states:

$$
\frac{\sqrt n(\bar X_n-\mu)}{\sigma}
\xrightarrow{d}N(0,1).
$$

The arrow $\xrightarrow{d}$ means **convergence in distribution**, which differs from convergence almost surely or in probability.

### Delta method: a bridge from derivatives to statistics

If $\sqrt n(\hat\theta_n-\theta)\xrightarrow{d}N(0,\sigma^2)$ and $g$ is differentiable at $\theta$, then

$$
\sqrt n\,[g(\hat\theta_n)-g(\theta)]
\xrightarrow{d}
N(0,\,[g'(\theta)]^2\sigma^2).
$$

**Why:** use first-order Taylor expansion:

$$
g(\hat\theta_n)
\approx g(\theta)+g'(\theta)(\hat\theta_n-\theta).
$$

Thus a derivative propagates approximate uncertainty through a nonlinear transformation. In several dimensions, the gradient/Jacobian plays the same role.

---

## 23. Numerical methods, approximation, and error

### Why numerical methods exist

Many limits, integrals, and differential equations have no convenient closed-form answer. Numerical analysis replaces the exact problem with a computable approximation and studies:

- **Consistency:** Does the approximation tend toward the correct mathematical operation as resolution improves?
- **Stability:** Do perturbations and rounding errors remain controlled?
- **Convergence:** Does the numerical solution approach the true solution?
- **Conditioning:** How sensitive is the original problem to changes in its inputs?

An algorithm may be implemented correctly but be unstable; conversely, even a stable algorithm cannot completely overcome an intrinsically ill-conditioned problem.

### Finite-difference derivatives from Taylor expansions

Expand around $x$:

$$
f(x+h)=f(x)+hf'(x)+\frac{h^2}{2}f''(x)
+\frac{h^3}{6}f'''(x)+O(h^4),
$$

$$
f(x-h)=f(x)-hf'(x)+\frac{h^2}{2}f''(x)
-\frac{h^3}{6}f'''(x)+O(h^4).
$$

**Forward difference:**

$$
\frac{f(x+h)-f(x)}{h}=f'(x)+O(h).
$$

**Central difference:** subtract the two expansions:

$$
\boxed{
\frac{f(x+h)-f(x-h)}{2h}
=f'(x)+O(h^2)
}.
$$

The leading even-order error cancels, giving second-order accuracy.

**Second derivative:** add the expansions:

$$
\boxed{
\frac{f(x+h)-2f(x)+f(x-h)}{h^2}
=f''(x)+O(h^2)
}.
$$

Smaller $h$ reduces truncation error initially, but extremely small $h$ can amplify floating-point cancellation; there is usually a practical optimal range.

### Bisection for finding roots

If $f$ is continuous on $[a,b]$ and $f(a)f(b)<0$, IVT guarantees a root between the endpoints.

At each iteration:

1. Compute midpoint $m=(a+b)/2$.
2. Check the sign of $f(m)$.
3. Retain the half interval containing the sign change.
4. Repeat.

After $n$ iterations the bracket width is $(b-a)/2^n$. Bisection is reliable but linearly convergent.

### Newton–Raphson root finding — derived

To solve $f(x)=0$, approximate the curve by its tangent at $x_n$:

$$
f(x)\approx f(x_n)+f'(x_n)(x-x_n).
$$

Set the tangent approximation to zero:

$$
0=f(x_n)+f'(x_n)(x_{n+1}-x_n).
$$

Solve for the next estimate:

$$
\boxed{x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}}.
$$

For $f(x)=x^2-2$ and $x_0=1$:

$$
x_1=1-\frac{1-2}{2}=1.5,
$$

$$
x_2=1.5-\frac{1.5^2-2}{3}=1.416666\ldots
$$

This approaches $\sqrt2\approx1.414214$. Newton's method can converge quadratically near a simple root with suitable hypotheses, but can diverge or fail when started badly or when the derivative vanishes.

### Numerical integration: trapezoidal rule

Approximate the curve between adjacent points with a straight line. For one interval:

$$
\int_a^b f(x)\,dx
\approx\frac{b-a}{2}[f(a)+f(b)].
$$

For $n$ equal subintervals of width $h=(b-a)/n$, the composite trapezoidal rule is

$$
\boxed{
\int_a^bf(x)\,dx
\approx h\left[\frac{f(x_0)}2
+\sum_{i=1}^{n-1}f(x_i)+\frac{f(x_n)}2\right]
}.
$$

For sufficiently smooth $f$, the global truncation error is $O(h^2)$ on a fixed interval.

### Simpson's rule

Approximate with quadratic polynomials instead of straight segments:

$$
\int_a^bf(x)\,dx
\approx\frac{b-a}{6}\left[
f(a)+4f\!\left(\frac{a+b}{2}\right)+f(b)\right].
$$

Composite Simpson's rule uses an **even** number of equal subintervals. For sufficiently smooth functions, its global error is $O(h^4)$.

### Numerical ODEs: Euler's method

For the initial-value problem $y'=F(t,y)$ and a step size $h$:

$$
\boxed{y_{n+1}=y_n+hF(t_n,y_n)}.
$$

**Derivation:** first-order Taylor expansion:

$$
y(t+h)\approx y(t)+hy'(t)=y(t)+hF(t,y(t)).
$$

Example: $y'=y$, $y(0)=1$, and $h=0.1$:

$$
y_1=1+0.1(1)=1.1.
$$

The exact solution is $e^t$, so $y(0.1)=e^{0.1}\approx1.10517$. Euler's method underestimates it on this step.

### Runge–Kutta fourth order (RK4)

For $y'=F(t,y)$, classical RK4 computes:

$$
\begin{aligned}
k_1&=F(t_n,y_n),\\
k_2&=F(t_n+h/2,y_n+hk_1/2),\\
k_3&=F(t_n+h/2,y_n+hk_2/2),\\
k_4&=F(t_n+h,y_n+hk_3),\\
y_{n+1}&=y_n+\frac h6(k_1+2k_2+2k_3+k_4).
\end{aligned}
$$

Under sufficient smoothness, its global error is $O(h^4)$, substantially better than Euler's $O(h)$ for the same step-size asymptotics. This does not guarantee RK4 is always preferable; stiff equations may require implicit or specialized solvers.

### Numerical solution of the heat equation

Discretize $u_t=\alpha u_{xx}$ on a grid $x_i=i\Delta x$, $t_n=n\Delta t$.

Approximate the time derivative by a forward difference and the spatial second derivative by a central difference:

$$
\frac{u_i^{n+1}-u_i^n}{\Delta t}
=\alpha\frac{u_{i+1}^n-2u_i^n+u_{i-1}^n}{(\Delta x)^2}.
$$

Rearrange:

$$
\boxed{
u_i^{n+1}
=u_i^n+r(u_{i+1}^n-2u_i^n+u_{i-1}^n),
\qquad r=\frac{\alpha\Delta t}{(\Delta x)^2}
}.
$$

For the standard one-dimensional explicit scheme, stability requires $r\le1/2$ under the usual grid and boundary assumptions. Refining the spatial grid without also adjusting the time step can therefore destabilize the calculation.

This is a concrete example of why a mathematically valid differential equation is not enough: the **numerical discretization also has its own mathematical properties**.

---

# Part IV — Reference and review

## 24. Formula and theorem reference

### Limits and continuity

| Topic | Key statement |
|---|---|
| Finite function limit | $0<|x-a|<\delta\Rightarrow |f(x)-L|<\varepsilon$ |
| Continuity at $a$ | $\lim_{x\to a}f(x)=f(a)$ |
| One-sided limits | A two-sided finite limit exists iff both one-sided finite limits agree |
| Squeeze theorem | A function bounded between two functions with the same limit shares their limit |
| IVT | A continuous function attains every intermediate value |
| EVT | A continuous function on a compact interval attains extrema |
| Differentiability | Implies continuity; converse is false |

### Derivative rule sheet

$$
\begin{aligned}
(cf+g)'&=cf'+g',\\
(fg)'&=f'g+fg',\\
\left(\frac fg\right)'&=\frac{f'g-fg'}{g^2},\\
(f\circ g)'&=(f'\circ g)g',\\
(x^n)'&=nx^{n-1},\\
(e^x)'&=e^x,\quad(\ln|x|)'=\frac1x,\\
(\sin x)'&=\cos x,\quad(\cos x)'=-\sin x,\\
(\tan x)'&=\sec^2x.
\end{aligned}
$$

Common nested patterns:

$$
\begin{aligned}
\frac d{dx}[u(x)]^n&=n[u(x)]^{n-1}u'(x),\\
\frac d{dx}\ln|u(x)|&=\frac{u'(x)}{u(x)},\\
\frac d{dx}e^{u(x)}&=e^{u(x)}u'(x),\\
\frac d{dx}\sin(u(x))&=\cos(u(x))u'(x).
\end{aligned}
$$

### Antiderivatives and techniques

$$
\begin{aligned}
\int x^n\,dx&=\frac{x^{n+1}}{n+1}+C\quad(n\ne-1),\\
\int\frac{dx}{x}&=\ln|x|+C,\\
\int e^x\,dx&=e^x+C,\\
\int\cos x\,dx&=\sin x+C,\\
\int\sin x\,dx&=-\cos x+C.
\end{aligned}
$$

$$
\int u\,dv=uv-\int v\,du,
\qquad
\int f(g(x))g'(x)\,dx=\int f(u)\,du.
$$

### Convergence reference

| Expression / test | Result |
|---|---|
| $\sum_{n=0}^\infty ar^n$ | $a/(1-r)$ when $|r|<1$ |
| $\sum_{n=1}^\infty 1/n^p$ | Converges iff $p>1$ |
| $\int_1^\infty x^{-p}\,dx$ | Converges iff $p>1$ |
| $\int_0^1 x^{-p}\,dx$ | Converges iff $p<1$ |
| Ratio / root test result $L<1$ | Absolute convergence |
| Ratio / root test result $L>1$ | Divergence |
| Ratio / root test result $L=1$ | Inconclusive |
| Alternating test | Decreasing positive magnitudes tending to zero imply convergence |
| $\sum|a_n|$ converges | $\sum a_n$ converges absolutely |

### Multivariable and vector calculus

$$
\begin{aligned}
df&=\sum_i f_{x_i}\,dx_i,\\
\frac{df}{dt}&=\nabla f\cdot\frac{d\mathbf x}{dt},\\
D_{\mathbf u}f&=\nabla f\cdot\mathbf u,\\
J_{F\circ G}&=J_F(G)\,J_G,\\
H_f&=(f_{x_ix_j})_{i,j},\\
\nabla f&=\lambda\nabla g\quad\text{(one equality constraint)}.
\end{aligned}
$$

$$
dA_{\mathrm{polar}}=r\,dr\,d\theta,\qquad
dV_{\mathrm{spherical}}=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta.
$$

$$
\nabla\cdot\mathbf F=P_x+Q_y+R_z,\qquad
\nabla^2f=f_{xx}+f_{yy}+f_{zz}.
$$

### ODE and PDE recognition

| Form | Name / characteristic |
|---|---|
| $y'=ky$ | Exponential growth or decay |
| $y'+p(x)y=q(x)$ | First-order linear ODE; integrating factor |
| $ay''+by'+cy=0$ | Linear constant-coefficient ODE; characteristic polynomial |
| $u_t=\alpha u_{xx}$ | Heat / diffusion PDE |
| $u_{tt}=c^2u_{xx}$ | Wave PDE |
| $\nabla^2u=0$ | Laplace PDE |
| $\nabla^2u=f$ | Poisson PDE |
| $u_t+cu_x=0$ | Transport / advection PDE |

### Important mathematical distinctions

| Often confused | Distinction |
|---|---|
| Limit vs function value | The limit concerns nearby points; $f(a)$ may not exist |
| Convergent sequence vs convergent series | Series convergence refers to its sequence of partial sums |
| Differentiability vs continuity | Differentiability implies continuity, not conversely |
| Inflection point vs $f''=0$ | Inflection requires a change in concavity |
| Critical point vs local extremum | A zero derivative might be a saddle/stationary inflection |
| Partial vs total derivative | Partial holds other independent inputs fixed; total tracks all dependencies |
| Gradient vs Hessian | First-order direction/sensitivity vs second-order curvature |
| Correlation vs dependence | Zero correlation does not generally imply independence |
| ODE vs PDE | Ordinary derivative in one independent variable vs partial derivatives in several |
| Analytical vs numerical solution | Exact symbolic form vs controlled approximation |
| Truncation error vs floating-point error | Discretization/model approximation vs finite-precision arithmetic |

### Complex exponentials and Euler's identity

Complex numbers enter calculus, oscillations, Fourier analysis, and differential equations through

$$
\boxed{e^{i\theta}=\cos\theta+i\sin\theta},\qquad i^2=-1.
$$

**Taylor-series derivation:** expand the exponential in powers of $i\theta$:

$$
e^{i\theta}
=1+i\theta-\frac{\theta^2}{2!}
-i\frac{\theta^3}{3!}
+\frac{\theta^4}{4!}+\cdots.
$$

Collect the real and imaginary parts:

$$
\left(1-\frac{\theta^2}{2!}+\frac{\theta^4}{4!}-\cdots\right)
+i\left(\theta-\frac{\theta^3}{3!}+\frac{\theta^5}{5!}-\cdots\right).
$$

These are exactly the Maclaurin series of $\cos\theta$ and $\sin\theta$.

At $\theta=\pi$:

$$
\boxed{e^{i\pi}+1=0}.
$$

Complex exponentials are especially helpful because differentiation becomes multiplication:

$$
\frac{d}{dt}e^{i\omega t}=i\omega e^{i\omega t}.
$$

This makes them natural building blocks for oscillatory solutions of ODEs and PDEs.

### Laplace transforms and solving ODEs

For a suitable function $f(t)$ defined for $t\ge0$:

$$
\mathcal L\{f\}(s)
=\int_0^\infty e^{-st}f(t)\,dt.
$$

Under appropriate growth and regularity conditions, integration by parts gives

$$
\boxed{\mathcal L\{f'\}(s)=sF(s)-f(0)},
$$

where $F(s)=\mathcal L\{f\}(s)$.

**Derivation:**

$$
\int_0^\infty e^{-st}f'(t)\,dt
=\left[e^{-st}f(t)\right]_0^\infty
+s\int_0^\infty e^{-st}f(t)\,dt
=-f(0)+sF(s).
$$

For $y'+ay=0$ and $y(0)=y_0$:

$$
sY(s)-y_0+aY(s)=0
\quad\Rightarrow\quad
Y(s)=\frac{y_0}{s+a}.
$$

The inverse transform gives $y(t)=y_0e^{-at}$. A differential equation has been converted into an **algebraic equation** in transform space.

---

## 25. Worked problems with solutions

The problems combine foundational calculations with reasoning about assumptions, critical points, and multivariable behaviour.

### Problem 1 — A removable discontinuity

Evaluate

$$
\lim_{x\to2}\frac{x^2-4}{x-2}.
$$

**Solution.** Factor the numerator:

$$
\frac{(x-2)(x+2)}{x-2}=x+2\qquad(x\ne2).
$$

Take the limit of the simplified expression: **4**. The original function is undefined at 2, but its limit exists.

### Problem 2 — A limit using Taylor expansion

Find

$$
\lim_{x\to0}\frac{e^x-1-x}{x^2}.
$$

**Solution.** Use $e^x=1+x+x^2/2+O(x^3)$:

$$
\frac{e^x-1-x}{x^2}
=\frac{x^2/2+O(x^3)}{x^2}
=\frac12+O(x).
$$

Hence the limit is **1/2**. Two applications of L'Hôpital's rule give the same result.

### Problem 3 — Chain and product rules together

Differentiate $f(x)=x^2e^{-x}$.

**Solution.**

$$
f'(x)=2xe^{-x}+x^2(-e^{-x})
=e^{-x}(2x-x^2).
$$

The stationary points are $x=0$ and $x=2$.

- For $x<0$, $f'<0$.
- For $0<x<2$, $f'>0$.
- For $x>2$, $f'<0$.

So $x=0$ is a **local minimum**, $f(0)=0$, and $x=2$ is a **local maximum**, $f(2)=4e^{-2}$. The latter is *not* the global maximum on $\mathbb R$ because $x^2e^{-x}\to\infty$ as $x\to-\infty$.

### Problem 4 — A stationary point need not be an extremum

Classify the origin for $f(x)=x^3$.

**Solution.** $f'(x)=3x^2$, so $f'(0)=0$. But $f$ is strictly increasing everywhere: values to the left of zero are negative and to the right are positive. Thus zero is neither a maximum nor a minimum.

Its second derivative $f''(x)=6x$ changes sign at zero, so the origin is a **stationary inflection point**.

### Problem 5 — An implicit ellipse

For $4x^2+9y^2=36$, calculate $dy/dx$.

**Solution.** Differentiate implicitly:

$$
8x+18y\frac{dy}{dx}=0.
$$

Therefore

$$
\boxed{\frac{dy}{dx}=-\frac{4x}{9y}}\qquad(y\ne0).
$$

At a point with $y=0$, the curve has a vertical tangent rather than a finite derivative $dy/dx$.

### Problem 6 — Integration by substitution

Compute $\int_0^1 x\sqrt{1+x^2}\,dx$.

**Solution.** Let $u=1+x^2$; then $du=2x\,dx$. The limits become $u=1$ and $u=2$:

$$
\begin{aligned}
\int_0^1 x\sqrt{1+x^2}\,dx
&=\frac12\int_1^2 u^{1/2}\,du\\
&=\frac13[u^{3/2}]_1^2\\
&=\frac{2\sqrt2-1}{3}.
\end{aligned}
$$

### Problem 7 — Improper integral and convergence

Does $\int_1^\infty x^{-3/2}\,dx$ converge?

**Solution.** The exponent is $p=3/2>1$, so the $p$-integral test predicts convergence. Verify:

$$
\int_1^R x^{-3/2}\,dx
=[-2x^{-1/2}]_1^R
=2-\frac2{\sqrt R}\longrightarrow2.
$$

The integral converges to **2**.

### Problem 8 — Ratio test with factorials

Does $\sum_{n=1}^\infty n!/n^n$ converge?

**Solution.** Set $a_n=n!/n^n$. Then

$$
\frac{a_{n+1}}{a_n}
=\frac{(n+1)!}{(n+1)^{n+1}}\frac{n^n}{n!}
=\left(\frac n{n+1}\right)^n.
$$

Since $(1+1/n)^n\to e$, the ratio tends to $1/e<1$. Therefore the series **converges absolutely**.

### Problem 9 — Approximation and error bound

Approximate $\sin(0.2)$ using its third-degree Maclaurin polynomial and bound the error.

**Solution.** Use

$$
\sin x=x-\frac{x^3}{3!}+\frac{x^5}{5!}-\cdots.
$$

So

$$
\sin(0.2)\approx0.2-\frac{0.2^3}{6}
=0.1986666667.
$$

Because the omitted terms form an alternating series with decreasing magnitudes at $x=0.2$,

$$
|\text{error}|\le\frac{0.2^5}{5!}
\approx2.67\times10^{-6}.
$$

The actual value is approximately $0.198669331$, consistent with the bound.

### Problem 10 — Tangent plane to a surface

For $f(x,y)=x^2+2y^2$, find the tangent plane at $(x,y)=(1,-1)$.

**Solution.** The point on the surface is $(1,-1,3)$. The first partials are $f_x=2x$ and $f_y=4y$. At the point, they are 2 and $-4$.

Thus

$$
\begin{aligned}
z&=3+2(x-1)-4(y+1)\\
&=\boxed{2x-4y-3}.
\end{aligned}
$$

The plane matches both the function value and the two first partial derivatives at the selected point.

### Problem 11 — The difference between partial and total derivatives

Let $f(x,y)=x^2+y^2$, $x(t)=t$, $y(t)=t^2$. Find $df/dt$.

**Solution A — substitute first.** $f(t)=t^2+t^4$, so

$$
\frac{df}{dt}=2t+4t^3.
$$

**Solution B — use the multivariable chain rule.**

$$
\frac{df}{dt}
=2x\frac{dx}{dt}+2y\frac{dy}{dt}
=2t(1)+2t^2(2t)
=2t+4t^3.
$$

Both methods agree. A partial derivative $f_x=2x$ **alone** would miss the change caused by $y(t)$.

### Problem 12 — Hessian classification

Classify the stationary point of $f(x,y)=3x^2+2xy+2y^2$.

**Solution.** The gradient is

$$
\nabla f=
\begin{pmatrix}
6x+2y\\2x+4y
\end{pmatrix}.
$$

It vanishes at $(0,0)$, which is the only stationary point because the linear system has nonzero determinant.

The Hessian is

$$
H_f=\begin{pmatrix}6&2\\2&4\end{pmatrix}.
$$

The first leading principal minor is $6>0$ and determinant is $24-4=20>0$. Thus the Hessian is positive definite; the origin is the **unique global minimum** (the objective is a strictly convex quadratic).

### Problem 13 — Lagrange multipliers on a circle

Maximize $f(x,y)=x+2y$ subject to $x^2+y^2=1$.

**Solution.** The condition $\nabla f=\lambda\nabla g$ yields

$$
(1,2)=\lambda(2x,2y).
$$

Thus $x=1/(2\lambda)$ and $y=1/\lambda$, so $y=2x$. The constraint gives

$$
5x^2=1
\quad\Rightarrow\quad
(x,y)=\left(\frac1{\sqrt5},\frac2{\sqrt5}\right)
$$

for the maximum, with objective value $\sqrt5$. The opposite point yields the minimum $-\sqrt5$.

**Geometric check:** $\max_{\|\mathbf x\|=1}(1,2)\cdot\mathbf x=\|(1,2)\|=\sqrt5$ by Cauchy–Schwarz.

### Problem 14 — A double integral over a triangle

Let $D=\{(x,y):x\ge0,\ y\ge0,\ x+y\le1\}$. Compute $\iint_D(x+y)\,dA$.

**Solution.** For a fixed $x\in[0,1]$, $y$ ranges from 0 to $1-x$:

$$
\begin{aligned}
\iint_D(x+y)\,dA
&=\int_0^1\int_0^{1-x}(x+y)\,dy\,dx\\
&=\int_0^1\left[x(1-x)+\frac{(1-x)^2}{2}\right]dx\\
&=\int_0^1\left(\frac12-\frac{x^2}{2}\right)dx\\
&=\boxed{\frac13}.
\end{aligned}
$$

As a geometric check, the triangle has area $1/2$ and centroid $(1/3,1/3)$; since $x+y$ is linear, its average over the triangle is $2/3$, giving integral $(1/2)(2/3)=1/3$.

### Problem 15 — Verify a heat-equation solution

Show that

$$
u(x,t)=e^{-4\alpha t}\sin(2x)
$$

satisfies $u_t=\alpha u_{xx}$.

**Solution.** Differentiate:

$$
u_t=-4\alpha e^{-4\alpha t}\sin(2x),
$$

$$
u_{xx}=-4e^{-4\alpha t}\sin(2x).
$$

Therefore $\alpha u_{xx}=u_t$. The equality holds for every $(x,t)$ in the domain.

This is a direct **verification**, not a derivation of the most general solution.

### Problem 16 — Solve an initial-value ODE

Solve $y'+3y=6$ with $y(0)=5$.

**Solution.** The integrating factor is $e^{3t}$:

$$
(e^{3t}y)'=6e^{3t}.
$$

Integrating:

$$
y=2+Ce^{-3t}.
$$

Use $y(0)=5$:

$$
5=2+C\quad\Rightarrow\quad C=3.
$$

Hence

$$
\boxed{y(t)=2+3e^{-3t}}.
$$

The solution approaches equilibrium 2 as $t\to\infty$.

### Problem 17 — A symmetric nonlinear relationship with zero covariance

Let $X$ be uniform on $[-1,1]$ and set $Y=X^2$. Find $\operatorname{Cov}(X,Y)$.

**Solution.** The density of $X$ is $1/2$ on $[-1,1]$. Compute:

$$
E[X]=\frac12\int_{-1}^1x\,dx=0,
$$

$$
E[X^3]=\frac12\int_{-1}^1x^3\,dx=0,
$$

because the integrands are odd functions on a symmetric interval.

Therefore

$$
\operatorname{Cov}(X,Y)
=E[X^3]-E[X]E[X^2]
=\boxed{0}.
$$

Yet $Y$ is a deterministic function of $X$. Thus zero Pearson correlation here says **no linear association**, not independence.

### Problem 18 — Newton's method for a square root

Approximate $\sqrt2$ by solving $f(x)=x^2-2=0$ from $x_0=1$.

**Solution.**

$$
x_{n+1}=x_n-\frac{x_n^2-2}{2x_n}
=\frac12\left(x_n+\frac2{x_n}\right).
$$

Compute:

| Iteration | Estimate |
|---|---:|
| $x_0$ | 1.000000 |
| $x_1$ | 1.500000 |
| $x_2$ | 1.416667 |
| $x_3$ | 1.414216 |
| $x_4$ | 1.414214 |

This is the classical Babylonian method for square roots, rediscovered here as Newton's method.

---

# Appendix — Symbols, conventions, and common traps

| Symbol | Meaning |
|---|---|
| $\forall$, $\exists$ | For all; there exists |
| $\in$, $\subseteq$ | Is an element of; is a subset of |
| $\Rightarrow$, $\Leftrightarrow$ | Implies; if and only if |
| $\to$, $\xrightarrow{d}$ | Approaches; convergence in distribution |
| $\varepsilon$, $\delta$ | Positive tolerances used in limit definitions |
| $O(h^p)$ | Error bounded in magnitude by a constant multiple of $|h|^p$ for small $h$ |
| $o(h^p)$ | Error negligible relative to $h^p$ as $h\to0$ |
| $\nabla$ | Gradient / del operator |
| $\partial$ | Partial derivative |
| $\Delta$ | Finite difference, or Laplacian in some contexts |
| $\lambda$ | Eigenvalue, Lagrange multiplier, or model parameter depending on context |
| $\rho$, $\tau$ | Often Pearson/Spearman and Kendall correlation symbols, respectively |
| $\|\mathbf x\|$ | Norm or length of a vector |
| $\mathbb E[X]$ | Expected value |
| $\operatorname{Cov}$, $\operatorname{Var}$ | Covariance and variance |

**Units and dimensions:** Derivatives have units of output/input, integrals have units of integrand times input, variances have squared units, and correlation coefficients are dimensionless. Dimensional consistency is an efficient check on many physics and applied-mathematics calculations.

**Endpoint conditions:** A formula may be valid only on intervals where denominators are nonzero, logarithms have real arguments, or an inverse function is differentiable. Always state the domain.

**Necessary versus sufficient:** Conditions such as $f'=0$, $\nabla f=0$, and $f''=0$ typically identify **candidates**, not automatically extrema or inflection points. A separate sign, Hessian, or global argument establishes the classification.

**Local versus global:** Derivatives and tangent approximations describe nearby behavior. Correlation describes association across a distribution or dataset. Global optimization requires extra information, such as convexity, compactness, or boundary checks.

**Classical versus weak solutions:** A differential equation solved by repeatedly differentiating an explicit formula is a classical solution. Modern PDE theory also uses weaker notions of solution when physical fields are not sufficiently smooth; the relevant definitions depend on the equation and function space.
