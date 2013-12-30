[URAL1183] Brackets sequence
============================

:date: 2007-6-1 16:25
:tags: OI, algorithm, dynamic programming

Let us define a regular brackets sequence in the following way:

Empty sequence is a regular sequence. If S is a regular sequence, then (S) and [S] are both regular sequences. If A and B are regular sequences, then AB is a regular sequence. For example, all of the following sequences of characters are regular brackets sequences: :

::

    (), [], (()), ([]), ()[], ()[()]

And all of the following character sequences are not: :

::

    (, [, ), )(, ([)], ([(]

Some sequence of characters ‘(‘, ‘)’, ‘[', and ']‘ is given. You are to find the shortest possible regular brackets sequence, that contains the given character sequence as a subsequence. Here, a string a1a2…an is called a subsequence of the string b1b2…bm, if there exist such indices 1 ≤ i1 < i2 < … < in ≤ m, that aj=bij for all 1 ≤ j ≤ n.

Input
-----

The input file contains at most 100 brackets (characters ‘(‘, ‘)’, ‘[' and ']‘) that are situated on a single line without any other characters among them.

Output
------

Write to the output file a single line that contains some regular brackets sequence that has the minimal possible length and contains the given sequence as a subsequence.

Solution
--------

终于过了这题……WA了两次。第一次是判断括号匹配的栈写错了，WA#9；第二次是没有考虑输入文件是空串的情况，WA#13并持续一周 -\_-\|\|\|

而且这次也写垃圾了，长达80多行。好像原来的ural的内存限制是1000K？这样说我开一个100\*100的string数组真是件奢侈的事情呢……

.. code:: cpp

    #include <iostream>
    #include <fstream>
    #include <string>
    #include <cassert>
    using namespace std;
    ifstream fin("bracket.in");
    ofstream fout("bracket.out");
    string S;
    inline bool isregular(int i,int j)  //判断原串中的子串S[i...j]是否规则
    {
       if(j<i)  return true;
       else if(j==i)  return false;
       char stack[100];  int p=0;
       for(int k=i;k<=j;k++)
       {
          if(p==0)
          {
             if(S[k]=='('||S[k]=='[')   stack[p++]=S[k];
             else return false;
          }
          else{
             if(( stack[p-1]=='('&&S[k]==')' )||( stack[p-1]=='['&&S[k]==']' ))  p--;
             else if(S[k]==')'||S[k]==']') return false;
             else  stack[p++]=S[k];
          }
       }
       return (p==0);
    }
    string s[100][100];  //[i][j]：按照最少原则添加括号规则化S[i...j]后得到的串
    string memo(int i, int j)  //记忆化搜索
    {
       if(s[i][j]!="")   return s[i][j];
       if(isregular(i,j))   //若S[i...j]本身就已经是规则的
       {
          s[i][j].assign(S,i,j-i+1);
          return s[i][j];
       }
       if(i==j) //若当前串仅由一个字符组成
       {
          if(S[i]=='('||S[i]==')')   s[i][j]="()";
          else if(S[i]=='['||S[i]==']') s[i][j]="[]";
          else assert(0);
          return s[i][j];
       }
       string ans,tmp,tmp2;
       unsigned size=UINT_MAX;
       if(( S[i]=='('&&S[j]==')' )||( S[i]=='['&&S[j]==']' ))  //若S[i...j]首尾配对，则只需使S[i+1...j-1]规则就得到一个解
       {
          ans=S[i]+memo(i+1,j-1)+S[j];
          size=ans.size();
       }
       else if(( S[i]=='('&&S[j]!=')' )||( S[i]=='['&&S[j]!=']' ))   //S[i...j]首尾不配对，与以上类似
       {
          ans=S[i]+memo(i+1,j);
          if(S[i]=='(')  ans=ans+')';
          else if(S[i]=='[')   ans=ans+']';
          else assert(0);
          size=ans.size();
       }
       else if(( S[i]!='('&&S[j]==')' )||( S[i]!='['&&S[j]==']' ))
       {
          ans=memo(i,j-1)+S[j];
          if(S[j]==')')  ans='('+ans;
          else if(S[j]==']')   ans='['+ans;
          else assert(0);
          size=ans.size();
       }
       for(int k=i;k<j;k++) //规则化S[i...k]和S[k+1...j]后合并得到的串
          if(size>memo(i,k).size()+memo(k+1,j).size())
          {
             ans=memo(i,k)+memo(k+1,j);
             size=memo(i,k).size()+memo(k+1,j).size();
          }
       return (s[i][j]=ans);
    }
    int main()
    {
       fin >> S;
       if(S.size()==0)
       {
          fout << endl;
          return 0;
       }
       fout << memo(0,S.size()-1) << endl;
       return 0;
    }

