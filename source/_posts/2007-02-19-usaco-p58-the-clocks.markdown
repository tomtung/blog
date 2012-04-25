---
layout: post
title: "[USACO] The Clocks"
date: 2007-2-19 2:22
comments: true
categories: [OI, Algorithm, USACO]
---

Consider nine clocks arranged in a 3×3 array thusly:

```
 |-------|    |-------|    |-------|
 |       |    |       |    |   |   |
 |---O   |    |---O   |    |   O   |
 |       |    |       |    |       |
 |-------|    |-------|    |-------|
     A            B            C

 |-------|    |-------|    |-------|
 |       |    |       |    |       |
 |   O   |    |   O   |    |   O   |
 |   |   |    |   |   |    |   |   |
 |-------|    |-------|    |-------|
     D            E            F

 |-------|    |-------|    |-------|
 |       |    |       |    |       |
 |   O   |    |   O---|    |   O   |
 |   |   |    |       |    |   |   |
 |-------|    |-------|    |-------|
     G            H            I
```

The goal is to find a minimal sequence of moves to return all the dials to 12 o’clock. Nine different ways to turn the dials on the clocks are supplied via a table below; each way is called a move. Select for each move a number 1 through 9 which will cause the dials of the affected clocks (see next table) to be turned 90 degrees clockwise.

<table border="1">
<tbody>
<tr>
<td>Move</td>
<td>Affected clocks</td>
</tr>
<tr>
<td align="middle">1</td>
<td align="middle">ABDE</td>
</tr>
<tr>
<td align="middle">2</td>
<td align="middle">ABC</td>
</tr>
<tr>
<td align="middle">3</td>
<td align="middle">BCEF</td>
</tr>
<tr>
<td align="middle">4</td>
<td align="middle">ADG</td>
</tr>
<tr>
<td align="middle">5</td>
<td align="middle">BDEFH</td>
</tr>
<tr>
<td align="middle">6</td>
<td align="middle">CFI</td>
</tr>
<tr>
<td align="middle">7</td>
<td align="middle">DEGH</td>
</tr>
<tr>
<td align="middle">8</td>
<td align="middle">GHI</td>
</tr>
<tr>
<td align="middle">9</td>
<td align="middle">EFHI</td>
</tr>
</tbody>
</table>

## EXAMPLE ##

Each number represents a time accoring to following table:

```
9 9 12          9 12 12       9 12 12        12 12 12         12 12 12
6 6 6   5 ->    9  9  9   8-> 9  9  9   4 -> 12  9  9   9 ->  12 12 12
6 3 6           6  6  6       9  9  9        12  9  9         12 12 12
```

[But this might or might not be the `correct' answer; see below.]


## PROGRAM NAME: clocks ##

## INPUT FORMAT ##

<table border="1">
<tr>
<td>Line1:</td>
<td>
Three lines of three space-separated numbers; each number represents the start time of one clock, 3, 6, 9, or 12. The ordering of the numbers corresponds to the first example above.
</td>
</tr>
</table>

## OUTPUT FORMAT ##

A single line that contains a space separated list of the shortest sequence of moves (designated by numbers) which returns all the clocks to 12:00. If there is more than one solution, print the one which gives the lowest number when the moves are concatenated (e.g., 5 2 4 6 < 9 3 1 1).

## SOLUTION ##

### 广度优先搜索 ###

这道题叙述感觉很像最少步数问题，因此我第一个想到的就是BFS。开始的思路是这样的：搜索树为一个”九叉树”，从根节点到每一个节点的路径代表一个操作序列。每一个节点扩展出9个节点。当在某一深度找到可行解时，则完成该深度所有节点的检查，取其中操作序列连接的数字最小的为答案。

但是很明显，这个算法在时间复杂度和空间复杂度上都不可接受。

我们又发现：1.任何一个操作执行4次就等于没有执行；2.同一个操作序列，各个操作的顺序改变不影响整个序列的操作效果。

根据以上两点，我们可以进行如下改进：1.任何操作不超过3次；2.为了避免同一操作序列由于顺序不同造成的节点重复，我们每次扩展节点时，都只对操作号大于当前操作号的操作进行尝试。

这样，我们就得到了一棵小得多的搜索树。这棵树的最大深度为3*9=27，节点数为4的9次方即262144，根节点到任意节点路径所代表的操作序列都是不重复的。（要知道原来的搜索树有无限的深度和节点数，且充满了重复）。而且我们发现，由于节点的生成方式，我们通过bfs找到的第一个可行解必然就是最优解。

bfs另一个麻烦的问题是内存空间。我把储存节点的struct中int改成了short int，然后又改成了char，算了算，一个节点占49字节，满足要求，这才过的。说实话，我是第一次这么一个字节一个字节地锱铢必较。源码如下：

{% codeblock clocks.cpp %}
/*
ID:tom.tun1
PROG:clocks
LANG:C++
*/
#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;
ifstream fin("clocks.in");
ofstream fout("clocks.out");
struct
{
  char Time[9];//九个钟表的状态：0,3,6,9
  char depth;//当前节点的深度
  char num[28];//记录到达该节点的各个操作编号
  char operate_times[9 + 1];//operate_times[i]的值为已经进行i操作的次数
  char operation;//记录直接得到本节点的操作
}Clocks[270000];
const char operate[9 + 1][6] =
{
  /*每个操作影响的钟表号，每个操作的序列以-1结尾*/
  0, 0, 0, 0, 0, 0, 0, 1, 3, 4, -1, 0, 0, 1, 2, -1, 0, 0, 1, 2, 4, 5, -1, 0,
  0, 3, 6, -1, 0, 0, 1, 3, 4, 5, 7, -1, 2, 5, 8, -1, 0, 0, 3, 4, 6, 7, -1, 0,
  6, 7, 8, -1, 0, 0, 4, 5, 7, 8, -1, 0
};
 
int
main()
{
  /*输入及初始化*/
  for (int i = 0,c; i < 9; i++)
    {
      fin >> c;
      if (c == 12)
          c = 0;
      Clocks[0].Time[i] = c + '0';
    }
  Clocks[0].depth = 0;
  Clocks[0].operation = 1;
  memset(Clocks[0].operate_times, 0, sizeof(Clocks[0].operate_times));
 
  /*BFS*/
  int head = 0, tail = 1;/*首尾指针*/
  bool flag = true;
  while (flag && head < tail)
    {
      for (int i = Clocks[head].operation;
           i <= 9;
           i++)/*生成的i对应操作的编号*/
        {
          /*如果某操作执行超过3次则取消本次循环*/
          if (Clocks[head].operate_times[i] + 1 > 3)
              continue;
 
          /*产生节点*/
          strcpy(Clocks[tail].Time, Clocks[head].Time);/*Time[9]部份*/
          for (int j = 0; operate[i][j] != -1; j++)
            {
              int n = operate[i][j];
              if (Clocks[head].Time[n] == '9')
                  Clocks[tail].Time[n] = '0';
              else
                  Clocks[tail].Time[n] = Clocks[head].Time[n] + 3;
            }
          Clocks[tail].depth = Clocks[head].depth + 1;/*depth部份*/
          strcpy(Clocks[tail].num, Clocks[head].num);/*num[]部份*/
          Clocks[tail].num[Clocks[head].depth] = i + '0';
          /*operate_times[]部份*/
          memcpy(Clocks[tail].operate_times, Clocks[head].operate_times,
                 sizeof(Clocks[0].operate_times));
          Clocks[tail].operate_times[i]++;
          Clocks[tail].operation = i;/*operation部份*/
          /*节点产生完毕*/
 
          /*判断是否达到目标节点*/
          flag = false;
          for (int j = 0; j < 9; j++)
              if (Clocks[tail].Time[j] != '0')
                {
                  flag = true;
                  break;
                }
          if (!flag)
              break;
          tail++;
        }
      head++;
    }
 
  /*输出答案*/
  for (int i = 0; i < strlen(Clocks[tail].num); i++)
    {
      if (i == strlen(Clocks[tail].num) - 1)
          fout << Clocks[tail].num[i] << endl;
      else
          fout << Clocks[tail].num[i] << ' ';
    }
  //system("pause");
  return 0;
}
{% endcodeblock %}

### 深度优先搜索 ###

当我们得到了上面那棵搜索树后，我们发现由于深度和节点数都不大，DFS是完全可行的，而且更易于编写，省去了节省内存空间的麻烦。如同ghost所说，此题穷举才是正解。我们搜索过程中不断更新得到的最优解，当整棵树都遍历后就输出答案。可见此算法耗时相当稳定。我这里根据深度进行了小小的剪枝，完美AC。有牛说其实完全可以不要任何剪枝的，时间就可以稳定在0.3s。

源码如下：

{% codeblock clocks.cpp %}
/*
ID:tom.tun1
PROG:clocks
LANG:C++
*/
#include <iostream>
#include <fstream>
using namespace std;
ifstream fin("clocks.in");
ofstream fout("clocks.out");
struct Clocks
{
  char Time[9];//九个钟表的状态：0,3,6,9
  int depth;//当前节点的深度
  char num[28];//记录到达该节点的各个操作编号
  int operate_times[9 + 1];//operate_times[i]的值为已经进行i操作的次数
}FirstClock;
const char operate[9 + 1][6] =
{
  /*每个操作影响的钟表号，每个操作的序列以-1结尾*/
  0, 0, 0, 0, 0, 0, 0, 1, 3, 4, -1, 0, 0, 1, 2, -1, 0, 0, 1, 2, 4, 5, -1, 0,
  0, 3, 6, -1, 0, 0, 1, 3, 4, 5, 7, -1, 2, 5, 8, -1, 0, 0, 3, 4, 6, 7, -1, 0,
  6, 7, 8, -1, 0, 0, 4, 5, 7, 8, -1, 0
};
char min_num[28], min_depth = 30;
void
search(struct Clocks Clock, int i)//DFS递归函数，Clock为当前节点，i操作编?
{
  /*节点产生*/
  struct Clocks NextClock;
  /*depth部分*/
  NextClock.depth = Clock.depth + 1;
  if (NextClock.depth > min_depth)
      return;
  /*num部分*/
  strcpy(NextClock.num, Clock.num);
  NextClock.num[NextClock.depth - 1] = i + '0';
  /*Time[9]部分*/
  strcpy(NextClock.Time, Clock.Time);
  for (int j = 0; operate[i][j] != -1; j++)
    {
      int n = operate[i][j];
      if (Clock.Time[n] == '9')
          NextClock.Time[n] = '0';
      else
          NextClock.Time[n] = Clock.Time[n] + 3;
    }
  /*operate_times部分*/
  memcpy(NextClock.operate_times, Clock.operate_times,
         sizeof(Clock.operate_times));
  if (++NextClock.operate_times[i] > 3)
      return;
 
  /*检查是否为目标节点*/
  if (strcmp(NextClock.Time, "000000000") == 0)
    {
      /*更新min_depth和min_num的值*/
      if (NextClock.depth < min_depth)
        {
          strcpy(min_num, NextClock.num);
          min_depth = NextClock.depth;
          return;
        }
    }
 
  /*递归*/
  for (int j = i; j <= 9; j++)
      search(NextClock, j);
}
int
main()
{
  /*输入及初始化*/
  for (int i = 0,c; i < 9; i++)
    {
      fin >> c;
      if (c == 12)
          c = 0;
      FirstClock.Time[i] = c + '0';
    }
  FirstClock.depth = 0;
  memset(FirstClock.operate_times, 0, sizeof(FirstClock.operate_times));
 
  /*DFS*/
  for (int i = 1; i <= 9; i++)
      search(FirstClock, i);
 
  /*输出答案*/
  for (int i = 0; i < min_depth; i++)
    {
      if (i == min_depth - 1)
          fout << min_num[i] << endl;
      else
          fout << min_num[i] << ' ';
    }
  return 0;
}
{% endcodeblock %}

### 特殊方法 ###

上面两种方法只是常规的，不足为奇。下面贴出我翻译自USACO官方Analysis的两种方法。非常精彩。

> ** Lucian Boca提交了一种常数时间的解法 **

> 你可以预先计算一个如下的矩阵：

> a[i][0],a[i][1],….,a[i][8]是“仅仅”将第i个钟表（0<=i<=8，共有9个钟表：0=A, 1=B, … 8=I）顺时针转动90度所必须的操作1、2、3…9的执行次数。这样你就得到了一个矩阵：

{% codeblock lang:cpp %}
int a[9][9]= {
	{3,3,3,3,3,2,3,2,0},
	{2,3,2,3,2,3,1,0,1},
	{3,3,3,2,3,3,0,2,3},
	{2,3,1,3,2,0,2,3,1},
	{2,3,2,3,1,3,2,3,2},
	{1,3,2,0,2,3,1,3,2},
	{3,2,0,3,3,2,3,3,3},
	{1,0,1,3,2,3,2,3,2},
	{0,2,3,2,3,3,3,3,3}
};
{% endcodeblock %}

> 这意味着**仅仅**将钟表0（钟表A）顺时针转动90度，你必须执行{3,3,3,3,3,2,3,2,0}，即操作1执行3次，操作2执行3次，…，操作8执行2次，操作9执行0次，等等。

> **仅仅**将钟表8（钟表I）顺时针转动90度，你必须执行{0,2,3,2,3,3,3,3,3}：操作1执行0次，操作2执行2次…操作9执行3次…

> 没错！你可以在一个数组v[9]里记录每一种必须执行操作的次数，答案就是它取4的模（任何一种操作执行5次与执行1次效果一样）。源码：

{% codeblock clocks.c %}
#include <stdio.h>
 
int a[9][9]= { {3,3,3,3,3,2,3,2,0},
               {2,3,2,3,2,3,1,0,1},
               {3,3,3,2,3,3,0,2,3},
               {2,3,1,3,2,0,2,3,1},
               {2,3,2,3,1,3,2,3,2},
               {1,3,2,0,2,3,1,3,2},
               {3,2,0,3,3,2,3,3,3},
               {1,0,1,3,2,3,2,3,2},
               {0,2,3,2,3,3,3,3,3} };
int v[9];
 
int main() {
    int i,j,k;
    freopen("clocks.in","r",stdin);
    for (i=0; i<9; i++) {
        scanf("%d",&k);
        for(j=0; j<9; j++)
             v[j]=(v[j]+(4-k/3)*a[i][j])%4;
    }
    fclose(stdin);
 
    k=0;
    freopen("clocks.out","w",stdout);
    for (i=0; i<9; i++)
        for (j=0; j<v[i]; j++)
            if (!k) { printf("%d",i+1); k=1; }
            else    printf(" %d",i+1);
    printf("\n");
    fclose(stdout);
    return 0;
}
{% endcodeblock %}

> **这是来自Sopot Cela的另一种解法**——没有循环，常数时间。但这个实在是极端的复杂：在比赛的环境下想要写对这样一个程序将是一种极限挑战。

{% codeblock clocks.pas %}
program clocks;
const
  INV : array[3..12] of byte =(1, 0, 0, 2, 0, 0, 3, 0, 0, 0);
 
var inp, out: text;
    a, b, c, d, e, f, g, h, i: integer;
    ax, bx, cx, dx, ex, fx, gx, hx, ix,l: integer;
    t,an: array[1..9] of integer;
begin
    assign (inp, 'clocks.in'); reset (inp);
    readln(inp, ax, bx, cx);
    readln(inp, dx, ex, fx);
    readln(inp, gx, hx, ix);
    a:=inv[ax]; b:=inv[bx]; c:=inv[cx]; d:=inv[dx];
    e:=inv[ex]; f:=inv[fx]; g:=inv[gx]; h:=inv[hx];
    i:=inv[ix];
    t[1] := (8+a+2*b+c+2*d+2*e-f+g-h) mod 4;
    t[2] := (a+b+c+d+e+f+2*g+    2*i) mod 4;
    t[3] := (8+  a+2*b+  c  -d+2*e+2*f      -h+  i) mod 4;
    t[4] := (    a+  b+2*c+  d+  e+      g+  h+2*i) mod 4;
    t[5] := (4+  a+2*b+  c+2*d  -e+2*f+  g+2*h+  i) mod 4;
    t[6] := (  2*a+  b+  c+      e+  f+2*g+  h+  i) mod 4;
    t[7] := (8+  a  -b+    2*d+2*e  -f+  g+2*h+  i) mod 4;
    t[8] := (  2*a+    2*c+  d+  e+  f+  g+  h+  i) mod 4;
    t[9] := (8      -b+  c  -d+2*e+2*f+  g+2*h+  i) mod 4;
    assign(out, 'clocks.out'); rewrite(out);
    for a := 1 to 9 do
        for b := 1 to t[a] do Begin
            inc(l);
            an[l]:=a;
        end;
    for a:=1 to l-1 do
        write(out,an[a],' ');
    write(out,an[l]);
    writeln(out); close(out)
end.
{% endcodeblock %}
