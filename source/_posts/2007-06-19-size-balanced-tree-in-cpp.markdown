---
layout: post
title: "Size Balanced Tree in C++"
date: 2007-6-19 14:07
comments: true
categories: [OI, Algorithm, Size Balanced Tree]
---

修改是在上一个版本的基础上进行的，从ghost那学了两个小技巧（是什么呢？呵呵~），一下子使得维护部分的代码量减少了一半，并且减少了烦琐的判空，这样代码的实际长度就在90行左右了，“宽度”也减小了不少。代码中有的地方注明了是“维护p”，那是由于有的时候维护父指针p(arent)会方便些。如果不需要，直接删掉这些语句就行了。当然，还有其它一些小改动。

觉得如果没有错误的话就没有必要再继续改动了。再改动也不可能改变它的时间复杂度，顶多是优化一下常数，尽早开始背吧。

当然如果你发现了程序中哪些不合理的地方导致了速度变慢也请指出，谢谢……

（为什么我的sbt会比ghost的treap慢呢，旋转的次数也比他的少多了啊，郁闷~）

> 1. 修改了Delete的函数原型说明：它与后面的Delete函数算法描述部分的不一致。
> 2. 删除了Insert部分中关于具有相同关键字节点插入子树的左右说明：它显然是不对的（我竟然一直没意识到直至我的ural1028SBT版用rank后 WA掉），因为一Maintain原来插入的位置就有可能变化。

> ——2007年6月21日更新

> 加入了退化版SBT的说明（在Maintain处）。经测试在一般数据下退化版的确实要快——这在OI比赛中也许很实用。

> ——2007年7月2日更新

> 小更新。完善了部分注释，并且把delete里的两句做了优化，使之更短更快。修改了rank，把每次对于i和size关系的判断（它事实上只需要进行一次）写到了注释里，要求i<=T->size，否则每次都要判断实在太慢了。把.cc的扩展名改成了.h，因为我默写的时候都是把SBT默写到一个.h文件里，然后用另外一个写好的cpp文件调用它来检查对错。这样也许会方便些吧。

> ——2007年7月6日更新

{% codeblock sbt.cpp %}
/****************************************
*                 SBT.h
*
*       Fri Jul 18 20:40:08 2007
*       Copyright  2007  巨菜逆铭
*
******************************************/
 
#include <iostream>
#include <cassert>
using namespace std;
 
//————SBT的储存结构————
struct SBTNode{
    SBTNode *ch[2],*p;    //ch[0]、ch[1]分别为左右孩子，p为双亲
    long key;    //这里省略了卫星数据域
    unsigned long size;
    SBTNode(long _key,unsigned long _size);
}NIL=SBTNode(0,0);
typedef SBTNode *SBTree;
SBTNode::SBTNode(long _key,unsigned long _size=1){ //构造函数：未考虑卫星数据
    ch[0]=ch[1]=p=&NIL;
    size=_size;
    key=_key;
}
 
//————SBT基本操作函数原型说明————
SBTNode *SBT_Search(SBTree T,long key);
    //在T中中寻找关键字为key的结点
    //若能找到则返回指向它的指针，否则返回NULL
void SBT_Insert(SBTree &T, SBTNode* x);
    //将节点x插入树中
SBTNode *SBT_Delete(SBTree &T, long key);
    //从以T为根的SBT中删除一个关键字为key的结点并返回“实际”被删除结点的指针
    //如果树中没有一个这样的结点，删除搜索到的最后一个结点并返回其指针
SBTNode *SBT_Pred(SBTree T, long key);
    //返回指向关键字为key的节点在T的中序遍历中的直接前趋的指针
    //要求T中必须有关键字为key的节点
SBTNode *SBT_Succ(SBTree T,long key);
    //返回指向关键字为key的节点在T的中序遍历中的直接后继的指针
    //要求T中必须有关键字为key的节点
SBTNode *SBT_Select(SBTree T, unsigned long i);
    //从树T中找到关键字第i小的结点并返回其指针
unsigned long SBT_Rank(SBTree T, long key);
    //返回关键字为key的节点在树T中的秩
    //若不存在此节点则返回0
 
//————SBT的修复操作的算法描述————
inline void SBT_Rotate(SBTree &x,bool flag){
    SBTNode *y=x->ch[!flag];
    assert(x!=&NIL&&y!=&NIL);
    //维护p
    y->p=x->p;
    x->p=y;
    if(y->ch[flag]!=&NIL) y->ch[flag]->p=x;
    //维护x和y的ch[]
    x->ch[!flag]=y->ch[flag];
    y->ch[flag]=x;
    //维护size
    y->size=x->size;
    x->size=x->ch[0]->size+x->ch[1]->size+1;
    //维护原x父节点的ch[]
    x=y;
}
void SBT_Maintain(SBTree &T,bool flag){
    //维护操作的核心：保持
    if(T->ch[flag]->ch[flag]->size>T->ch[!flag]->size)    //情况1
        SBT_Rotate(T,!flag);
    //此函数内剩余代码被注释掉后SBT将在插入“人”字型代码时退化
    //但是对于一般数据将会更快
    else if(T->ch[flag]->ch[!flag]->size>T->ch[!flag]->size){ //情况2
        SBT_Rotate(T->ch[flag],flag);
        SBT_Rotate(T,!flag);
    }
    else return;    //无需修复
    SBT_Maintain(T->ch[0],0),SBT_Maintain(T->ch[1],1);    //修复左右子树
    SBT_Maintain(T,0),SBT_Maintain(T,1);    //修复整棵树
}
 
//————SBT基本操作的算法描述————
SBTNode *SBT_Search(SBTree T,long key){
    //在T中中寻找关键字为key的结点
    //若能找到则返回指向它的指针，否则返回NULL
    return T==&NIL||T->key==key?T:SBT_Search(T->ch[key>T->key],key);
}
 
void SBT_Insert(SBTree &T, SBTNode* x){
    //将节点x插入树中
    if(T==&NIL)    T=x;
    else{
        T->size++;
        x->p=T;    //维护p
        SBT_Insert(T->ch[x->key>T->key],x);
        SBT_Maintain(T,x->key>T->key);
    }
}
 
SBTNode *SBT_Delete(SBTree &T, long key){
    //从以T为根的SBT中删除一个关键字为key的结点并返回“实际”被删除结点的指针
    //如果树中没有一个这样的结点，删除搜索到的最后一个结点并返回其指针
    if(T==&NIL)    return &NIL;
    T->size--;
    if(T->key==key||T->ch[key>T->key]==&NIL){
        SBTNode *toDel;
        if(T->ch[0]==&NIL||T->ch[1]==&NIL){
            toDel=T;
            T=T->ch[T->ch[1]!=&NIL];
            if(T!=&NIL)    T->p=toDel->p;    //维护p
        }else{
            toDel=SBT_Delete(T->ch[1],key-1);
            T->key=toDel->key;
        }
        return toDel;
    }
    else return SBT_Delete(T->ch[key>T->key],key);
}
 
SBTNode *SBT_Pred(SBTree T, long key){
    //返回指向拥有比key小的最大关键字的节点的指针
    if(T==&NIL)    return &NIL;
    if(key<=T->key)    return SBT_Pred(T->ch[0],key);
    else{
        SBTNode *pred=SBT_Pred(T->ch[1],key);
        return (pred!=&NIL?pred:T);
    }
}
 
SBTNode *SBT_Succ(SBTree T,long key){
    //返回指向拥有比key大的最小关键字的节点的指针
    if(T==&NIL)    return &NIL;
    if(key>=T->key)    return SBT_Succ(T->ch[1],key);
    else{
        SBTNode *succ= SBT_Succ(T->ch[0],key);
        return(succ!=&NIL?succ:T);
    }
}
 
SBTNode *SBT_Select(SBTree T, unsigned long i){
    //从树T中找到关键字第i小的结点并返回其指针
    //要求i<=T->size
    unsigned long r = T->ch[0]->size+1;
    if(i==r)    return T;
    else return SBT_Select(T->ch[i>r],i>r?i-r:i);
}
 
unsigned long SBT_Rank(SBTree T, long key){
    //返回关键字为key的节点在树T中的秩
    //若不存在此节点则返回0
    if(T==&NIL)    return 0;
    if(T->key==key)    return T->ch[0]->size+1;
    else if(key<T->key)    return SBT_Rank(T->ch[0],key);
    else{
        unsigned long r=SBT_Rank(T->ch[1],key);
        return r==0?0:r+T->ch[0]->size+1;
    }
}
{% endcodeblock %}
