[Uva #258] Mirror Maze
======================

:date: 2007-6-6 20:58
:tags: OI, algorithm

In a galaxy far far away from our’s, there lived a team of scientists who invented a device that could kill all computervirusses that do terrible things to MS-DOS computers. This device could do its job in the entire universe because it used a magic laser beam. But, just like in all great devices, this device had a strange component in it. This component is a two-dimensional maze with black holes and mirrors in it. Nobody knew the reason for this component but the scientists said it was a crucial component.

This maze has two openings in it. One of these openings is in front of the magic laser. All the mirrors in the maze have two reflecting sides. These mirrors always make an angle of 45 degrees with the laser beam but they can be rotated over 90 degrees, so each mirror can be in 2 states only. The laser beam will be totally absorbed by a black hole. The laser beam may cross itself (with an angle of 90 degrees) in an empty place of the maze.

In this problem you are given several mazes (one at a time) in which you have to position the mirrors in such a way that the laser beam can travel from one entrance to the other. The border of each maze is marked by black holes (except for two places which are the two entrances of the maze). The mirrors in the given mazes will probably not have a correct angle to reflect a laser beam from one entrance of the maze to the other. The mirrors in the given mazes can be positioned in such a way that a laser beam can travel through the maze.

Your program must read the mazes from the input file and position the mirrors in it in such a way that a laser beam that enters through one entrance exits through the other.

Input
-----

The input for your program is a textflle. This file contains severas mazes. A specification of a single maze is given by the following description:

-  First a line that contains two positive integers (say M and N) separated by one space which specify the number of columns and the number of rows (in that order) of the maze to come. These integers can have a value from 3 to 50 inclusive.
-  On the next N lines follows the maze with the mirrors and black holes. Mirrors are given by a ``\`` (backslash) or a ``/`` (divide). Here and / correspond to the 2 states of a mirror. Black holes are given by \* (star). Empty places in the maze are given by dots.

The last line of the input file is given by \`-1 -1‘.

Output
------

The output file is a textfile which contains the resulting mazes. The mazes in the output file must be separated from each other by one empty line.

Solution
--------

AC的第一道Uva，庆祝下……

这题的算法是DFS。但我并没有直接用lrj书上说的拆结点的方法，而是换了一种方式。首先预处理地图中镜子的信息，记录它们上下左右相邻的镜子都是哪些，并且记录哪两个镜子是和出、如口相邻的（它们都可以作为搜索的起点）。我们知道光路的走向到达镜子处时如何变化仅仅取决于两个因素：入射方向和镜子的状态。这样我们就根据一个出、如口的位置确定第一面镜子的入射方向，然后我们顺着往下走就行，如果不通就回溯并改变镜子状态，直到找到一个可行解时输出就行了。有一点要注意的是光可能两次经过同一面镜子的不同面（同面显然不可能）。这样回溯时就要注意了：这么镜子是否已经被光经过了？如果是，那么它就一定不能再被翻了。还有就是出口直接对入口不需要镜子这种特殊情况的处理。

uva的测评好严格啊……我开始交了n多次竟然一直ce找不到原因。结果在论坛里发了帖子问了才知道（p.s.uva的管理员很尽职啊，回答迅速准确友好），原来我用了memset却没#include，所以错了（这是我第一次意识到memset是string.h里面的东西）。而这个在我的winxp和ubuntu下面用g++都能编译通过……要是noi的评测也来这么一手岂不是很囧……

下面是代码。长度不短、速度不快、空间消耗不小，因此仅供参考：

.. code:: cpp

    #include <iostream>
    #include <cassert>
    #include <cstring>
    using namespace std;
    int M,N;
    char map[51][51];
    int mirror_sum;//镜子的个数
    int mirror_num[51][51];//[x][y]:(x,y)处镜子的编号；出/入口为-1
    struct Mirror{
       short neighbor[4];   //4个方向上的相邻镜子编号：0为不存在，-1为出/入口
       //关于方向的定义：0上，1左，2下，3右
       short x,y;//镜子坐标
    }mirror[2500];
    bool state[2500];//[i]:第[i]面镜子的状态：0为'/'，1为'\'

    bool used[2500];
    //used[i]:dfs中记录第i个镜子是否原来已经使用（即镜子能否翻转而不影响已知的光线路径？）
    inline void get_next(int i,int j,int &next_i,int &next_j)
    //dfs调用的子过程，根据当前镜子编号和入射方向确定下一面镜子的编号和入射方向
    {
       int d[4];
       if(state[i]==0)//下-右，上-左
       {
          d[0]=1;d[1]=0;d[2]=3;d[3]=2;
       }
       else{ //上-右，下-左
          d[0]=3;d[1]=2;d[2]=1;d[3]=0;
       }
       next_j=(d[j]+2)%4;
       next_i=mirror[i].neighbor[d[j]];
    }
    bool dfs(int i, int j)  //射向第i面镜子，入射方向为j。若找到解则返回true
    {
       if(i==-1)   return true;   //到达出口
       int next_i,next_j;
       bool used_i=used[i],flag=false;
       used[i]=true;
       get_next(i,j,next_i,next_j);
       if(next_i!=0)
          flag=dfs(next_i,next_j);
       if(flag) return true;
       if(!used_i)
       {
          state[i]=!state[i];
          get_next(i,j,next_i,next_j);
          flag=dfs(next_i,next_j);
          if(flag) return true;
          state[i]=!state[i];
       }
       used[i]=used_i;
       return false;
    }

    int main()
    {
       int counter=0;
       while(1)
       {
          cin >> M >> N;
          if(M==-1&&N==-1)   break;   //判断输入结束
          if(counter++>0)   cout << endl;
          /*初始化*/
          mirror_sum=0;
          memset(mirror_num,'\0',sizeof(mirror_num));
          memset(mirror,'\0',sizeof(mirror));
          memset(used,'\0',sizeof(used));
          memset(state,'\0',sizeof(state));

          //读入数据
          for(int x=1;x<=N;x++)
             for(int y=1;y<=M;y++)
             {
                cin >> map[x][y];
                if(map[x][y]=='/'||map[x][y]=='\\') //记录镜子的信息
                {
                   mirror_sum++;
                   mirror_num[x][y]=mirror_sum;
                   mirror[mirror_sum].x=x;
                   mirror[mirror_sum].y=y;
                   state[mirror_sum]=(map[x][y]=='\\');
                }
                else if((x==N||y==M||x==1||y==1)&&map[x][y]=='.')   //记录出/入口的信息
                   mirror_num[x][y]=-1;
             }

          //处理各镜子的相邻镜子信息
          const int dir_x[4]={-1,0,1,0},dir_y[4]={0,-1,0,1};
          int first_mirror=-1,first_dir=-1;
          for(int i=1,x,y;i<=mirror_sum;i++)
             for(int d=0;d<=3;d++)
             {
                if(mirror[i].neighbor[d]!=0)  continue;
                x=mirror[i].x,y=mirror[i].y;
                while(1)
                {
                   x+=dir_x[d];
                   y+=dir_y[d];
                   assert(x>=1&&x<=N&&y>=1&&y<=M);
                   if(map[x][y]=='*')   break;   //遇到黑洞
                   if(mirror_num[x][y]==-1)   //遇到出/入口
                   {
                      mirror[i].neighbor[d]=-1;
                      first_mirror=i;
                      first_dir=d;
                      break;
                   }
                   if(mirror_num[x][y]>0)  //遇到镜子
                   {
                      mirror[i].neighbor[d]=mirror_num[x][y];
                      mirror[mirror_num[x][y]].neighbor[(d+2)%4]=i;
                      break;
                   }
                }
             }

          if(first_mirror!=-1&&first_dir!=-1)
          {
             bool flag=dfs(first_mirror,first_dir);//搜索可行解
             assert(flag);
          }

          for(int i=1;i<=N;i++)//输出可行解
          {
             for(int j=1;j<=M;j++)
                if(mirror_num[i][j]==0||mirror_num[i][j]==-1)   cout << map[i][j];
                else cout << (state[mirror_num[i][j]]?'\\':'/');
             cout << endl;
          }
       }
       return 0;
    }

题外话：这题的题干实在没有上海ACM的那个救公主的故事编得好。这个故事仿佛一个小学生的蹩脚“科幻故事”，读起来实在让人比较郁闷…- -
