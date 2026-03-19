# 📘 Aalto Dictionary of Machine Learning (ADictML)

A multilingual, open-access glossary for ML and AI — available as a **PDF** and as an **[MCP server](./mcp/)** for AI coding assistants.
Developed by the **Aalto Machine Learning Group** for students, researchers, and educators at **Aalto University**.

[![MCP Server](https://img.shields.io/badge/MCP-Server-blueviolet?logo=anthropic&style=for-the-badge)](./mcp/)

---

## 🤖 Use ADictML in Your AI Assistant (MCP)

ADictML is now available as a **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server** — letting AI coding assistants like Claude Code look up, search, and cross-reference dictionary terms directly in context.

**Claude Code**
```bash
pip install -r mcp/requirements.txt
claude mcp add --scope user aalto-dictionary \
  -- python ~/AaltoDictionaryofML.github.io/mcp/server.py
```

**VS Code (Copilot / GitHub Copilot Chat)**
Add to `~/.config/Code/User/mcp.json` (Linux/macOS: `~/Library/Application Support/Code/User/mcp.json`):
```json
{
  "servers": {
    "aalto-dictionary": {
      "type": "stdio",
      "command": "python",
      "args": ["~/AaltoDictionaryofML.github.io/mcp/server.py"]
    }
  }
}
```

Once connected, ask your assistant things like:
- *"Look up Byzantine robustness in the Aalto Dictionary"*
- *"List all Regulation terms"*
- *"What terms are related to federated learning?"*

→ See [mcp/README.md](./mcp/README.md) for full setup and tool reference.

---

<!-- ADICTML_STATS_BEGIN -->
## 📘 Dictionary at a Glance

- **Total terms:** 567
- **Machine Learning Concepts:** 285
- **Mathematical Tools:** 219
- **Machine Learning Systems:** 33
- **Machine Learning Regulation:** 15
- **Reinforcement Learning:** 15
- **Last updated:** 2026-03-19

<!-- ADICTML_STATS_END -->

## 📥 Download

- **[📘 English PDF (latest release)](./ADictML_Main.pdf)**
- **[🌐 Translations](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io/tree/main/translations/)**  
  *(Spanish, German, French, Greek, Finnish)*

--- 

## 🧑‍🤝‍🧑 Authors & Contributors

**Editor-in-Chief:**  
Alexander Jung — Associate Professor, Aalto University  
[ORCID: 0000-0001-7538-0990](https://orcid.org/0000-0001-7538-0990)

**Contributors:**
- Konstantina Olioumtsevits — Aalto University  
- Ekkehard Schnoor — Aalto University  
- Tommi Flores Ryynänen — Aalto University  
- Juliette Gronier — ENS Lyon  
- Salvatore Rastelli — Aalto University  
- Mikko Seesto — Aalto University  

Full contributor list: [AUTHORS.md](./AUTHORS.md)

---

## 💰 Funding and Acknowledgements

The *Aalto Dictionary of Machine Learning (ADictML)* has been partially supported by:

- **XAI-based software-defined energy networks via packetized management for fossil fuel-free next-generation of industrial cyber-physical systems (X-SDEN)**
  *Research Council of Finland*, Grant No. **349966**
- **Mathematical Theory of Trustworthy Federated Learning (MATHFUL)**  
  *Research Council of Finland*, Grant No. **363624**
- **A Mathematical Theory of Federated Learning (TRUST-FELT)**  
  *Jane and Aatos Erkko Foundation*, Grant No. **A835**
- **FLAIG – AI Governance in Banking and Insurance**  
  *Business Finland*  

These projects have enabled the open development of teaching materials, LaTeX figures,  
and the public ADictML repository.  

[![Funding: Research Council of Finland](https://img.shields.io/badge/Funding-RCoF_349966-blue)](#)
[![Funding: Research Council of Finland](https://img.shields.io/badge/Funding-RCoF_363624-blue)](#)
[![Funding: TRUST-FELT](https://img.shields.io/badge/Funding-JAEF_TRUST--FELT-lightgrey)](#)
[![Funding: Business Finland](https://img.shields.io/badge/Funding-BF_FLAIG-orange)](#)

---

## 📌 Citation

If you use or refer to ADictML, please cite as:

> A. Jung and K. Olioumtsevits and E. Schnoor and T. Flores Ryynänen and J. Gronier and S. Rastelli and M. Seesto (2026).  
> *Aalto Dictionary of Machine Learning (ADictML)*.  
> Aalto University. 

A formal companion edition will appear in the [*Springer Dictionary of Applied Machine Learning (MRW)*](https://books.google.fi/books/about/Dictionary_of_Applied_Machine_Learning.html?id=JLGT0QEACAAJ&redir_esc=y).

---

## 🧾 License

This work, **Aalto Dictionary of Machine Learning**, is licensed under the 
**Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license,
  and indicate if changes were made.

---

## 🧭 Repository Links

- GitHub: [AaltoDictionaryofML.github.io](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io)
- MCP Server: [mcp/](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io/tree/main/mcp/)

---