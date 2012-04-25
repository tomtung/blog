---
layout: post
title: "[学习笔记] Expectation-Maximization(EM) 算法"
date: 2011-10-13 00:54 
comments: true
categories: [Statistics, Algorithm, Machine Learning]
---

果然还是有必要保持记笔记的习惯呐。前两天实验室讲 [pLSA](http://en.wikipedia.org/wiki/PLSA) 的推导，用到 EM 竟然完全记不清了，竟然还把 [Jensen 不等式](http://en.wikipedia.org/wiki/Jensen's_inequality)和 SVM 的 minmax=maxmin 什么的记混= = （这么一说 SVM 具体怎么回事也记不清了。。。）赶紧补一篇复习笔记。

Expectation-Maximization 算法是统计学中用来给带[隐含变量](http://en.wikipedia.org/wiki/Latent_variable)的模型做最大似然（和最大后验概率）的一种方法。EM 的应用特别广泛，经典的比如做概率密度估计用的 [Gaussian Mixture Model](http://en.wikipedia.org/wiki/Gaussian_mixture_model)。这两天我或许还会写 p 的笔记放上来，也是 EM 应用的例子。

下面我会先解释 EM 算法要解决的问题，然后直接给出算法的过程，最后再说明算法的正确性。

## 问题 ##

首先我们定义要解决的问题。给定一个训练集 $$X=\{x^{(1)},...,x^{(m)}\}$$，我们希望拟合包含隐含变量 $$z$$ 的模型 $$P(x,z;\theta)$$ 中的参数 $$\theta$$。根据模型的假设，每个我们观察到的 $$x^{(i)}$$ 还对应着一个我们观察不到的隐含变量 $$z^{(i)}$$，我们记 $$Z=\{z^{(1)},...,z^{(m)}\}$$。做最大对数似然就是要求 $$ \theta $$ 的“最优值”：

$$\theta=\arg\max_\theta{L(\theta;X)}$$

其中 $$L(\theta;X)=log{P(X;\theta)}=\log{\sum_Z P(X,Z;\theta)}$$

想用这个$$\log$$套$$\sum$$的形式直接求解 $$\theta$$ 往往非常困难。而如果能观察到隐含变量 $$z$$ ，求下面的似然函数的极大值会容易许多：

$$L(\theta;X,Z)=\log{P(X, Z;\theta)}$$

问题是实际上我们没法观察到 $$z$$ 的值，只能在给定 $$\theta$$ 时求 $$z$$ 的后验概率 $$P(z|x;\theta)$$ 。[^bayes_theorem] EM 算法就可以帮我们打破这样的困境。

[^bayes_theorem]:
	一般可以利用[贝叶斯定理](http://en.wikipedia.org/wiki/Bayes%27_theorem)：
	
	$$P(z|x;\theta) = \frac{P(x|z;\theta)P(z;\theta)}{\sum_z{P(x|z;\theta)P(z;\theta)}}$$
	
	而 $$P(x|z;\theta)$$ 和 $$P(z;\theta)$$ 往往是模型假设的一部分。

## 算法 ##
下面给出 EM 算法的过程。其中$$\theta_t$$ 是第 t-1 次迭代时算出的 $$\theta$$ 值；$$\theta_0$$ 为任意初值。

<blockquote>Repeat until converge {
<ol>
	<li>(E-step) Calculate \( P(Z|X;\theta_t) \), in order to get:
$$
\begin{eqnarray}
E_{Z|X;\theta_t}[L(\theta;X,Z)] &amp;:=&amp; E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}] \\
&amp;=&amp; \sum_Z P(Z|X;\theta_t) \log{P(X,Z;\theta)}
\end{eqnarray}
$$
</li>
	<li>(M-step) $$\theta_{t+1} := \arg\max_\theta E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}]$$</li>
</ol>
}</blockquote>


对，就这么短。所以我总觉得称之为 algorithm 不如称之为 method 更恰当。上面的过程在收敛后就得到了我们需要的 $$ \theta=\arg\max_\theta{L(\theta;X)} $$ [^local_optima]。

[^local_optima]: 实际上在某些特殊情况下，$$\theta$$ 还可能收敛在局部最优点或鞍点上。这时可以多跑几次算法，每次随机不同的 $$\theta_0$$，最后取最好的结果。为简明起见，本文忽略这种情况。

先简单说说这短短两步都做了些啥。EM 算法每次迭代都建立在上轮迭代对 $$\theta$$ 的最优值的估计 $$\theta_t$$ 上，利用它可以求出 $$Z$$ 的后验概率 $$P(Z|X;\theta_t)$$ ，进而求出 $$L(\theta;X,Z)$$ 在分布 $$Z \sim P(Z|X;\theta)$$ 上的期望 $$E_{Z|X;\theta_t}[L(\theta;X,Z)]$$。在第一节中我们提到 $$ \arg\max_\theta L(\theta;X,Z) $$ 在未知 $$Z$$ 的情况下难以直接计算，于是 EM 算法就转而通过最大化它的期望 $$E_{Z|X;\theta_t}[L(\theta;X,Z)]$$ 来逼近 $$\theta$$ 的最优值，得到 $$\theta_{t+1}$$ 。注意由于 $$L(\theta;X,Z)$$ 的这个期望是在 $$Z$$ 的一个分布上求的，这样得到的表达式就只剩下 $$\theta$$ 一个未知量，因而绕过了 $$z$$ 未知的问题。而 $$\theta_{t+1}$$ 又可以作为下轮迭代的基础，继续向最优逼近。算法中 E-step 就是在利用 $$\theta_t$$ 求期望 $$E_{Z|X;\theta_t}[L(\theta;X,Z)]$$，这就是所谓“Expectation”；M-step 就是通过寻找 $$\theta_{t+1}$$ 最大化这个期望来逼近 $$ \theta $$ 的最优值，这就叫“Maximization”。EM 算法因此得名。

另外，如果数据满足独立同分布的条件，分别枚举 $$z^{(i)}$$ 的值可能要比枚举整个 $$Z$$ 方便些，可把 $$E_{Z|X;\theta_t}[L(\theta;X,Z)]$$ 替换成：

$$
\begin{eqnarray}
\sum_i E_{z^{(i)}|x^{(i)};\theta_t}[L(\theta;x^{(i)},z^{(i)}]
&:=& \sum_i E_{z^{(i)}|x^{(i)};\theta_t}[\log{P(x^{(i)},z^{(i)};\theta)}] \\
&=& \sum_i \sum_{z^{(i)}} P(z^{(i)}|x^{(i)};\theta_t) \log{P(x^{(i)},z^{(i)};\theta)}
\end{eqnarray}
$$

## 原理 ##

为什么这样 E一步，M一步，一步E，一步M，就能逼近极大似然？具体而言，为什么通过迭代计算 $$\arg\max_\theta E_{Z|X;\theta_t}[L(\theta;X,Z)]$$ 可以逼近 $$\theta$$ 的最优值 $$\arg\max_\theta L(\theta;X,Z)$$？我们稍后会看到，这是因为每次迭代得到的 $$\theta_{t+1}$$ 一定比 $$\theta_t$$ 更优，即算法是在对 $$\theta$$ 的最优值做单调逼近。

不过首先让我们先抛开最大似然，考虑一个更一般的问题。假设有一个凹函数 $$ F(\theta) $$，我们想求 $$ \arg\max_\theta F(\theta) $$，但直接求很困难。不过对于任意给定的 $$ \theta_t $$，假设我们都能找到 $$ F(\theta) $$ 的一个下界函数 $$ G_{\theta_t}(\theta) $$，满足 $$ F(\theta) \geq G_{\theta_t}(\theta) $$ 且 $$ F(\theta_t) = G_{\theta_t}(\theta_t) $$ ——我管 $$ G_{\theta_t}(\theta) $$ 这样的函数叫 $$ F $$ 的“在 $$ \theta_t $$ 处相等的下界函数”。现在考虑 $$ \theta_{t+1} := \arg\max_\theta G_{\theta_t}(\theta) $$，它一定会满足：

$$ F(\theta_{t+1}) \geq G_{\theta_t}(\theta_{t+1}) \geq G_{\theta_t}(\theta_t) = F(\theta_t) $$

也就是说，$$ \theta_{t+1} $$ 一定比 $$ \theta_t $$ 更优。而接下来我们又可以用 $$ \theta_{t+1} $$ 找到一个 $$ G_{\theta_{t+1}}(\theta) $$，再据此算出比 $$ \theta_{t+1} $$ 还优的 $$ \theta_{t+2} := \arg\max_\theta G_{\theta_{t+1}}(\theta) $$ 。如此不断迭代，就能不断步步逼近 $$ \theta $$ 的最优值了。由此可见，如果对任意 $$ \theta_t $$ 都能找到 $$F$$ 的“在 $$ \theta_t $$ 处相等的下界函数”$$ G_{\theta_t}(\theta) $$，我们就得到了一个能单调逼近 $$\theta$$ 的最优值的算法：


<blockquote>Repeat until converge {
<ol>
	<li>找到函数 \( F(\theta) \) 的“在 \( \theta_t \) 处相等的下界函数” \( G_{\theta_t}(\theta) \)</li>
	<li>\( \theta_{t+1} := \arg\max_\theta G_{\theta_t}(\theta) \)</li>
</ol>
}</blockquote>


上面的算法看起来和 EM 算法的每步都分别对应——事实上也正如此。下面是从 [PRML](http://research.microsoft.com/en-us/um/people/cmbishop/prml/) 中偷的一张图改的，展示了上述逼近的过程：

{% img /img/2011-10-13-em-algo.png %}

现在我们回到最大似然问题 $$\theta=\arg\max_\theta{L(\theta;X)}$$ 。如果我们想套用上面的算法来逼近 $$ \theta $$ 的这个最优解，就需要找到对于每个 $$ \theta_t $$，函数 $$ L(\theta;X) $$ 的“在 $$ \theta_t $$ 处相等的下界函数”。该怎么找呢？让我们从 $$ L(\theta) $$ 的初始形式开始推导：

$$
\begin{eqnarray}
L(\theta) &=& \log{P(X;\theta)} \\
&=& \log{\sum_Z P(X,Z;\theta)}
\end{eqnarray}
$$

又卡在这个$$\log$$套$$\sum$$的形式上了……我们说过麻烦在于观察不到 $$Z$$ 的值，那不妨给它任意引入一个概率分布 $$Q(Z)$$ [^distribution]，利用分子分母同乘 $$Q(Z)$$ 的小 trick，得到：

[^distribution]: $$Q(Z)$$ 为概率分布，意即需满足 $$\sum_Z Q(Z) = 1$$ 且 $$Q(Z) \geq 0$$

$$
\begin{eqnarray}
L(\theta) &=& \log{\sum_Z P(X,Z;\theta)} \\
&=& \log{\sum_Z Q(Z) \frac{P(X,Z;\theta)}{Q(Z)}} \\
&=& \log E_{Z \sim Q}\left[ \frac{P(X,Z;\theta)}{Q(Z)} \right]
\end{eqnarray}
$$

根据 Jensen 不等式 [^jesen]，对于任意分布 $$Q$$ 都有：

[^jesen]:
	Jensen 不等式：
	
	$$f$$ 为凸函数，$$X$$ 为随机变量。则
	
	$$ E[f(X)] \geq f(EX) $$
	
	若 $$f$$ 是严格凸的，则上式取等号当前仅当 $$X$$ 为常数。

	在这里 $$\log$$ 函数是严格凹的，所以要把上面的不等号方向调转。

$$
L(\theta) = \log E_{Z \sim Q}\left[ \frac{P(X,Z;\theta)}{Q(Z)} \right] \geq E_{Z \sim Q}\left[ \log\frac{P(X,Z;\theta)}{Q(Z)} \right]
$$

且上面的不等式在 $$ \frac {P(X,Z;\theta)} {Q(Z)}$$ 为常数时取等号。

于是我们就得到了 $$ L(\theta;X) $$ 的一个下界函数。我们要想套用上面的算法，还要让这个不等式在 $$ \theta_t $$ 处取等号，这就这要求在 $$ \theta = \theta_t $$ 时 $$ \frac {P(X,Z;\theta)} {Q(Z)}$$ 为常数，即 $$Q(Z) \propto P(X,Z;\theta_t)$$。由于 $$Q(Z)$$ 是一个概率分布，必须满足 $$\sum_z Q_i(z) = 1$$，所以这样的 $$Q(Z)$$ 只能是 $$Q(Z) = \frac {P(X,Z;\theta_t)} {\sum_Z P(X,Z;\theta_t)} = P(Z|X;\theta_t)$$。那我们就把 $$ Q(Z) = P(Z|X;\theta_t) $$ 代入上式，得到：

$$
L(\theta) \geq E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right]
$$

且该不等式在 $$ \theta = \theta_t $$ 时取到等号。那么……$$ E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right] $$ 就是 $$ L(\theta;X) $$ 的“在 $$ \theta_t $$ 处相等的下界函数”——这不就是我们要找的么！于是把它塞进本节开始得到的算法里替换“$$ G_{\theta_t}(\theta) $$”就可以用啦。也就是说，迭代计算 $$ \arg\max_\theta E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right] $$ 就可以逼近 $$ \theta $$ 的最优值了。而由于利用 Jensen 不等式的那一步搞掉了$$\log$$套$$\sum$$的形式，它算起来往往要比直接算 $$ \arg\max_\theta{L(\theta;X)} $$ 容易不少。

我们还可以再做几步推导，得到一个更简单的形式：

$$\begin{eqnarray}
\theta_{t+1}
&:=& \arg\max_\theta E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right] \\
&=& \arg\max_\theta \sum_{Z} P(Z|X;\theta_t) \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \\
&=& \arg\max_\theta \sum_{Z} [P(Z|X;\theta_t)\log P(X,Z;\theta) - P(Z|X;\theta_t) \log P(Z|X;\theta_t)] \\
&=& \arg\max_\theta \sum_{Z} P(Z|X;\theta_t)\log P(X,Z;\theta) \\
&=& \arg\max_\theta E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}]
\end{eqnarray}$$

其中倒数第二步是因为 $$- P(Z|X;\theta_t) \log P(Z|X;\theta_t)]$$ 这一项与 $$\theta$$ 无关，所以就直接扔掉了。这样就得到了本文第二节 EM 算法中的形式——它就是这么来的。

以上就是 EM 了。至于独立同分布的情况推导也类似。

顺带一提，$$ \arg\max_\theta E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}] $$ 有时也比较难算。这时我们其实可以退而求其次，不要求这个期望最大化了，只要它在 $$ \theta_{t+1} $$ 处的值大于在 $$ \theta_t $$ 处的值就行了。根据上面的推导，这样也能逼近 $$ \theta $$ 的最优值，只是收敛速度较慢。这就是所谓 GEM (Generalized EM) 算法了。

p.s. [MathJax](http://www.mathjax.org/) 很神嘛。

p.p.s. 这篇笔记竟然断断续续写写改改了两天多，我对 EM 的认识也越来越清晰。“[‘教’是最好的‘学’](http://mindhacks.cn/2009/02/15/why-you-should-start-blogging-now/)”真是一点没错。

---
更新历史:

- 2011.10.12 重写了“原理”部分，把利用函数的“在 $$\theta_t$$ 处相等的下界函数”逼近 $$\theta$$ 的最优值的算法单独提到前面说，这样似乎清楚很多。
- 2011.10.13 修正了对在利用 Jensen 不等式的那一步要取 $$ Q(Z) = P(Z|X;\theta_t) $$ 的解释

---