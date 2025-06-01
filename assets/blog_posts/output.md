---
bibliography: ../Literature.bib
---

# Generalization {#generalization .unnumbered}

Generalization refers to the ability of a model trained on a training
set to make accurate predictions on new, unseen data points. This is a
central goal of machine learning (ML) and artificial intelligence (AI):
to learn patterns that extend beyond the training set. Most machine
learning (ML) systems use empirical risk minimization (ERM) to learn a
hypothesis $\hat{h} \in \mathcal{H}$ by minimizing the average loss over
a training set of data points ${\bf z}^{(1)}, \ldots, {\bf z}^{(m)}$,
denoted as $\mathcal{D}^{(\rm train)}$. However, success on the training
set does not guarantee success on unseen data - this discrepancy is the
challenge of generalization. To study generalization mathematically, we
need to formalize the notion of "unseen" data. A widely used approach is
to assume a probabilistic model for data generation, such as the
independent and identically distributed assumption (i.i.d. assumption).
Here, we interpret data points as independent random variable (RV)s with
an identical probability distribution $p({\bf z})$. This probability
distribution, which is assumed fixed but unknown, allows us to define
risk of a trained model $\hat{h}$ as the expected loss
$$\risk{\hat{h}} := \expect_{{\bf z} \sim p({\bf z})} \big\{ L(\hat{h}, {\bf z}) \big\}.$$
The difference between risk $\risk{\hat{h}}$ and empirical risk
$\emprisk{\hat{h}}{\mathcal{D}^{(\rm train)}}$ is known as the
generalization gap. Tools from probability theory, such as concentration
inequalities and uniform convergence, allow us to bound this gap under
certain conditions (Shalev-Shwartz and Ben-David 2014).\
**Generalization without probability.**
[probability]{acronym-label="probability" acronym-form="singular+short"}
theory is one way to study how well a model generalizes beyond the
training set, but it is not the only way. Another option is to use
simple, deterministic changes to the data points in the training set.
The basic idea is that a good model $\hat{h}$ should be robust: its
prediction $\hat{h}({\bf x})$ should not change much if we slightly
change the features ${\bf x}$ of a data point ${\bf z}$. For example, an
object detector trained on smartphone photos should still detect the
object if a few random pixels are masked (Su, Vargas, and Sakurai 2019).
Similarly, it should deliver the same result if we rotate the object in
the image (Mallat 2016).

![Two data points ${\bf z}^{(1)},{\bf z}^{(2)}$ that are used as a
training set to learn a hypothesis $\hat{h}$ via empirical risk
minimization (ERM). We can evaluate $\hat{h}$ outside
$\mathcal{D}^{(\rm train)}$ either by an independent and identically
distributed assumption (i.i.d. assumption) with some underlying
probability distribution $p({\bf z})$ or by perturbing the data
points.](blog_posts/images/generalization_tikz.png){#fig:polynomial_fit_dict
width="80%"}

See also: machine learning (ML), artificial intelligence (AI), empirical
risk minimization (ERM), model, hypothesis, loss, empirical risk, data
point, training set, probabilistic model, independent and identically
distributed assumption (i.i.d. assumption), data, independent and
identically distributed (i.i.d.), realization, probability distribution,
risk, random variable (RV), prediction.

:::::: {#refs .references .csl-bib-body .hanging-indent entry-spacing="0"}
::: {#ref-MallatUnderstandingDeepLearning .csl-entry}
Mallat, Stéphane. 2016. "Understanding Deep Convolutional Networks."
*Philosophical Transactions of the Royal Society A: Mathematical,
Physical and Engineering Sciences* 374 (2065): 20150203.
<https://doi.org/10.1098/rsta.2015.0203>.
:::

::: {#ref-ShalevMLBook .csl-entry}
Shalev-Shwartz, S., and S. Ben-David. 2014. *Understanding Machine
Learning: From Theory to Algorithms*. New York, NY, USA: Cambridge Univ.
Press.
:::

::: {#ref-OnePixelAttack .csl-entry}
Su, J., D. V. Vargas, and K. Sakurai. 2019. "One Pixel Attack for
Fooling Deep Neural Networks." *IEEE Trans. Evol. Comput.* 23 (5):
828--41. <https://doi.org/10.1109/TEVC.2019.2890858>.
:::
::::::
