# Contributing

The dictionary is a set of `\newglossaryentry` definitions spread over
`ADictML_Math.tex`, `ADictML_CoreML.tex`, `ADictML_RL.tex`,
`ADictML_Regulation.tex`, `ADictML_MLSystems.tex` and
`ADictML_HealthCare.tex`. An entry looks like this:

```latex
\newglossaryentry{key}
{name={full name (ABBR)},
    description={First\index{full name (ABBR)} sentence defines the term.
        ...
        \\
        See also: \gls{relatedterm1}, \gls{relatedterm2}.},
    first={full name (ABBR)},
    type=CHAPTER_TYPE,
    text={ABBR}
}
```

## Three rules that keep the build green

1. **Every `\gls{key}` must name an existing entry.** An undefined key stops
   the build. Check before you use one:
   `grep -rn 'newglossaryentry{key}' ADictML_*.tex`.
2. **No blank line inside a `\newglossaryentry`.** Its options group is not
   `\long`, so a paragraph break fails the build at that entry. Separate
   paragraphs with `\\`.
3. **No `\\` immediately after `\end{figure}`.** The float already ends the
   paragraph, and the extra break raises "There's no line here to end."

## Editor support

`dictml_lsp.py` is a language server for this repository. It needs no
dependencies — standard-library Python 3.8+ speaking LSP over stdio — and it
answers, while you type, the questions that otherwise cost a build:

* completion for `\gls{}` / `\glspl{}` (every key, with its `name=` and the
  opening of its description), for `\citep[...]{}` from
  `assets/Literature.bib`, and for the macros of `assets/ml_macros.tex`;
* hover and go-to-definition for all three;
* rename of a glossary key across every source file at once;
* diagnostics for an unknown `\gls{}` key and for a macro one or two
  keystrokes away from a real one (`\hilbertpace` → `\hilbertspace`), each
  with a suggestion.

Check that it works without an editor:

```bash
python3 dictml_lsp.py --selftest    # one of each request
python3 dictml_lsp.py --index       # what it found in this checkout
```

**VS Code.** Install the two-file client once:

```bash
cd vscode-dictml && npm install
mkdir -p ~/.vscode/extensions/dictml-ls
cp -R package.json extension.js node_modules ~/.vscode/extensions/dictml-ls/
```

Then *Developer: Reload Window*, open one of the `ADictML_*.tex` files, and
hover a `\gls{...}` key. `dictml.serverPath` may be left empty: the client
looks for `dictml_lsp.py` in the workspace folder. The server is stdlib-only,
so `dictml.pythonPath` can stay `python3` — no virtual environment to point
at. Its output, including any traceback, goes to the **ML Dictionary**
channel of the Output panel, and *ML Dictionary: Restart Server* is in the
command palette.

**Neovim.**

```lua
vim.lsp.start({name = 'dictml',
               cmd = {'python3', vim.fn.getcwd() .. '/dictml_lsp.py'},
               root_dir = vim.fn.getcwd()})
```

It runs alongside LaTeX Workshop or texlab rather than replacing them: the
editor queries every provider registered for the file and merges the
results, so one hover shows both the LaTeX intelligence and the glossary
entry.

## Style

* Impersonal voice, American English, no self-reference to the book.
* Open concrete, then abstract: the first sentence should be readable by a
  first-year student without looking up a formalism.
* One word per concept — a data point is not a sample or an instance;
  training is not fitting.
* Link technical nouns with `\gls{}` in the prose, not only under
  "See also".
* Macros before raw notation: check `assets/ml_macros.tex` before writing
  `\mathbf{x}`.
* Give a pinpoint with a citation (`\citep[Sect.~2.3.1]{Key}`) when you can
  verify it against the source. An unverified section number is worse than
  none.

## Pull requests

One term per commit, with the message starting `add entry: <key>` or
`revise entry: <key>`, so `git log --grep=<key>` finds the history of a
term. Notes in the diff about things that look wrong are welcome even when
you do not fix them.
