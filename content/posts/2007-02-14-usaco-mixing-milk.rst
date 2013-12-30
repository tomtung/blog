[USACO] Mixing Milk
===================

:date: 2007-2-14 21:12
:tags: OI, algorithm, USACO

Since milk packaging is such a low margin business, it is important to keep the price of the raw product (milk) as low as possible. Help Merry Milk Makers get the milk they need in the cheapest possible manner.

The Merry Milk Makers company has several farmers from which they may buy milk, and each one has a (potentially) different price at which they sell to the milk packing plant. Moreover, as a cow can only produce so much milk a day, the farmers only have so much milk to sell per day. Each day, Merry Milk Makers can purchase an integral amount of milk from each farmer, less than or equal to the farmer’s limit.

Given the Merry Milk Makers’ daily requirement of milk, along with the cost per gallon and amount of available milk for each farmer, calculate the minimum amount of money that it takes to fulfill the Merry Milk Makers’ requirements.

Note: The total milk produced per day by the farmers will be sufficient to meet the demands of the Merry Milk Makers.

PROGRAM NAME: milk
------------------

INPUT FORMAT
------------

+--------------------------------------+--------------------------------------+
| Line1:                               | Two integers, N and M.               |
|                                      |                                      |
|                                      | The first value, N, (0 <= N <=       |
|                                      | 2,000,000) is the amount of milk     |
|                                      | that Merry Milk Makers’ want per     |
|                                      | day. The second, M, (0 <= M <=       |
|                                      | 5,000) is the number of farmers that |
|                                      | they may buy from.                   |
+--------------------------------------+--------------------------------------+
| Lines2..M+1:                         | The next M lines each contain two    |
|                                      | integers, Pi and Ai.                 |
|                                      |                                      |
|                                      | Pi (0 <= Pi <= 1,000) is price in    |
|                                      | cents that farmer i charges.         |
|                                      |                                      |
|                                      | Ai (0 <= Ai <= 2,000,000) is the     |
|                                      | amount of milk that farmer i can     |
|                                      | sell to Merry Milk Makers per day.   |
+--------------------------------------+--------------------------------------+

OUTPUT FORMAT
-------------

A single line with a single integer that is the minimum price that Merry Milk Makers can get their milk at for one day.

SOLUTION
--------

这个题当然是巨弱的题，基本上即使不知道有贪心这回事的人也能凭感觉做出来。但是我看到官方的Analysis，觉得很不错，就发上来了。它用一个最简单的例子向我们展示了最优美的代码是怎样炼成的。

下面是代码我翻译的说明、注释。

    因为我们获得的东西都是同样大小的（在这里是单位量的牛奶），贪心算法可以满足要求：我们按照出价对农夫们进行排序，然后向出价最低的农夫买牛奶，买光他的牛奶后在向下一个出价次低的农夫买。

    实现方法：我们把数据读入Farmer结构体中，按照出价对数组进行排序，扫描数组，依次买牛奶直到牛奶量达到所需。

    .. code:: cpp

        #include <stdio.h>
        #include <stdlib.h>
        #include <string.h>
        #include <assert.h>

        #define MAXFARMER 5000

        typedef struct Farmer Farmer;
        struct Farmer {
         int p; /* 每加仑的价格*/
         int a; /* 要卖的总量*/
        };

        int
        farmcmp(const void *va, const void *vb)
        {
         return ((Farmer*)va)->p - ((Farmer*)vb)->p;
        }

        int nfarmer;
        Farmer farmer[MAXFARMER];

        void
        main(void)
        {
         FILE *fin, *fout;
         int i, n, a, p;

         fin = fopen("milk.in", "r");
         fout = fopen("milk.out", "w");

         assert(fin != NULL && fout != NULL);

         fscanf(fin, "%d %d", &n, &nfarmer);
         for(i=0; i<nfarmer; i++)
          fscanf(fin, "%d %d", &farmer[i].p, &farmer[i].a);

         qsort(farmer, nfarmer, sizeof(farmer[0]), farmcmp);

         p = 0;
         for(i=0; i<nfarmer && n > 0; i++) {
        /* 向farmer[i]买尽可能多的牛奶，最大为amount n */
          a = farmer[i].a;
          if(a > n)
           a = n;
          p += a*farmer[i].p;
          n -= a;
         }

         fprintf(fout, "%d\n", p);
         exit(0);
        }

    加拿大的Ran Pang写道：

        这里有个程序能在线性时间内解决问题的程序，而我觉得官方给出的算法是O(n log n)的。

    .. code:: c

        #include<stdio.h>

        #define MAXPRICE 1001

        int amount_for_price[MAXPRICE]={0};
        int N, M;

        int Cal(void);
        int Read(void);

        int main(void) {
            Read();
            Cal();
            return 0;
        }

        int Cal(void) {
            int i;
            int price_total=0;
            int milk_total=0;
            for(i=0;i<MAXPRICE;i++) {
                if(amount_for_price[i]) {
                    if(milk_total+amount_for_price[i]<N) {
                        price_total+=(i*amount_for_price[i]);
                        milk_total+=amount_for_price[i];
                    }
                    else {
                        int amount_needed = N-milk_total;
                        price_total+=(i*amount_needed);
                        break;
                    }
                }
            }
            {
                FILE* out=fopen("milk.out","w");
                fprintf(out,"%d\n",price_total);
                fclose(out);
            }
            return 0;
        }

        int Read(void) {
            FILE* in = fopen("milk.in","r");
            int i, price, amount;
            fscanf(in,"%d %d",&N,&M);
            for(i=0;i<M;i++) {
                fscanf(in, "%d %d", &(price), &(amount));
                amount_for_price[price]+=amount;
            }
            fclose(in);
            return 0;
        }

    另一个解法，来自SVK（这是哪啊？）的Adam Okruhlica

        完全没有必要用O(nlgn)的时间对价格进行快排，因为价格有一个$1000的上界，而且我们知道所有价格都是整数。我们可以用count sort对数组进行排序。我们可以给每一个可用的价格（0..1000）建立一个“盒子”。我们把输入数据存入一个数组，然后扫描每一个农夫，记录他在（0..1000）数组中的下标，此下标就等于他的出价。因此我们可以把出价相同的农夫放入一个链表中。最后，我们从0到1000扫描整个数组，并从链表中取出农夫们的下标。这很容易实现，且时间复杂度为O(n)。

    .. code:: pascal

        program milk;

        type pList = ^List;
              List = record
                        farmer:longint;
                        next:pList;
                      end;
              HeadList = record
                           head:pList;
                           tail:pList;
                          end;

        var fIn,fOut:text;
            sofar,i,x,want,cnt,a,b:longint;
            sorted,cost,amount:array[1..5010] of longint;
            csort:array[0..1010] of HeadList;

            t:pList;

        begin
            assign(fIn,'milk.in');reset(fIn);
            assign(fOut,'milk.out'); rewrite(fOut);

            readln(fIn,want,cnt);
            for i:=1 to cnt do readln(fIn,cost[i],amount[i]);

            for i:=0 to 1000 do begin
                 new(csort[i].head);
                 csort[i].tail:=csort[i].head;
                 csort[i].head^.farmer:=-1;
            end;

            {向数组中存入下标}
            for i:=1 to cnt do begin

               t:=csort[cost[i]].tail;
               if t^.farmer = -1 then t^.farmer:=i;
               new(t^.next);
               t^.next^.farmer:=-1;
               csort[cost[i]].tail:=t^.next;
            end;

            {取出下标}
            x:=1;
            for i:=0 to 1000 do begin
                t:=csort[i].head;
                while t^.farmer > 0 do begin
                  sorted[x]:=t^.farmer;
                  inc(x);
                  t:=t^.next;
                end;
            end;

            sofar:=0;
            for i:=1 to cnt do begin
              if want < amount[sorted[i]] then begin
                inc(sofar,want*cost[sorted[i]]);
                want:=0; break;
              end

              else inc(sofar,amount[sorted[i]]*cost[sorted[i]]);
              dec(want,amount[sorted[i]]);
            end;

            writeln(fOut,sofar);
            close(fOut);
        end.

    Dwayne Crooks写道：

        我们真的需要一个SVK的Adam Okruhlica在解答中使用的链表吗？我不这么想。这里有一个解法，本质上和Adam的一样，却没有使用链表。此解法是O(max(MAXP,M)) 的（MAXP=1000，M<=5000）。编辑注：为了避免溢出，Dwayne应该使用 long long integers (64 bit)而非int。

    .. code:: cpp

        #include <iostream>
        #include <fstream>

        #define MAXP 1000

        using namespace std;

        int main() {
            ifstream in("milk.in");
            ofstream out("milk.out");

            int N, M;
            int P[MAXP+1];

            in >> N >> M;
            for (int i = 0; i <= MAXP; i++) P[i]=0;
            for (int i = 0; i < M; i++) {
                int price, amt;
                in >> price >> amt;

                 // 我们可以将价格相同的各个农民手中牛奶的总量相加
                // 因为x加仑售价c美分、
                //          y加仑售价c美分
                // 和x+y加仑售价c美分
                //      是一回事
                P[price] += amt;
            }

            // 贪心策略：尽可能多的买售价最低的
            int res = 0;
            for (int p = 0; p<=MAXP && N>0; p++) {
                if (P[p]>0) {
                    res+=p*(N<P[p]?N:P[p]);
                    N-=P[p];
                }
            }
            out << res << endl;

            in.close();
            out.close();

            return 0;
        }

    做为结语，保加利亚的Miroslav Paskov从以上所有精彩的想法中提炼出了这个简单的解法：

    .. code:: cpp

        #include <fstream>
        #define MAXPRICE 1001
        using namespace std;

        int main() {
            ifstream fin ("milk.in");
            ofstream fout ("milk.out");
            unsigned int i, needed, price, paid, farmers, amount, milk[MAXPRICE][2];
            paid = 0;
            fin>>needed>>farmers;
            for(i = 0;i<farmers;i++){
                fin>>price>>amount;
                milk[price][0] += amount;
            }
            for(i = 0; i<MAXPRICE && needed;i++){
                if(needed> = milk[i][0]) {
                    needed -= milk[i][0];
                    paid += milk[i][0] * i;
                } else if(milk[i][0]>0) {
                    paid += i*needed;
                    needed = 0;
                }
            }
            fout << paid << endl;
            return 0;
        }

