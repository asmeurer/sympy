# Markdown Demo

(md-header-2)=
## Level 2 header

The anchor for this header in the URL will also be `#md-header-2`.

### Level 3 header

This is a file written in Markdown.

Here is some code

```py
def func(x):
    return x + 1
```

Inline math like $\sin^2 x + \cos^2 x = 1$ and equations like

$$
\int_0^\infty \frac{1}{x^2}\,dx
$$

are supported.

<!-- Bad math looks like $\notareallatexfunction$. -->

Markdown supports mixed formatting, like `code`, *italics*, and *`italics
code`*.

The linkify extension makes links like https://sympy.org or docs.sympy.org
automatically clickable without using formatting.

Footnotes are supported.[^footnote]

[^footnote]: And footnotes can *include* `Markdown` **formatting**, of course.

Links can cross-reference other parts of the documentation. Here is a link to
the [simplify()](sympy.simplify.simplify.simplify) documentation. Here is a
link to a header in [this document](md-header-2).

You can use arbitrary rst directives with three backquotes. For example

```{note}
This is a note. Even though `note` is an RST directive, the formatting here is
still done in Markdown.
```

There is also a fallback for evaluating raw RST (this is currently needed, for
instance, to use autodoc directives):

```{eval-rst}

.. list-table:: Table of functions
   :header-rows: 1

   * - Function
     - Description
   * - ``simplify``
     - simplifies expressions
   * - ``solve``
     - solves equations
```

Cross-references are specified using `(section-name)=`. These can be
referenced from other Markdown documents or from RST documents using the usual
RST cross-reference syntax (e.g.,  ``` :ref:`section-name` ```).
