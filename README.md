# Linter for HTML files

Has your browser ever changed your HTML for you, breaking your design or
javascript in the process? That can happen when your HTML is not up to spec.
`lint_html.py` is a wrapper around [Tidy](https://html-tidy.org) that will
tell you if and where your HTML is not correct.

Example use:

```./lint_html.py index.html```

```./lint_html.py index.html --custom-inline-tags math```

Dependencies: [Tidy](https://html-tidy.org) and python3.

## The competition

### html5-lint

https://github.com/mozilla/html5-lint

- well maintained
- nice interface, not very configurable
- official from [Mozilla](https://www.mozilla.org/)
- *does not work offline*

### htmllint-cli

https://github.com/htmllint/htmllint-cli

- well maintained
- very configurable
- very pupular - but not based on a parser that is affiliated with something official
- works offline

### Tidy (best official offline option)

https://html-tidy.org

- well maintained
- *clunky interface*
- affiliated with the [W3C](http://www.w3.org/)
- works offline

### lint_html

https://github.com/melonmouse/lint_html

- just starting
- simple interface, not very configurable
- based on official parser (Tidy)
- works offline
