---
layout: post
title: "[USACO] Arithmetic Progressions"
date: 2007-2-21 16:43
comments: true
categories: [OI, Algorithm, USACO]
---

An arithmetic progression is a sequence of the form a, a+b, a+2b, …, a+nb where n=0,1,2,3,… . For this problem, a is a non-negative integer and b is a positive integer.

Write a program that finds all arithmetic progressions of length n in the set S of bisquares. The set of bisquares is defined as the set of all integers of the form p2 + q2 (where p and q are non-negative integers).

## TIME LIMIT: 5 secs ##

## PROGRAM NAME: ariprog ##

## INPUT FORMAT ##

<table border="1">
	<tr>
		<td>Line1:</td>
		<td>
			N (3 <= N <= 25), the length of progressions for which to search
		</td>
	</tr>
	<tr>
		<td>Line2:</td>
		<td>
			M (1 <= M <= 250), an upper bound to limit the search to the bisquares with 0 <= p,q <= M.
		</td>
	</tr>
</table>

## OUTPUT FORMAT ##

If no sequence is found, a singe line reading `NONE’. Otherwise, output one or more lines, each with two integers: the first element in a found sequence and the difference between consecutive elements in the same sequence. The lines should be ordered with smallest-difference sequences first and smallest starting number within those sequences first.

There will be no more than 10,000 sequences.

## SOLUTION ##

这道题就是简单的穷举，但是搞不好就超时。下面是星牛的解析：

> 这道题就是暴力搜索，时限是5s，方法是很简单的：枚举所有的可能解，没有剪枝的。

> 但是在编程细节上要注意，很多时候你的程序复杂度没有问题，但常数过大就决定了你的超时（比如说，你比别人多赋值一次，这在小数据时根本没有区别，但对于1个运行5s的大数据，你可能就要用10s甚至更多）。

> 具体来说，预处理把所有的bisquare算出来，用bene[i]记录i是否是bisquare，另外为了加速，用list记录所有的 bisquare（除去中间的空位置，这在对付大数据时很有用），list中的数据要有序。

> 然后枚举list中的数，把较小的作为起点，两数的差作为公差，接下来就是用bene判断是否存在n个等差数，存在的话就存入path中，最后排序输出。

> 运行时间：case 8 超时 （case 7 4.xs）

> 我一度曾抱怨Pascal的代码不够高效，想用c++编，但用不惯，于是又拐回Pascal来。

> 费时最多的地方是枚举list中的数，所以对这个地方的代码加一些小修改，情况就会不一样：

> 1.在判断是否存在n个等差数时，从末尾向前判断（这个不是主要的）。

> 2.在枚举list中的数时，假设为i,j，那么如果list[i]+(list[j]-list[i])×(n-1)>lim（lim是最大可能的bisquare），那么对于之后的j肯定也是大于lim的，所以直接break掉。（这个非常有效）

> AC，最大数据1.4xs。

事实上我第一次写就和这个完全一样。但是就是AC不了：第八个点开始时间就超过5s了……狂ft了一阵，试着加了些优化，还是不行，晕啊~~明明和人家的做法一样怎么就是不过呢？莫非数据改了？还是rob这会子在测评机上玩魔兽，导致速度变慢？

百思不得其解后，我找了个牛的源码仔细看了看，恍然大悟。星牛所说的利用 list[i]+(list[j]-list[i])×(n-1)>lim 进行剪枝应该是放在每次check之前。如果已经大于最大值了，则直接跳出循环，对下一个首项进行穷举。而我则是放到check之内，仅仅避免了当前枚举的首项和第二项中的计算，没有想到再继续在首项不变的情况下枚举第二项已经没有意义了。

就是这样一个小小的差别，导致了高达4s的差距。真是细节决定成败！

源码：

{% codeblock ariprog.cpp %}
/*
ID:tom.tun1
PROG:ariprog
LANG:C++
*/
#include <iostream>
#include <fstream>
#include <ctime>
using namespace std;
ifstream fin("ariprog.in");
ofstream fout("ariprog.out");
int prog_len, max_num;
bool set[125001] =
{
  0
};
int bsq[31375], bsq_num = 0, max_bsq;
int ans_num = 0;
struct Answer
{
  int a;
  int b;
}ans[40000];
int
cmp(const void* a, const void* b)
{
  return (*(int *) a - *(int *) b);
}
int
cmp2(const void* a, const void* b)
{
  struct Answer* aa = (Answer*) a;
  struct Answer* bb = (Answer*) b;
  if ((aa->b) != (bb->b))
      return((aa->b) - (bb->b));
  else
      return((aa->a) - (bb->a));
}
void
check(int a, int b)/*给出首项a和公差b，检查等差数列长度并处理*/
{
  for (int i = 0; i < prog_len / 2 + 1; i++)
      if (!set[a + b * i] || !set[a + b * (prog_len - 1 - i)])
          return;
  ans[ans_num].a = a;
  ans[ans_num].b = b;
  ans_num++;
}
int
main()
{
  fin >> prog_len >> max_num;
  max_bsq = max_num * max_num * 2;
  for (int p = 0; p <= max_num; p++)
      for (int q = p; q <= max_num; q++)
        {
          int n = p* p + q* q;
          if (!set[n])
            {
              set[n] = true;
              bsq[bsq_num++] = n;
            }
        }
  qsort(bsq, bsq_num, sizeof(bsq[0]), cmp);
  for (int i = 0; i < bsq_num - prog_len + 1; i++)
      for (int j = i + 1; j < bsq_num; j++)
        {
          int a = bsq[i], b = bsq[j] - bsq[i];
          if (a + b * (prog_len - 1) > max_bsq)
              break;
          check(a, b);
        }
  if (ans_num == 0)
      fout << "NONE" << endl;
  else
    {
      qsort(ans, ans_num, sizeof(ans[0]), cmp2);
      for (int i = 0; i < ans_num; i++)
          fout << ans[i].a << ' ' << ans[i].b << endl;
    }
  return 0;
}
{% endcodeblock %}
