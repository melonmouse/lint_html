# Linter for HTML files

Has your browser ever changed your HTML for you, breaking your design or
javascript in the process? That can happen when your HTML is not up to spec.
`lint_html.py` is a wrapper around [Tidy](https://html-tidy.org) that will
tell you if and where your HTML is not correct.

Example use:

```./lint_html.py index.html```

```./lint_html.py index.html --custom-inline-tags math```
