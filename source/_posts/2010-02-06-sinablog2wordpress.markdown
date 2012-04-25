---
layout: post
title: "从新浪博客搬家到WordPress"
date: 2010-02-06 21:23 
comments: true
categories: [Scala, WordPress]
---

要从新浪搬到Wordpres，网上广为流传的方法是利用blogbus的博客搬家服务获得blogbus格式的xml，然后再用一个Python写的脚本把它转换成WordPress认识的格式。但是这种方法在最近新浪博客升级以后就失效了。于是自己用现学的scala写了一个小程序，搬家时能保留标签、目录、评论及评论回复这些信息。

猛击[这里](http://sinablog2wordpress.googlecode.com/files/sina2wordpress.jar)下载。注意，此程序仅支持2010年初的新版新浪博客，之前或之后的版本都不支持。

要运行程序，你需要确保已经安装过[JRE](http://sinablog2wordpress.googlecode.com/files/sina2wordpress.jar)。双击运行后显示如图界面，填入自己的博客地址（不要省略“ http:// ”），然后点击“Start”即可。这时“Start”按钮变为灰色，标题栏显示“Extracting”。等待几分钟，当标题栏显示为“Done”、“Start”按钮重新变为可用时，程序所在目录下会出现一个blog.xml文件。把这个文件直接导入WordPress就可以了。

代码也打在jar包里了，MIT协议。欢迎报告bug。

下面是废话。

恩由于新浪用了ajax，评论信息是通过xhr异步读取的，用一般的方法没法抓到。我纠结许久，最后是用了非常ad hoc的方法解决的，不知道有没有什么什么不太麻烦的通用解决方案呢。

再扯两句scala。我都想不起来当初具体是怎么想到要学scala的，也许是为了了解下函数式编程，也许只是想在jvm上有一个喜欢的语言吧——Java写起来太不爽了；Java社区的低效和保守也已经开始显出C++的影子。

scala确实是非常强大和灵活；我在见到一些颇富技巧性的hack之后都有些怀疑scala社区的风气会不会慢慢变得像C++社区一样过分热衷技巧的炫耀。不过scala的设计目标就是以较简单的语法规则获得最大的scalability，不需要通过挖掘语言规范里的犄角旮旯来实现一些必要功能，所以不会像C++一样成为一门本身已相当复杂，却还需要别人反过来教语言发明者如何使用的语言。

scala毕竟表现力比Java强太多，代码也简洁太多。比如这次我需要实现一个抛出异常后重试若干次的逻辑，只需定义一个函数：

{% codeblock lang:scala %}
def tryFor[T](times: Int)(op: => T): T = {
  if (times <= 0) throw new RuntimeException("Operation failed.")
  try { return op } catch {
    case e: Throwable => e.printStackTrace
    tryFor(times - 1)(op)
  }
}
{% endcodeblock %}

然后这样使用：

{% codeblock lang:scala %}
val source = tryFor(5) {new Source(url)}
{% endcodeblock %}

程序就会不断获得网页源代码，并在5次失败后抛出异常。Java实现同样的东西可不会如此优雅了。又如下面这段代码返回一篇博文xml：

{% codeblock lang:scala %}
private def generateEntryXml(entry: BlogEntry) = {
  <item>
    <title>
      {entry.title}
    </title>
    <wp:post_date>
      {dateFormat.format(entry.postDate)}
    </wp:post_date>
    <category>
      {entry.category}
    </category>
    {for (tag <- entry.tags) yield <category domain="tag">{tag}</category>}
    <content:encoded>
      {xml.Unparsed(handleNewLines(entry.content))}
    </content:encoded>
    <wp:status>publish</wp:status>
    {for (comment <- entry.comments) yield generateCommentXml(comment)}
  </item>
}
{% endcodeblock %}

注意，xml标签直接作为scala的源代码的一部分在代码中出现！虽然我觉得这样会使scala语言多出一种“特殊情况”，增加语言的复杂性，但不得不承认这样的设计确实非常优美简洁。

我比较看好scala，以后自己做跑在jvm上的东西scala应该是首选语言。推荐有兴趣的童鞋也了解一下。

