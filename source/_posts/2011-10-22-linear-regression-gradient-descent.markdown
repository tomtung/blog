---
layout: post
title: "[学习笔记] 线性回归（及梯度下降）"
date: 2011-10-22 23:59 
comments: true
categories: [Algorithm, Machine Learning]
---
这个做的是 [Stanford 的机器学习公开课](http://www.ml-class.org/)的笔记。前两课很简单，吴大牛讲得又极清楚，我很多地方就简单记了。

线性回归解决的是一个回归问题（怎么像废话），即要预测的目标变量（target variable）是连续值。我们有一个大小为$$m$$ 的训练集，
其中数据点 $$ x^{(i)} $$ 分别对应目标变量 $$ y^{(i)} $$ $$ (1 \leq i \leq m) $$；每个 $$x^{(i)}$$ 是一个 $$n+1$$ 维向量，
$$n$$ 为一个数据点的属性（feature）数。（为后面书写简便我们在 $$n$$ 个属性前再加一维 $$ x_0^{(i)} = 1 $$，即
$$ x^{(i)} = (1, x_1^{(i)}, x_2^{(i)}, ..., x_n^{(i)})^{\rm T} $$。）给定这样一个训练集，我们希望知道对于某个训练集外的 $$ x $$，
它对应的 $$ y $$ 是什么。

线性回归的假设（hypothesis）是，数据点的属性 $$x$$ 和对应的目标变量 $$y$$ 是线性关系，可以用一条直线
$$  h_\theta(x) = \theta^{\rm T} x $$ 来拟合[^fitting]，就像下面这样（图片盗自维基）：

[^fitting]:
	这里讲得有点 sloppy 了（不过你能明白我的意思就行=.=）。更严格一点说，应该是训练集中的数据满足：
	
	$$ y^{(i)} = \theta^{\rm T} x^{(i)} + \epsilon^{(i)} $$
	
	其中 $$ \epsilon^{(i)} $$ 表示误差；各 $$ \epsilon^{(i)} $$ 满足均值为零，方差相同且互不相关
	（参见[高斯-马尔科夫定理](http://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem)）。

	顺带一提，我们如果进一步假设 $$ \epsilon^{(i)} \sim N(0,\sigma^2) $$，有
	$$ y^{(i)}|x^{(i)};\theta \sim N(\theta^{\rm T} x^{(i)},\sigma^2) $$，则这个模型成为
	[广义线性模式](http://en.wikipedia.org/wiki/Generalized_linear_model)（Generalized linear model）
	的一个特例。我们用极大log似然法
	
	$$ \arg\max_\theta L(\theta) = \arg\max_\theta \sum_i \log(P(y^{(i)}|x^{(i)};\theta)) $$
	
	可以推出和下面提到的最小二乘法一样的形式。——如果你不知道我上面在说什么，忽略吧，不碍得的。

{% img /img/2011-10-22-linear-regression.png %}

其中 $$ \theta $$ 也是一个 $$n+1$$ 维向量，就是我们想拟合的参数，因为假如能求出 $$ \theta $$，
对于一个训练集外的点 $$ x $$ 我们就能预测它对应的 $$ y = \theta^{\rm T} x $$ 了。

为了评价我们估计的 $$ \theta $$ 的优劣，我们需要引入一个目标函数/费用函数（cost function）。
根据[最小二乘法](http://en.wikipedia.org/wiki/Least_squares)，我们定义下面的 $$ J(\theta) $$
为我们需要最小化的目标函数：

$$ J(\theta) = \frac{1}{2m} \sum_i^m (h_\theta(x) - y^{(i)})^2 $$

其中 $$ 1/2m $$ 这个常系数并非必须，只是为了计算便利加上去的。我们要求的就是 $$ \arg\min_\theta J(\theta) $$。

不过在继续之前我们先把 $$ J(\theta) $$ 的记法再进一步 vectorize 一下。我们定义一个 $$ m \times n $$
的[设计矩阵](http://en.wikipedia.org/wiki/Design_matrix) $$ X $$，其第 $$i$$ 行为 $$ (x^{(i)})^{\rm T} $$，即

$$
X := \begin{pmatrix} (x^{(1)})^{\rm T} \\ (x^{(2)})^{\rm T} \\ \vdots \\ (x^{(m)})^{\rm T} \end{pmatrix}
= \begin{pmatrix} 1 & x_1^{(1)} & x_2^{(1)} & ... & x_n^{(1)} \\
1 & x_1^{(2)} & x_2^{(2)} & ... & x_n^{(2)} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_1^{(m)} & x_2^{(m)} & ... & x_n^{(m)} \end{pmatrix}
$$

我们再定义

$$
\begin{eqnarray}
&&\vec{y} := (y^{(1)},y^{(2)},...,y^{(m)})^{\rm T} \\
&&\vec{h_\theta} := \big( h_\theta(x^{(1)}),h_\theta(x^{(2)}),...,h_\theta(x^{(m)}) \big)^{\rm T} = X\theta
\end{eqnarray}
$$

不难推出 $$ J(\theta) $$ 可以写成下面的形式：

$$
J(\theta) = \frac{1}{2m} (\vec{h_\theta} - \vec{y})^{\rm T} (\vec{h_\theta} - \vec{y})
$$

我们还可以接着求出 $$ J(\theta) $$ 的[梯度](http://en.wikipedia.org/wiki/Gradient) $$ \nabla_\theta J(\theta) $$ [^gradient]：

[^gradient]: 推导其实挺麻烦的。教授在课上没讲，我也懒得敲了=.=

$$
\nabla_\theta J(\theta) = \frac{1}{m} X^{\rm T} (\vec{h_\theta} - \vec{y}) = \frac{1}{m} X^{\rm T} (X\theta - \vec{y})
$$

我们知道函数在极值处梯度为零，因此*第一种解法*就是直接求 $$ \nabla_\theta J(\theta) = 0 $$。这样可以得到一个解析解：

$$
\theta = (X^{\rm T} X)^{-1} X^{\rm T} \vec{y}
$$

注意其中 $$ X^{\rm T} X $$ 是一个 $$ n \times n $$ 的矩阵，而矩阵求逆的的复杂度一般是 $$ O(n^3) $$。
所以这种解法在 $$n$$ 比较小的时候非常高效，但在 $$n$$ 较大时就瞎了。

我们还知道 $$ J(\theta) $$ 上某一点的梯度向量指向 $$ J(\theta) $$ 增长最快的方向，长度为这个增长的变化率。
因此*第二种解法*就是让 $$ \theta $$ 的值向着 $$ -\nabla_\theta J(\theta) $$ 的方向，即 $$ J(\theta) $$
减小最快的方向迭代变化，这样就可以逼近 $$ J(\theta) $$ 的极小值了。因此我们可以得到下面被称为
[梯度下降](http://en.wikipedia.org/wiki/Gradient_descent)的算法：

<blockquote>Repeat until converge {

$$
\begin{eqnarray} 
\theta_{t+1} &:=& \theta_t - \alpha \nabla_\theta J(\theta) \\
&=& \theta_t - \frac{\alpha}{m} X^{\rm T} (\vec{h_\theta} - \vec{y})
\end{eqnarray} 
$$

}</blockquote>
[^incremental]

[^incremental]:
	注意这里每次迭代的运算都会考虑整个训练集，这称为批量梯度下降（batch gradient descent），
	当训练集很大时这可能导致很大的开销。我们也可以每次迭代只依次选取训练集中的一个实例 $$x^{(i)}$$，更新
	
	$$ \theta_{t+1} := \theta_{t} - \alpha (\theta^{\rm T} x^{(i)} – y^{(i)}) x^{(i)} $$
	
	这个叫增量梯度下降（incremental gradient descent）。好处在于每次迭代开销小，因而收敛速度较快，
	在处理大数据集时可能很有用。但坏处在于这算法可能永远都收敛不到极小值，而是一直围着极小值转——不过在实际应用中这个也能接受了。
	
其中 $$\alpha$$ 称为学习速率（learning rate），意思就是……学习的速率= = 这个参数控制着每次迭代 $$\theta$$ 值变化的保守或激进程度；
如果太大，一次迭代对 $$\theta$$ 改变过大，导致“冲得太猛”越过了极值点没法收敛；如果太小，一次迭代对 $$\theta$$ 改变太少，算法收敛太慢。
决定 $$ \alpha $$ 的方法是……呃，就是试，“0.01 太小，0.1 太大，0.03 有点小，咦 0.06 正好”这样。

对于线性回归和梯度下降，课上还谈到了另外两个话题。一是属性缩放（feature scaling）。如果不同属性数量级差得太大，
会严重影响梯度下降的性能。这时可以对分别对每项属性做类似“减去均值，除以标准差”这样的缩放。二是
[多项式回归](http://en.wikipedia.org/wiki/Polynomial_regression)（polynomial regression）。
属性值和目标变量值之间的关系可能不是线性的，而是多项式的关系，比如 $$ y = \theta_0 + \theta_1 x + \theta_2 x^2 $$ 这样。
但由于这个式子对于 $$ \theta $$ 仍然是线性的，所以用最小二乘法时可以直接把 $$x$$、$$x^2$$ 看成是彼此独立的不同的属性，
然后按上面的方法如法炮制。至于多项式回归时属性的次数怎么取，应该会在讲 bias-variance trade-off 的时候讲吧，我到时候再写好了。
