---
layout: post
title: "Surprises in Scala’s 'Uniform Return Type' Magic"
date: 2012-01-16 07:59
comments: true
categories: [C#, Scala, LINQ]
---

There's an increasingly heated debate about Scala's complexity. A recent post talks about Scala's
"[true complexity](http://yz.mit.edu/wp/true-scala-complexity/)": the terrifying intricacy you will encounter,
if you try to extend Scala's Collections Library with a method that achieves the "perfect" behavior. 

Yet it also might be worth asking: what are the motivations of these "perfect" behaviors? Are they always desirable?

One important aspect of the "perfect" collection behavior is the magical *uniform return type principle*.
Sloppily speaking, this means that transforming a collection should give you another collection of the same kind.
For instance:

{% codeblock lang:scala %}
// Filtering a List gives you a filtered List
scala> List(1,2,3,4).filter(_%2==0)
res: List[Int] = List(2, 4)

// Mapping a Set gives you a mapped Set
scala> Set(1,2,3,4).map(1+)
res: scala.collection.immutable.Set[Int] = Set(2, 3, 4, 5)

// Uniform return type at both compile time and runtime
scala> val iterable : Iterable[Int] = Set(1,2,3,4)
iterable: Iterable[Int] = Set(1, 2, 3, 4)

scala> iterable.map(1+)
res: Iterable[Int] = Set(2, 3, 4, 5)

// Works for Strings, too
scala> "E is the most frequent letter in English".map(
     |    c => if(c=='e'|c=='E') '3' else c)
res: String = 3 is th3 most fr3qu3nt l3tt3r in 3nglish
{% endcodeblock %}

Clean and consistent, can't be more intuitive. Of course filtering a List should return a List, and mapping
a Set should give you a Set. Both compile time and runtime. Works even for non-collections like Strings.

When I first saw this, I thought "yeah, cool", and then forgot about it. I took it for granted as just another
Scala magic that makes my life easier, without realizing its intricate implications. Not until recently have
I realized that Scala's collections were much smarter, or trickier, than I had expected.

The uniform return type principle is fairly straightforward for operations like `filter`, `take`, `drop` and `slice`,
but situations get complicated in the cases of some other operations like `map` and `flatMap`. Consider the following:

{% codeblock lang:scala %}
scala> Set(1,2,3,4).map(_ % 2 == 0)
res: scala.collection.immutable.Set[Boolean] = Set(false, true)
{% endcodeblock %}

It starts getting interesting. When mapping a `Set`, you should get a `Set`, which by definition doesn't contain
repeated values. So you get a `Set[Boolean]` which consists of only 2 values. You might get surprised here if
you are familiar with LINQ in C#. In C#

{% codeblock lang:csharp %}
new HashSet(new[] {1, 2, 3, 4}).Select(x =&gt; x%2 == 0)
{% endcodeblock %}

gives you an `IEnumerable` that consists of "`false`, `true`, `false`, `true`" in order, because the `HashSet` is simply
iterated through as a Normal `IEnumerable`. Some say C#/LINQ sucks, because the type information of original collection is "lost".

In Scala, `Map[K, V]` is a subtype of `Iterable[(K, V)]`, thus can be seen as a collection of key-value pairs.
Now stop for a moment and think about it: what happens if you `map` a `Map`?

{% codeblock lang:scala %}
scala> Map('a'->1,'b'->2,'c'->3,'d'->4).map(t => t._2 -> t._1)
res: scala.collection.immutable.Map[Int,Char] = Map(1 -> a, 2 -> b, 3 -> c, 4 -> d)

scala> Map('a'->0,'b'->1,'c'->0,'d'->1).map(t => t._1)
res: scala.collection.immutable.Iterable[Char] = List(a, b, c, d)
{% endcodeblock %}

Ideally, according to the uniform return type principle, mapping a `Map` should give you another `Map`.
But this is only possible when the target element type is key-value pair. Otherwise, the best we can
do is to treat the `Map` as just an `Iterable` of key-value pairs and return an `List` of the target elements.

However, there is still the problem of inconsistency. Here's an example:
{% codeblock lang:scala %}
scala> Map(1->'a', 2->'b', 3->'c').map(_._2)
res: scala.collection.immutable.Iterable[Char] = List(a, b, c)

scala> Map(1->('a','b'), 2->('a','c'), 3->('b','c')).map(_._2)
res: scala.collection.immutable.Map[Char,Char] = Map(a -> c, b -> c)
{% endcodeblock %}

Same operation on two `Set`s, but the behaviors are totally different, simply because these two `Set`s have
different types of values? This is weird. The problem is that 2-tuples are selected to represent the key-value pairs,
but are not exclusively used for this purpose. So when user map the elements to 2-tuples, there's this unavoidable ambiguity. 

It becomes even more error-prone if the actual class type of the collection is not known at compile time.
We know that Map has a property "keys" that gives you an `Iterable` of its keys. Consider the following example:

{% codeblock lang:scala %}
scala> val m = Map(1 -> 'a', 2 -> 'b', 3 -> 'c', 4 -> 'd')
m: scala.collection.immutable.Map[Int,Char] = Map(1 -> a, 2 -> b, 3 -> c, 4 -> d)

scala> m.keys.map(_%2==0)
res: Iterable[Boolean] = Set(false, true)
{% endcodeblock %}

Ah...the runtime type of "keys" is `Set[Int]`, so repeated values in the returned collection are also ignored.
The behavior should surprise you if you haven't think of this. In fact, when given a Iterable without knowing its actual type, 
in any case the behaviors of collection operations are simply unpredictable. Scala guys can argue that this is just how it works,
but this doesn't seems to be a good thing, given that Iterables have been widely used between interfaces to pass data collections
around without specifying their internal structures.

To sum up, the behavior of the map operation depends on not only the *type of the collection on which it invokes*, both static and
dynamic, but also on the *type of the mapped elements*.

How is this magic implemented? If you take a look at the source code, you will probably see the most complicated collection library
you've ever seen in your life. I'll try to give a brief and simplified explanation. Here is the actual signature of the map method:

{% codeblock lang:scala %}
def map[MappedElem, That](p: Elem => MappedElem)
    (implicit bf: CanBuildFrom[This, MappedElem, That]): That
{% endcodeblock %}

As you can see there's an extra [implicit parameter](http://docs.scala-lang.org/tutorials/tour/implicit-parameters.html) `bf` of type 
`CanBuildFrom[This, MappedElem, That]`, which will give you a `Builder[MappedElem, That]` that can build a collection (of type `That`)
from the mapped elements (of type `MappedElem`). In short, `CanBuildFrom[This, MappedElem, That]` is a factory for `Builder[MappedElem, That]`,
which itself is a factory for `That`. When both type parameters `This` and `MappedElem` are given, the compiler can find the best eligible
for `bf` (according to [some](http://docs.scala-lang.org/tutorials/FAQ/finding-implicits.html) 
[perplexing](http://eed3si9n.com/revisiting-implicits-without-import-tax)
[rules](http://eed3si9n.com/implicit-parameter-precedence-again)) and consequently determines the static type of `That`. For example:

{% codeblock lang:scala %}
// bf : CanBuildFrom[Map[_,_], (Char, Int), Map[Char, Int]]
Map(1 -> ‘a’, 2 -> ‘b’).map(t => t._2 -> t._1)

// bf: CanBuildFrom[Iterable[_], Int, Iterable[Int]]
Map(1 -> ‘a’, 2 -> ‘b’).map(_._1)
{% endcodeblock %}

The `CanBuildFrom` can forward the call to the `genericBuilder[MappedElem]` method of the collection inferred in compile time,
so that the "right" runtime type can be selected via virtual dispatch.

Now you should have noticed the conceptual and implementation complexity brought by the seemingly simple "uniform return type principle".
But why do we need this at the first place?

Let's digress to talk about LINQ for a moment. I don't think the argument "LINQ sucks, because the type information of original collection is lost"
really stands, because I think this is exactly what it was designed to ignore. For most of the times, we often don't care about whether the `Iterable`
is a `Seq` or a `Set` or a `Map` or whatever. What we do with a collection is often just querying and consuming its content.
LINQ provides a uniform interface with consistent, lazy behavior to facilitate this. When you need a collection of certain type,
you explicitly convert the query result to it. When you need special behaviors of a `Set` or `Map` (`Dictionary`), you use their own interfaces.
But queries are queries, different collections are treated equally. Such simplicity is not a weakness, but a feature.

In my point of view, LINQ and Scala's collection operation are cosmetically similar but semantically different. LINQ *queries* a collection;
Scala's collection operation *transforms* a collection. (This may give you the clue why LINQ doesn't have a ForEach extension method.)
Scala's functional nature necessitates the collection transformation semantic: you need to be able to deal with the value of a collection
and compute a new value from it. And since Scala is also statically and strongly typed, the "uniform return type principle" is required to
make the system consistent. Thus the behaviors of collection operations should of course depend on the actual collection type and the type of
the target element. The operations are non-lazy (strict) by default to avoid unintended delay of the side-affects within the operations
(there's a more detailed explanation about the decision on laziness at the bottom of [this page](http://docs.scala-lang.org/overviews/collections/views.html)). 

What if we only want to query and consume the content of the collection, like we do in LINQ? I suggest using Iterator directly or convert the
collection to Stream:

{% codeblock lang:scala %}
scala> Set(1,2,3,4).iterator.map(_%2).foreach(print)
1010
scala> Set(1,2,3,4).toStream.map(_%2).foreach(print)
1010
{% endcodeblock %}

What comes with the complexity is great flexibility and power. Scala is expressive and seems quite easy, but the paradox is that you need to
spend much time learning to avoid misusing it. Scala is not easy, even in the case of these basic collection operations; it's important to
recognize that.