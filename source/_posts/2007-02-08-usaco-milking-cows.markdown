---
layout: post
title: "[USACO] Milking Cows / [Vijos1165] 火烧赤壁"
date: 2007-02-08 15:44
comments: true
categories: [OI, Algorithm, USACO]
---

# Milking Cows #

Three farmers rise at 5 am each morning and head for the barn to milk three cows. The first farmer begins milking his cow at time 300 (measured in seconds after 5 am) and ends at time 1000. The second farmer begins at time 700 and ends at time 1200. The third farmer begins at time 1500 and ends at time 2100. The longest continuous time during which at least one farmer was milking a cow was 900 seconds (from 300 to 1200). The longest time no milking was done, between the beginning and the ending of all milking, was 300 seconds (1500 minus 1200).
Your job is to write a program that will examine a list of beginning and ending times for N (1 <= N <= 5000) farmers milking N cows and compute (in seconds):

- The longest time interval at least one cow was milked.
- The longest time interval (after milking starts) during which no cows were being milked.

## PROGRAM NAME: milk2 ##

## INPUT FORMAT ##

<table>
<tr>
<td>Line1:</td>
<td>The single integer</td>
</tr>
<tr>
<td>Lines2..N+1:</td>
<td>Two non-negative integers less than 1000000, the starting and ending time in seconds after 0500</td>
</tr>
</table>

## OUTPUT FORMAT ##

A single line with two integers that represent the longest continuous time of milking and the longest idle time.

## SOLUTION ##

这道题是本巨菜第一次做出的涉及区间处理的题（虽然至今搞不清“离散化”是什么意思），具有重大的意义~~~~~我是参照[这个说明](http://oiflyingforever.spaces.live.com/blog/cns!5C715499A28E16A!146.entry)做的：

> 按照开始时间将挤奶信息升序排序，然后按照如下方法从左到右扫描一遍，即可得到结果。
设r1为最长连续挤奶时间，r2为最长连续空闲时间，r1、r2初始时均为0。
每条挤奶信息都是一个区间，那么我们用变量c记录当前连续区间，初始时当前区间变量为排序后的第一个区间(c=milk[1])。

> 如果下一个区间i和当前区间相交或当前区间包含区间i(milk[i].start<=c.end)，就将两个区间的并集作为当前区间 (c.end=max(c.end,milk[i].end))； 如果下一个区间i和当前区间不相交(milk[i].start>c.end)，则更新r1、r2的值(r1=max(r1,c.end- c.start)，r2=max(r2,milk[i].start-c.end))，并将区间i作为当前区间(c=milk[i])。

> 因为我们只在下一个区间和当前区间不相交时才会去更新最优解，所以最后一个连续区间我们并没有更新，因此别忘了再更新一下 r1(r1=max(r1,c.end-c.start))。
r1，r2即为所求。

源码如下：

{% codeblock milk.cpp %}
/*
ID: tom.tun1
PROG: milk2
LANG: C++
*/
#include <iostream>
#include <fstream>
using namespace std;
ifstream fin("milk2.in");
ofstream fout("milk2.out");
struct time
{
  int start;
  int end;
}milk[5000], present;
int N, MaxWork = 0, MaxBreak = 0;
int Partition(int first, int end);
void QuickSort(int first, int end);
void compute(int j);
bool intersection(struct time, struct time);//判断是否有交集
struct time unite(struct time, struct time);//求并集 
 
int
main()
{
  fin >> N;
  for (int j = 0; j < N; j++)
      fin >> milk[j].start >> milk[j].end;
  QuickSort(0, N - 1);
  present = milk[0];
 
  for (int j = 1; j < N; j++)
      compute(j);
  MaxWork = max(MaxWork, present.end - present.start);
  fout << MaxWork << ' ' << MaxBreak << endl;
  return 0;
}
 
void
compute(int j)
{
  if (intersection(milk[j], present))
      present = unite(milk[j], present);
  else
    {
      MaxWork = max(MaxWork, present.end - present.start);
      MaxBreak = max(MaxBreak, milk[j].start - present.end);
      present = milk[j];
    }
}
 
bool
intersection(struct time a, struct time b)
{
  if (a.end < b.start || b.end < a.start)
      return false;
  else
      return true;
}
 
struct time
unite(struct time a, struct time b)
{
  struct time x;
  x.start = min(a.start, b.start);
  x.end = max(a.end, b.end);
  return x;
}
 
void
QuickSort(int first, int end)
{
  if (first < end)
    {
      int pivot = Partition(first, end);
      QuickSort(first, pivot - 1);
      QuickSort(pivot + 1, end);
    }
}
int
Partition(int first, int end)
{
  int i = first, j = end;
  while (i < j)
    {
      while (i < j && milk[i].start <= milk[j].start)
          j--;
      if (i < j)
        {
          swap(milk[i], milk[j]);
          i++;
        }
      while (i < j && milk[i].start <= milk[j].start)
          i++;
      if (i < j)
        {
          swap(milk[i], milk[j]);
          j--;
        }
    }
  return i;
}
{% endcodeblock %}

虽然不优美，但是AC了~~~~多谢那位写题解的牛！

USACO上的Analysis提到里提到的方法一即此方法，方法二是我原来一直用的。<del>方法三至今看不懂，渴望有达人解释一下，多谢！</del>
我听从了ghost牛的建议进行手工单步，终于搞懂了官方给出的第三种解法，hoho~~~~兴奋中~~~~~这里特别感谢ghost给我讲qsort()是怎么用的……

该算法将每次有farmer开始或结束挤奶做为一个单独“事件”看待。每一个事件包括两个信息：事件的开始时间、该事件记录的是开始挤奶还是结束挤奶。其中后者可以用1和-1表示。先把所有事件按照时间先后排序。每次处理事件的第二个信息时直接加和即可。有人开始挤奶，人数就+1；有人结束挤奶，人数就-1.这样，我们只需要看此加和的值即能知道当前事件发生后有几个人在挤奶。

这样我们就能很容易地找到一个有人挤奶或无人挤奶的完整时间段的起始点和终点（也就是另一个完整时间段的起点）。得到长度后再与当前最大值比较……剩下就很容易了。

下面附上官方的此算法源码以及我加的详细注释（注释均针对前一语句）：

{% codeblock milk.cpp %}
#include <fstream.h>
#include <stdlib.h>
 
struct event
{
 long seconds;   /*记录该事件发生时离早上5点有多少秒*/
 signed char ss; /*若该事件是某人开始挤奶，则为1；若是某人结束挤奶，则为-1*/
};
 
int eventcmp (const event *a, const event *b)
{
 if (a->seconds != b->seconds)
  return (a->seconds - b->seconds); /*早发生的事件排在前面*/
 
 return (b->ss - a->ss);
 /* 若两个事件同时发生，
     则记录某人开始挤奶的事件排在前面*/
}
 
int main ()
{
 ifstream in;
 ofstream out;
 
 in.open("milk2.in");
 out.open("milk2.out");
 
 int num_intervals, num_events, i;
 /*num_intervals即输入的农夫数N，
    num_events即相应的事件数*/
 event events[5000 * 2];/*记录所有事件的数组*/
 
 in >> num_intervals;
 num_events = num_intervals * 2;/*很明显，事件数为农夫数的二倍*/
 for (i = 0; i < num_intervals; ++i)
 {
  in >> events[2*i].seconds; events[2*i].ss = 1;
  in >> events[2*i+1].seconds; events[2*i+1].ss = -1;
 }
 
 qsort(events, num_events, sizeof(event),
  (int(*)(const void*, const void*)) eventcmp);
  /*对所有事件进行排序，详见eventcmp处的注释*/
 
/* for (i = 0; i < num_events; ++i)
  out << events[i].seconds
    << (events[i].ss == 1 ? " start" : " stop") << endl; */
   /*测试一下排序结果如何*/
 
 int num_milkers = 0, was_none = 1;
 /*num_milkers为当前事件发生时挤奶者的数目
   （包括当前事件本身对其的影响），
    was_none为上一个事件发生时挤奶者的数目
   （包括上一事件本身对其的影响）*/
 int longest_nomilk = 0, longest_milk = 0;/*记录最大值的变量*/
 int istart, ilength;
 /*istart记录当前正在处理的完整时间段的起始位置，
    ilength是在比较当前完整时间段与最大完整时间段大小时的中间变量*/
 
 for (i = 0; i < num_events; ++i)
 {
  num_milkers += events[i].ss;
 
  if (!num_milkers && !was_none)
  /*当num_milkers==was_none==0时。
     num_milkers==0表示此时无挤奶者，
     was_none==0表示上一个“事件”时有挤奶者。
     这样后一个事件就成了上一挤奶完整时间段的终点
     和下一完整无人挤奶时间段的起点，
     应该计算结束的时间段长度并与longest_milk比较*/
 {
   ilength = (events[i].seconds - istart);
   if (ilength > longest_milk)
    longest_milk = ilength;
   istart = events[i].seconds;
  }
  else if (num_milkers && was_none)
  /*当num_milkers!=0&&was_none!=0时。
     num_milkers!=0表示此时有挤奶者，
     was_none!=0表示上一个“事件”时无挤奶者。
     这样后一个事件就成了上一无人挤奶完整时间段的终点
     和下一完整挤奶时间段的起点，
     应该计算计算结束的时间段长度并与longest_nomilk比较*/
  {
   if (i != 0)
   {
    ilength = (events[i].seconds - istart);
    if (ilength > longest_nomilk)
     longest_nomilk = ilength;
   }
   istart = events[i].seconds;
  }
 
  was_none = (num_milkers == 0);
 }
 
 out << longest_milk << " " << longest_nomilk << endl;
 
 return 0;
}
{% endcodeblock %}


----------

解决了上面那道题，我就做了原来不会做的 Vijos 上的那个火烧赤壁，巩固一下方法。

# 火烧赤壁 #

## 描述 Description ##
曹操平定北方以后，公元208年，率领大军南下，进攻刘表。他的人马还没有到荆州，刘表已经病死。他的儿子刘琮听军声势浩大，吓破了胆，先派人求降了。

孙权任命周瑜为都督，拨给他三万水军，叫他同刘备协力抵抗曹操。

隆冬的十一月，天气突然回暖，刮起了东南风。

没想到东吴船队离开北岸大约二里距离，前面十条大船突然同时起火。火借风势，风助火威。十条火船，好比十条火龙一样，闯进曹军水寨。那里的船舰，都挤在一起，又躲不开，很快地都烧起来。一眨眼工夫，已经烧成一片火海。

曹操气急败坏的把你找来，要你钻入火海把连环线上着火的船只的长度统计出来！

## 输入格式 Input Format ##
第一行：N
以后N行，每行两个数：Ai  Bi(表示连环线上着火船只的起始位置和终点,-10^9<=Ai,Bi<=10^9)

## 输出格式 Output Format ##
输出着火船只的总长度

## 样例输入 Sample Input ##
3
-1 1
5 11
2 9

## 样例输出 Sample Output ##
11

## 注释 Hint ##
n<=20000
如果Ai=Bi是一个点则看作没有长度

## 题解 Solution ##

看看原来大牛们的题解吧：
> 线段树或者平面扫除法的一维情形
> 离散化+快排+二分查找，一定不会超时的^^

这种题解对我这样的巨菜来说和没有一样……现在终于通过Milking Cows搞定了这道问题。此题应该说比Milking Cows简单，只是要注意Ai=Bi的情况。

{% codeblock vijos1165.cpp %}
#include <iostream>
using namespace std;
int num=0;
struct ship{
 __int64 start;
 __int64 end;
}ships[20000],current;
 
struct ship Unite(struct ship,struct ship);
void QuickSort(int first,int end);
int Partition(int first,int end);
int main()
{
 int N;
 cin >> N;
 __int64 a,b;
 for(int i=0;i<N;i++)
 {
  cin >> a >> b;
  if(a!=b)
  {
   ships[num].start=a;
   ships[num].end=b;
   num++;
  }
 }
 QuickSort(0,num-1);
 /*for(int i=0;i<num;i++)
  cout << ships[i].start << '~' << ships[i].end << endl;*/
 
 __int64 length=0;
 current=ships[0];
 for(int i=1;i<num;i++)
 {
  if(ships[i].start>current.end)
  {
   length+=(current.end-current.start);
   current=ships[i];
  }
  else current=Unite(current,ships[i]);
 }
 length+=(current.end-current.start);
 cout << length << endl;
 return 0;
}
 
struct ship Unite(struct ship a,struct ship b)
{
 struct ship c;
 c.start=min(a.start,b.start);
 c.end=max(a.end,b.end);
 return c;
}
 
void QuickSort(int first,int end)
{
 if(first<end)
 {
  int pivot=Partition(first,end);
  QuickSort(first,pivot-1);
  QuickSort(pivot+1,end);
 }
}
int Partition(int first,int end)
{
 int i=first,j=end;
 while(i<j)
 {
  while(i<j&&ships[i].start<=ships[j].start) j--;
  if(i<j)
  {
   swap(ships[i],ships[j]);
   i++;
  }
  while(i<j&&ships[i].start<=ships[j].start) i++;
  if(i<j)
  {
   swap(ships[j],ships[i]);
   j--;
  }
 }
 return i;
}
{% endcodeblock %}
