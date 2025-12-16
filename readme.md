# 📘 Aalto Dictionary of Machine Learning (ADictML)

A multilingual, open-access glossary for mastering machine learning and AI terms.  
Developed by the **Aalto Machine Learning Group** for students, researchers, and educators at **Aalto University**.

[![RSS Feed](https://img.shields.io/badge/RSS-Feed-blue?logo=rss&style=for-the-badge)](https://aaltodictionaryofml.github.io/feed.xml)

---

<!-- ADICTML_STATS_BEGIN -->
## 📘 Dictionary at a Glance

- **Total terms:** 451
- **Machine Learning Concepts:** 298
- **Mathematical Tools:** 140
- **Machine Learning Regulation:** 7
- **Reinforcement Learning:** 6
- **Last updated:** 2025-12-16

<!-- ADICTML_STATS_END -->

## 📥 Download

- **[📘 English PDF (latest release)](./ADictML_English.pdf)**
- **[🌐 Translations](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io/tree/main/translations/)**  
  *(Spanish, German, French, Greek, Finnish)*

--- 

## 📈 Interactive Term Network

Explore relationships between terms:  
👉 [**View Glossary Network (HTML)**](./assets/glossary_network.html)

- Terms are color-coded by semantic clusters  
- Hover for definitions, zoom and pan to explore  

--- 

## 🧩 How to Contribute

We warmly welcome contributions from students, researchers, and educators worldwide!  
Follow these steps to propose new entries, translations, or figure improvements.

### **Step 1 — Fork the Repository**
1. Visit the [AaltoDictionaryofML GitHub repository](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io).  
2. Click **“Fork”** (top-right corner) to create your own copy under your GitHub account.

### **Step 2 — Clone Your Fork**
```bash
git clone https://github.com/<your-username>/AaltoDictionaryofML.github.io.git
cd AaltoDictionaryofML.github.io
```

### **Step 3 — Create a New Branch**
```bash
git checkout -b add-new-term-loss-function
```

---

### **Step 4 — Understand the Project Structure**

All content is written in LaTeX and structured as follows:

| File | Purpose |
|------|----------|
| **`ADictML_English.tex`** | *Front matter and main LaTeX driver.* Loads macros, bibliography, and includes the main glossary file. Defines title page, TOC, and layout settings. |
| **`ADictML_Glossary_English.tex`** | *Main content file.* Contains all English glossary entries, each created via `\newglossaryentry{...}`. Contributors usually edit this file when adding or revising terms. |
| **`/assets/ml_macros.tex`** | *Macro definitions.* Provides standardized LaTeX commands for common ML notation (e.g. `\lossfunc`, `\dataset`, `\feature`, `\weights`, etc.). New entries should reuse these macros for consistency. |
| **`/assets/Literature.bib`** | *Bibliographic database.* Contains BibTeX entries for textbooks, journal articles, and reports cited across entries. Use `\cite{}` commands to reference them. |

Example of a glossary entry:
```latex
\newglossaryentry{optmethod}
{name={optimization method},
	description={An\index{optimization method} optimization method is an \gls{algorithm} that 
		reads in a representation of an \gls{optproblem} and delivers an (approximate) solution 
		as its output \cite{BoydConvexBook}, \cite{BertsekasNonLinProgr}, \cite{nesterov04}.
		 \\
		 See also: \gls{algorithm}, \gls{optproblem}.},
	first={optimization method},
	firstplural={optimization methods}, 
	plural={optimization methods}, 
	text={optimization method}
}
```

By default, all figures are created using **TikZ** code (see the [TikZ & PGF Manual](https://ctan.org/pkg/pgf?lang=en) for guidance).

---

### **Step 5 — Commit and Push**
```bash
git add .
git commit -m "Add glossary entry: Loss Function"
git push origin add-new-term-loss-function
```

---

### **Step 6 — Open a Pull Request**
1. Go to your fork on GitHub.  
2. Click **“Compare & pull request.”**  
3. Describe your contribution briefly and submit.  
4. The editorial team will review, comment, and merge upon approval.

---

### 💡 Contribution Tips

- Keep definitions concise (3–6 sentences).  
- Follow notation from `/assets/ml_macros.tex`.  
- Add cross-links via the `see=` field in `\newglossaryentry`.  
- When citing references, use keys from `/assets/Literature.bib`.  
- Discuss major new ideas via [GitHub Issues](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io/issues).

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

Full contributor list: [AUTHORS.md](./AUTHORS.md)

---

## 💰 Funding and Acknowledgements

The *Aalto Dictionary of Machine Learning (ADictML)* has been partially supported by:

- **XAI-based software-defined energy networks via packetized management for fossil fuel-free next-generation of industrial cyber-physical systems (X-SDEN)**
  *Research Council of Finland*, Grant No. **349966**
- **Mathematical Theory of Trustworthy Federated Learning (MATHFUL)**  
  *Research Council of Finland*, Grant No. **363624**
- **TRUST-FELT – Trustworthy Federated Learning Technologies**  
  *Jane and Aatos Erkko Foundation*, Finland  
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

> Jung, A., Olioumtsevits, K., Schnoor, E., Flores Ryynänen, T., Gronier, J., & Rastelli, S. (2025).  
> *Aalto Dictionary of Machine Learning (ADictML)*.  
> Aalto University. DOI: [10.5281/zenodo.17273736](https://doi.org/10.5281/zenodo.17273736)

A formal companion edition will appear in the [*Springer Dictionary of Applied Machine Learning (MRW)*](https://books.google.fi/books/about/Dictionary_of_Applied_Machine_Learning.html?id=JLGT0QEACAAJ&redir_esc=y).

---

## 🧾 License

This work is licensed under a **Creative Commons Attribution–ShareAlike 4.0 International License**.  
See [LICENSE](./LICENSE) for details.

---

## 🧭 Repository Links

- GitHub: [AaltoDictionaryofML.github.io](https://github.com/AaltoDictionaryofML/AaltoDictionaryofML.github.io)  
- Zenodo DOI: [10.5281/zenodo.17273736](https://doi.org/10.5281/zenodo.17273736)  
- Springer MRW: *Dictionary of Applied Machine Learning* (forthcoming)

---