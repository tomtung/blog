---
layout: post
title: "小试模板元编程"
date: 2009-03-01 14:37 
comments: true
categories: [C++]
---

很久不更新了，再水一下吧。

前两天新开的数据结构课布置上机作业，里面又出现了不知道之前出现过多少次的[输出质数](http://acm.buaa.edu.cn/oj/problem_show.php?c=99&p=101330)。每次都交表也会很乏味，所以……这次还是要交表 - -\|\|\|  不过要玩一点小花样——让编译器在编译期把质数表算出来。

这个当然涉及到一点[模板元编程](http://zh.wikipedia.org/w/index.php?title=%E6%A8%A1%E6%9D%BF%E5%85%83%E7%B7%A8%E7%A8%8B&variant=zh-cn)了。之前虽然看了《Effective C++》里关于模板元的简介挺感兴趣，但看到《[学习C++：实践者的方法](http://blog.csdn.net/pongba/archive/2007/12/11/1930150.aspx)》里告诫不要在这种“20%场景下的复杂性”上白花时间：

> 这些细节或技术在日常编程中极少用到，尤其是各种语言缺陷衍生出来的workarounds，
> 构成了一个巨大的长尾……绝大多数只在库开发当中需要用到

我因而一直对模板元编程敬而远之。这次也只是消遣一下，并无深入学习的打算。

以下是代码：

{% codeblock prime.cpp %}
#include <iostream>
#include <vector>
#include <iterator>
#include <algorithm>

std::vector<int> Primes;

template <int toTest, int factor> // factor should be odd
class IsPrime
{
   public:
      enum {
         result = ( toTest == 2 )
         ||  toTest % factor
          && IsPrime < toTest , factor - 2 >::result
      };
};

template<int toTest>
class IsPrime<toTest, 1>
{
   public:
      enum {result = ( toTest == 2 )  || ( toTest & 1 ) };
};

template <int upperBound> // upperBound should be odd or 2
class PrimePick : public PrimePick < upperBound - 2 >
{
   public:
      enum {
         isPrime = IsPrime < upperBound, ( upperBound >> 1 ) | 1 >::result
      };
      PrimePick<upperBound>() {
         if ( isPrime )
            Primes.push_back ( upperBound );
      }
};

template<>
class PrimePick<2>
{
   public:
      PrimePick<2>() {
         Primes.push_back ( 2 );
      }
};

template<>
class PrimePick<1> : public PrimePick<2> {};

int main()
{
   PrimePick<999> PrimeInitializer;

   int m;
   std::cin >> m;
   for ( int i = 0; i < m; ++i ) {
      int n;
      std::cin >> n;

      std::vector<int>::iterator end = Primes.begin();
      while ( end != Primes.end() && *end <= n )
         ++end;

      std::ostream_iterator<int> out ( std::cout, " " );
      std::copy ( Primes.begin(), end, out );
      std::cout << std::endl;
   }
}
{% endcodeblock %}

原理比较简单，主函数第一行初始化 PrimeInitializer 时，由于继承关系，构造函数会层层递归调用，从里至外利用另一个模板类 IsPrime 判断模板参数是否是质数，并把测试确认的质数放进一个 vector 里，这样就得到了编译期计算出的质数表。IsPrime 则使用最原始的试除方法判断质数。代码里一些写得很纠结的地方，一方面是为了尽量简化计算，减少编译时间，另一方面更主要是因为 g++ 默认最大只能实例化500层模板，以题目的数据规模（1000）不纠结一下编译器会抱怨。

这个程序……很不幸没能 AC。Buaa 的 OJ 在设计时估计就考虑了这种情况，对编译时间做出了限制，在编译20秒左右还没编译成功时会结束编译，直接判 CE……这个程序在我的系统上编译需要20分钟(VC 编译)到半个小时以上( g++ 编译)的时间，冬冬的64位 Ubuntu 上用 g++ 编译也需要将近10分钟时间。如果OJ不做这个限制估计会像当年vijos一样pending很多页吧……

恩，第一次模板元编程经历就以这样悲惨收场了 T_T

更新：

vijos[果然被卡住了](http://fanfou.com/statuses/RNTyv6omdrE) – -

{% img /img/2009-03-01-vijos-puppy-stuck.jpg 可怜的puppy %}

已作为bug报告。

