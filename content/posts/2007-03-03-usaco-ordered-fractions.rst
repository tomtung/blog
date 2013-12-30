[USACO] Ordered Fractions
=========================

:date: 2007-3-3 15:50
:tags: OI, algorithm, USACO

Consider the set of all reduced fractions between 0 and 1 inclusive with denominators less than or equal to N.

Here is the set when N = 5: :

::

    0/1 1/5 1/4 1/3 2/5 1/2 3/5 2/3 3/4 4/5 1/1

Write a program that, given an integer N between 1 and 160 inclusive, prints the fractions in order of increasing magnitude.

PROGRAM NAME: frac1
-------------------

INPUT FORMAT
------------

One line with a single integer N.

OUTPUT FORMAT
-------------

One fraction per line, sorted in order of magnitude.

SOLUTION
--------

这是一道很好过的题目。我的方法是穷举所有可能的分数，然后排序后输出。就这种最直观最笨的方法也不会超时。代码很好写，这里就略去了。

下面是我在usaco的官方Analysis上看到的解法，它利用递归直接生成分数并输出，没有互质数判断，没有排序。真是非常漂亮——虽然其中数学原理我还是有点搞不懂。比如：它怎么保证每次得到的分数分子分母都互质的？两个分数分子分母分别相加的到的分数，为什么它的值一定介于两者之间？希望能有达人仔细解释。

下面是我翻译自usaco的：

    下面是来自Russ的超快解法：

    我们发现可以把0/1和1/1分别作为起点和终点，然后通过增大分子和分母来递归地生成中间的点。

    ::

        0/1                                                             1/1
                                        1/2
                          1/3                       2/3
                1/4              2/5          3/5              3/4
            1/5      2/7     3/8    3/7    4/7   5/8     5/7        4/5

    每个分数都是由它左边和右边的分数生成的。这种想法有助于在递归过深时跳出。

.. code:: cpp

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <assert.h>

    int n;
    FILE *fout;

    /* 打印在n1/d1和n2/d2之间且分母小于等于n的分数*/
    void
    genfrac(int n1, int d1, int n2, int d2)
    {
      if(d1+d2 > n)  /*跳出递归*/
      return;

      genfrac(n1,d1, n1+n2,d1+d2);
      fprintf(fout, "%d/%d\n", n1+n2, d1+d2);
      genfrac(n1+n2,d1+d2, n2,d2);
    }

    void
    main(void)
    {
      FILE *fin;

      fin = fopen("frac1.in", "r");
      fout = fopen("frac1.out", "w");
      assert(fin != NULL && fout != NULL);

      fscanf(fin, "%d", &n);

      fprintf(fout, "0/1\n");
      genfrac(0,1, 1,1);
      fprintf(fout, "1/1\n");
    }

Update: 据查，这个解法利用了法里数列及其相关性质。详见：\ `资料1 <http://www.wikilib.com/wiki/%E6%B3%95%E9%87%8C%E6%95%B0%E5%88%97>`__ `资料2 <http://mathdb.org/resource_sharing/number_theory/se_farey.pdf>`__
