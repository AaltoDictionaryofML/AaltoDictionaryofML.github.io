#!/usr/bin/env python3
r"""
dictml_lsp.py — a language server for this dictionary.

The generic LaTeX servers (texlab, digestif) know \ref and \cite but nothing
about \gls{}, the book's macros, or its linters — which is where this
project's mistakes actually live: an undefined \gls key or a mistyped macro
fails the main `make`, and the per-term export only warns. This server
answers, inside the editor, the questions that otherwise cost a build:

  completion    \gls{ | \glspl{ | \Gls{ | \Glspl{   -> glossary keys
                \citep{ | \citealp{ | \citet{       -> bib keys
                \                                    -> macros of ml_macros.tex
  hover         a key shows the entry's name and the opening of its
                description; a bib key its author/title/year; a macro its body
  definition    jump to \newglossaryentry{key}, to the Literature.bib entry,
                or to the \newcommand in assets/ml_macros.tex
  rename        rename a glossary key across every chapter file at once
                (the featuremap -> featuretransformation kind of change)
  diagnostics   live: \gls{} keys and \ macros that do not exist
                on save: the fast deterministic linters, whose output is
                already "file:line:col: CODE message"

Speaks LSP 3.17 over stdio with no third-party dependency: the framing and
JSON-RPC are ~60 lines below, matching the stdlib-only convention of the
check_*.py scripts.

Editor setup
------------
Neovim:
    vim.lsp.start({name='dictml', cmd={'python3','scripts/dictml_lsp.py'},
                   root_dir=vim.fn.getcwd()})
VS Code: any generic LSP-client extension, pointed at
    python3 /Users/.../scripts/dictml_lsp.py     (filetype: latex/tex)

Try it without an editor
------------------------
    python3 scripts/dictml_lsp.py --selftest     # index + one of each request
    python3 scripts/dictml_lsp.py --index        # what the server knows
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The same book lives in two repositories with different file names: the
# working copy calls its glossary files chapter_*.tex, the public course
# edition (github.com/AaltoDictionaryofML) calls them ADictML_*.tex. Nothing
# below is hardcoded to either — the root is where the entry files are, and
# the macro file and bibliography are found by name under it.
ENTRY_GLOBS = ("chapter_*.tex", "ADictML_*.tex")
MACRO_NAMES = ("ml_macros.tex",)
BIB_NAMES = ("Literature.bib",)


def _find_root(start):
    """Nearest directory at or above `start` that holds glossary files."""
    d = os.path.abspath(start)
    for _ in range(6):
        for pat in ENTRY_GLOBS:
            if glob.glob(os.path.join(d, pat)):
                return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return os.path.abspath(start)


def _find_file(root, names):
    for name in names:
        direct = os.path.join(root, "assets", name)
        if os.path.isfile(direct):
            return direct
        hits = glob.glob(os.path.join(root, "**", name), recursive=True)
        if hits:
            return sorted(hits, key=len)[0]
    return None


def set_root(start):
    """Point the server at a book: env override, else the given directory,
    else the script's own repository. The editor's rootUri wins when it
    names a directory that actually holds glossary files, so running the
    script by absolute path from another checkout indexes THAT checkout."""
    global ROOT, MACROS, BIB
    ROOT = _find_root(os.environ.get("DICTML_ROOT") or start)
    MACROS = _find_file(ROOT, MACRO_NAMES)
    BIB = _find_file(ROOT, BIB_NAMES)
    return ROOT


ROOT = MACROS = BIB = None
set_root(os.getcwd() if any(glob.glob(os.path.join(os.getcwd(), p))
                            for p in ENTRY_GLOBS) else os.path.dirname(HERE))


def entry_files(root=None):
    root = root or ROOT
    out = []
    for pat in ENTRY_GLOBS:
        out += glob.glob(os.path.join(root, pat))
    return sorted(set(out))

# linters that are fast and deterministic enough to run on every save; each
# prints "file:line[:col]: ... message" lines that map straight to diagnostics
SAVE_LINTERS = ["check_parbreaks", "check_articles", "check_plurals",
                "check_bullshit", "check_raw_notation", "check_margins"]

GLS_RE = re.compile(r"\\(Gls|Glspl|gls|glspl)\{([^}]*)\}")
CITE_RE = re.compile(r"\\(?:citep|citealp|citet|cite)\s*(?:\[[^\]]*\])*\{([^}]*)\}")
MACRO_USE_RE = re.compile(r"\\([a-zA-Z]+)")
ENTRY_RE = re.compile(r"\\newglossaryentry\{([^}]*)\}")
DEF_RE = re.compile(r"(?m)^\s*\\(?:newcommand|renewcommand|DeclareMathOperator)\*?\{?\\([a-zA-Z]+)\}?")

# macros that come from LaTeX or loaded packages rather than ml_macros.tex
KNOWN_LATEX = set("""begin end newglossaryentry gls glspl Gls Glspl citep citealp citet cite
ref eqref label index texttt emph textbf textit href url item itemize enumerate figure center
caption tikzpicture addplot axis draw fill node foreach scope shift includegraphics
frac sqrt sum prod int lim log exp min max argmin argmax sup inf cdot cdots ldots vdots dots
left right big Big bigg Bigg quad qquad text mathrm mathbf mathcal mathbb operatorname
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi
pi rho sigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon
Phi Psi Omega partial nabla infty in notin subset subseteq supseteq cup cap setminus times
leq geq neq approx equiv sim propto rightarrow leftarrow mapsto to top bot forall exists
langle rangle lVert rVert lvert rvert mid colon nonumber align equation split cases matrix
pmatrix bmatrix vspace hspace centering small scriptsize footnotesize normalsize par newline
citealt bibliography printglossary makeglossaries newpage clearpage phantom widehat widetilde
overline underline boldsymbol displaystyle limits
succ prec succeq preceq wedge vee tanh sinh cosh arcsin arccos arctan mbox mathsf mathit
star dagger ddagger circ bullet oplus otimes perp parallel angle triangle square diamond
lfloor rfloor lceil rceil binom choose pmod bmod gcd deg dim ker det Pr
huge Huge LARGE Large large tiny lstset lstinputlisting labelsep labelwidth itemsep parskip
parindent textwidth columnwidth linewidth hfill vfill noindent newcommand renewcommand
documentclass usepackage input include maketitle tableofcontents appendix chapter section
subsection subsubsection paragraph footnote textcolor colorbox definecolor setlength
addtolength renewcommand providecommand ensuremath relax hspace hrule vrule multicolumn
hline cline toprule midrule bottomrule captionsetup subcaption subfigure""".split())


# ── index ─────────────────────────────────────────────────────────────
class Index:
    """Everything the server knows, rebuilt from disk on demand."""

    def __init__(self):
        self.keys = {}     # gls key   -> {file, line, name, blurb}
        self.bib = {}      # bib key   -> {file, line, label}
        self.macros = {}   # macro     -> {file, line, body}
        self.build()

    def build(self):
        self.keys, self.bib, self.macros = {}, {}, {}
        self.local, self.usage = set(), {}
        for f in entry_files():
            txt = open(f, encoding="utf-8", errors="replace").read()
            starts = [0]
            for ln in txt.split("\n"):
                starts.append(starts[-1] + len(ln) + 1)
            for m in ENTRY_RE.finditer(txt):
                key = m.group(1)
                line = txt.count("\n", 0, m.start())
                span = txt[m.end():m.end() + 3000]
                name = (re.search(r"name=\{([^}]*)\}", span) or [None, key])[1] \
                    if re.search(r"name=\{([^}]*)\}", span) else key
                desc = re.search(r"description=\{(.{0,400})", span, re.S)
                blurb = _plain(desc.group(1)) if desc else ""
                self.keys[key] = {"file": f, "line": line, "name": name,
                                  "blurb": blurb}
        if BIB and os.path.isfile(BIB):
            txt = open(BIB, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"(?m)^@(\w+)\s*\{\s*([^,\s]+)\s*,", txt):
                body = txt[m.end():m.end() + 1200]
                def field(n):
                    mm = re.search(rf"{n}\s*=\s*\{{(.*?)\}}", body, re.S)
                    return re.sub(r"\s+", " ", mm.group(1)).strip() if mm else ""
                self.bib[m.group(2)] = {
                    "file": BIB, "line": txt.count("\n", 0, m.start()),
                    "label": f"{field('author')} ({field('year')}). "
                             f"{field('title')}"}
        self.local = set()
        for f in sorted(glob.glob(os.path.join(ROOT, "*.tex"))) + \
                sorted(glob.glob(os.path.join(ROOT, "assets", "*.tex"))) + \
                ([MACROS] if MACROS else []):
            txt = open(f, encoding="utf-8", errors="replace").read()
            self.local |= set(re.findall(
                r"\\(?:def|newcommand|renewcommand|providecommand|"
                r"pgfmathsetmacro|newlength|newsavebox)\*?\{?\\([a-zA-Z]+)", txt))
        self.usage = {}
        for f in entry_files():
            for name in MACRO_USE_RE.findall(
                    open(f, encoding="utf-8", errors="replace").read()):
                self.usage[name] = self.usage.get(name, 0) + 1
        if MACROS and os.path.isfile(MACROS):
            txt = open(MACROS, encoding="utf-8", errors="replace").read()
            for m in DEF_RE.finditer(txt):
                line = txt.count("\n", 0, m.start())
                self.macros[m.group(1)] = {
                    "file": MACROS, "line": line,
                    "body": txt.split("\n")[line].strip()}

    def known_macro(self, name):
        return name in self.macros or name in KNOWN_LATEX


def _plain(tex):
    t = re.sub(r"\\(?:Gls|Glspl|gls|glspl)\{([^}]*)\}", r"\1", tex)
    t = re.sub(r"\\(?:citep|citealp|citet|cite)\s*(?:\[[^\]]*\])*\{[^}]*\}", "", t)
    t = re.sub(r"\\index\{[^}]*\}", "", t)
    return re.sub(r"\s+", " ", t).strip()[:280]


# ── LSP plumbing (stdio, Content-Length framing) ──────────────────────
def read_message(stream):
    headers = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        line = line.decode("utf-8").strip()
        if not line:
            break
        k, _, v = line.partition(":")
        headers[k.strip().lower()] = v.strip()
    n = int(headers.get("content-length", 0))
    return json.loads(stream.read(n).decode("utf-8")) if n else None


def write_message(stream, payload):
    data = json.dumps(payload).encode("utf-8")
    stream.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii"))
    stream.write(data)
    stream.flush()


def uri_to_path(uri):
    return uri[7:] if uri.startswith("file://") else uri


def path_to_uri(path):
    return "file://" + os.path.abspath(path)


# ── features ──────────────────────────────────────────────────────────
def context_at(line, col):
    """What is being typed at the cursor: ('gls'|'cite'|'macro'|None, prefix)."""
    head = line[:col]
    m = re.search(r"\\(?:Gls|Glspl|gls|glspl)\{([^}]*)$", head)
    if m:
        return "gls", m.group(1)
    m = re.search(r"\\(?:citep|citealp|citet|cite)\s*(?:\[[^\]]*\])*\{([^}]*)$", head)
    if m:
        return "cite", m.group(1).split(",")[-1].strip()
    m = re.search(r"\\([a-zA-Z]*)$", head)
    if m:
        return "macro", m.group(1)
    return None, ""


def completions(idx, kind, prefix):
    items = []
    if kind == "gls":
        for k, v in idx.keys.items():
            if k.startswith(prefix):
                items.append({"label": k, "kind": 6, "detail": v["name"],
                              "documentation": v["blurb"]})
    elif kind == "cite":
        for k, v in idx.bib.items():
            if k.lower().startswith(prefix.lower()):
                items.append({"label": k, "kind": 6, "detail": v["label"][:90]})
    elif kind == "macro":
        for k, v in idx.macros.items():
            if k.startswith(prefix):
                items.append({"label": k, "kind": 3, "detail": v["body"][:90],
                              "insertText": k})
    return sorted(items, key=lambda i: i["label"])[:200]


def token_at(text, line_no, col):
    """The (kind, key, range) of the \\gls / \\cite / macro under the cursor."""
    lines = text.split("\n")
    if line_no >= len(lines):
        return None
    line = lines[line_no]
    for m in GLS_RE.finditer(line):
        if m.start(2) <= col <= m.end(2):
            return "gls", m.group(2), (m.start(2), m.end(2))
    for m in CITE_RE.finditer(line):
        if m.start(1) <= col <= m.end(1):
            keys = [k.strip() for k in m.group(1).split(",")]
            return "cite", keys[0] if len(keys) == 1 else _key_at(m, line, col), \
                (m.start(1), m.end(1))
    for m in MACRO_USE_RE.finditer(line):
        if m.start() <= col <= m.end():
            return "macro", m.group(1), (m.start() + 1, m.end())
    return None


def _key_at(m, line, col):
    off = m.start(1)
    for part in m.group(1).split(","):
        if off <= col <= off + len(part):
            return part.strip()
        off += len(part) + 1
    return m.group(1).split(",")[0].strip()


def hover_text(idx, kind, key):
    if kind == "gls" and key in idx.keys:
        v = idx.keys[key]
        return f"**{v['name']}**  \n`\\gls{{{key}}}` — {os.path.basename(v['file'])}:{v['line']+1}\n\n{v['blurb']}"
    if kind == "cite" and key in idx.bib:
        return f"**{key}**  \n{idx.bib[key]['label']}"
    if kind == "macro" and key in idx.macros:
        v = idx.macros[key]
        return f"`\\{key}`  \n```latex\n{v['body']}\n```"
    return None


def location_of(idx, kind, key):
    tbl = {"gls": idx.keys, "cite": idx.bib, "macro": idx.macros}.get(kind, {})
    if key not in tbl:
        return None
    v = tbl[key]
    return {"uri": path_to_uri(v["file"]),
            "range": {"start": {"line": v["line"], "character": 0},
                      "end": {"line": v["line"], "character": 0}}}


def _near(name, known, maxd=2):
    """The defined macro closest to `name`, if within `maxd` edits."""
    best, bestd = None, maxd + 1
    for cand in known:
        if abs(len(cand) - len(name)) > maxd or cand == name:
            continue
        d = _lev(name, cand, maxd)
        if d < bestd:
            best, bestd = cand, d
    return best


def _lev(a, b, cap):
    """Levenshtein distance, abandoned once it exceeds `cap`."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def live_diagnostics(idx, text):
    """The two classes that fail the main build while the per-term export
    only warns: an unknown \\gls key, and a macro that is one or two
    keystrokes away from a real one (\\hilbertpace for \\hilbertspace).

    A macro that is simply unknown is NOT flagged: TikZ bodies are full of
    \\x, \\coordinate and locally defined names, and flagging those buries
    the real finding under a thousand false ones."""
    out = []
    tikz = _tikz_spans(text)
    for i, line in enumerate(text.split("\n")):
        if line.lstrip().startswith("%"):
            continue
        for m in GLS_RE.finditer(line):
            if m.group(2) and m.group(2) not in idx.keys:
                near = _near(m.group(2), idx.keys)
                hint = f" (did you mean '{near}'?)" if near else ""
                out.append(_diag(i, m.start(2), m.end(2),
                                 f"unknown glossary key '{m.group(2)}'{hint} — "
                                 f"the main build fails on this", 1))
        if i in tikz:
            continue                      # TikZ has its own macro namespace
        for m in MACRO_USE_RE.finditer(line):
            name = m.group(1)
            if len(name) < 4 or idx.known_macro(name) or name in idx.local:
                continue
            # a command used repeatedly across the book is established
            # (\mbox, \tanh, \succ), whereas a typo appears once or twice
            if idx.usage.get(name, 0) >= 3:
                continue
            near = _near(name, idx.macros)
            if near:
                out.append(_diag(i, m.start(), m.end(),
                                 f"unknown macro \\{name} — did you mean "
                                 f"\\{near}?", 1))
    return out


def _tikz_spans(text):
    """Line numbers inside a tikzpicture, where macro checking is off."""
    inside, lines = False, set()
    for i, line in enumerate(text.split("\n")):
        if "\\begin{tikzpicture}" in line:
            inside = True
        if inside:
            lines.add(i)
        if "\\end{tikzpicture}" in line:
            inside = False
    return lines


def _diag(line, c0, c1, msg, severity):
    return {"range": {"start": {"line": line, "character": c0},
                      "end": {"line": line, "character": c1}},
            "severity": severity, "source": "dictml", "message": msg}


LINT_LINE = re.compile(r"^(chapter_[\w]+\.tex|[\w/]+\.tex):(\d+)(?::(\d+))?:?\s*(.*)$")


def save_diagnostics(path):
    """Run the fast deterministic linters and map their output to the file."""
    out = []
    for name in SAVE_LINTERS:
        script = os.path.join(HERE, f"{name}.py")
        if not os.path.isfile(script):
            continue
        try:
            p = subprocess.run([sys.executable, script], cwd=ROOT,
                               capture_output=True, timeout=90)
        except Exception:
            continue
        for raw in p.stdout.decode("utf-8", "replace").split("\n"):
            m = LINT_LINE.match(raw.strip())
            if not m:
                continue
            if os.path.abspath(os.path.join(ROOT, m.group(1))) != os.path.abspath(path):
                continue
            line = max(0, int(m.group(2)) - 1)
            col = max(0, int(m.group(3) or 1) - 1)
            out.append(_diag(line, col, col + 1, f"[{name}] {m.group(4)}", 2))
    return out


def rename_edits(idx, key, new_key):
    """Every \\gls-family use plus the \\newglossaryentry header."""
    changes = {}
    for f in entry_files() + [os.path.join(ROOT, "ListSymbols_English.tex")]:
        if not os.path.isfile(f):
            continue
        edits = []
        for i, line in enumerate(open(f, encoding="utf-8",
                                      errors="replace").read().split("\n")):
            for m in GLS_RE.finditer(line):
                if m.group(2) == key:
                    edits.append(_edit(i, m.start(2), m.end(2), new_key))
            for m in ENTRY_RE.finditer(line):
                if m.group(1) == key:
                    edits.append(_edit(i, m.start(1), m.end(1), new_key))
        if edits:
            changes[path_to_uri(f)] = edits
    return {"changes": changes}


def _edit(line, c0, c1, text):
    return {"range": {"start": {"line": line, "character": c0},
                      "end": {"line": line, "character": c1}},
            "newText": text}


# ── server loop ───────────────────────────────────────────────────────
class Server:
    def __init__(self):
        self.idx = Index()
        self.docs = {}

    def run(self):
        stdin, stdout = sys.stdin.buffer, sys.stdout.buffer
        while True:
            msg = read_message(stdin)
            if msg is None:
                return
            reply = self.handle(msg, stdout)
            if reply is not None and "id" in msg:
                write_message(stdout, {"jsonrpc": "2.0", "id": msg["id"],
                                       "result": reply})

    def publish(self, out, uri, diags):
        write_message(out, {"jsonrpc": "2.0",
                            "method": "textDocument/publishDiagnostics",
                            "params": {"uri": uri, "diagnostics": diags}})

    def handle(self, msg, out):
        method, params = msg.get("method"), msg.get("params") or {}
        if method == "initialize":
            root = params.get("rootUri") or ""
            if root.startswith("file://"):
                cand = uri_to_path(root)
                if any(glob.glob(os.path.join(cand, p)) for p in ENTRY_GLOBS):
                    set_root(cand)
                    self.idx.build()
            return {"capabilities": {
                "textDocumentSync": 1,
                "completionProvider": {"triggerCharacters": ["{", "\\", ","]},
                "hoverProvider": True,
                "definitionProvider": True,
                "renameProvider": True,
            }, "serverInfo": {"name": "dictml", "version": "1.0"}}
        if method == "shutdown":
            return None
        if method == "exit":
            sys.exit(0)

        td = params.get("textDocument") or {}
        uri = td.get("uri", "")
        if method == "textDocument/didOpen":
            self.docs[uri] = td.get("text", "")
            self.publish(out, uri, live_diagnostics(self.idx, self.docs[uri]))
            return None
        if method == "textDocument/didChange":
            self.docs[uri] = params["contentChanges"][-1]["text"]
            self.publish(out, uri, live_diagnostics(self.idx, self.docs[uri]))
            return None
        if method == "textDocument/didSave":
            self.idx.build()
            text = self.docs.get(uri, "")
            self.publish(out, uri, live_diagnostics(self.idx, text)
                         + save_diagnostics(uri_to_path(uri)))
            return None

        text = self.docs.get(uri, "")
        pos = params.get("position") or {}
        line_no, col = pos.get("line", 0), pos.get("character", 0)
        lines = text.split("\n")
        line = lines[line_no] if line_no < len(lines) else ""

        if method == "textDocument/completion":
            kind, prefix = context_at(line, col)
            return {"isIncomplete": False,
                    "items": completions(self.idx, kind, prefix) if kind else []}
        if method == "textDocument/hover":
            tok = token_at(text, line_no, col)
            if tok:
                md = hover_text(self.idx, tok[0], tok[1])
                if md:
                    return {"contents": {"kind": "markdown", "value": md}}
            return None
        if method == "textDocument/definition":
            tok = token_at(text, line_no, col)
            return location_of(self.idx, tok[0], tok[1]) if tok else None
        if method == "textDocument/rename":
            tok = token_at(text, line_no, col)
            if tok and tok[0] == "gls":
                return rename_edits(self.idx, tok[1], params["newName"])
            return None
        return None


# ── CLI helpers ───────────────────────────────────────────────────────
def selftest():
    idx = Index()
    print(f"index: {len(idx.keys)} glossary keys, {len(idx.bib)} bib keys, "
          f"{len(idx.macros)} macros")
    ok = True

    kind, prefix = context_at(r"		a \gls{convex", 14)
    items = completions(idx, kind, prefix)
    print(f"  completion after '\\gls{{conv': {len(items)} items, "
          f"first = {items[0]['label'] if items else '-'}")
    ok &= any(i["label"] == "convex" for i in items)

    kind, prefix = context_at(r"\citep[Sect.~2.3.1]{Boyd", 24)
    items = completions(idx, kind, prefix)
    print(f"  completion after '\\citep[..]{{Boyd': "
          f"{[i['label'] for i in items][:3]}")
    ok &= any(i["label"] == "BoydConvexBook" for i in items)

    txt = "a \\gls{convex} set and \\featurevec\n\\gls{opmethod} \\hilbertpace"
    tok = token_at(txt, 0, 9)
    print(f"  token under cursor: {tok}")
    ok &= tok and tok[0] == "gls" and tok[1] == "convex"
    print(f"  hover: {(hover_text(idx, 'gls', 'convex') or '')[:60]}…")
    ok &= location_of(idx, "gls", "convex") is not None
    ok &= location_of(idx, "macro", "featurevec") is not None

    # the two build-breaking classes of this session, each with its suggestion
    diags = live_diagnostics(idx, txt)
    print(f"  live diagnostics: {[d['message'][:52] for d in diags]}")
    ok &= len(diags) == 2
    ok &= any("optmethod" in d["message"] for d in diags)
    ok &= any("hilbertspace" in d["message"] for d in diags)

    # noise control: a macro that resembles nothing is NOT reported, or a
    # TikZ body would bury the real findings under a thousand false ones
    quiet = live_diagnostics(idx, "\\zzzqqqmacro and \\foreach \\x in {1,2}")
    print(f"  unrelated macros reported: {len(quiet)} (want 0)")
    ok &= len(quiet) == 0

    ed = rename_edits(idx, "convex", "convexset")
    n = sum(len(v) for v in ed["changes"].values())
    print(f"  rename 'convex' would touch {n} sites in "
          f"{len(ed['changes'])} file(s)")
    ok &= n > 10
    print("\nSELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--index" in sys.argv:
        idx = Index()
        print(f"{len(idx.keys)} glossary keys, {len(idx.bib)} bib keys, "
              f"{len(idx.macros)} macros")
        sys.exit(0)
    Server().run()


if __name__ == "__main__":
    main()
