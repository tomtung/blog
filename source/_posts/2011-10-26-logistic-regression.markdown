---
layout: post
title: "[学习笔记] Logistic 回归"
date: 2011-10-26 04:08
comments: true
categories: [Algorithm, Machine Learning]
---
本文为 [Stanford 的机器学习公开课](http://www.ml-class.org/)第三周的笔记，不过和上课内容的细节有些出入。

Logistic 回归解决的并不是回归问题，而是分类问题，即目标变量（target variable）的值是离散而非连续的。
这时目标变量也可称为标签（label）。如果仍用线性回归硬搞，得到的结果会非常不靠谱。

我们先考虑简单的情况：数据点只有 0 和 1 两个标签（binary classification），即 $$ y \in \{0,1\} $$，
且大致上是线性可分的（linearly separable）。如图：

{% img /img/2011-10-26-binary-classification.png %}

那么现在问题就是要找到一个 $$\theta$$，使得直线 $$\theta^{\rm T} x = 0$$ [^extra_one] 能够将上面图中的
positive 和 negative 两类数据点“分开”；这样的一条直线称为决策边界（decision boundary）。
——但具体什么叫“分开”？或者说，如果已知 $$\theta$$，对于一个标签未知的数据点 $$x$$，怎么判断它是 positive 还是 negative？

[^extra_one]:
	和上节线性规划中一样，每个 $$x^{(i)}$$ 是一个 $$n+1$$ 维向量，为书写简便我们在 $$n$$ 个属性前再加一维 $$x^{(i)}_0=1$$。

直观上看，在给定 $$\theta$$ 和 $$x$$ 的情况下，$$y$$ 应该满足一个[0-1 分布](http://en.wikipedia.org/wiki/Bernoulli_distribution)，即

$$ y|x;\theta \sim Bernoulli\big(\phi(\theta^{\rm T} x)\big) $$

其中 $$ \phi(\theta^{\rm T} x) = P(y = 1|x;\theta) $$ 应该满足：

1. 首先 $$ 0 \leq \phi(\theta^{\rm T} x) \leq 1 $$
2. 若 $$\theta^{\rm T} x > 0$$，我们可以认为 $$ y=1 $$ 的可能性相对更大，即 $$ \phi(\theta^{\rm T} x) > 0.5 $$，
   且如果数据点离边界越远，即 $$\theta^{\rm T} x$$ 越大，$$\phi(\theta^{\rm T} x)$$ 也应该越大。
3. 反之，若 $$\theta^{\rm T} x < 0$$，则 $$ \phi(\theta^{\rm T} x) < 0.5 $$，且随 $$\theta^{\rm T} x$$ 减小而减小。
4. 当 $$\theta^{\rm T} x = 0$$ 时，点落在决策边界上，我们无从判断它的标签 $$y$$，因此 $$ \phi(\theta^{\rm T} x) = 0.5 $$。

那 $$\phi$$ 应该取什么样的函数呢？我们知道 [logistic 函数](http://en.wikipedia.org/wiki/Logistic_function) 恰巧满足上述条件，
不妨就取它（“logistic 回归”也因此得名）[^glm]。即：

$$ \phi(z) = \frac{1}{1+\exp(-z)} $$

[^glm]:
	这里说“不妨”似乎有点太随意了。事实上，如果假设在给定 $$x$$ 的情况下 $$y$$ 服从 0-1 分布，那么$$\phi$$ 取 logistic
	函数实际上可以由[广义线性模式](http://en.wikipedia.org/wiki/Generalized_linear_model)（Generalized linear model）的假设推导得出。

logistic 函数的图像是：

{% img /img/2011-10-26-logistic-curve.png %}

可以直观地看到它确实是满足我们要求的。这样我们就得到了：

$$ P(y = 1|x;\theta) = \phi(\theta^{\rm T} x) = \frac{1}{1+\exp(-\theta^{\rm T} x)} $$

我们记 $$ h_\theta(x) = P(y = 1|x;\theta) $$，表示这是我们希望预测的量，也就是模型的假设（hypothesis）[^expect]。在实际分类应用中，
$$h_\theta(x) > 0.5$$ 时我们可以给出判断 $$y = 1$$ ，$$h_\theta(x) < 0.5$$ 时 $$y = 0$$ ，$$h_\theta(x) = 0.5$$ 的话就蒙一个吧。

[^expect]:
	注意到和[上节课](/2011/10/linear-regression-gradient-descent/)讲的线性回归一样，我们要预测的 $$h_\theta(x)$$ 其实都是期望 $$E_{y|x;\theta}$$。

接下来 $$\theta$$ 该怎么求呢？根据log极大似然法，可知 $$\theta$$ 的最优值就是 $$\arg\max_\theta L(\theta)$$，其中

$$
\begin{eqnarray}
L(\theta) &=& \log \prod_i P(y^{(i)}|x^{(i)};\theta) \\
&=& \log \prod_i h_\theta(x^{(i)})^{y^{(i)}} \big(1-h_\theta(x^{(i)})\big)^{1-y^{(i)}} \\
&=& \sum_i y^{(i)} \log h_\theta(x^{(i)}) + (1-y^{(i)}) \log h_\theta(1-x^{(i)})
\end{eqnarray}
$$

其中第二步有点小 tricky。注意到 $$ h_\theta(x)^y \big(1-h_\theta(x)\big)^{1-y} $$ 在 $$y=0$$ 时值为 $$h_\theta(x)^y$$，在
$$y=1$$ 时值为 $$\big(1-h_\theta(x)\big)^{1-y}$$。这样就把 $$y$$ 两种取值的情况合并写在一个式子里了。

接下来我们可以求出梯度 $$\nabla_\theta L(\theta)$$。如果我们像[上篇笔记](/2011/10/linear-regression-gradient-descent)中一样定义：

$$
X := \begin{pmatrix} (x^{(1)})^{\rm T} \\ (x^{(2)})^{\rm T} \\ \vdots \\ (x^{(m)})^{\rm T} \end{pmatrix} \quad
\vec{y} := \begin{pmatrix} y^{(1)} \\ y^{(2)} \\ \vdots \\ y^{(m)} \end{pmatrix} \quad
\vec{h_\theta} := \begin{pmatrix} h_\theta(x^{(1)}) \\ h_\theta(x^{(2)}) \\ \vdots \\ h_\theta(x^{(m)}) \end{pmatrix}
$$

可以推导得到：

$$ \nabla_\theta L(\theta) = \frac{1}{m} X^{\rm T} (\vec{y} - \vec{h_\theta}) $$

接下来，根据梯度上升算法 [^gradient_ascent]，我们就可以迭代计算下式来逼近 $$\arg\max_\theta L(\theta)$$：

$$
\begin{eqnarray}
\theta_{t+1} &:=& \theta_t + \alpha \nabla_\theta L(\theta) \\
&=& \theta_t – \frac{\alpha}{m} X^{\rm T} (\vec{h_\theta} – \vec{y})
\end{eqnarray}
$$

[^gradient_ascent]: 
	由于这里要求的是 $$L(\theta)$$ 的*最大值*，因此是梯度上升而非梯度下降。课程视频中取要最小化的目标函数
	$$J(\theta)=-L(\theta)$$，因此是梯度下降。实际是一回事。
	
注意到这个更新式的形式和之前线性规划+最小二乘法+梯度下降得到是一样的，只是 $$\vec{h_\theta}$$ 变了。

以上就是用梯度上升做 Logistic 回归的算法了。课上还谈到了另外 3 个问题：

1. 如果要把 Logistic 回归推广到多个分类的情况，可以利用一种叫“1 vs all”的方法。具体地说，即每次取一个分类为 positive，
   其它分类都为 negative。这样针对每一个分类都学习得到一个 Logistic 回归模型。要判断一个新数据点的标签，用每一个模型都测一下，
   取对应 $$ h_\theta(x) $$ 最大的分类为预测结果。
2. 如果数据点不是线性可分的，类似线性回归到多项式回归（polynomial regression）的推广，可以将同一属性次数不同的项看成是彼此独立的，
   再和普通 Logistic 回归问题一样处理。
3. 属性过多可能会造成模型过分复杂，导致过拟合问题。关于 overfit 和 underfit 的问题可以参见[这篇文章](http://blog.pluskid.org/?p=39)的
   3~6 段，这位学长讲得非常深入浅出了。课上提到的一种解决方法叫 regularization，即对 $$\theta$$ 中希望加以限制的各项 $$\theta_i$$，在
   $$L(\theta)$$ 后加上 $$-\lambda \theta_i^2 $$，使这些值过大时“惩罚”目标函数。这里 $$\lambda > 0$$ 的取值也要注意，
   如果取得太小解决不了过拟合问题，但取得太大又会造成 underfit。


p.s. 今天早睡的目标又达成失败了……………………