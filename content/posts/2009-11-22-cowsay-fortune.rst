有爱的小脚本：启动终端时显示一句箴言
====================================

:date: 2009-11-22 18:46
:tags: fun, linux

效果就是每次启动终端时都有一个小动物什么的讲一句有意思的话：

|image0|

说话的东西和说的话都随机出现。这个效果是我在\ `Linux Mint <http://www.linuxmint.com/>`__\ 里面看到的，感觉很有爱。下周考Unix环境编程，周末恶补一下，顺便写这个小脚本练手。

以我在用的 ubuntu 为例。首先确保安装 `fortunes <http://en.wikipedia.org/wiki/Fortune_%28Unix%29>`__ 和 `cowsay <http://en.wikipedia.org/wiki/Cowsay>`__ 两个包。前者用于显示各种各样的趣味短句，后者则提供了一头会说话的奶牛（和其它各种诡异的东西）。关于fortunes还有一些有趣的包你可能也想一起安装，比如fortune-zh里有唐诗宋词，fortunes-ubuntu-server则有关于使用Ubuntu Server的贴士，等等。

.. code:: sh

    #!/bin/bash
    # Cow randomly says a hopefully interesting adage

    # Get a short message from fortune, both offensive and not.
    # Remove -a if you don't want to see offensive ones.
    # Remove -s if you don't mind reading the long messages.
    msg=`fortune -a -s`

    # Randomly pick a mode of the cow
    modes=("" -b -d -g -p -s -t -w -y ); mode=${modes[$(($RANDOM % 9))]}

    # cowsay or cowthink?
    cowdos=(cowsay cowthink); cowdo=${cowdos[$(($RANDOM % 2))]}

    # Radomly pick a cow picture file
    speaker=`cowsay -l | sed '1d;s/ /n/g'| sort -R | head -1`

    # That's it ^^
    echo "$msg" | $cowdo -n -f $speaker $mode

保存后加上执行权限：

.. code:: sh

    chmod +x cowsay-fortune

然后把这个文件复制到\ ``/usr/bin``\ 下

.. code:: sh

    sudo cp cowsay-fortune /usr/bin

最后打开\ ``/etc/bash.bashrc``

.. code:: sh

    sudo gedit /etc/bash.bashrc

并在最后加上一行：

.. code:: 

    cowsay-fortune

保存后打开终端，应该就是这个效果了：

|image1|

.. |image0| image:: /images/2009-11-22-cowsay-fortune-1.png
.. |image1| image:: /images/2009-11-22-cowsay-fortune-2.png
