=========================
A Rationale for protograf
=========================

.. |dash| unicode:: U+2014 .. EM DASH SIGN
.. |check| unicode:: U+2610 .. BALLOT BOX

Why do this?
============

I realize that there are many software programs available that can be used for
creating graphics and layouts for games, some of which are very sophisticated
indeed; for example, Photoshop, CorelDraw, Affinity, Inkscape etc. as well as
various ones designed specifically for the Mac which obviously excels in this
field.

However, for someone like myself who is not a graphics designer and doesn't
want to spend time learning all the complexities of these programs, I wanted
a tool that was simple but flexible, aligned with my own capabilities
and ambitions.

To be clear: **protograf** is *not* a tool that in any way competes with
full-scale graphics or art programs, and if you are already fully proficient
with such programs for designing games, you may want to skip this one...

Why use this?
=============

**protograf** is not going to change your life forever and make you wonder how
you ever managed without it. It's not the best tool for every project nor is
it better than everything else.  However, it is possible that for some cases
for some people it will be a helpful tool in the process of board game design.

Most people who start off a game's design process are going to be drawing by
hand on sheets of paper or card, or scribbling on small card-sized pieces.

When things are in a state of flux, you don't want to be committed to anything
fancy that takes lots of time or effort to change.  However, at some point,
you need to share your creation with a wider group of people; friends, family
or even fellow game designers and game playtesters.  This means converting the
scribbles into a digital format which has legible text and clear graphics.

At this point you're **not** trying to create a fancy polished project that is
ready for production and sale.  You just need a prototype.  If you are *not* a
graphic designer, then you have a choice. Do you now try and learn a graphic
design program, or do you rather just make use of any existing tools that you
have |dash| for example, a word-processor or spreadsheet |dash| which are not
specifically designed to meet the typical requirements for a game layout
and could be awkward to work with?

At this point you can consider looking at **protograf** to meet your needs.

Who would use this?
===================

The approach taken by **protograf** is one that might appeal to those who are
less visual thinkers and more logic / word thinkers.

The primary way that you express yourself is through logically constructed
discussions and arguments where the details matter.  With **protograf**, you
start off simple and gradually add more layers of detail as you go on.
Its very easy to turn things on and off, and everything that you've done so
far is directly visible to you, and not hidden away in layers of menus, or
complex sequences of changes.

Getting to a final product might seem intimidating if you are looking at a
100-line long "final script", but because it's a *process* that you are in
control of from start to finish, your involvement in that process means that
all the steps in it will make sense to you.

In addition, when you come back to your **protograf** script in three months,
six months |dash| or even a year! |dash| it should remain just as readable
as it was when you first created it.

How is this designed?
=====================

The aim was to develop a program that is reasonably simple, quick and useful;
and which supports rapid development of a clean and simple prototype design
that will change and develop over a number of versions.

The three principles of **protograf** |dash| as much as any piece of software
can have "principles" |dash| are clarity, consistency, and comprehensiveness.

*Clarity* means that the terminology and approach to constructing elements
of a game design should be reasonably obvious.  I appreciate that nothing
is fully intuitive and inherently obvious, and every new thing we do relies to
some degree on our previous knowledge. So **protograf** tries to avoid jargon,
and also to use "long hand", rather than quirky abbreviations or special
characters, which may not be that easy to remember.

As an example, to draw a rectangle on a page you would use a command like:
``Rectangle(x=3, y=5, height=6, width=7)``.  If you understand the basic
notation that ``x`` is used to measure distance of the Rectangle's top corner
from the left-hand edge of the page and ``y`` is used to measure its distance
from the top edge of the page, then it's reasonably clear where this rectangle
would be drawn and what it would look like.

The language used for **protograf** tries to match everyday usage of terms
and/or terms already used by existing, similar software.

*Consistency* is about doing similar things in the same way.  An ellipse shape
is similar to a rectangle except that - obviously! - it's drawn with curves
rather than straight lines.  The instruction for **protograf** to do this would
look something like ``Ellipse(x=4, y=6, height=7, width=8)``. Hopefully it's
obvious that there is consistency in the way you draw these two kinds of shapes.

*Comprehensiveness* is much more of a challenge.  By it's very nature graphics
is an open-ended domain and almost anything that one can imagine can be
depicted in some way, shape or form.  It's therefore unlikely that any single
software program can hope to emulate that degree of creativity; the best you
can ever achieve is some reasonable subset of that.  That's where the evolving
nature of programs such as **protograf** comes in.

Hopefully, though, there is a reasonable enough set of features available to
make **protograf** useful now |dash| as more people use it, ideas for new or
different kinds of things will be incorporated and more polish will be
added to existing features.
