---
layout: post
title: "[NOIP06] 2^k进制数"
date: 2007-09-01 23:09 
comments: true
categories: [OI, Combinatorics]
---

## 描述 ##

设r是个2^k 进制数，并满足以下条件：

（1）r至少是个2位的2^k进制数。

（2）作为2^k进制数，除最后一位外，r的每一位严格小于它右边相邻的那一位。

（3）将r转换为2进制数q后，则q的总位数不超过w。

在这里，正整数k（1≤k≤9）和w（k<w≤30000）是事先给定的。

问：满足上述条件的不同的r共有多少个？

我们再从另一角度作些解释：设S是长度为w 的01字符串（即字符串S由w个“0”或“1”组成），S对应于上述条件（3）中的q。将S从右起划分为若干个长度为k 的段，每段对应一位2k进制的数，如果S至少可分成2段，则S所对应的二进制数又可以转换为上述的2k 进制数r。

例：设k=3，w=7。则r是个八进制数（23=8）。由于w=7，长度为7的01字符串按3位一段分，可分为3段（即1，3，3，左边第一段只有一个二进制位），则满足条件的八进制数有：

2位数：高位为1：6个（即12，13，14，15，16，17），高位为2：5个，…，高位为6：1个（即67）。共6+5+…+1=21个。

3位数：高位只能是1，第2位为2：5个（即123，124，125，126，127），第2位为3：4个，…，第2位为6：1个（即167）。共5+4+…+1=15个。

所以，满足要求的r共有36个。


## 输入格式 ##

输入只有1行，为两个正整数，用一个空格隔开：k W

## 输出格式 ##

输出为1行，是一个正整数，为所求的计算结果，即满足条件的不同的r的个数（用十进制数表示），要求最高位不得为0，各数字之间不得插入数字以外的其他字符（例如空格、换行符、逗号等）。

（提示：作为结果的正整数可能很大，但不会超过200位）


## 题解 ##

想起去年NOIP做到这题时，我还是巨巨巨巨巨巨巨菜，看了这题的标题就直接放弃了……现在看来这题也不是那么难的。

题目中“从另一角度作些解释”是很重要的，这几乎直接给我们提供了算法（往下看之前请仔细阅读题目中的相关部分）。令N为2^k进制数的最大允许位数，(a_0) 为最高位允许的最大值，则有：

$$N= \left\lceil \frac{W}{K} \right\rceil$$ $$a_0=2^{W \mod K}-1$$

那么问题其实就等同于：取N个数（对应于\(2^k\)进制数中的N位），第1个数num[1]（对应于最高位）取值范围为[1,a0]，其余第2~N个数num[i]取值范围都为[1,2^K)。现从其中第i(\( 1 \leq i \leq N-1\))个数num[i]开始取数，一直取到最后一个数num[N]，要求对于任意的j&gt;i满足num[j-1]&lt;num[j]。问取数方案的总数。这就是很基础的组合数学问题了。

先不考虑第1个数，因为限制一个最大值会稍微麻烦一点。我们考虑一般情况。显然，如果取后i个数（\( 2 \leq i &lt; N \)），可供选择的数有 \(2^k-1\) 个，则方案总数就为 \(C(i,2^k-1)\)。因此，从第2~N个数开始取的方案总数就为：$$\sum_{i=2}^{n-1}C_{2^k-1}^i$$

如果从第1个数开始取，则第1个数有1~\(a_0\)共\(a0\)个选择。如果选择a(\(1 \leq a \leq a_0\))，那么[1,\(2^K\))范围内剩下比a大的数就有\(2^k-a-1\)个，剩下N-1个数的可能选择方案就有\(C(2^k-i-1,n-1)\)个。那么从第1个数开始取的总方案数就为：$$\sum_{a=1}^{a_0}C_{2^k-a-1}^{n-1}$$

综上，要求的总方案数就为：$$ans=\sum_{a=1}^{a_0}C_{2^k-a-1}^{n-1}+\sum_{i=2}^{n-1}C_{2^k-1}^i$$

其中组合数\(C(N,K)\)可以利用下面递推式加上一点记忆化来在最短时间内计算得出 $$C_n^k=C_{n-1}^{k-1}+C_{n-1}^k$$

现在按照这个写应该会很简单了。这个如果用Pascal的int64据说能过7个点，用C++的unsigned long long则能过8个，性价比相当高了。但要想AC唯有高精。

源码：

{% codeblock digital.cpp %}
#include <iostream>
#include <fstream>
#include <cmath>
#include <cassert>
#define SIZE 400
using namespace std;
class _int{
	int b[SIZE],l;
public:
	_int(){};
	_int(int n);
	int& operator()(const int&pos){return b[pos];}
	friend const _int operator+(const _int& b1,const _int& b2);
	friend ostream& operator<<(ostream& is,const _int& b);
};
_int::_int(int n){
	memset(b,0,sizeof(b));
	l=0;
	while(n!=0)
		b[l]=n%10,n/=10,l++;
}
const _int operator+(const _int& b1,const _int& b2){
	_int Ans=_int(0);
	Ans.l=b1.l;
	if(Ans.l<b2.l) Ans.l=b2.l;
	for(int i=0;i<Ans.l;i++) Ans.b[i]=b1.b[i]+b2.b[i];
	for(int i=0;i<Ans.l;i++){
		Ans.b[i+1]+=Ans.b[i]/10;
		Ans.b[i]%=10;
		if(Ans.b[Ans.l]!=0) Ans.l++;
	}
	return Ans;
}
ostream& operator<<(ostream& os,const _int& b){
	for(int i=b.l-1;i>=0;i–) os<<b.b[i];
	return os;
}
const unsigned pow2[10]={1,2,4,8,16,32,64,128,256,512};
unsigned K,W,N,a0;
_int ans,c[512][512];
bool flag[512][512];
_int C(int n,int k){
	if(n<k)	return _int(0);
	if(n==k||k==0)	return _int(1);
	assert(n<512);
	if(flag[n][k])	return c[n][k];
	flag[n][k]=1;
	return c[n][k]=C(n-1,k-1)+C(n-1,k);
}
int main(){
	ifstream cin("digital.in");
	cin >> K >> W;
	N=long(ceil(double(W)/K));
	a0=pow2[W%K]-1!=0?pow2[W%K]-1:pow2[K];
	for(int i=1;i<=a0&&pow2[K]-i-1>=N-1;i++)	ans=ans+C(pow2[K]-i-1,N-1);
	for(int i=2;i<=N-1&&pow2[K]-1>=i;i++)	ans=ans+C(pow2[K]-1,i);
	ofstream cout("digital.out");
	cout << ans << endl;
	return 0;
}
{% endcodeblock %}
