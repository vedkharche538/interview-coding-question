Arachnys Backend Test - Ultimate Beneficial Owners
==================================================

Introduction
------------

Company ownership can be complicated: a single company has ownership
divided many ways (shares, partnership stakes, etc), and some of those
owning entities are in turn companies that issue shares which are owned
by many different entities -- and so on for many levels.

Most of the time, this is just a normal part of "the economy is
complicated". However, this complexity can be used to enable fraud,
money-laundering, and other criminal activity: the true beneficiary of
a financial transaction can be obfuscated behind many layers of proxy
ownership, or hidden by creating a self-referential structure in which
a company ultimately "owns itself" (via multiple intermediaries) with
no traceability to a human.

Efficiently reasoning about complex financial ownership structures is
therefore important to prevent crime, and manage risk. Automating this
process is part of our product offering at Arachnys.

For this task, we'll be asking you to write a program to process a set
of ownership relationships and identify ultimate beneficial owners
(i.e. resolving and removing intermediary owners).

Please keep your solution private and do not share it or post it
publicly.


Problem Specification
---------------------

Given a set of ownership relationships (including intermediate owners),
calculate the ultimate ownership of an entity, flattening and removing
intermediate owners.

### Input and output format

Both input and output to your program should be a sequence of text
lines, each consisting of:

- An owned entity label, as a string consisting of lowercase ASCII
  letters (`a-z`) 
- An owning entity label, as a string consisting of lowercase ASCII
  letters (`a-z`)
- The percentage ownership, as an integer between zero and 100

with each element being separated by spaces.

The lines forming the input will be provided **to** your program on
standard input. The lines forming the output must be written **by**
your program to standard output.

Order of lines is unimportant for both input and output.


### Ownership calculations

For each set of input lines, your program must identify the ultimate
beneficial owners of the entity identified by the label `a` (ASCII
0x61). You do not need to provide any configuration mechanism to adjust
this `a` to some other label.

In the case of simple flat ownership, your program may not need to do
anything. For example, a very simple input might be:

```
a b 50
a c 30
a d 20
```
which would mean:

- `b` owns 50% of `a`
- `c` owns 30% of `a`
- `d` owns 20% of `a`


the correct output would be:

```
a b 50
a c 30
a d 20
```

(this, and all and of the other examples in this document, along with
their expected output, are available in the `sample` directory you
received with this test).

### Unrelated ownerships

The input may contain unrelated ownership relationships, which should not
appear in the output:

```
a b 50         a b 50
a c 30    ->   a c 30
a d 20         a d 20
e f 100
```

(`e` and `f` are never linked to `a`)


### Intermediate owners

Some entities are "intermediate owners": they own an entity, and are
themselves _owned by_ another entity. Ultimate Beneficial Ownership is
about ownership by "natural persons", so intermediate entities cannot
be _ultimate_ beneficial owners. If the input contains intermediate
entities, they should not appear in the output, although they _should_
be used to calculate the ultimate ownership:

```
a b 50         a b 50
a c 50    ->   a d 50
c d 100
```  

(`c` is an intermediate owner)

### Unattributed ownership

In some situations, ownership information for an entity is incomplete.
It's useful to understand what fraction of the ownership of an entity
is unattributed.

Your program should determine what fraction of the ownership of the
target entity (`a`) is not attributed to any owning entity, and
assign it to the special entity `?` (ASCII 0x3f).

```
a b 40         a ? 35
a c 50    ->   a b 40
c d 50         a d 25
```  

(10% of ownership is "lost" because it isn't attributed to either `b`
or `c`, and 25% is lost because `c` owns 50% and itself is missing half
of its ownership).

### Ownership cycles

One way to disguise the ownership of an entity is to create cyclic
ownership relationships, where multiple shell companies are owned by
each other with no link back to a real human. Each individual shell
company has a plausible set of ownership relationships, but the overall
structure makes it impossible to determine ultimate ownership.

In cases where ownership passes through such a cyclic structure, your
program should assign the _entire_ fraction of ownership that touches
the cycle to the special entity `?`, as if it were unknown:

```
a b 50         a ? 50
a c 50    ->   a b 50
c d 50
c e 50
d c 50
d e 50
e c 50
e d 50
```  

(50% of ownership goes to `c`, which is in a triangular ownership
structure with `d` and `e` where each owns half of the other two).


Tests
-----

The `sample` directory includes a number of examples of input
(`in_<n>.txt`) and their corresponding output (`out_<n>.txt`),
including all the examples shown above.

There is a helper script `run_tests.py` which will
help you to check your solution against these samples.

For example, if your solution were an executable file called `ubo.py`,
you could check it using:

    python3 run_tests.py python3 ./ubo.py

or alternatively if your solution contains the shebang line:

    python3 run_tests.py ./ubo.py

These tests will sort the output of your program, and then diff it
against the expected output in `sample/out_<n>.txt`, displaying any
mismatches in unified diff format.

You are not required to use these: they are provided for your
convenience.

Assessment Notes
----------------

The purpose of this test is to help you demonstrate to us that you have
the technical skills we're looking for, and to do so in a way that is
respectful of your time and tries to control for as many confounding
factors as possible.

We're looking for a solution that, ideally:

- Passes all the test cases
- Is reasonably general (i.e. could tolerate most comparable test cases)
- Is simple and clear enough that a junior engineer could confidently
  review it and sign off on using it in production


To help us control for extraneous factors, we aren't looking for:

- Lots of time spent polishing
- Unit tests
- Documentation
- Handling of edge cases not described in the spec
- Optimisations and fast handling of much larger test cases
- Defensive error-handling and logging


(We care about many of those those things, but we can't evaluate
solutions consistently and fairly if we weight them in our review).


The following sections go into these topics in more detail. This
guidance is primarily intended to ensure that you don't burn time on
areas that we can't fairly assess you on.


### Time

This problem is supposed to take up to two hours of your time. It's
possible to do it faster, although you should not feel pressured to do
so: if your solution is correct for all the test cases, there is no
magic missing trick.

The two hour bound is unenforced, and based on trust, but please don't
sink significant extra time into the problem. If you've spent about two
hours and are passing some but not all of the test cases, please _do_
send us your solution anyway: scoring for this exercise is not binary.


### Language & Portability

Please write your solution as a single executable Python 3 script with
no dependencies.


### Tests & Documentation

We care a lot about testing, and we value clear documentation, but it's
difficult for us to evaluate your solution on this basis without
selecting for time spent tidying up the solution.

Therefore:

- We will not evaluate you on any tests you send us
  along with your solution
- We will not evaluate you on any prose documentation
  (including docstrings, JavaDoc, etc) you send us along with your
  solution; short embedded comments are fine, but we won't take large
  prose block comments into account
- We will not evaluate you on the presence of Python type hints in
  your solution: we use Mypy ourselves, but while type
  hints can be more than documentation, they are subject to the same
  "polishing" pressures as documentation
- We will not evaluate you on logging from your code

If there are any notes necessary to build & run your solution, please
add them to `CANDIDATE-NOTES.md`.


### Code Style

We will be looking at your code from the perspective of clarity,
structure, and style. We won't nitpick minor formatting details, but we
will be thinking about how easy your code would be for others to
review, understand, and modify.


### Performance

We don't want to divert your time into optimisation or specialised
algorithms: we assume you could look those up if you needed to,
and we don't want you to spend your test time debugging complex
optimisations.

If your solution is fast enough to solve the test cases we have
provided without being painfully slow (e.g. it takes a few seconds on a
typical modern laptop), that's fast enough.


### Error Handling

You should assume that we will provide syntactically and
semantically valid input to your program, except as explicitly
documented in the specification.


Feedback & Questions
--------------------

We'd love to hear any feedback you have on this test (either on details
or on the concept).

If you have any questions or identify any ambiguities, please get in
touch, and we'll clarify if we feel we can do so in a way that doesn't
bias the test.
