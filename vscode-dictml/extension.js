// ML Dictionary — VS Code client for scripts/dictml_lsp.py
//
// The server is stdlib-only Python speaking LSP over stdio, so this client
// does nothing but locate it, start it, and surface its stderr. It runs
// alongside LaTeX Workshop or texlab: VS Code queries every provider
// registered for the file and merges the results, so a hover shows both the
// LaTeX intelligence and the glossary entry.

const fs = require("fs");
const path = require("path");
const vscode = require("vscode");
const { LanguageClient, TransportKind } = require("vscode-languageclient/node");

let client = null;
let output = null;

/** Absolute path of dictml_lsp.py: the setting, else a search of the workspace. */
function findServer() {
  const configured = vscode.workspace.getConfiguration("dictml").get("serverPath");
  if (configured) return configured;
  for (const folder of vscode.workspace.workspaceFolders || []) {
    for (const rel of ["dictml_lsp.py", "scripts/dictml_lsp.py"]) {
      const p = path.join(folder.uri.fsPath, rel);
      if (fs.existsSync(p)) return p;
    }
  }
  return null;
}

async function start() {
  const server = findServer();
  if (!server) {
    output.appendLine(
      "no server found: set dictml.serverPath, or open the folder that " +
        "contains scripts/dictml_lsp.py"
    );
    return;
  }
  const python = vscode.workspace.getConfiguration("dictml").get("pythonPath") || "python3";
  output.appendLine(`starting: ${python} ${server}`);

  const serverOptions = {
    run: { command: python, args: [server], transport: TransportKind.stdio },
    debug: { command: python, args: [server], transport: TransportKind.stdio },
  };
  const clientOptions = {
    documentSelector: [
      { scheme: "file", language: "latex" },
      { scheme: "file", language: "tex" },
    ],
    outputChannel: output,
    // the server rebuilds its index on save; watching the sources means a new
    // \newglossaryentry is completable without a restart
    synchronize: {
      fileEvents: vscode.workspace.createFileSystemWatcher(
        "**/{chapter_*.tex,assets/ml_macros.tex,assets/Literature.bib}"
      ),
    },
  };
  client = new LanguageClient("dictml", "ML Dictionary", serverOptions, clientOptions);
  await client.start();
  output.appendLine("server ready");
}

async function stop() {
  if (client) {
    await client.stop();
    client = null;
  }
}

function activate(context) {
  output = vscode.window.createOutputChannel("ML Dictionary");
  context.subscriptions.push(output);
  context.subscriptions.push(
    vscode.commands.registerCommand("dictml.restart", async () => {
      output.appendLine("restarting…");
      await stop();
      await start();
    })
  );
  start().catch((err) => output.appendLine(`failed to start: ${err}`));
}

function deactivate() {
  return stop();
}

module.exports = { activate, deactivate };
