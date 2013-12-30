[POJ1771] Elevator Stopping Plan
================================

:date: 2009-11-21 00:33
:tags: algorithm, dynamic programming

Description
-----------

ZSoft Corp. is a software company in GaoKe Hall. And the workers in the hall are very hard-working. But the elevator in that hall always drives them crazy. Why? Because there is only one elevator in GaoKe Hall, while there are hundreds of companies in it. Every morning, people must waste a lot of time waiting for the elevator.

Hal, a smart guy in ZSoft, wants to change this situation. He wants to find a way to make the elevator work more effectively. But it’s not an easy job.

There are 31 floors in GaoKe Hall. It takes 4 seconds for the elevator to raise one floor. It means:

It costs ``(31-1)*4=120`` seconds if the elevator goes from the 1st floor to the 31st floor without stop. And the elevator stops 10 second once. So, if the elevator stops at each floor, it will cost ``30*4+29*10 = 410`` seconds (It is not necessary to calculate the stopping time at 31st floor). In another way, it takes 20 seconds for the workers to go up or down one floor. It takes ``30*20 = 600`` seconds for them to walk from the 1st floor to the 31st floor. Obviously, it is not a good idea. So some people choose to use the elevator to get a floor which is the nearest to their office.

After thinking over for a long time, Hal finally found a way to improve this situation. He told the elevator man his idea: First, the elevator man asks the people which floors they want to go. He will then design a stopping plan which minimize the time the last person need to arrive the floor where his office locates. For example, if the elevator is required to stop at the 4th, 5th and 10th floor,the stopping plan would be: the elevator stops at 4th and 10th floor. Because the elevator will arrive 4th floor at ``3*4 = 12`` second, then it will stop 10 seconds, then it will arrive 10th floor at ``3*4+10+6*4 = 46`` second. People who want to go 4th floor will reach their office at 12 second, people who want to go to 5th floor will reach at ``12+20 = 32`` second and people who want to go to 10th floor will reach at 46 second. Therefore it takes 46 seconds for the last person to reach his office. It is a good deal for all people.

Now, you are supposed to write a program to help the elevator man to design the stopping plan,which minimize the time the last person needs to arrive at his floor.

Input
-----

The input consists of several testcases. Each testcase is in a single line as the following: n f1 f2 … fn

It means, there are totally n floors at which the elevator need to stop, and n = 0 means no testcases any more. f1 f2 … fn are the floors at which the elevator is to be stopped (n <= 30, 2 <= f1 < f2 … fn <= 31). Every number is separated by a single space.

Output
------

For each testcase, output the time the last reading person needs in the first line and the stopping floors in the second line. Please note that there is a summary of the floors at the head of the second line. There may be several solutions, any appropriate one is accepted. No extra spaces are allowed.

Source
------

Asia Guangzhou 2003

Solution
--------

很久不更新了，写个水水的解题报告充数。。。这是最近做的算法习题，网上看到这题的题解都是二分+贪心的，这里提供一个dp解法。

理解题意的时候有一点需要特别注意：题目所描述的整个过程是“并行”的。所以所有人都到达各自楼层的用时只与最晚到达的人有关。

首先，由于去各楼层乘客的具体数目对结果没有影响，为表述方便，我们假设每个目标楼层只有一个人要去，并且把各个目标楼层与要去该楼层的那个乘客对应。下面在说“电梯里还剩i个人”的时候，就是在说“电梯里的乘客还要去i个楼层”。

粗略的阶段划分和状态表示还是很简单的。

电梯从第1层开始层层上升，每层都看做一个阶段，任意时刻的状态都可以由“电梯在几楼”和“电梯上都有谁”这两个参数唯一确定。初始状态就是“电梯在1楼”和“所有人都在电梯上”。

在每个阶段需要做出决策，选择让电梯上的哪些人下来自己走（如果没人下来就表示电梯在这层不停）。每个决策发生后，原来电梯里的人被分成两拨：一拨留在电梯上继续上升，另一拨离开电梯开始爬楼锻炼身体。要求某个状态下电梯里的所有人到达各自楼层所需的最短时间，只需要找到一个最优的决策，使得上述两拨人中最晚到达的人尽早到达。

即，若设决策后留在电梯里的人全部到达各自楼层需要时间 T1，离开电梯的人全部到达需要时间 T2，则要求的就是 min{ max(T1, T2) }。其中 T1 可由“当前层数+1”和“决策后剩下的人”确定的状态得到；T2 则是下电梯的人中走的最远的那位所花的时间。

按照上述想法很容易列出转移方程。但是“电梯上都有谁”这一参数有 2^n 种取值，整个算法的复杂度因此能到达令人发指的O(m\*2^2n)，对于m=31，n=30的数据规模这是不可接受的。

我们需要设法减少需要考虑的状态数目。下面给出两个引理：

1. 电梯决定停在第k层时：要去 1..k 层的人应选择在这时下电梯，这样一定可以得到当前决策下的一个最优解。如图：

|image1|

2. 电梯在第k层时，若要去 k+r 层的人选择在这时下电梯，则：要去k+1..k+r-1层的人也应选择在此时下电梯，这样一定可以得到当前决策下的一个最优解。如图：

|image2|

以上两点很容易证明。由这两点可以得到一个很简单但足以解决问题的结论：

**无论电梯停在哪一层，若要去第 k 层的人选择在这时下电梯，则：所有要去低于k层（第1..k-1层）的人也应选择在此时下电梯，这样一定可以得到当前决策下的一个最优解。**\ 如图：

|image3|

也就是说，如果把初始时的 n 名乘客按照各自要去的层数从高到低（注意此顺序与输入相反）排列，并依此编号为第 1、2、3…n 个人，第 i 个人要去第 f[i] 层（f[1]>f[2]>…>f[n]），那么可以认为\ *任意时刻电梯里乘客的编号都是 1, 2,..,x 这样一个连续序列*\ 。也就是说，对于电梯里的人我们只需要考虑编号为 1, 2, 3 或 1, 2, 3, 4, 5 这样连续排列的情况，而无需考虑 1, 2, 4（缺3）或2, 3, 4（缺1）这样的情况。

|image4|

这样一来，每个状态都能由两个数[i,j]来表示：电梯在第i层，电梯里有j个人，即要去楼层最高的第1,2,..,j个人。

下面给出转移方程：

``f[i,j]``\ 表示电梯在第i层，电梯上有要去楼层最高的j个人时，电梯上的人全部到达各自楼层所需的最短时间

::

    f[i,j] = min{ max(t1, t2) } (0<=k<=j)

    t1 = f[i+1, k] + 电梯停留时间 + 电梯上升一层所用时间

    t2 = max{ |d[l] – i| * 人爬一层楼所用时间 } ( k+1<=l<=j )

边界条件、最优解的构造方法以及其它细节问题不再赘述，详见代码。复杂度O(m\*n^2)。代码中其实还有优化的空间，但已经是0ms过的，没必要了。

.. code:: cpp

    #include <iostream>
    using std::cin;
    using std::cout;
    using std::endl;

    #include <cstring>
    using std::memset;

    #include <algorithm>
    using std::max;

    #include <cmath>
    using std::abs;

    #include <limits>
    using std::numeric_limits;

    #include <vector>
    using std::vector;

    const int maxN = 30, maxF = 31;
    const int ve = 4, st = 10, vw = 20; // 电梯上一层所需时间；电梯停一层所需时间；人走一层所需时间

    int n, f[maxN + 1];

    bool input()
    {
        cin >> n;
        if (n==0) return false;

        // 注意：f[1..n]中楼层数从高到底排列
        for (int i = n; i>=1; --i)
            cin >> f[i];

        return true;
    }

    int dp[maxF + 1][maxN + 1], nextJ[maxF + 1][maxN + 1];

    // 现在电梯在第currF层，第L到第R人离开电梯
    // 函数返回这些离开电梯的人中最晚到达目的楼层所需的时间
    int tLeave(int currF, int l, int r)
    {
        if (l>r)  return 0;
        // 仅需考虑两端
        return max(abs(currF-f[l]), abs(currF-f[r])) * vw;
    }

    // 现在电梯在第i层，电梯里本来有j个人，在要下电梯的人离开后还剩jj个人
    // 函数返回这些留在电梯里的人中最晚到达目的楼层所需的时间
    int tStay(int i, int j, int jj)
    {
        // 没人下电梯
        if (j==jj)
            return dp[i+1][jj] + ve;
        // 所有人都离开电梯
        else if (jj==0)
            return 0;
        // 第1层不计算电梯停留时间
        else if (i==1)
            return dp[i+1][jj] + ve;
        //普通情况
        else
            return dp[i+1][jj] + ve + st;
    }

    void calculate()
    {
        // 边界：电梯在顶楼时所有人都必须下电梯
        int topFloor = f[1];
        for (int j = 1; j<=n; ++j)
            dp[topFloor][j] = tLeave(topFloor,1,j);

        for (int i = topFloor - 1; i>=1; --i)
            for (int j = 1; j<=n; ++j)
            {
                dp[i][j] = numeric_limits<int>::max();
                for (int jj = 0; jj <= j; ++jj)
                {
                    // 取离开电梯的人和留下的人中的最晚到达者
                    int tmp = max(tStay(i,j,jj),tLeave(i,jj+1,j));
                    if (dp[i][j] > tmp)
                    {
                        dp[i][j] = tmp;
                        nextJ[i][j] = jj;
                    }
                }
            }
        cout << dp[1][n] << endl;
    }

    void rebuildSolution()
    {
        vector<int> stops;
        int j = nextJ[1][n], topFloor = f[1];
        for (int i = 2; i<=topFloor; ++i)
            if (nextJ[i][j]!=j)
            {
                stops.push_back(i);
                j = nextJ[i][j];
                if (j==0) break;
            }

        cout << stops.size();
        for (int i = 0; i!=stops.size(); ++i)
            cout << ' ' << stops[i];
        cout << endl;
    }

    void solve()
    {
        memset(dp,0,sizeof(dp));
        memset(nextJ,0,sizeof(nextJ));
        calculate();
        rebuildSolution();
    }

    int main()
    {
        while (input())
            solve();
    }

.. |image1| image:: /images/2009-11-21-poj1771_1.png
.. |image2| image:: /images/2009-11-21-poj1771_2.png
.. |image3| image:: /images/2009-11-21-poj1771_3.png
.. |image4| image:: /images/2009-11-21-poj1771_4.png
