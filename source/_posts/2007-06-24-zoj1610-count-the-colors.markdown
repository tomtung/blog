---
layout: post
title: "[ZOJ1610] Count the Colors"
date: 2007-06-24 00:24
comments: true
categories: [OI, Algorithm, Size Balanced Tree]
---

Time limit: 1 Seconds

Memory limit: 32768K

Painting some colored segments on a line, some previously painted segments may be covered by some the subsequent ones.

Your task is counting the segments of different colors you can see at last.

## Input ##

The first line of each data set contains exactly one integer n, 1 <= n <= 8000, equal to the number of colored segments.

Each of the following n lines consists of exactly 3 nonnegative integers separated by single spaces:

`x1 x2 c`

`x1` and `x2` indicate the left endpoint and right endpoint of the segment, `c` indicates the color of the segment.

All the numbers are in the range `[0, 8000]`, and they are all integers.

Input may contain several data set, process to the end of file.

## Output ##

Each line of the output should contain a color index that can be seen from the top, following the count of the segments of this color, they should be printed according to the color index.

If some color can’t be seen, you shouldn’t print it.

Print a blank line after every dataset.

## Source ##

ZOJ Monthly, May 2003

## Solution ##

第一个用线段树过的题目啊~~呵呵。基础题目，虽然对我来说并不简单。在处理最后数线段条数的问题上颇费了些周折，先是问大牛，结果没搞懂，就自力更生地写出来了。。。

话说特别巧，我刚好是第1000个过这道题的人，哈哈

{% img /img/2007-06-24-zoj1610-1.jpg %}

我的时空开销：

{% img /img/2007-06-24-zoj1610-2.jpg %}

代码（发现我越来越不爱写注释了）：

{% codeblock zoj1610.cpp %}
#include <cstdio>
#include <cassert>
#include <cstring>
#define NDEBUG
//#define FILE_IO
using namespace std;
#ifdef FILE_IO
	FILE *fin = fopen("INPUT.TXT","r");
	FILE *fout= fopen("OUTPUT.TXT","w");
#else
	FILE *fin = stdin;
	FILE *fout= stdout;
#endif
const unsigned short min_a=0, max_b=8000;
unsigned short N;
struct STNode{
	unsigned short a,b,lch,rch;
	short color;	//-1为无色，-2为杂色 
	STNode(unsigned short __a, unsigned short __b){
		a=__a;
		b=__b;
		color=-1;
		lch=rch=0;
	}
	STNode(void){;}
};
STNode STree[(max_b-min_a)*2];
unsigned short i;
void ST_Build(unsigned short a, unsigned short b){
	unsigned now=i++;
	STree[now]=STNode(a,b);
	if(b-a>1){
		STree[now].lch=i;
		ST_Build(a,(a+b)>>1);
		STree[now].rch=i;
		ST_Build((a+b)>>1,b);
	}
}
void ST_Insert(unsigned short i,unsigned short a, unsigned short b, short color){
	assert(a<b);
	if(STree[i].color==color)	return;
	if(a<=STree[i].a&&STree[i].b<=b)	STree[i].color=color;
	else{
		if(STree[i].color!=-2&&STree[i].color!=-1){
			STree[STree[i].lch].color=STree[i].color;
			STree[STree[i].rch].color=STree[i].color;
		}
		STree[i].color=-2;
		unsigned short m=((STree[i].a+STree[i].b)>>1);
		if(a<m)	ST_Insert(STree[i].lch,a,b,color);
		if(b>m)	ST_Insert(STree[i].rch,a,b,color);
	}
}
unsigned colors[8001];
void SgCount(unsigned short i, short &a_color, short &b_color){
	//在在color中增加以i节点为根的ST中各色的线段数目
	//并返回最左、最右端的颜色分别为a_color和b_color
	if(STree[i].color!=-2){
		a_color=b_color=STree[i].color;
		if(STree[i].color!=-1)	colors[STree[i].color]++;
	}
	else{
		short m1_color,m2_color;
		SgCount(STree[i].lch,a_color,m1_color);
		SgCount(STree[i].rch,m2_color,b_color);
		if(m1_color==m2_color&&m1_color!=-1)
			colors[m1_color]--;
	}
}
int main()
{
	while(fscanf(fin,"%dn",&N)==1){
		i=1;
		ST_Build(min_a,max_b);
		for(int i=0,a,b,color;i<N;i++){
			fscanf(fin,"%d %d %dn",&a,&b,&color);
			ST_Insert(1,a,b,color);
		}
		memset(colors,'',sizeof(colors));
		short a_color,b_color;
		SgCount(1,a_color,b_color);
		for(int i=0;i<=8000;i++)
			if(colors[i]!=0)	fprintf(fout,"%d %dn",i,colors[i]);
		fprintf(fout,"n");
	}
	return 0;
}
{% endcodeblock %}