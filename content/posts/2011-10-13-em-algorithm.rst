Expectation-Maximization(EM) 算法
=================================

:date: 2011-10-13 00:54
:tags: statistics, algorithm, machine learning

Expectation-Maximization 算法是统计学中用来给带\ `隐含变量 <http://en.wikipedia.org/wiki/Latent_variable>`__\ 的模型做最大似然（和最大后验概率）的一种方法。EM 的应用特别广泛，经典的比如做概率密度估计用的 `Gaussian Mixture Model <http://en.wikipedia.org/wiki/Gaussian_mixture_model>`__\ 。这两天我或许还会写 p 的笔记放上来，也是 EM 应用的例子。

下面我会先解释 EM 算法要解决的问题，然后直接给出算法的过程，最后再说明算法的正确性。

问题
----

首先我们定义要解决的问题。给定一个训练集 :math:`X=\{x^{(1)},...,x^{(m)}\}`\ ，我们希望拟合包含隐含变量 :math:`z` 的模型 :math:`P(x,z;\theta)` 中的参数 :math:`\theta`\ 。根据模型的假设，每个我们观察到的 :math:`x^{(i)}` 还对应着一个我们观察不到的隐含变量 :math:`z^{(i)}`\ ，我们记 :math:`Z=\{z^{(1)},...,z^{(m)}\}`\ 。做最大对数似然就是要求 :math:`\theta` 的“最优值”：

.. math:: \theta=\arg\max_\theta{L(\theta;X)}

其中

.. math:: L(\theta;X)=log{P(X;\theta)}=\log{\sum_Z P(X,Z;\theta)}

想用这个 :math:`\log` 套 :math:`\sum` 的形式直接求解 :math:`\theta` 往往非常困难。而如果能观察到隐含变量 :math:`z` ，求下面的似然函数的极大值会容易许多：

.. math:: L(\theta;X,Z)=\log{P(X, Z;\theta)}

问题是实际上我们没法观察到 :math:`z` 的值，只能在给定 :math:`\theta` 时求 :math:`z` 的后验概率 :math:`P(z|x;\theta)` 。  [1]_ EM 算法就可以帮我们打破这样的困境。

算法
----

下面给出 EM 算法的过程。其中 :math:`\theta_t` 是第 t-1 次迭代时算出的 :math:`\theta` 值；\ :math:`\theta_0` 为任意初值。

    Repeat until converge {

        1. (E-step) 计算 :math:`P(Z|X;\theta_t)` 以得到

           .. math::

              E_{Z|X;\theta_t}[L(\theta;X,Z)]
              &:= E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}] \\\\
              &= \sum_Z P(Z|X;\theta_t) \log{P(X,Z;\theta)}

        2. (M-step)

           .. math:: \theta_{t+1} := \arg\max_\theta E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}]

    }

对，就这么短。所以我总觉得称之为 algorithm 不如称之为 method 更恰当。上面的过程在收敛后就得到了我们需要的 :math:`\theta=\arg\max_\theta{L(\theta;X)}`  [2]_。

先简单说说这短短两步都做了些啥。EM 算法每次迭代都建立在上轮迭代对 :math:`\theta` 的最优值的估计 :math:`\theta_t` 上，利用它可以求出 :math:`Z` 的后验概率 :math:`P(Z|X;\theta_t)` ，进而求出 :math:`L(\theta;X,Z)` 在分布 :math:`Z \sim P(Z|X;\theta)` 上的期望 :math:`E_{Z|X;\theta_t}[L(\theta;X,Z)]`\ 。在第一节中我们提到 :math:`\arg\max_\theta L(\theta;X,Z)` 在未知 :math:`Z` 的情况下难以直接计算，于是 EM 算法就转而通过最大化它的期望 :math:`E_{Z|X;\theta_t}[L(\theta;X,Z)]` 来逼近 :math:`\theta` 的最优值，得到 :math:`\theta_{t+1}` 。注意由于 :math:`L(\theta;X,Z)` 的这个期望是在 :math:`Z` 的一个分布上求的，这样得到的表达式就只剩下 :math:`\theta` 一个未知量，因而绕过了 :math:`z` 未知的问题。而 :math:`\theta_{t+1}` 又可以作为下轮迭代的基础，继续向最优逼近。算法中 E-step 就是在利用 :math:`\theta_t` 求期望 :math:`E_{Z|X;\theta_t}[L(\theta;X,Z)]`\ ，这就是所谓“Expectation”；M-step 就是通过寻找 :math:`\theta_{t+1}` 最大化这个期望来逼近 :math:`\theta` 的最优值，这就叫“Maximization”。EM 算法因此得名。

另外，如果数据满足独立同分布的条件，分别枚举 :math:`z^{(i)}` 的值可能要比枚举整个 :math:`Z` 方便些，可把 :math:`E_{Z|X;\theta_t}[L(\theta;X,Z)]` 替换成：

.. math::

   \sum_i E_{z^{(i)}|x^{(i)};\theta_t}[L(\theta;x^{(i)},z^{(i)}]
   &:= \sum_i E_{z^{(i)}|x^{(i)};\theta_t}[\log{P(x^{(i)},z^{(i)};\theta)}] \\\\
   &= \sum_i \sum_{z^{(i)}} P(z^{(i)}|x^{(i)};\theta_t) \log{P(x^{(i)},z^{(i)};\theta)}

原理
----

为什么这样 E一步，M一步，一步E，一步M，就能逼近极大似然？具体而言，为什么通过迭代计算 :math:`\arg\max_\theta E_{Z|X;\theta_t}[L(\theta;X,Z)]` 可以逼近 :math:`\theta` 的最优值 :math:`\arg\max_\theta L(\theta;X,Z)`\ ？我们稍后会看到，这是因为每次迭代得到的 :math:`\theta_{t+1}` 一定比 :math:`\theta_t` 更优，即算法是在对 :math:`\theta` 的最优值做单调逼近。

不过首先让我们先抛开最大似然，考虑一个更一般的问题。假设有一个凹函数 :math:`F(\theta)` ，我们想求 :math:`\arg\max_\theta F(\theta)` ，但直接求很困难。不过对于任意给定的 :math:`\theta_t`\ ，假设我们都能找到 :math:`F(\theta)` 的一个下界函数 :math:`G_{\theta_t}(\theta)`\ ，满足 :math:`F(\theta) \geq G_{\theta_t}(\theta)` 且 :math:`F(\theta_t) = G_{\theta_t}(\theta_t)` ——我管 :math:`G_{\theta_t}(\theta)` 这样的函数叫 :math:`F` 的“在 :math:`\theta_t` 处相等的下界函数”。现在考虑 :math:`\theta_{t+1} := \arg\max_\theta G_{\theta_t}(\theta)`\ ，它一定会满足：

.. math:: F(\theta_{t+1}) \geq G_{\theta_t}(\theta_{t+1}) \geq G_{\theta_t}(\theta_t) = F(\theta_t)

也就是说， :math:`\theta_{t+1}` 一定比 :math:`\theta_t` 更优。而接下来我们又可以用 :math:`\theta_{t+1}` 找到一个 :math:`G_{\theta_{t+1}}(\theta)`\ ，再据此算出比 :math:`\theta_{t+1}` 还优的 :math:`\theta_{t+2} := \arg\max_\theta G_{\theta_{t+1}}(\theta)` 。如此不断迭代，就能不断步步逼近 :math:`\theta` 的最优值了。由此可见，如果对任意 :math:`\theta_t` 都能找到 :math:`F` 的“在 :math:`\theta_t` 处相等的下界函数” :math:`G_{\theta_t}(\theta)`\ ，我们就得到了一个能单调逼近 :math:`\theta` 的最优值的算法：

    Repeat until converge {

        1. 找到函数 :math:`F(\theta)` 的“在 :math:`\theta_t` 处相等的下界函数” :math:`G_{\theta_t}(\theta)`
        2. 更新参数

           .. math:: \theta_{t+1} := \arg\max_\theta G_{\theta_t}(\theta)

    }

上面的算法看起来和 EM 算法的每步都分别对应——事实上也正如此。下面是从 `PRML <http://research.microsoft.com/en-us/um/people/cmbishop/prml/>`__ 中偷的一张图改的，展示了上述逼近的过程：

|image0|

现在我们回到最大似然问题 :math:`\theta=\arg\max_\theta{L(\theta;X)}` 。如果我们想套用上面的算法来逼近 :math:`\theta` 的这个最优解，就需要找到对于每个 :math:`\theta_t`\ ，函数 :math:`L(\theta;X)` 的“在 :math:`\theta_t` 处相等的下界函数”。该怎么找呢？让我们从 :math:`L(\theta)` 的初始形式开始推导：

.. math::

   L(\theta)
   &= \log{P(X;\theta)} \\\\
   &= \log{\sum_Z P(X,Z;\theta)}

又卡在这个 :math:`\log` 套 :math:`\sum` 的形式上了……我们说过麻烦在于观察不到 :math:`Z` 的值，那不妨给它任意引入一个概率分布 :math:`Q(Z)`  [3]_，利用分子分母同乘 :math:`Q(Z)` 的小 trick，得到：

.. math::

   L(\theta)
   &= \log{\sum_Z P(X,Z;\theta)} \\\\
   &= \log{\sum_Z Q(Z) \frac{P(X,Z;\theta)}{Q(Z)}} \\\\
   &= \log E_{Z \sim Q}\left[ \frac{P(X,Z;\theta)}{Q(Z)} \right]

根据 Jensen 不等式  [4]_，对于任意分布 :math:`Q` 都有：

.. math:: L(\theta) = \log E_{Z \sim Q}\left[ \frac{P(X,Z;\theta)}{Q(Z)} \right] \geq E_{Z \sim Q}\left[ \log\frac{P(X,Z;\theta)}{Q(Z)} \right]

且上面的不等式在 :math:`\frac {P(X,Z;\theta)} {Q(Z)}` 为常数时取等号。

于是我们就得到了 :math:`L(\theta;X)` 的一个下界函数。我们要想套用上面的算法，还要让这个不等式在 :math:`\theta_t` 处取等号，这就这要求在 :math:`\theta = \theta_t` 时 :math:`\frac {P(X,Z;\theta)} {Q(Z)}` 为常数，即 :math:`Q(Z) \propto P(X,Z;\theta_t)`\ 。由于 :math:`Q(Z)` 是一个概率分布，必须满足 :math:`\sum_z Q_i(z) = 1`\ ，所以这样的 :math:`Q(Z)` 只能是 :math:`Q(Z) = \frac {P(X,Z;\theta_t)} {\sum_Z P(X,Z;\theta_t)} = P(Z|X;\theta_t)`\ 。那我们就把 :math:`Q(Z) = P(Z|X;\theta_t)` 代入上式，得到：

.. math:: L(\theta) \geq E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right]

且该不等式在 :math:`\theta = \theta_t` 时取到等号。那么…… :math:`E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right]` 就是 :math:`L(\theta;X)` 的“在 :math:`\theta_t` 处相等的下界函数”——这不就是我们要找的么！于是把它塞进本节开始得到的算法里替换“ :math:`G_{\theta_t}(\theta)` ”就可以用啦。也就是说，迭代计算 :math:`\arg\max_\theta E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right]`\ 就可以逼近 :math:`\theta` 的最优值了。而由于利用 Jensen 不等式的那一步搞掉了\ :math:`\log`\ 套\ :math:`\sum`\ 的形式，它算起来往往要比直接算 :math:`\arg\max_\theta{L(\theta;X)}` 容易不少。

我们还可以再做几步推导，得到一个更简单的形式：

.. math::

   \theta_{t+1}
   &:= \arg\max_\theta E_{Z|X;\theta_t}\left[ \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \right] \\\\
   &\equiv \arg\max_\theta \sum_{Z} P(Z|X;\theta_t) \log\frac{P(X,Z;\theta)}{P(Z|X;\theta_t)} \\\\
   &= \arg\max_\theta \sum_{Z} [P(Z|X;\theta_t)\log P(X,Z;\theta) - P(Z|X;\theta_t) \log P(Z|X;\theta_t)] \\\\
   &= \arg\max_\theta \sum_{Z} P(Z|X;\theta_t)\log P(X,Z;\theta) \\\\
   &\equiv \arg\max_\theta E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}]

其中倒数第二步是因为 :math:`- P(Z|X;\theta_t) \log P(Z|X;\theta_t)]` 这一项与 :math:`\theta` 无关，所以就直接扔掉了。这样就得到了本文第二节 EM 算法中的形式——它就是这么来的。

以上就是 EM 了。至于独立同分布的情况推导也类似。

顺带一提，\ :math:`\arg\max_\theta E_{Z|X;\theta_t}[\log{P(X,Z;\theta)}]` 有时也比较难算。这时我们其实可以退而求其次，不要求这个期望最大化了，只要它在 :math:`\theta_{t+1}` 处的值大于在 :math:`\theta_t` 处的值就行了。根据上面的推导，这样也能逼近 :math:`\theta` 的最优值，只是收敛速度较慢。这就是所谓 GEM (Generalized EM) 算法了。

p.s. `MathJax <http://www.mathjax.org/>`__ 很神嘛。

p.p.s. 这篇笔记竟然断断续续写写改改了两天多，我对 EM 的认识也越来越清晰。“\ `‘教’是最好的‘学’ <http://mindhacks.cn/2009/02/15/why-you-should-start-blogging-now/>`__\ ”真是一点没错。

.. [1]
   一般可以利用\ `贝叶斯定理 <http://en.wikipedia.org/wiki/Bayes%27_theorem>`__\ ：

   .. math:: P(z|x;\theta) = \frac{P(x|z;\theta)P(z;\theta)}{\sum_z{P(x|z;\theta)P(z;\theta)}}

   而 :math:`P(x|z;\theta)` 和 :math:`P(z;\theta)` 往往是模型假设的一部分。

.. [2]
   实际上在某些特殊情况下，\ :math:`\theta` 还可能收敛在局部最优点或鞍点上。这时可以多跑几次算法，每次随机不同的 :math:`\theta_0`\ ，最后取最好的结果。为简明起见，本文忽略这种情况。

.. [3]
   :math:`Q(Z)` 为概率分布，意即需满足 :math:`\sum_Z Q(Z) = 1` 且 :math:`Q(Z) \geq 0`

.. [4]
   Jensen 不等式：

   :math:`f` 为凸函数，\ :math:`X` 为随机变量。则

   .. math:: E[f(X)]\geq f(E[X])

   若 :math:`f` 是严格凸的，则上式取等号当前仅当 :math:`X` 为常数。

   在这里 :math:`\log` 函数是严格凹的，所以要把上面的不等号方向调转。

.. |image0| image:: /images/2011-10-13-em-algo.png
