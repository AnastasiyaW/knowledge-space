---
title: Mathematics for Machine Learning
category: foundations
tags: [data-science, math, calculus, optimization, gradient]
---

# Mathematics for Machine Learning

The essential math underlying ML algorithms. Focus on what you need to understand WHY algorithms work, not just how to call them.

## Calculus for ML

### Derivatives

f'(x) = lim(h->0) [f(x+h) - f(x)] / h. Rate of change. Slope of tangent line.

**Key rules:**
- Power: (x^n)' = n*x^(n-1)
- Chain rule: (f(g(x)))' = f'(g(x)) * g'(x)
- Product: (fg)' = f'g + fg'
- e^x: (e^x)' = e^x
- ln(x): (ln(x))' = 1/x

### Partial Derivatives and Gradient

For f(x1, ..., xn): gradient = vector of partial derivatives.

nabla f = [df/dx1, df/dx2, ..., df/dxn]

**Gradient points in direction of steepest ascent.** Gradient descent moves opposite: w -= lr * nabla_f.

### Critical Points and Optimization

- Critical point: gradient = 0
- Second derivative test: f''(x) > 0 -> minimum, f''(x) < 0 -> maximum
- **Hessian matrix**: second partial derivatives. Eigenvalues determine nature of critical point
- **Convex functions**: any local minimum is global minimum. MSE is convex for linear regression

### Backpropagation

Chain rule through computation graph. For layer output = sigma(Wx + b):
```
d(Loss)/dW = d(Loss)/d(output) * d(output)/d(Wx+b) * d(Wx+b)/dW
```

Computational graph + automatic differentiation make this tractable for deep networks.

### Taylor Series

f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)^2/2! + ...

Key expansions: e^x = 1 + x + x^2/2! + ..., ln(1+x) = x - x^2/2 + ...

In ML: understanding loss behavior near optima, Newton's method (second-order approximation).

## Optimization

### Gradient Descent

w_(t+1) = w_t - alpha * nabla f(w_t)

- **Learning rate** alpha: too large -> diverge, too small -> slow
- **Stochastic GD**: single-sample gradient (noisy but fast)
- **Mini-batch GD**: small batch (balance)
- **Momentum**: v_t = beta*v_(t-1) + nabla f. Accelerates through narrow valleys
- **Convergence**: O(1/t) for convex with Lipschitz gradient

### Newton's Method

w_new = w_old - H^(-1) * gradient. Uses second derivatives (Hessian). Converges faster but H^(-1) is expensive.

**Quasi-Newton** (L-BFGS): approximate Hessian inverse cheaply.

### Lagrange Multipliers

Optimize f(x) subject to g(x) = 0: nabla f = lambda * nabla g.

In ML: SVM optimization (maximize margin subject to constraints).

## Log-Sum-Exp Trick

Avoid numerical overflow in softmax/log-likelihood:
```
log(sum(exp(x_i))) = c + log(sum(exp(x_i - c)))  where c = max(x_i)
```

## Integration in ML

- Computing expected values and probabilities (area under PDF)
- Normalization constants for distributions
- KL-divergence between distributions
- Lebesgue integral: foundation of modern probability theory

## Gotchas
- Gradient descent on non-convex functions (neural nets) finds local minima, not global - but this is usually fine
- Numerical stability matters: use log-space for products of probabilities
- Hessian computation is O(n^2) in parameters - impractical for large models
- Chain rule errors propagate - always verify gradients numerically

## See Also
- [[math-linear-algebra]] - vectors, matrices, eigenvalues
- [[linear-models]] - direct application of calculus to ML
- [[neural-networks]] - backpropagation uses chain rule
- [[probability-distributions]] - integration for expected values
