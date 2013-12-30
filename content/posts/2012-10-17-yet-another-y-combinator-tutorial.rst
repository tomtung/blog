Yet Another Y Combinator Tutorial
=================================

:date: 2012-10-17 11:32
:tags: functional, Lisp

After reading about the Y combinator in the book `The Little Schemer <http://www.amazon.com/dp/0262560992/>`__, simply staring at its code becomes a great way to kill time. In the past few days, whenever I got bored (or need an excuse for procrastination), I spent hours trying to make sense out of its mysterious implementation. It's like monad: everybody has a hard time reaching that "Eureka" moment, but once he finally groks it, he believes that he can explain it more clearly than the tutorial he read (which is often not the case).

So here I am writing yet another Y combinator tutorial. I think the reason why Y combinator is so hard to fathom is that when you read the code, you are facing its entire complexity. In fact, however, its derivation can be broken into a few fairly intuitive steps, and if each step is well-motivated, we no long need a "Eurika" to understand the whole thing.

The code snippets in this tutorial are written in `Racket <http://racket-lang.org/>`__, but it should be trivial to translate them into other Lisp dialects or other dynamic functional languages.  [1]_

``Y``? Why?
-----------

Before deriving the Y combinator, let see what it is about. Consider the following simple recursive function that returns the length of a given list:

.. code:: scheme

    (define len
      (λ (lst)
        (cond
          [(empty? lst) 0]
          [else (+ 1 (len (rest lst)))])))

    (len '(1 2 3 4 5)) ; => 5

Simple enough, except that if you think about it, it's quite weird: ``len`` is used in the process of defining ``len`` itself - that is, the identifier ``len`` is used before it has been bound to anything, since the lambda to which we intend to bind it hasn't yet been defined at that point! We should expect an "unbound identifier" error, but somehow the interpreter helps take care of it. But what if the interpreter is not so helpful? We have been able to write *anonymous functions* using lambda literals; can we write *recursive anonymous functions*, too?

Answering this question helps us better understand the essence of the language. If recursive anonymous functions is impossible, then ``define`` should be something essential to the language; otherwise it is merely a syntactic sugar, since everything can be anonymous.

Tell Me About ``U``\ r-\ ``self``
---------------------------------

.. raw:: html

   <!--
     This section uses the U combinator to implement an 'ugly' version of non-recursive 'len'.
     In the last section, we will use U to remove recursion from F to get Y.
   -->

We can't write the ``len`` function as we like to, so what shall we do? Maybe we can write some other function ``mk-len`` that constructs ``len`` for us. Let's start by simply wrapping a lambda without arguments around ``len`` to get a new function ``mk-len``. Then all uses of ``len`` can be substituted with ``(mk-len)``.

.. code:: scheme

    (define mk-len
      (λ ()
        (λ (lst)
          (cond
            [(empty? lst) 0]
            [else (+ 1 ((mk-len) (rest lst)))]))))

    ((mk-len) '(1 2 3 4 5)) ; => 5

We haven't got rid of the recursion in ``mk-len`` yet. Well, to achieve the effect of recursion, ``mk-len`` needs to somehow refer to itself using some name anyway - but not the name we ``define``\ d. Is there another way of binding a value to a name?

It turns out that there is: when we pass a value to a function as its argument, the value is automatically bound to the name of the corresponding parameter within the body of the function. That's why ``((λ (x) x) 123)`` returns ``123`` instead of an error "unbound identifier: x".

So how about passing the function ``mk-len`` as a argument of itself, so that it can refer to itself using the name of that parameter? Let's see:

.. code:: scheme

    (define mk-len
      (λ (self)
        (λ (lst)
          (cond
            [(empty? lst) 0]
            [else (+ 1 ((self self) (rest lst)))]))))

    ((mk-len mk-len) '(1 2 3 4 5)) ; => 5

With this simple trick, now ``mk-len`` can recurse without knowing its name! Let's further extract a function ``U`` to do the self-application ``(mk-len mk-len)``:

.. code:: scheme

    (define U
      (λ (f) (f f)))

    ((U mk-len) '(1 2 3 4 5)) ; => 5

Now we no longer need to give the function ``mk-len`` a name:

.. code:: scheme

    ((U (λ (self)
          (λ (lst)
            (cond
              [(empty? lst) 0]
              [else (+ 1 ((self self) (rest lst)))]))))
     '(1 2 3 4 5)) ; => 5

Congratulations! Now you know how to do recursion on anonymous functions!

By the way, the simple function ``U`` has a name: the **U combinator**. (Hold on, we'll get to the Y soon.)

The Chicken Or The Egg Or The Fixed Point
-----------------------------------------

.. raw:: html

   <!--
     This section explains why the fixed-point of mk-len is len,
     and implements a recursive function F for computing fixed-point.
   -->

While the U combinator allows us to write recursive anonymous functions, at the point of recursion we must always do the ugly self-application ``(self self)``. This is annoying. We would really want to write our ``mk-len`` as:

.. code:: scheme

    (define mk-len
      (λ (rlen)
        (λ (lst)
          (cond
            [(empty? lst) 0]
            [else (+ 1 (rlen (rest lst)))]))))

Now the problem is to find some function ``F`` that transforms ``mk-len`` into another function that behaves exactly the same as ``len``.

First let's take a look at this new function for a moment. It takes a function ``rlen`` as its argument and returns another function. It basically says: "give me a function ``rlen`` that can be used to compute the length of ``(rest lst)``, then I will *make* a function for you that can compute the length of ``lst``".

If ``lst`` is empty, what ``rlen`` you provide doesn't matter, since ``((mk-len rlen) empty)`` always returns ``0`` without calling ``rlen``. But when ``lst`` is not empty, if we want ``((mk-len rlen) lst)`` to return the length of ``lst``, we need to provide a ``rlen`` that correctly computes the length of ``(rest lst)``. If we provide a function that can compute the length of a list with 10 elements, ``mk-len`` returns a function that can compute the length of a list with 11 elements. If ``rlen`` is able to compute the length of a list with 100 elements, ``(mk-len rlen)`` can compute the length of a list with 101 elements.

It follows that if we could provide a ``rlen`` such that ``(rlen (rest lst))`` always correctly returns the length of ``(rest lst)`` for *any* non-empty ``lst``, then ``((mk-len rlen) lst)`` would always return the length of ``lst`` - that is, ``(mk-len rlen)`` would behave like the recursive ``len`` we defined at the beginning of this tutorial.

So what function should ``rlen`` be? Since ``lst`` can be *any list*, ``(rest lst)`` can also be *any list* (when ``lst`` is not empty). So we are basically asking for a ``rlen`` that is able to compute the length of *any list* - that is, ``rlen`` should also behave like ``len``.

In other words, to transform ``mk-len`` into a function that behaves like ``len``, we need to pass it a function ``rlen`` that behaves like ``len``, but the only way to get such a function is by transforming ``mk-len``. Now we seem to be stuck at this chicken-egg dilemma!

What should we do? Let's just cheat by passing ``len`` to ``mk-len``:

.. code:: scheme

    ((mk-len len) '(1 2 3 4 5)) ; => 5

It works as we expected. Observe carefully, we can notice something curious: ``(mk-len len)`` not only *behaves* like ``len``; in fact they are exactly *the same function*, i.e. ``len = (mk-len len)``. Therefore ``len`` is by definition the `fixed point <http://en.wikipedia.org/wiki/Fixed_point_(mathematics)>`__ of ``mk-len``. We can just define ``len`` in terms of ``mk-len`` following this definition, and it is equivalent to the original ``len``.

.. code:: scheme

    (define len
      (mk-len
       (λ (lst) (len lst))))

    (len '(1 2 3 4 5)) ; => 5

Now we can extract a function ``F`` that computes ``mk-len``'s fixed point ``len``:

.. code:: scheme

    (define F
      (λ (f)
        (local [(define fx
                  (f (λ (x)
                       (fx x))))]
          fx)))

    ((F mk-len) '(1 2 3 4 5)) ; => 5

And again the function ``mk-len`` can be anonymous:

.. code:: scheme

    ((F (λ (rlen)
          (λ (lst)
            (cond
              [(empty? lst) 0]
              [else (+ 1 (rlen (rest lst)))]))))
     '(1 2 3 4 5)) ; => 5

Congratulations (again)! Now you know how to do recursion on anonymous functions without the ugly ``(self self)``! We are done...right?

Simply ``Y``
------------

.. raw:: html

   <!--
     This section use U to get Y from F.
     Then derive the Turing combinator using the same technique.
   -->

Not quite, because we are still cheating: the definition of fixed point ``fx`` in ``F`` blatantly calls its own name to recurse. It seems that we are starting all over again. Are we making any progress?

In fact we have made progress: the users of our ``F`` function can now write recursive anonymous functions using a very clean syntax, and we are free to do whatever we want to eliminate recursion of ``fx`` in ``F``, as long as its behavior doesn't change.

What do we do? Remember how we used the simple U combinator to avoid recursion? Let's try it on ``fx``:

.. code:: scheme

    (define F
      (λ (f)
        (U (λ (self)
             (f (λ (x)
                  ((self self) x)))))))

    ((F mk-len) '(1 2 3 4 5)) ; => 5

The self-application ``(self self)`` is still somewhat ugly, but it only appears once in ``F``. Someone needs to do the dirty job, so that all functions like ``mk-len`` can be pretty. That's life.

Now if we put the definition of ``U`` in ``F``, and change a few names, we get:

.. code:: scheme

    (define Y
      (λ (f)
        ((λ (g) (g g))
         (λ (g)
           (f (λ (x) ((g g) x)))))))

    ((Y mk-len) '(1 2 3 4 5)) ; => 5

This ``Y`` is what we call: (drum roll) ... the famous **Y combinator** discovered by `Haskell Curry <http://en.wikipedia.org/wiki/Haskell_Curry>`__! There you have it. Not that hard, right?

In fact, if we define ``F`` in different ways and then use ``U`` to remove recursion, we can easily get many non-recursive functions that work just like ``Y``. For example, because ``(F f)`` returns the fixed point of ``f``, then by definition ``(F f) = (f (F f))``. Let's write the definition of ``F`` in this way  [2]_:

.. code:: scheme

    (define F
      (λ (f)
        (f (λ (x)
             ((F f) x)))))

    ((F mk-len) '(1 2 3 4 5)) ; => 5

Similarly, we can use ``U`` to remove the recursion:

.. code:: scheme

    (define F
      (U (λ (self)
           (λ (f)
             (f (λ (x)
                  (((self self) f) x)))))))

    ((F mk-len) '(1 2 3 4 5)) ; => 5

Then, again, put in the definition of ``U`` and change some names:

.. code:: scheme

    (define Θ
      ((λ (f) (f f))
       (λ (g) (λ (f)
                (f (λ (x)
                     (((g g) f) x)))))))

    ((Θ mk-len) '(1 2 3 4 5)) ; => 5

This ``Θ`` is what we call: (drum roll) ... the (less) famous **Turing combinator** discovered by `Alan Turing <http://en.wikipedia.org/wiki/Alan_Turing>`__!

I can go on and on. Such higher-order functions like ``Y`` and ``Θ`` that computes a fixed-point of other functions are called `fixed-point combinators <http://en.wikipedia.org/wiki/Fixed-point_combinator>`__. In fact, there are *infinitely many* of them.

So ``Y`` is not so mysterious, and it's not so special, either. I hope you are not too disappointed.

Wrap It Up (Pun Intended)
-------------------------

.. raw:: html

   <!--
     This section demonstrates the power we get from parameterizing the
     recursion point. [Mcadam 97]
   -->

Now you know what Y combinator does: it computes the fixed point of another function. We can use Y to achieve anonymous recursion because a recursive function (like ``len``) can be rewritten as the fixed-point of another function (like ``mk-len``). So ``(Y mk-len)`` gives us ``len``.

But there's something more interesting. Consider some function ``f``, in its definition it invokes another function ``g``. If we want to control who ``f`` is talking to, we can make ``g`` an parameter. Now step back and stare at ``mk-len`` for a moment. Think about what we have done: we parameterized the point of recursion! When the normal ``len`` calls itself, it is very certain about it, and there's nothing we can do. However, ``mk-len`` has no idea what ``rlen`` we pass to it! By writing recursion as fixed point computation, we gain the power and freedom of controlling what happens in a recursive call without modifying ``mk-len``'s code.

Consider that we want to print some log at each recursive call. For a normal recursive function like ``len``, there's nothing we can do but to modify the code. If there are 10 such functions, we need to modify each of them and create a lot of mess. On the other hand, for functions like ``mk-len``, obviously we can simply modify our fixed-point combinator:

.. code:: scheme

    (define Y
      (λ (f)
        ((λ (g) (g g))
         (λ (g)
           (f (λ (x) (begin (displayln x) 
                            ((g g) x))))))))
    ((Y mk-len) '(1 2 3 4 5))

This prints out the following:

::

    (2 3 4 5)
    (3 4 5)
    (4 5)
    (5)
    ()

Now if we want to print log *after* each recursive call, we would need to modify the ``Y`` again. If we want to do something else, modify again...

Well, we can do better than this. We can create *wrappers* around functions like ``mk-len`` that controls the recursion calls in different ways. Here's an example:

.. code:: scheme

    (define log-start-wrapper
      (λ (mk-len)
        (λ (log)
          (λ (x)
            (begin
              (printf "Start computing for: ~a~n" x)
              ((mk-len log) x))))))

    ((Y (log-start-wrapper mk-len)) '(1 2 3 4 5))

It prints out the following:

::

    Start computing for: (1 2 3 4 5)
    Start computing for: (2 3 4 5)
    Start computing for: (3 4 5)
    Start computing for: (4 5)
    Start computing for: (5)
    Start computing for: ()

Similarly, we can define ``log-start-wrapper`` that prints a log *after* each recursive call:

.. code:: scheme

    (define log-end-wrapper
      (λ (mk-len)
        (λ (log)
          (λ (x)
            (local [(define result
                      ((mk-len log) x))]
              (begin
                (printf "Result for ~a is: ~a~n" x result)
                result))))))

    ((Y (log-end-wrapper mk-len)) '(1 2 3 4 5))

It prints out:

::

    Result for () is: 0
    Result for (5) is: 1
    Result for (4 5) is: 2
    Result for (3 4 5) is: 3
    Result for (2 3 4 5) is: 4
    Result for (1 2 3 4 5) is: 5

We can even use several wrappers together:

.. code:: scheme

    ((Y (log-start-wrapper (log-end-wrapper mk-len))) '(1 2 3 4 5))

This gives you:

::

    Start computing for: (1 2 3 4 5)
    Start computing for: (2 3 4 5)
    Start computing for: (3 4 5)
    Start computing for: (4 5)
    Start computing for: (5)
    Start computing for: ()
    Result for () is: 0
    Result for (5) is: 1
    Result for (4 5) is: 2
    Result for (3 4 5) is: 3
    Result for (2 3 4 5) is: 4
    Result for (1 2 3 4 5) is: 5

In this example, wrappers are like `decorators <http://en.wikipedia.org/wiki/Decorator_pattern>`__ for recursive function.

With such flexibility, there are actually more funky stuff we can do with wrappers. For example, we can cache the result of recursive calls to avoid redundant computation (a.k.a `memoization <http://en.wikipedia.org/wiki/Memoization>`__), or modify the result (or even change the type of the result) of the recursive calls. You can read this interesting paper `"That About Wraps it Up" <http://www.lfcs.inf.ed.ac.uk/reports/97/ECS-LFCS-97-375/>`__ for more information.

.. [1]
   In the cases of statically typed languages, it gets more complicated or even impossible. Let's just ignore them in this tutorial for the sake of clarity.

.. [2]
   A subtle point here: we write ``(λ (x) ((F f) x))`` instead of just ``(F f)``. This is because otherwise in order to pass ``(F f)`` as an argument of ``f``, we first need to evaluate ``(F f)``, which expands to ``(f (F f))``, to evaluate which we again need to evaluate first evaluate ``(F f)``... The program will hang until it finally crashes from a stack overflow. Wrapping a lambda around ``(F f)`` delays its evaluation, making sure ``x`` passed to ``(F f)`` is evaluated first.
