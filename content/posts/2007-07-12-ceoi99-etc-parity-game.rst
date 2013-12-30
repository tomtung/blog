[CEOI99][POJ1733][URAL1003][VIJOS1112] Parity Game
==================================================

:date: 2007-07-12 16:12
:tags: OI, algorithm, disjoint-set, data structure

Time Limit:1000MS

Memory Limit:65536K

Description
-----------

Now and then you play the following game with your friend. Your friend writes down a sequence consisting of zeroes and ones. You choose a continuous subsequence (for example the subsequence from the third to the fifth digit inclusively) and ask him, whether this subsequence contains even or odd number of ones. Your friend answers your question and you can ask him about another subsequence and so on. Your task is to guess the entire sequence of numbers.

You suspect some of your friend’s answers may not be correct and you want to convict him of falsehood. Thus you have decided to write a program to help you in this matter. The program will receive a series of your questions together with the answers you have received from your friend. The aim of this program is to find the first answer which is provably wrong, i.e. that there exists a sequence satisfying answers to all the previous questions, but no such sequence satisfies this answer.

Input
-----

The first line of input contains one number, which is the length of the sequence of zeroes and ones. This length is less or equal to 1000000000. In the second line, there is one positive integer which is the number of questions asked and answers to them. The number of questions and answers is less or equal to 5000. The remaining lines specify questions and answers. Each line contains one question and the answer to this question: two integers (the position of the first and last digit in the chosen subsequence) and one word which is either ‘even’ or ‘odd’ (the answer, i.e. the parity of the number of ones in the chosen subsequence, where ‘even’ means an even number of ones and ‘odd’ means an odd number).

Output
------

There is only one line in output containing one integer X. Number X says that there exists a sequence of zeroes and ones satisfying first X parity conditions, but there exists none satisfying X+1 conditions. If there exists a sequence of zeroes and ones satisfying all the given conditions, then number X should be the number of all the questions asked.

Solution
--------

终于搞定。

首先有一步关键转化要做。我们同时处理一个范围内数字1的个数的奇偶比较麻烦。如果a到b之间有n个1，那么可以看成0到b之间1的个数减去0到a-1之间1的个数为n。我们假想知道了所有1的位置，那么0到任意i之间1的个数就是确定的。也就是说，通过这种转化，数据范围内每个数都对应了一个确定的数，它表示0到此数之间数字1的个数。

而我们事实上并不知道这些数确切是什么。我们知道的是一些数对之间奇偶性的关系。而这种关系是可以传递转移的。我们需要判断在给出关系的过程中是否出现矛盾。

于是就可以用并查集来解决这个问题了。它与我前面做过的食物链相比，本质上是一样的，但是处理起来还简单。你可以参照那个题的题解来理解这个题。

除了这步转化以外，对我而言处理起来比较麻烦的就是离散化了。这题串最大长度为10亿，而仅仅给出最多5千条询问，明显不离散化是不行了。我用的Hash。Hash和并查集的联合我从前是没搞过的。

P.S.这题其实是个骗分的好题（ACMer们别打我。。。）。不离散化最少70分。如果内存放宽一点就有80分。即使奇偶搞反了都有50分……总之怎么着都能得分的。CEOI的标程好像不是用并查集做的，但是要慢一些。就不管它了。

时空开销：

URAL的数据貌似有问题，就再不管了。

|image0|

|image1|

.. code:: cpp

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
        short color;    //-1为无色，-2为杂色 
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
        if(STree[i].color==color)   return;
        if(a<=STree[i].a&&STree[i].b<=b)    STree[i].color=color;
        else{
            if(STree[i].color!=-2&&STree[i].color!=-1){
                STree[STree[i].lch].color=STree[i].color;
                STree[STree[i].rch].color=STree[i].color;
            }
            STree[i].color=-2;
            unsigned short m=((STree[i].a+STree[i].b)>>1);
            if(a<m) ST_Insert(STree[i].lch,a,b,color);
            if(b>m) ST_Insert(STree[i].rch,a,b,color);
        }
    }
    unsigned colors[8001];
    void SgCount(unsigned short i, short &a_color, short &b_color){
        //在在color中增加以i节点为根的ST中各色的线段数目
        //并返回最左、最右端的颜色分别为a_color和b_color
        if(STree[i].color!=-2){
            a_color=b_color=STree[i].color;
            if(STree[i].color!=-1)  colors[STree[i].color]++;
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
                if(colors[i]!=0)    fprintf(fout,"%d %dn",i,colors[i]);
            fprintf(fout,"n");
        }
        return 0;
    }

.. |image0| image:: /images/2007-07-12-parity-game-poj.png
.. |image1| image:: /images/2007-07-12-parity-game-vijos.png
