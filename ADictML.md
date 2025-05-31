name=minimum, description=Given a set of real numbers, the minimum is
the smallest of those numbers., first=minimum,text=minimum

name=epigraph, description=

The epigraph of a real-valued function
$f : \mathbb{R}^n \to \mathbb{R} \cup \{+\infty\}$ is the set of points
lying on or above its graph:
$$\operatorname{epi}(f) = \left\{ (\mathbf{x}, t) \in \mathbb{R}^n \times \mathbb{R} \,\middle|\, f(\mathbf{x}) \leq t \right\}.$$
A function is [convex]{acronym-label="convex"
acronym-form="singular+short"} if and only if its epigraph is a
[convex]{acronym-label="convex" acronym-form="singular+short"} set
[@BoydConvexBook], [@BertCvxAnalOpt].

<figure>

<figcaption>Epigraph of the function <span
class="math inline"><em>f</em>(<em>x</em>) = <em>x</em><sup>2</sup></span>
(i.e., shaded area).</figcaption>
</figure>

See also: [convex]{acronym-label="convex"
acronym-form="singular+short"}.

, first=epigraph, text=epigraph, plural=epigraphs

name=maximum, description=The maximum of a set
$\mathcal{A} \subseteq \mathbb{R}$ of real numbers is the greatest
element in that set, if such an element exists. A set $\mathcal{A}$ has
a maximum if it is bounded above and attains its
[supremum]{acronym-label="supremum" acronym-form="singular+short"}
[@RudinBookPrinciplesMatheAnalysis Sec. 1.4].\
See also: [supremum]{acronym-label="supremum"
acronym-form="singular+short"}., first=maximum,text=maximum

name=supremum (or least upper bound), description=The supremum of a set
of real numbers is the smallest number that is greater than or equal to
every element in the set. More formally, a real number $a$ is the
supremum of a set $\mathcal{A} \subseteq \mathbb{R}$ if: 1) $a$ is an
upper bound of $\mathcal{A}$; and 2) no number smaller than $a$ is an
upper bound of $\mathcal{A}$. Every non-empty set of real numbers that
is bounded above has a supremum, even if it does not contain its
supremum as an element [@RudinBookPrinciplesMatheAnalysis Sec. 1.4].,
first=supremum (or least upper bound),text=supremum

name=discrepancy, description= Consider an [fl]{acronym-label="fl"
acronym-form="singular+short"} application with
[netdata]{acronym-label="netdata" acronym-form="singular+short"}
represented by an [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}. [fl]{acronym-label="fl"
acronym-form="singular+short"} methods use a discrepancy measure to
compare [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} maps from
[localmodels]{acronym-label="localmodel" acronym-form="plural+short"} at
nodes $i,i'$ connected by an edge in the
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"}.\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[netdata]{acronym-label="netdata" acronym-form="singular+short"},
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[localmodel]{acronym-label="localmodel" acronym-form="singular+short"}.,
first=discrepancy,text=discrepancy

name=FedRelax, description=An [fl]{acronym-label="fl"
acronym-form="singular+short"}
[distributedalgorithm]{acronym-label="distributedalgorithm"
acronym-form="singular+short"}.\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[distributedalgorithm]{acronym-label="distributedalgorithm"
acronym-form="singular+short"}., first=FedRelax,text=FedRelax

name=FedAvg, description=

FedAvg refers to a family of iterative [fl]{acronym-label="fl"
acronym-form="singular+short"} [algorithms]{acronym-label="algorithm"
acronym-form="plural+short"}. It uses a server-client setting and
alternates between client-wise [localmodels]{acronym-label="localmodel"
acronym-form="plural+short"} re-training, followed by the aggregation of
updated [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} at the server [@pmlr-v54-mcmahan17a]. The
local update at client $i=1,\ldots,n$ at time $k$ starts from the
current [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} $\vw^{(k)}$ provided by the server and
typically amounts to executing few iterations of
[stochGD]{acronym-label="stochGD" acronym-form="singular+short"}. After
completing the local updates, they are aggregated by the server (e.g.,
by averaging them).
Fig. [1](#fig_single_iteration_fedavg){reference-type="ref"
reference="fig_single_iteration_fedavg"} illustrates the execution of a
single iteration of FedAvg.

<figure id="fig_single_iteration_fedavg">
<div class="center">

</div>
<figcaption>Illustration of a single iteration of FedAvg which
consisting of broadcasting <span data-acronym-label="modelparams"
data-acronym-form="singular+short">modelparams</span> by the server,
local updates at clients and their aggregation by the server. <span
id="fig_single_iteration_fedavg"
data-label="fig_single_iteration_fedavg"></span></figcaption>
</figure>

\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"},
[localmodel]{acronym-label="localmodel" acronym-form="singular+short"}.

, first=FedAvg,text=FedAvg

name=FedGD, description=An [fl]{acronym-label="fl"
acronym-form="singular+short"}
[distributedalgorithm]{acronym-label="distributedalgorithm"
acronym-form="singular+short"} that can be implemented as message
passing across an [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}.\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[distributedalgorithm]{acronym-label="distributedalgorithm"
acronym-form="singular+short"}, [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}, [gdmethods]{acronym-label="gdmethods"
acronym-form="singular+short"}., first=FedGD,text=FedGD

name=FedSGD, description=An [fl]{acronym-label="fl"
acronym-form="singular+short"}
[distributedalgorithm]{acronym-label="distributedalgorithm"
acronym-form="singular+short"} that can be implemented as message
passing across an [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}.\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[distributedalgorithm]{acronym-label="distributedalgorithm"
acronym-form="singular+short"}, [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}, [gdmethods]{acronym-label="gdmethods"
acronym-form="singular+short"}, [stochGD]{acronym-label="stochGD"
acronym-form="singular+short"}., first=FedSGD,text=FedSGD

name=horizontal federated learning (HFL),description= HFL uses
[localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} constituted by different
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} but
uses the same [features]{acronym-label="feature"
acronym-form="plural+short"} to characterize them [@HFLChapter2020]. For
example, weather forecasting uses a network of spatially distributed
weather (observation) stations. Each weather station measures the same
quantities, such as daily temperature, air pressure, and precipitation.
However, different weather stations measure the characteristics or
[features]{acronym-label="feature" acronym-form="plural+short"} of
different spatiotemporal regions. Each spatiotemporal region represents
an individual [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, each characterized by the same
[features]{acronym-label="feature" acronym-form="plural+short"} (e.g.,
daily temperature or air pressure).\
See also: [localdataset]{acronym-label="localdataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [fl]{acronym-label="fl"
acronym-form="singular+short"}, [vfl]{acronym-label="vfl"
acronym-form="singular+short"}, [cfl]{acronym-label="cfl"
acronym-form="singular+short"}., first=HFL,text=HFL

name=dimensionality reduction, description=

Dimensionality reduction refers to methods that learn a transformation
$\hypothesis: \mathbb{R}^{\featuredim} \rightarrow \mathbb{R}^{\featuredim'}$
of a (typically large) set of raw [features]{acronym-label="feature"
acronym-form="plural+short"}
$\feature_{1},\ldots,\feature_{\featuredim}$ into a smaller set of
informative [features]{acronym-label="feature"
acronym-form="plural+short"} $z_{1},\ldots,z_{\featuredim'}$. Using a
smaller set of [features]{acronym-label="feature"
acronym-form="plural+short"} is beneficial in several ways:

- Statistical benefit: It typically reduces the risk of
  [overfitting]{acronym-label="overfitting"
  acronym-form="singular+short"}, as reducing the number of
  [features]{acronym-label="feature" acronym-form="plural+short"} often
  reduces the [effdim]{acronym-label="effdim"
  acronym-form="singular+short"} of a [model]{acronym-label="model"
  acronym-form="singular+short"}.

- Computational benefit: Using fewer [features]{acronym-label="feature"
  acronym-form="plural+short"} means less computation for the training
  of [ml]{acronym-label="ml" acronym-form="singular+short"}
  [models]{acronym-label="model" acronym-form="plural+short"}. As a case
  in point, [linreg]{acronym-label="linreg"
  acronym-form="singular+short"} methods need to invert a matrix whose
  size is determined by the number of [features]{acronym-label="feature"
  acronym-form="plural+short"}.

- **Visualization.** Dimensionality reduction is also instrumental for
  [data]{acronym-label="data" acronym-form="singular+short"}
  visualization. For example, we can learn a transformation that
  delivers two [features]{acronym-label="feature"
  acronym-form="plural+short"} $z_{1},z_{2}$ which we can use, in turn,
  as the coordinates of a [scatterplot]{acronym-label="scatterplot"
  acronym-form="singular+short"}.
  Fig. [2](#fig:dimred-scatter){reference-type="ref"
  reference="fig:dimred-scatter"} depicts the
  [scatterplot]{acronym-label="scatterplot"
  acronym-form="singular+short"} of hand-written digits that are placed
  according transformed [features]{acronym-label="feature"
  acronym-form="plural+short"}. Here, the
  [datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
  are naturally represented by a large number of greyscale values (one
  of for each pixel).

<figure id="fig:dimred-scatter">

<figcaption>Example of dimensionality reduction: High-dimensional image
data (e.g., high-resolution images of hand-written digits) embedded into
2D using learned <span data-acronym-label="feature"
data-acronym-form="plural+short">features</span> <span
class="math inline">(<em>z</em><sub>1</sub>, <em>z</em><sub>2</sub>)</span>
and visualized in a <span data-acronym-label="scatterplot"
data-acronym-form="singular+short">scatterplot</span>.</figcaption>
</figure>

See also: [feature]{acronym-label="feature"
acronym-form="singular+short"},
[overfitting]{acronym-label="overfitting"
acronym-form="singular+short"}, [effdim]{acronym-label="effdim"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [linreg]{acronym-label="linreg"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"},
[scatterplot]{acronym-label="scatterplot"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}.

, first=dimensionality reduction,text=dimensionality reduction

name=machine learning (ML), description=ML aims to predict a
[label]{acronym-label="label" acronym-form="singular+short"} from the
[features]{acronym-label="feature" acronym-form="plural+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}. ML
methods achieve this by learning a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
from a [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"} (or [model]{acronym-label="model"
acronym-form="singular+short"}) through the minimization of a
[lossfunc]{acronym-label="lossfunc" acronym-form="singular+short"}
[@MLBasics], [@HastieWainwrightBook]. One precise formulation of this
principle is [erm]{acronym-label="erm" acronym-form="singular+short"}.
Different ML methods are obtained from different design choices for
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
(i.e., their [features]{acronym-label="feature"
acronym-form="plural+short"} and [label]{acronym-label="label"
acronym-form="singular+short"}), the [model]{acronym-label="model"
acronym-form="singular+short"}, and the
[lossfunc]{acronym-label="lossfunc" acronym-form="singular+short"}
[@MLBasics Ch. 3].\
See also: [label]{acronym-label="label" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[lossfunc]{acronym-label="lossfunc" acronym-form="singular+short"},
[erm]{acronym-label="erm" acronym-form="singular+short"}., first=machine
learning (ML),text=ML

name=feature learning, description=Consider an [ml]{acronym-label="ml"
acronym-form="singular+short"} application with
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
characterized by raw [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec \in \mathcal{X}$.
[feature]{acronym-label="feature" acronym-form="singular+short"}
learning refers to the task of learning a map
$${\bf \Phi}: \mathcal{X} \rightarrow \mathcal{X}': \featurevec \mapsto \featurevec',$$
that reads in raw [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec \in \mathcal{X}$ of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} and
delivers new [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec' \in \mathcal{X}'$ from a new
[featurespace]{acronym-label="featurespace"
acronym-form="singular+short"} $\mathcal{X}'$. Different
[feature]{acronym-label="feature" acronym-form="singular+short"}
learning methods are obtained for different design choices of
$\mathcal{X},\mathcal{X}'$, for a [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"} $\mathcal{H}$ of potential maps
${\bf \Phi}$, and for a quantitative measure of the usefulness of a
specific ${\bf \Phi} \in \mathcal{H}$. For example,
[pca]{acronym-label="pca" acronym-form="singular+short"} uses
$\mathcal{X} \defeq \mathbb{R}^{d}$,
$\mathcal{X}' \defeq \mathbb{R}^{d'}$ with $d' < d$, and a
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"}
$$\mathcal{H}\defeq \big\{ {\bf \Phi}: \mathbb{R}^{d}
        \!\rightarrow\! \mathbb{R}^{d'}\!:\!\featurevec'\!\defeq\!\mathbf{F} \featurevec \mbox{ with some } \mathbf{F} \!\in\! \mathbb{R}^{d' \times d} \big\}.$$
[pca]{acronym-label="pca" acronym-form="singular+short"} measures the
usefulness of a specific map
${\bf \Phi}(\featurevec)= \mathbf{F} \featurevec$ by the
[minimum]{acronym-label="minimum" acronym-form="singular+short"} linear
reconstruction error incurred on a [dataset]{acronym-label="dataset"
acronym-form="singular+short"} such that
$$\min_{\mathbf{G} \in \mathbb{R}^{d \times d'}} \sum_{r=1}^{m} \normgeneric{\mathbf{G} \mathbf{F} \featurevec^{(r)} - \featurevec^{(r)}}{2}^{2}.$$\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[featurespace]{acronym-label="featurespace"
acronym-form="singular+short"}, [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"}, [pca]{acronym-label="pca"
acronym-form="singular+short"}, [minimum]{acronym-label="minimum"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}., first=feature learning,text=feature
learning

name=autoencoder, description=An autoencoder is an
[ml]{acronym-label="ml" acronym-form="singular+short"} method that
simultaneously learns an encoder map
$\hypothesis(\cdot) \in \mathcal{H}$ and a decoder map
$\hypothesis^{*}(\cdot) \in \mathcal{H}^{*}$. It is an instance of
[erm]{acronym-label="erm" acronym-form="singular+short"} using a
[loss]{acronym-label="loss" acronym-form="singular+short"} computed from
the reconstruction error
$\featurevec - \hypothesis^{*}\big(  \hypothesis \big( \featurevec \big) \big)$.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[erm]{acronym-label="erm" acronym-form="singular+short"},
[loss]{acronym-label="loss" acronym-form="singular+short"}.,
first=autoencoder,text=autoencoder

name=vertical federated learning (VFL), description=

VFL refers to [fl]{acronym-label="fl" acronym-form="singular+short"}
applications where [devices]{acronym-label="device"
acronym-form="plural+short"} have access to different
[features]{acronym-label="feature" acronym-form="plural+short"} of the
same set of [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} [@VFLChapter]. Formally, the underlying
global [dataset]{acronym-label="dataset" acronym-form="singular+short"}
is
$$\dataset^{(\mathrm{global})} \defeq \left\{ \left(\featurevec^{(1)}, \truelabel^{(1)}\right), \ldots, \left(\featurevec^{(m)}, \truelabel^{(m)}\right) \right\}.$$
We denote by
$\featurevec^{(r)} = \big( \feature^{(r)}_{1}, \ldots, \feature^{(r)}_{\featuredim'} \big)^{T}$,
for $r=1,\ldots,m$, the complete
[featurevecs]{acronym-label="featurevec" acronym-form="plural+short"}
for the [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}. Each [device]{acronym-label="device"
acronym-form="singular+short"} $i \in \mathcal{V}$ observes only a
subset $\mathcal{F}^{(i)} \subseteq \{1,\ldots,\featuredim'\}$ of
[features]{acronym-label="feature" acronym-form="plural+short"},
resulting in a [localdataset]{acronym-label="localdataset"
acronym-form="singular+short"} $\mathcal{D}^{(i)}$ with
[featurevecs]{acronym-label="featurevec" acronym-form="plural+short"}
$$\featurevec^{(i,r)} = \big( \feature^{(r)}_{\featureidx_{1}}, \ldots, \feature^{(r)}_{\featureidx_{\featuredim}} \big)^{T}.$$
Some of the [devices]{acronym-label="device"
acronym-form="plural+short"} might also have access to the
[labels]{acronym-label="label" acronym-form="plural+short"}
$\truelabel^{(r)}$, for $r=1,\ldots,m$, of the global
[dataset]{acronym-label="dataset" acronym-form="singular+short"}. One
potential application of VFL is to enable collaboration between
different healthcare providers. Each provider collects distinct types of
measurements---such as blood values, electrocardiography, and lung
X-rays---for the same patients. Another application is a national social
insurance system, where health records, financial indicators, consumer
behavior, and mobility [data]{acronym-label="data"
acronym-form="singular+short"} are collected by different institutions.
VFL enables joint learning across these parties while allowing
well-defined levels of [privprot]{acronym-label="privprot"
acronym-form="singular+short"}.

<figure id="fig_vertical_FL">
<div class="center">

</div>
<figcaption>VFL uses <span data-acronym-label="localdataset"
data-acronym-form="plural+short">localdatasets</span> that are derived
from the <span data-acronym-label="datapoint"
data-acronym-form="plural+short">datapoints</span> of a common global
<span data-acronym-label="dataset"
data-acronym-form="singular+short">dataset</span>. The <span
data-acronym-label="localdataset"
data-acronym-form="plural+short">localdatasets</span> differ in the
choice of <span data-acronym-label="feature"
data-acronym-form="plural+short">features</span> used to characterize
the <span data-acronym-label="datapoint"
data-acronym-form="plural+short">datapoints</span>.<span
id="fig_vertical_FL" data-label="fig_vertical_FL"></span></figcaption>
</figure>

See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[device]{acronym-label="device" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[featurevec]{acronym-label="featurevec" acronym-form="singular+short"},
[localdataset]{acronym-label="localdataset"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"}, [privprot]{acronym-label="privprot"
acronym-form="singular+short"}.

, first=vertical federated learning (VFL),text=VFL

name=interpretability,description= An [ml]{acronym-label="ml"
acronym-form="singular+short"} method is interpretable for a specific
user if they can well anticipate the
[predictions]{acronym-label="prediction" acronym-form="plural+short"}
delivered by the method. The notion of interpretability can be made
precise using quantitative measures of the
[uncertainty]{acronym-label="uncertainty" acronym-form="singular+short"}
about the [predictions]{acronym-label="prediction"
acronym-form="plural+short"} [@JunXML2020].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"}.,
first=interpretability,text=interpretability

name=multitask learning,description= Multitask learning aims at
leveraging relations between different
[learningtasks]{acronym-label="learningtask"
acronym-form="plural+short"}. Consider two
[learningtasks]{acronym-label="learningtask"
acronym-form="plural+short"} obtained from the same
[dataset]{acronym-label="dataset" acronym-form="singular+short"} of
webcam snapshots. The first task is to predict the presence of a human,
while the second task is to predict the presence of a car. It might be
useful to use the same [deepnet]{acronym-label="deepnet"
acronym-form="singular+short"} structure for both tasks and only allow
the [weights]{acronym-label="weights" acronym-form="singular+short"} of
the final output layer to be different.\
See also: [learningtask]{acronym-label="learningtask"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [deepnet]{acronym-label="deepnet"
acronym-form="singular+short"}, [weights]{acronym-label="weights"
acronym-form="singular+short"}., first=multitask learning,text=multitask
learning

name=learning task, plural=learning tasks, description= Consider a
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset$ constituted by several [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}, each of them characterized by
[features]{acronym-label="feature" acronym-form="plural+short"}
$\featurevec$. For example, the [dataset]{acronym-label="dataset"
acronym-form="singular+short"} $\dataset$ might be constituted by the
images of a particular database. Sometimes it might be useful to
represent a [dataset]{acronym-label="dataset"
acronym-form="singular+short"} $\dataset$, along with the choice of
[features]{acronym-label="feature" acronym-form="plural+short"}, by a
[probdist]{acronym-label="probdist" acronym-form="singular+short"}
$p(\featurevec)$. A learning task associated with $\dataset$ consists of
a specific choice for the [label]{acronym-label="label"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} and
the corresponding [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}. Given a choice for the
[lossfunc]{acronym-label="lossfunc" acronym-form="singular+short"} and
[model]{acronym-label="model" acronym-form="singular+short"}, a learning
task gives rise to an instance of [erm]{acronym-label="erm"
acronym-form="singular+short"}. Thus, we could define a learning task
also via an instance of [erm]{acronym-label="erm"
acronym-form="singular+short"}, i.e., via an
[objfunc]{acronym-label="objfunc" acronym-form="singular+short"}. Note
that, for the same [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, we obtain different learning tasks by
using different choices for the [features]{acronym-label="feature"
acronym-form="plural+short"} and [label]{acronym-label="label"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.
These learning tasks are related, as they are based on the same
[dataset]{acronym-label="dataset" acronym-form="singular+short"}, and
solving them jointly (via
[multitask learning]{acronym-label="multitask learning"
acronym-form="singular+short"} methods) is typically preferable over
solving them separately [@Caruana:1997wk], [@JungGaphLassoSPL],
[@CSGraphSelJournal].\
See also: [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}, [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [objfunc]{acronym-label="objfunc"
acronym-form="singular+short"},
[multitask learning]{acronym-label="multitask learning"
acronym-form="singular+short"}., first=learning task,text=learning task

name=explainability,description= We define the (subjective)
explainability of an [ml]{acronym-label="ml"
acronym-form="singular+short"} method as the level of simulatability
[@Colin:2022aa] of the [predictions]{acronym-label="prediction"
acronym-form="plural+short"} delivered by an [ml]{acronym-label="ml"
acronym-form="singular+short"} system to a human user. Quantitative
measures for the (subjective) explainability of a trained
[model]{acronym-label="model" acronym-form="singular+short"} can be
constructed by comparing its [predictions]{acronym-label="prediction"
acronym-form="plural+short"} with the
[predictions]{acronym-label="prediction" acronym-form="plural+short"}
provided by a user on a [testset]{acronym-label="testset"
acronym-form="singular+short"} [@Colin:2022aa], [@Zhang:2024aa].
Alternatively, we can use [probmodels]{acronym-label="probmodel"
acronym-form="plural+short"} for [data]{acronym-label="data"
acronym-form="singular+short"} and measure the explainability of a
trained [ml]{acronym-label="ml" acronym-form="singular+short"}
[model]{acronym-label="model" acronym-form="singular+short"} via the
conditional (or differential) entropy of its
[predictions]{acronym-label="prediction" acronym-form="plural+short"},
given the user [predictions]{acronym-label="prediction"
acronym-form="plural+short"} [@JunXML2020], [@Chen2018].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[testset]{acronym-label="testset" acronym-form="singular+short"},
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"},
[data]{acronym-label="data" acronym-form="singular+short"}. ,
first=explainability,text=explainability

name=local interpretable model-agnostic explanations (LIME),description=

Consider a trained [model]{acronym-label="model"
acronym-form="singular+short"} (or learned
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"})
$\widehat{\hypothesis} \in \mathcal{H}$, which maps the
[featurevec]{acronym-label="featurevec" acronym-form="singular+short"}
of a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} to the
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
$\widehat{\truelabel}= \widehat{\hypothesis}$. LIME is a technique for
explaining the behavior of $\widehat{\hypothesis}$, locally around a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
with [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"} $\featurevec^{(0)}$ [@Ribeiro2016]. The
[explanation]{acronym-label="explanation" acronym-form="singular+short"}
is given in the form of a local approximation $g \in \mathcal{H}'$ of
$\widehat{\hypothesis}$ (see Fig. [4](#fig_lime){reference-type="ref"
reference="fig_lime"}). This approximation can be obtained by an
instance of [erm]{acronym-label="erm" acronym-form="singular+short"}
with a carefully designed [trainset]{acronym-label="trainset"
acronym-form="singular+short"}. In particular, the
[trainset]{acronym-label="trainset" acronym-form="singular+short"}
consists of [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} with
[featurevec]{acronym-label="featurevec" acronym-form="singular+short"}
$\featurevec$ close to $\featurevec^{(0)}$ and the
(pseudo-)[label]{acronym-label="label" acronym-form="singular+short"}
$\widehat{\hypothesis}(\featurevec)$. Note that we can use a different
[model]{acronym-label="model" acronym-form="singular+short"}
$\mathcal{H}'$ for the approximation from the original
[model]{acronym-label="model" acronym-form="singular+short"}
$\mathcal{H}$. For example, we can use a
[decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"} to approximate (locally) a
[deepnet]{acronym-label="deepnet" acronym-form="singular+short"}.
Another widely-used choice for $\mathcal{H}'$ is the
[linmodel]{acronym-label="linmodel" acronym-form="singular+short"}.

<figure id="fig_lime">
<div class="center">

</div>
<figcaption>To explain a trained <span data-acronym-label="model"
data-acronym-form="singular+short">model</span> <span
class="math inline">$\widehat{\hypothesis} \in \mathcal{H}$</span>,
around a given <span data-acronym-label="featurevec"
data-acronym-form="singular+short">featurevec</span> <span
class="math inline">$\featurevec^{(0)}$</span>, we can use a local
approximation <span
class="math inline"><em>g</em> ∈ ℋ<sup>′</sup></span>. </figcaption>
</figure>

See also: [model]{acronym-label="model" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[featurevec]{acronym-label="featurevec" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[explanation]{acronym-label="explanation"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"},
[decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"}, [deepnet]{acronym-label="deepnet"
acronym-form="singular+short"}, [linmodel]{acronym-label="linmodel"
acronym-form="singular+short"}.

, first=LIME,text=LIME

name=Gaussian process (GP), description=

A GP is a collection of [rvs]{acronym-label="rv"
acronym-form="plural+short"}
$\{f(\featurevec)\}_{\featurevec \in \mathcal{X}}$ indexed by input
values $\featurevec$ from some input space $\mathcal{X}$, such that for
any finite subset
$\featurevec^{(1)}, \ldots, \featurevec^{(m)} \in \mathcal{X}$, the
corresponding [rvs]{acronym-label="rv" acronym-form="plural+short"}
$f(\featurevec^{(1)}, \ldots, \featurevec^{(m)}$ have a joint
multivariate Gaussian distribution:
$$\left( f(\featurevec^{(1)}, \ldots, \featurevec^{(m)} \right) \sim \mathcal{N}(\boldsymbol{\mu}, \mathbf{K}).$$
For a fixed input space $\mathcal{X}$, a GP is fully specified (or
parametrized) by

- a [mean]{acronym-label="mean" acronym-form="singular+short"} function
  $\mu(\featurevec) = \expect\{ f(\featurevec)\}$

- and a covariance function
  $K\big(\featurevec,\featurevec'\big)= \expect\{ \big(f(\featurevec)-\mu(\featurevec)\big) \big(f(\featurevec')-\mu(\featurevec')\big) \big\}$.

We can interpret the temperature distribution across Finland (at a
specific point in time) as the [realization]{acronym-label="realization"
acronym-form="singular+short"} of a GP $f(\featurevec)$, where each
input $\featurevec = (\text{lat}, \text{lon})$ denotes a geographic
location. Temperature observations from [fmi]{acronym-label="fmi"
acronym-form="singular+short"} weather stations provide samples of
$f(\featurevec)$ at specific locations (see
Fig. [5](#fig_gp_FMI){reference-type="ref" reference="fig_gp_FMI"}). A
GP allows us to predict the temperature nearby [fmi]{acronym-label="fmi"
acronym-form="singular+short"} weather stations and to quantify the
[uncertainty]{acronym-label="uncertainty" acronym-form="singular+short"}
of these predictions.

<figure id="fig_gp_FMI">
<div class="center">

</div>
<figcaption>We can interpret the temperature distribution over Finland
as a <span data-acronym-label="realization"
data-acronym-form="singular+short">realization</span> of a GP indexed by
geographic coordinates and sampled at <span data-acronym-label="fmi"
data-acronym-form="singular+short">fmi</span> weather stations
(indicated by blue dots). <span id="fig_gp_FMI"
data-label="fig_gp_FMI"></span></figcaption>
</figure>

See also: [rv]{acronym-label="rv" acronym-form="singular+short"},
[mean]{acronym-label="mean" acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [fmi]{acronym-label="fmi"
acronym-form="singular+short"},
[uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"}.

, first = GP, text = GP

name=squared error loss, description=The squared error
[loss]{acronym-label="loss" acronym-form="singular+short"} measures the
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
error of a [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\hypothesis$ when predicting a numeric
[label]{acronym-label="label" acronym-form="singular+short"}
$\truelabel \in \mathbb{R}$ from the [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$ of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}. It
is defined as $$\nonumber
%   \label{equ_squared_loss_gls}
    L\left((\featurevec,\truelabel),\hypothesis \right) \defeq \big(\truelabel - \underbrace{\hypothesis(\featurevec)}_{=\predictedlabel} \big)^{2}.$$\
See also: [loss]{acronym-label="loss" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}. ,
first=squared error loss, text=squared error loss

name=projection, description=Consider a subset
$\mathcal{W} \subseteq \mathbb{R}^{d}$ of the $d$-dimensional
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}. We define the projection
$\projection{\mathcal{W}}{\vw}$ of a vector $\vw \in \mathbb{R}^{d}$
onto $\mathcal{W}$ as $$\label{equ_def_proj_generic_dict}
         \projection{\mathcal{W}}{\vw} = \argmin_{\vw' \in \mathcal{W}} \left\Vert  {\vw - \vw'} \right\Vert_{2}.$$
In other words, $\projection{\mathcal{W}}{\vw}$ is the vector in
$\mathcal{W}$ which is closest to $\vw$. The projection is only
well-defined for subsets $\mathcal{W}$ for which the above
[minimum]{acronym-label="minimum" acronym-form="singular+short"} exists
[@BoydConvexBook].\
See also: [euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}, [minimum]{acronym-label="minimum"
acronym-form="singular+short"}., first=projection, text=projection

name=projected gradient descent (projected GD), description=

Consider an [erm]{acronym-label="erm"
acronym-form="singular+short"}-based method that uses a parametrized
[model]{acronym-label="model" acronym-form="singular+short"} with
[paramspace]{acronym-label="paramspace" acronym-form="singular+short"}
$\mathcal{W} \subseteq \mathbb{R}^{d}$. Even if the
[objfunc]{acronym-label="objfunc" acronym-form="singular+short"} of
[erm]{acronym-label="erm" acronym-form="singular+short"} is
[smooth]{acronym-label="smooth" acronym-form="singular+short"}, we
cannot use basic [gd]{acronym-label="gd" acronym-form="singular+short"},
as it does not take into account contraints on the optimization variable
(i.e., the [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}). Projected [gd]{acronym-label="gd"
acronym-form="singular+short"} extends basic [gd]{acronym-label="gd"
acronym-form="singular+short"} to handle constraints on the optimization
variable (i.e., the [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}). A single iteration of projected
[gd]{acronym-label="gd" acronym-form="singular+short"} consists of first
taking a [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"} and then projecting the result back onto
the [paramspace]{acronym-label="paramspace"
acronym-form="singular+short"}.

<figure id="fig_projected_GD_dict">
<div class="center">

</div>
<figcaption>Projected <span data-acronym-label="gd"
data-acronym-form="singular+short">gd</span> augments a basic <span
data-acronym-label="gradstep"
data-acronym-form="singular+short">gradstep</span> with a <span
data-acronym-label="projection"
data-acronym-form="singular+short">projection</span> back onto the
constraint set <span class="math inline">𝒲</span>.</figcaption>
</figure>

See also: [erm]{acronym-label="erm" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[paramspace]{acronym-label="paramspace" acronym-form="singular+short"},
[objfunc]{acronym-label="objfunc" acronym-form="singular+short"},
[smooth]{acronym-label="smooth" acronym-form="singular+short"},
[gd]{acronym-label="gd" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}, [projection]{acronym-label="projection"
acronym-form="singular+short"}.

, first=projected gradient descent (projected GD), text=projected GD

name=differential privacy (DP), description=Consider some
[ml]{acronym-label="ml" acronym-form="singular+short"} method
$\mathcal{A}$ that reads in a [dataset]{acronym-label="dataset"
acronym-form="singular+short"} (e.g., the
[trainset]{acronym-label="trainset" acronym-form="singular+short"} used
for [erm]{acronym-label="erm" acronym-form="singular+short"}) and
delivers some output $\mathcal{A}(\dataset)$. The output could be either
the learned [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} or the
[predictions]{acronym-label="prediction" acronym-form="plural+short"}
for specific [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}. DP is a precise measure of
[privleakage]{acronym-label="privleakage" acronym-form="singular+short"}
incurred by revealing the output. Roughly speaking, an
[ml]{acronym-label="ml" acronym-form="singular+short"} method is
differentially private if the [probdist]{acronym-label="probdist"
acronym-form="singular+short"} of the output $\mathcal{A}(\dataset)$
does not change too much if the [sensattr]{acronym-label="sensattr"
acronym-form="singular+short"} of one
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} in
the [trainset]{acronym-label="trainset" acronym-form="singular+short"}
is changed. Note that DP builds on a
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"} for
an [ml]{acronym-label="ml" acronym-form="singular+short"} method, i.e.,
we interpret its output $\mathcal{A}(\dataset)$ as the
[realization]{acronym-label="realization" acronym-form="singular+short"}
of an [rv]{acronym-label="rv" acronym-form="singular+short"}. The
randomness in the output can be ensured by intentionally adding the
[realization]{acronym-label="realization" acronym-form="singular+short"}
of an auxiliary [rv]{acronym-label="rv" acronym-form="singular+short"}
(i.e., adding noise) to the output of the [ml]{acronym-label="ml"
acronym-form="singular+short"} method.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[trainset]{acronym-label="trainset" acronym-form="singular+short"},
[erm]{acronym-label="erm" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"},
[privleakage]{acronym-label="privleakage"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [sensattr]{acronym-label="sensattr"
acronym-form="singular+short"}, [probmodel]{acronym-label="probmodel"
acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [rv]{acronym-label="rv"
acronym-form="singular+short"}., first = DP, text=DP

name=stability, description=

Stability is a desirable property of an [ml]{acronym-label="ml"
acronym-form="singular+short"} method $\mathcal{A}$ that maps a
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset$ (e.g., a [trainset]{acronym-label="trainset"
acronym-form="singular+short"}) to an output $\mathcal{A}(\dataset)$.
The output $\mathcal{A}(\dataset)$ can be the learned
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
or the [prediction]{acronym-label="prediction"
acronym-form="singular+short"} delivered by the trained
[model]{acronym-label="model" acronym-form="singular+short"} for a
specific [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. Intuitively, $\mathcal{A}$ is stable if
small changes in the input [dataset]{acronym-label="dataset"
acronym-form="singular+short"} $\dataset$ lead to small changes in the
output $\mathcal{A}(\dataset)$. Several formal notions of stability
exist that enable bounds on the
[generalization]{acronym-label="generalization"
acronym-form="singular+short"} error or [risk]{acronym-label="risk"
acronym-form="singular+short"} of the method (see [@ShalevMLBook
Ch. 13]). To build intuition, consider the three
[datasets]{acronym-label="dataset" acronym-form="plural+short"} depicted
in Fig. [7](#fig_three_data_stability){reference-type="ref"
reference="fig_three_data_stability"}, each of which is equally likely
under the same [data]{acronym-label="data"
acronym-form="singular+short"}-generating
[probdist]{acronym-label="probdist" acronym-form="singular+short"}.
Since the optimal [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} are determined by this underlying
[probdist]{acronym-label="probdist" acronym-form="singular+short"}, an
accurate [ml]{acronym-label="ml" acronym-form="singular+short"} method
$\mathcal{A}$ should return the same (or very similar) output
$\mathcal{A}(\dataset)$ for all three [datasets]{acronym-label="dataset"
acronym-form="plural+short"}. In other words, any useful $\mathcal{A}$
must be robust to variability in [sample]{acronym-label="sample"
acronym-form="singular+short"}
[realizations]{acronym-label="realization" acronym-form="plural+short"}
from the same [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, i.e., it must be stable.

<figure id="fig_three_data_stability">

<figcaption>Three <span data-acronym-label="dataset"
data-acronym-form="plural+short">datasets</span> <span
class="math inline">$\dataset^{(*)}$</span>, <span
class="math inline">$\dataset^{(\square)}$</span>, and <span
class="math inline">$\dataset^{(\triangle)}$</span>, each sampled
independently from the same <span data-acronym-label="data"
data-acronym-form="singular+short">data</span>-generating <span
data-acronym-label="probdist"
data-acronym-form="singular+short">probdist</span>. A stable <span
data-acronym-label="ml" data-acronym-form="singular+short">ml</span>
method should return similar outputs when trained on any of these <span
data-acronym-label="dataset"
data-acronym-form="plural+short">datasets</span>. <span
id="fig_three_data_stability"
data-label="fig_three_data_stability"></span></figcaption>
</figure>

See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[trainset]{acronym-label="trainset" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"},
[generalization]{acronym-label="generalization"
acronym-form="singular+short"}, [risk]{acronym-label="risk"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [sample]{acronym-label="sample"
acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}.

, first = stability, text=stability

name=privacy protection, description=Consider some
[ml]{acronym-label="ml" acronym-form="singular+short"} method
$\mathcal{A}$ that reads in a [dataset]{acronym-label="dataset"
acronym-form="singular+short"} $\dataset$ and delivers some output
$\mathcal{A}(\dataset)$. The output could be the learned
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
$\widehat{\vw}$ or the [prediction]{acronym-label="prediction"
acronym-form="singular+short"} $\hat{\hypothesis}(\featurevec)$ obtained
for a specific [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} with [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$. Many important
[ml]{acronym-label="ml" acronym-form="singular+short"} applications
involve [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} representing humans. Each
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} is
characterized by [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$, potentially a
[label]{acronym-label="label" acronym-form="singular+short"}
$\truelabel$, and a [sensattr]{acronym-label="sensattr"
acronym-form="singular+short"} $s$ (e.g., a recent medical diagnosis).
Roughly speaking, privacy protection means that it should be impossible
to infer, from the output $\mathcal{A}(\dataset)$, any of the
[sensattrs]{acronym-label="sensattr" acronym-form="plural+short"} of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} in
$\dataset$. Mathematically, privacy protection requires
non-invertibility of the map $\mathcal{A}(\dataset)$. In general, just
making $\mathcal{A}(\dataset)$ non-invertible is typically insufficient
for privacy protection. We need to make $\mathcal{A}(\dataset)$
sufficiently non-invertible.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [sensattr]{acronym-label="sensattr"
acronym-form="singular+short"}. , first = privacy protection,
text=privacy protection

name=privacy leakage, description=Consider an [ml]{acronym-label="ml"
acronym-form="singular+short"} application that processes a
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset$ and delivers some output, such as the
[predictions]{acronym-label="prediction" acronym-form="plural+short"}
obtained for new [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}. Privacy leakage arises if the output
carries information about a private (or sensitive)
[feature]{acronym-label="feature" acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
(which might be a human) of $\dataset$. Based on a
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"} for
the [data]{acronym-label="data" acronym-form="singular+short"}
generation, we can measure the privacy leakage via the
[mutualinformation]{acronym-label="mutualinformation"
acronym-form="singular+short"} between the output and the senstive
[feature]{acronym-label="feature" acronym-form="singular+short"}.
Another quantitative measure of privacy leakage is
[diffpriv]{acronym-label="diffpriv" acronym-form="singular+short"}. The
relations between different measures of privacy leakage have been
studied in the literature (see [@InfThDiffPriv]).\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"},
[data]{acronym-label="data" acronym-form="singular+short"},
[mutualinformation]{acronym-label="mutualinformation"
acronym-form="singular+short"}, [diffpriv]{acronym-label="diffpriv"
acronym-form="singular+short"}. , first = privacy leakage, text=privacy
leakage

name=probabilistic model, plural=probabilistic models, description=A
probabilistic [model]{acronym-label="model"
acronym-form="singular+short"} interprets
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} as
[realizations]{acronym-label="realization" acronym-form="plural+short"}
of [rvs]{acronym-label="rv" acronym-form="plural+short"} with a joint
[probdist]{acronym-label="probdist" acronym-form="singular+short"}. This
joint [probdist]{acronym-label="probdist" acronym-form="singular+short"}
typically involves [parameters]{acronym-label="parameters"
acronym-form="singular+short"} which have to be manually chosen or
learned via statistical inference methods such as
[maxlikelihood]{acronym-label="maxlikelihood"
acronym-form="singular+short"} estimation [@LC].\
See also: [model]{acronym-label="model" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [rv]{acronym-label="rv"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [parameters]{acronym-label="parameters"
acronym-form="singular+short"},
[maxlikelihood]{acronym-label="maxlikelihood"
acronym-form="singular+short"}. , first = probabilistic model,
text=probabilistic model

name=mean, plural=means, description=The mean of an
[rv]{acronym-label="rv" acronym-form="singular+short"} $\featurevec$,
taking values in an [euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"} $\mathbb{R}^{d}$, is its
[expectation]{acronym-label="expectation" acronym-form="singular+short"}
$\expect\{\featurevec\}$. It is defined as the Lebesgue integral of
$\featurevec$ with respect to the underlying
[probdist]{acronym-label="probdist" acronym-form="singular+short"} $P$
(e.g., see [@BillingsleyProbMeasure] or
[@RudinBookPrinciplesMatheAnalysis]), i.e.,
$$\expect\{\featurevec\} = \int_{\mathbb{R}^{d}} {\bf x} \, \mathrm{d}P({\bf x}).$$
We also use the term to refer to the average of a finite sequence
${\bf x}^{(1)}, \ldots, {\bf x}^{(m)} \in \mathbb{R}^{d}$. However,
these two definitions are essentially the same. Indeed, we can use the
sequence ${\bf x}^{(1)}, \ldots, {\bf x}^{(m)} \in \mathbb{R}^{d}$ to
construct a discrete [rv]{acronym-label="rv"
acronym-form="singular+short"} $\widetilde{{\bf x}}={\bf x}^{(I)}$, with
the index $I$ being chosen uniformly at random from the set
$\{1,\ldots,m\}$. The mean of $\widetilde{{\bf x}}$ is precisely the
average $\frac{1}{m} \sum_{r=1}^{m} {\bf x}^{(r)}$.\
See also: [rv]{acronym-label="rv" acronym-form="singular+short"},
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"},
[expectation]{acronym-label="expectation"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}., first = mean, text=mean

name=variance, description=The variance of a real-valued
[rv]{acronym-label="rv" acronym-form="singular+short"} $\feature$ is
defined as the [expectation]{acronym-label="expectation"
acronym-form="singular+short"}
$\expect\big\{ \big( x - \expect\{x \} \big)^{2} \big\}$ of the squared
difference between $\feature$ and its
[expectation]{acronym-label="expectation" acronym-form="singular+short"}
$\expect\{x \}$. We extend this definition to vector-valued
[rvs]{acronym-label="rv" acronym-form="plural+short"} $\featurevec$ as
$\expect\big\{ \big\| \featurevec - \expect\{\featurevec \} \big\|_{2}^{2} \big\}$.\
See also: [rv]{acronym-label="rv" acronym-form="singular+short"},
[expectation]{acronym-label="expectation"
acronym-form="singular+short"}. ,first=variance,text=variance

name=nearest neighbor (NN), description=NN methods learn a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hypothesis: \mathcal{X} \rightarrow \mathcal{Y}$ whose function value
$\hypothesis(\featurevec)$ is solely determined by the NNs within a
given [dataset]{acronym-label="dataset" acronym-form="singular+short"}.
Different methods use different metrics for determining the NNs. If
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} are
characterized by numeric [featurevecs]{acronym-label="featurevec"
acronym-form="plural+short"}, we can use their Euclidean distances as
the metric.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"}, [neighbors]{acronym-label="neighbors"
acronym-form="singular+short"}., first=nearest neighbor (NN),text=NN

name=neighborhood, description=The neighborhood of a node
$i \in \mathcal{V}$ is the subset of nodes constituted by the
[neighbors]{acronym-label="neighbors" acronym-form="singular+short"} of
$i$.\
See also: [neighbors]{acronym-label="neighbors"
acronym-form="singular+short"}., first=neighborhood,text=neighborhood

name=neighbors, description=The neighbors of a node $i \in \mathcal{V}$
within an [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"} are those nodes
$i' \in \mathcal{V} \setminus \{ i\}$ that are connected (via an edge)
to node $i$.\
See also: [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}., first=neighbors,text=neighbors

name=bias, description=Consider an [ml]{acronym-label="ml"
acronym-form="singular+short"} method using a parametrized
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"}
$\mathcal{H}$. It learns the [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} $\vw \in \mathbb{R}^{d}$ using the
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$$\dataset=\big\{ \pair{\featurevec^{(r)}}{\truelabel^{(r)}} \big\}_{r=1}^{m}.$$
To analyze the properties of the [ml]{acronym-label="ml"
acronym-form="singular+short"} method, we typically interpret the
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} as
[realizations]{acronym-label="realization" acronym-form="plural+short"}
of [iid]{acronym-label="iid" acronym-form="singular+short"}
[rvs]{acronym-label="rv" acronym-form="plural+short"},
$$\truelabel^{(r)} = \hypothesis^{(\overline{\vw})}\big( \featurevec^{(r)} \big) + \bm{\varepsilon}^{(r)}, r=1,\ldots,m.$$
We can then interpret the [ml]{acronym-label="ml"
acronym-form="singular+short"} method as an estimator $\widehat{\vw}$
computed from $\dataset$ (e.g., by solving [erm]{acronym-label="erm"
acronym-form="singular+short"}). The (squared) bias incurred by the
estimate $\widehat{\vw}$ is then defined as
$B^{2} \defeq \big\| \expect \{ \widehat{\vw}  \}- \overline{\vw}\big\|_{2}^{2}$.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [iid]{acronym-label="iid"
acronym-form="singular+short"}, [rv]{acronym-label="rv"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}., first=bias,text=bias

name=classification, description=Classification is the task of
determining a discrete-valued label $\truelabel$ for a given
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
based solely on its features $\featurevec$. The label $\truelabel$
belongs to a finite set, such as $\truelabel \in \{-1,1\}$ or
$\truelabel \in \{1,\ldots,19\}$, and represents the category to which
the corresponding [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} belongs.\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}.,first=classification,text=classification

name=privacy funnel, description=The privacy funnel is a method for
learning privacy-friendly [features]{acronym-label="feature"
acronym-form="plural+short"} of [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} [@PrivacyFunnel].\
See also: [feature]{acronym-label="feature"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}., first=privacy funnel,text=privacy
funnel

name=condition number, description=The condition number
$\kappa(\mathbf{Q}) \geq 1$ of a positive definite matrix
$\mathbf{Q} \in \mathbb{R}^{\featuredim \times \featuredim}$ is the
ratio $\alpha /\beta$ between the largest $\alpha$ and the smallest
$\beta$ [eigenvalue]{acronym-label="eigenvalue"
acronym-form="singular+short"} of $\mathbf{Q}$. The condition number is
useful for the analysis of [ml]{acronym-label="ml"
acronym-form="singular+short"} methods. The computational complexity of
[gdmethods]{acronym-label="gdmethods" acronym-form="singular+short"} for
[linreg]{acronym-label="linreg" acronym-form="singular+short"} crucially
depends on the condition number of the matrix
$\mathbf{Q} = {\bf X} {\bf X}^{T}$, with the
[featuremtx]{acronym-label="featuremtx" acronym-form="singular+short"}
${\bf X}$ of the [trainset]{acronym-label="trainset"
acronym-form="singular+short"}. Thus, from a computational perspective,
we prefer [features]{acronym-label="feature"
acronym-form="plural+short"} of [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} such that $\mathbf{Q}$ has a condition
number close to $1$.\
See also: [eigenvalue]{acronym-label="eigenvalue"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [gdmethods]{acronym-label="gdmethods"
acronym-form="singular+short"}, [linreg]{acronym-label="linreg"
acronym-form="singular+short"}, [featuremtx]{acronym-label="featuremtx"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}.,first=condition number,text=condition
number

name=classifier, description=A classifier is a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
(i.e., a map) $\hypothesis(\featurevec)$ used to predict a
[label]{acronym-label="label" acronym-form="singular+short"} taking
values from a finite [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}. We might use the function value
$\hypothesis(\featurevec)$ itself as a
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
$\predictedlabel$ for the [label]{acronym-label="label"
acronym-form="singular+short"}. However, it is customary to use a map
$\hypothesis(\cdot)$ that delivers a numeric quantity. The
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
is then obtained by a simple thresholding step. For example, in a binary
[classification]{acronym-label="classification"
acronym-form="singular+short"} problem with []{#labelspace
label="labelspace"} $\mathcal{Y} \in  \{ -1,1\}$, we might use a
real-valued [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} map
$\hypothesis(\featurevec) \in \mathbb{R}$ as a classifier. A
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
$\predictedlabel$ can then be obtained via thresholding,
$$\label{equ_def_threshold_bin_classifier_dict}
            \predictedlabel =1   \mbox{ for } \hypothesis(\featurevec)\!\geq\!0 \mbox{ and }    \predictedlabel =-1  \mbox{ otherwise.}$$
We can characterize a classifier by its
[decisionregions]{acronym-label="decisionregion"
acronym-form="plural+short"} $\mathcal{R}_{a}$, for every possible
[label]{acronym-label="label" acronym-form="singular+short"} value
$a \in \mathcal{Y}$.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"},
[classification]{acronym-label="classification"
acronym-form="singular+short"},
[decisionregion]{acronym-label="decisionregion"
acronym-form="singular+short"}. ,first=classifier,text=classifier

name=empirical risk, description=The empirical
[risk]{acronym-label="risk" acronym-form="singular+short"}
$\emprisk{\hypothesis}{\dataset}$ of a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
on a [dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset$ is the average [loss]{acronym-label="loss"
acronym-form="singular+short"} incurred by $\hypothesis$ when applied to
the [datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
in $\dataset$.\
See also: [risk]{acronym-label="risk" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[loss]{acronym-label="loss" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.,
first=empirical risk,text=empirical risk

name=node degree, description=The degree $d^{(i)}$ of a node
$i \in \mathcal{V}$ in an undirected [graph]{acronym-label="graph"
acronym-form="singular+short"} is the number of its
[neighbors]{acronym-label="neighbors" acronym-form="singular+short"},
i.e., $d^{(i)} \defeq \big|\mathcal{N}^{(i)}\big|$.\
See also: [graph]{acronym-label="graph" acronym-form="singular+short"},
[neighbors]{acronym-label="neighbors"
acronym-form="singular+short"}.,first=node degree,text=node degree

name=graph, description=A graph
$\mathcal{G} = \pair{\mathcal{V}}{\mathcal{E}}$ is a pair that consists
of a node set $\mathcal{V}$ and an edge set $\mathcal{E}$. In its most
general form, a graph is specified by a map that assigns each edge
$e \in \mathcal{E}$ a pair of nodes [@RockNetworks]. One important
family of graphs is simple undirected graphs. A simple undirected graph
is obtained by identifying each edge $e \in \mathcal{E}$ with two
different nodes $\{i,i'\}$. Weighted graphs also specify numeric
[weights]{acronym-label="weights" acronym-form="singular+short"}
$\edgeweight_{e}$ for each edge $e \in \mathcal{E}$.\
See also: [weights]{acronym-label="weights"
acronym-form="singular+short"}.,first=graph,text=graph

name=uncertainty, description=Uncertainty refers to the degree of
confidence---or lack thereof---associated with a quantity such as a
[model]{acronym-label="model" acronym-form="singular+short"}
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
parameter estimate, or observed [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. In [ml]{acronym-label="ml"
acronym-form="singular+short"}, uncertainty arises from various sources,
including noisy [data]{acronym-label="data"
acronym-form="singular+short"}, limited training
[samples]{acronym-label="sample" acronym-form="plural+short"}, or
ambiguity in [model]{acronym-label="model"
acronym-form="singular+short"} assumptions.
[probability]{acronym-label="probability" acronym-form="singular+short"}
theory offers a principled framework for representing and quantifying
such uncertainty.\
See also: [model]{acronym-label="model" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[ml]{acronym-label="ml" acronym-form="singular+short"},
[data]{acronym-label="data" acronym-form="singular+short"},
[sample]{acronym-label="sample" acronym-form="singular+short"},
[probability]{acronym-label="probability"
acronym-form="singular+short"}., first=uncertainty,text=uncertainty

name=upper confidence bound (UCB), description=Consider an
[ml]{acronym-label="ml" acronym-form="singular+short"} application that
requires selecting, at each time step $k$, an action $\action_{k}$ from
a finite set of alternatives $\actionset$. The utility of selecting
action $\action_{k}$ is quantified by a numeric
[reward]{acronym-label="reward" acronym-form="singular+short"} signal
$r^{(\action_{k})}$. A widely used [probmodel]{acronym-label="probmodel"
acronym-form="singular+short"} for this type of sequential
decision-making problem is the stochastic [mab]{acronym-label="mab"
acronym-form="singular+short"} setting [@Bubeck2012]. In this
[model]{acronym-label="model" acronym-form="singular+short"}, the
[reward]{acronym-label="reward" acronym-form="singular+short"} $r^{(a)}$
is viewed as the [realization]{acronym-label="realization"
acronym-form="singular+short"} of an [rv]{acronym-label="rv"
acronym-form="singular+short"} with unknown [mean]{acronym-label="mean"
acronym-form="singular+short"} $\mu^{(a)}$. Ideally, we would always
choose the action with the largest expected
[reward]{acronym-label="reward" acronym-form="singular+short"}
$\mu^{(a)}$, but these [means]{acronym-label="mean"
acronym-form="plural+short"} are unknown and must be estimated from
observed [data]{acronym-label="data" acronym-form="singular+short"}.
Simply choosing the action with the largest estimate
$\widehat{\mu}^{(a)}$ can lead to suboptimal outcomes due to estimation
[uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"}. The UCB strategy addresses this by
selecting actions not only based on their estimated
[means]{acronym-label="mean" acronym-form="plural+short"} but also by
incorporating a term that reflects the
[uncertainty]{acronym-label="uncertainty" acronym-form="singular+short"}
in these estimates---favoring actions with high potential
[reward]{acronym-label="reward" acronym-form="singular+short"} and high
[uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"}. Theoretical guarantees for the
performance of UCB strategies, including logarithmic
[regret]{acronym-label="regret" acronym-form="singular+short"} bounds,
are established in [@Bubeck2012].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[reward]{acronym-label="reward" acronym-form="singular+short"},
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"},
[mab]{acronym-label="mab" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [rv]{acronym-label="rv"
acronym-form="singular+short"}, [mean]{acronym-label="mean"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"},
[uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"}, [regret]{acronym-label="regret"
acronym-form="singular+short"}., first=upper confidence bound
(UCB),text=UCB

name=multi-armed bandit (MAB), description=A MAB problem models a
repeated decision-making scenario in which, at each time step $k$, a
learner must choose one out of several possible actions, often referred
to as arms, from a finite set $\actionset$. Each arm $a \in \actionset$
yields a stochastic [reward]{acronym-label="reward"
acronym-form="singular+short"} $r^{(a)}$ drawn from an unknown
[probdist]{acronym-label="probdist" acronym-form="singular+short"} with
[mean]{acronym-label="mean" acronym-form="singular+short"} $\mu^{(a)}$.
The learner's goal is to maximize the cumulative
[reward]{acronym-label="reward" acronym-form="singular+short"} over time
by strategically balancing exploration (i.e., gathering information
about uncertain arms) and exploitation (i.e., selecting arms known to
perform well). This balance is quantified by the notion of
[regret]{acronym-label="regret" acronym-form="singular+short"}, which
measures the performance gap between the learner's strategy and the
optimal strategy that always selects the best arm. MAB problems form a
foundational [model]{acronym-label="model"
acronym-form="singular+short"} in
[onlinelearning]{acronym-label="onlinelearning"
acronym-form="singular+short"}, reinforcement learning, and sequential
experimental design [@Bubeck2012].\
See also: [reward]{acronym-label="reward"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [mean]{acronym-label="mean"
acronym-form="singular+short"}, [regret]{acronym-label="regret"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}., first=MAB,text=MAB

name=optimism in the face of uncertainty, description=

[ml]{acronym-label="ml" acronym-form="singular+short"} methods learn
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
$\vw$ according to some performance criterion $\bar{f}(\vw)$. However,
they usually cannot access $\bar{f}(\vw)$ directly but rely on an
estimate (or approximation) $f(\vw)$ of $\bar{f}(\vw)$. As a case in
point, [erm]{acronym-label="erm" acronym-form="singular+short"}-based
methods use the average [loss]{acronym-label="loss"
acronym-form="singular+short"} on a given
[dataset]{acronym-label="dataset" acronym-form="singular+short"} (i.e.,
the [trainset]{acronym-label="trainset" acronym-form="singular+short"})
as an estimate for the [risk]{acronym-label="risk"
acronym-form="singular+short"} of a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}.
Using a [probmodel]{acronym-label="probmodel"
acronym-form="singular+short"}, one can construct a confidence interval
$\big[ l^{(\vw)},  u^{(\vw)} \big]$ for each choice $\vw$ for the
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}. One simple construction is
$l^{(\vw)} \defeq f(\vw) - \sigma/2$,
$u^{(\vw)} \defeq f(\vw)+ \sigma/2$, with $\sigma$ being a measure of
the (expected) deviation of $f(\vw)$ from $\bar{f}(\vw)$. We can also
use other constructions for this interval as long as they ensure that
$\bar{f}(\vw) \in\big[ l^{(\vw)},  u^{(\vw)} \big]$ with a sufficiently
high [probability]{acronym-label="probability"
acronym-form="singular+short"}. An optimist chooses the
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
according to the most favorable - yet still plausible - value
$\tilde{f}(\vw) \defeq  l^{(\vw)}$ of the performance criterion. Two
examples of [ml]{acronym-label="ml" acronym-form="singular+short"}
methods that use such an optimistic construction of an
[objfunc]{acronym-label="objfunc" acronym-form="singular+short"} are
[srm]{acronym-label="srm" acronym-form="singular+short"} [@ShalevMLBook
Ch. 11] and [ucb]{acronym-label="ucb" acronym-form="singular+short"}
methods for sequential decision making [@Bubeck2012 Sec. 2.2].

<figure>
<div class="center">

</div>
<figcaption><span data-acronym-label="ml"
data-acronym-form="singular+short">ml</span> methods learn <span
data-acronym-label="modelparams"
data-acronym-form="singular+short">modelparams</span> <span
class="math inline">$\vw$</span> by using some estimate of <span
class="math inline">$f(\vw)$</span> for the ultimate performance
criterion <span class="math inline">$\bar{f}(\vw)$</span>. Using a <span
data-acronym-label="probmodel"
data-acronym-form="singular+short">probmodel</span>, one can use <span
class="math inline">$f(\vw)$</span> to construct confidence intervals
<span class="math inline">$\big[ l^{(\vw)},  u^{(\vw)} \big]$</span>
which contain <span class="math inline">$\bar{f}(\vw)$</span> with a
high probability. The best plausible performance measure for a specific
choice <span class="math inline">$\vw$</span> of <span
data-acronym-label="modelparams"
data-acronym-form="singular+short">modelparams</span> is <span
class="math inline">$\tilde{f}(\vw) \defeq
l^{(\vw)}$</span>.</figcaption>
</figure>

See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [risk]{acronym-label="risk"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [probmodel]{acronym-label="probmodel"
acronym-form="singular+short"},
[probability]{acronym-label="probability"
acronym-form="singular+short"}, [objfunc]{acronym-label="objfunc"
acronym-form="singular+short"}, [srm]{acronym-label="srm"
acronym-form="singular+short"}, [ucb]{acronym-label="ucb"
acronym-form="singular+short"}.

,first=optimism in the face of uncertainty,text=optimism in the face of
uncertainty

name=federated learning network (FL network), description=An
[fl]{acronym-label="fl" acronym-form="singular+short"} network is an
undirected weighted [graph]{acronym-label="graph"
acronym-form="singular+short"} whose nodes represent
[data]{acronym-label="data" acronym-form="singular+short"} generators
that aim to train a local (or personalized)
[model]{acronym-label="model" acronym-form="singular+short"}. Each node
in an [fl]{acronym-label="fl" acronym-form="singular+short"} network
represents some [device]{acronym-label="device"
acronym-form="singular+short"} capable of collecting a
[localdataset]{acronym-label="localdataset"
acronym-form="singular+short"} and, in turn, train a
[localmodel]{acronym-label="localmodel" acronym-form="singular+short"}.
[fl]{acronym-label="fl" acronym-form="singular+short"} methods learn a
local [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\localhypothesis{i}$, for each node
$i \in \mathcal{V}$, such that it incurs small
[loss]{acronym-label="loss" acronym-form="singular+short"} on the
[localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"}.\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[graph]{acronym-label="graph" acronym-form="singular+short"},
[data]{acronym-label="data" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[device]{acronym-label="device" acronym-form="singular+short"},
[localdataset]{acronym-label="localdataset"
acronym-form="singular+short"}, [localmodel]{acronym-label="localmodel"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}.,first=federated learning network (FL
network),text=FL network

name=norm, description=A norm is a function that maps each (vector)
element of a vector space to a non-negative real number. This function
must be homogeneous and definite, and it must satisfy the triangle
inequality [@HornMatAnalysis]., first=norm,text=norm

name=dual norm, description=Every [norm]{acronym-label="norm"
acronym-form="singular+short"} $\left\Vert  {\cdot} \right\Vert_{}$
defined on an [euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"} $\mathbb{R}^{d}$ has an associated dual
[norm]{acronym-label="norm" acronym-form="singular+short"}, which is
denoted $\left\Vert  {\cdot} \right\Vert_{*}$ and defined as
$\normgeneric{{\bf y}}{*} \defeq \sup_{\norm{{\bf x}}{} \le 1} {\bf y}^{T} {\bf x}$.
The dual [norm]{acronym-label="norm" acronym-form="singular+short"}
measures the largest possible inner product between ${\bf y}$ and any
vector in the unit ball of the original [norm]{acronym-label="norm"
acronym-form="singular+short"}. For further details, see
[@BoydConvexBook Sec. A.1.6].\
See also: [norm]{acronym-label="norm" acronym-form="singular+short"},
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}., first=dual norm, text=dual norm

name=explanation, description=One approach to make
[ml]{acronym-label="ml" acronym-form="singular+short"} methods
transparent is to provide an explanation along with the
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
delivered by an [ml]{acronym-label="ml" acronym-form="singular+short"}
method. Explanations can take on many different forms. An explanation
could be some natural text or some quantitative measure for the
importance of individual [features]{acronym-label="feature"
acronym-form="plural+short"} of a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} [@Molnar2019]. We can also use visual
forms of explanations, such as intensity plots for image
[classification]{acronym-label="classification"
acronym-form="singular+short"} [@GradCamPaper].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[classification]{acronym-label="classification"
acronym-form="singular+short"}., first=explanation,text=explanation

name=risk, description=Consider a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hypothesis$ used to predict the [label]{acronym-label="label"
acronym-form="singular+short"} $\truelabel$ of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
based on its [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$. We measure the quality of a
particular [prediction]{acronym-label="prediction"
acronym-form="singular+short"} using a
[lossfunc]{acronym-label="lossfunc" acronym-form="singular+short"}
$L\left((\featurevec,\truelabel),\hypothesis \right)$. If we interpret
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} as
the [realizations]{acronym-label="realization"
acronym-form="plural+short"} of [iid]{acronym-label="iid"
acronym-form="singular+short"} [rvs]{acronym-label="rv"
acronym-form="plural+short"}, also the
$L\left((\featurevec,\truelabel),\hypothesis \right)$ becomes the
[realization]{acronym-label="realization" acronym-form="singular+short"}
of an [rv]{acronym-label="rv" acronym-form="singular+short"}. The
[iidasspt]{acronym-label="iidasspt" acronym-form="singular+short"}
allows us to define the risk of a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
as the expected [loss]{acronym-label="loss"
acronym-form="singular+short"}
$\expect \big\{L\left((\featurevec,\truelabel),\hypothesis \right) \big\}$.
Note that the risk of $\hypothesis$ depends on both the specific choice
for the [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"} and the
[probdist]{acronym-label="probdist" acronym-form="singular+short"} of
the [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [iid]{acronym-label="iid"
acronym-form="singular+short"} [rv]{acronym-label="rv"
acronym-form="singular+short"}, [iidasspt]{acronym-label="iidasspt"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}., first=risk,text=risk

name=activation function, description=Each artificial neuron within an
[ann]{acronym-label="ann" acronym-form="singular+short"} is assigned an
activation function $\sigma(\cdot)$ that maps a weighted combination of
the neuron inputs $\feature_{1},\ldots,\feature_{\featuredim}$ to a
single output value
$a = \sigma\big(\weight_{1} \feature_{1}+\ldots+\weight_{\featuredim} \feature_{\featuredim} \big)$.
Note that each neuron is parametrized by the
[weights]{acronym-label="weights" acronym-form="singular+short"}
$\weight_{1},\ldots,\weight_{\featuredim}$.\
See also: [ann]{acronym-label="ann" acronym-form="singular+short"},
[weights]{acronym-label="weights" acronym-form="singular+short"}.,
first=activation function,text=activation function

name=distributed algorithm, description=A distributed
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"} is
an [algorithm]{acronym-label="algorithm" acronym-form="singular+short"}
designed for a special type of computer, i.e., a collection of
interconnected computing devices (or nodes). These devices communicate
and coordinate their local computations by exchanging messages over a
network [@IntroDistAlg], [@ParallelDistrBook]. Unlike a classical
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"},
which is implemented on a single [device]{acronym-label="device"
acronym-form="singular+short"}, a distributed
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"} is
executed concurrently on multiple [devices]{acronym-label="device"
acronym-form="plural+short"} with computational capabilities. Similar to
a classical [algorithm]{acronym-label="algorithm"
acronym-form="singular+short"}, a distributed
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"} can
be modeled as a set of potential executions. However, each execution in
the distributed setting involves both local computations and
message-passing events. A generic execution might look as follows:
$$\begin{array}{l}
            \text{Node 1: } {\rm input}_1, s_1^{(1)}, s_2^{(1)}, \ldots, s_{T_1}^{(1)}, {\rm output}_1; \\
            \text{Node 2: } {\rm input}_2, s_1^{(2)}, s_2^{(2)}, \ldots, s_{T_2}^{(2)}, {\rm output}_2; \\
            \quad \vdots \\
            \text{Node N: } {\rm input}_N, s_1^{(N)}, s_2^{(N)}, \ldots, s_{T_N}^{(N)}, {\rm output}_N.
        \end{array}$$ Each [device]{acronym-label="device"
acronym-form="singular+short"} $i$ starts from its own local input and
performs a sequence of intermediate computations $s_{k}^{(i)}$ at
discrete time instants $k = 1, \dots, T_i$. These computations may
depend on both the previous local computations at the
[device]{acronym-label="device" acronym-form="singular+short"} and the
messages received from other [devices]{acronym-label="device"
acronym-form="plural+short"}. One important application of distributed
[algorithms]{acronym-label="algorithm" acronym-form="plural+short"} is
in [fl]{acronym-label="fl" acronym-form="singular+short"} where a
network of [devices]{acronym-label="device" acronym-form="plural+short"}
collaboratively trains a personal [model]{acronym-label="model"
acronym-form="singular+short"} for each [device]{acronym-label="device"
acronym-form="singular+short"}.\
See also: [algorithm]{acronym-label="algorithm"
acronym-form="singular+short"}, [device]{acronym-label="device"
acronym-form="singular+short"}, [fl]{acronym-label="fl"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}. , first=distributed algorithm,
text=distributed algorithm

name=algorithm, plural=algorithms, description=An algorithm is a
precise, step-by-step specification for how to produce an output from a
given input within a finite number of computational steps
[@Cormen:2022aa]. For example, an algorithm for training a
[linmodel]{acronym-label="linmodel" acronym-form="singular+short"}
explicitly describes how to transform a given
[trainset]{acronym-label="trainset" acronym-form="singular+short"} into
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
through a sequence of [gradsteps]{acronym-label="gradstep"
acronym-form="plural+short"}. This informal characterization can be
formalized rigorously via different mathematical
[models]{acronym-label="model" acronym-form="plural+short"}
[@Sipser2013]. One very simple [model]{acronym-label="model"
acronym-form="singular+short"} of an algorithm is a collection of
possible executions. Each execution is a sequence in the form of
$${\rm input},s_1,s_2,\ldots,s_T,{\rm output}$$ that respects the
constraints inherent to the computer executing the algorithm. Algorithms
may be deterministic, where each input results in a single execution, or
randomized, where executions can vary probabilistically. Randomized
algorithms can thus be analyzed by modeling execution sequences as
outcomes of random experiments, viewing the algorithm as a stochastic
process [@BertsekasProb], [@RandomizedAlgos], [@Gallager13]. Crucially,
an algorithm encompasses more than just a mapping from input to output;
it also includes the intermediate computational steps $s_1,\ldots,s_T$.\
See also: [linmodel]{acronym-label="linmodel"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}. , first=algorithm,text=algorithm

name=online learning, description= Some [ml]{acronym-label="ml"
acronym-form="singular+short"} methods are designed to process
[data]{acronym-label="data" acronym-form="singular+short"} in a
sequential manner, updating their
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
as new [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} become available---one at a time. A typical
example is time series data, such as daily minimum and maximum
temperatures recorded by a [fmi]{acronym-label="fmi"
acronym-form="singular+short"} weather station. These values form a
chronological sequence of observations. In online learning, the
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
(or its [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}) is refined incrementally with each newly
observed [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, without revisiting past
[data]{acronym-label="data" acronym-form="singular+short"}.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[data]{acronym-label="data" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [fmi]{acronym-label="fmi"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [onlineGD]{acronym-label="onlineGD"
acronym-form="singular+short"},
[onlinealgorithm]{acronym-label="onlinealgorithm"
acronym-form="singular+short"}. , first=online learning,text=online
learning

name=online algorithm, description=An online
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"}
processes input [data]{acronym-label="data"
acronym-form="singular+short"} incrementally, receiving
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
sequentially and making decisions or producing outputs (or decisions)
immediately without having access to the entire input in advance
[@PredictionLearningGames], [@HazanOCO]. Unlike an offline
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"},
which has the entire input available from the start, an online
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"}
must handle [uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"} about future inputs and cannot revise
past decisions. Similar to an offline
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"}, we
also represent an online [algorithm]{acronym-label="algorithm"
acronym-form="singular+short"} formally as a collection of possible
executions. However, the execution sequence for an online
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"} has
a distinct structure:
$${\rm in}_{1},s_1,{\rm out}_{1},{\rm in}_{2},s_2,{\rm out}_{2},\ldots,{\rm in}_{T},s_T,{\rm out}_{T}.$$
Each execution begins from an initial state (i.e., $\text{in}_{1}$) and
proceeds through alternating computational steps, outputs (or
decisions), and inputs. Specifically, at step $k$, the
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"}
performs a computational step $s_{k}$, generates an output
$\text{out}_{k}$, and then subsequently receives the next input
([datapoint]{acronym-label="datapoint" acronym-form="singular+short"})
$\text{in}_{k+1}$. A notable example of an online
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"} in
[ml]{acronym-label="ml" acronym-form="singular+short"} is
[onlineGD]{acronym-label="onlineGD" acronym-form="singular+short"},
which incrementally updates [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} as new
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
arrive.\
See also: [algorithm]{acronym-label="algorithm"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"},
[uncertainty]{acronym-label="uncertainty"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [onlineGD]{acronym-label="onlineGD"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"},
[onlinelearning]{acronym-label="onlinelearning"
acronym-form="singular+short"}. , first=online algorithm,text=online
algorithm

name=transparency, description=Transparency is a fundamental requirement
for [trustAI]{acronym-label="trustAI" acronym-form="singular+short"}
[@HLEGTrustworhtyAI]. In the context of [ml]{acronym-label="ml"
acronym-form="singular+short"} methods, transparency is often used
interchangeably with [explainability]{acronym-label="explainability"
acronym-form="singular+short"} [@JunXML2020], [@gallese2023ai]. However,
in the broader scope of [ai]{acronym-label="ai"
acronym-form="singular+short"} systems, transparency extends beyond
[explainability]{acronym-label="explainability"
acronym-form="singular+short"} and includes providing information about
the system's limitations, reliability, and intended use. In medical
diagnosis systems, transparency requires disclosing the confidence level
for the [predictions]{acronym-label="prediction"
acronym-form="plural+short"} delivered by a trained
[model]{acronym-label="model" acronym-form="singular+short"}. In credit
scoring, [ai]{acronym-label="ai" acronym-form="singular+short"}-based
lending decisions should be accompanied by explanations of contributing
factors, such as income level or credit history. These explanations
allow humans (e.g., a loan applicant) to understand and contest
automated decisions. Some [ml]{acronym-label="ml"
acronym-form="singular+short"} methods inherently offer transparency.
For example, [logreg]{acronym-label="logreg"
acronym-form="singular+short"} provides a quantitative measure of
[classification]{acronym-label="classification"
acronym-form="singular+short"} reliability through the value
$|\hypothesis(\featurevec)|$.
[decisiontrees]{acronym-label="decisiontree"
acronym-form="plural+short"} are another example, as they allow
human-readable decision rules [@rudin2019stop]. Transparency also
requires a clear indication when a user is engaging with an
[ai]{acronym-label="ai" acronym-form="singular+short"} system. For
example, [ai]{acronym-label="ai" acronym-form="singular+short"}-powered
chatbots should notify users that they are interacting with an automated
system rather than a human. Furthermore, transparency encompasses
comprehensive documentation detailing the purpose and design choices
underlying the [ai]{acronym-label="ai" acronym-form="singular+short"}
system. For instance, [model]{acronym-label="model"
acronym-form="singular+short"} datasheets [@DatasheetData2021] and
[ai]{acronym-label="ai" acronym-form="singular+short"} system cards
[@10.1145/3287560.3287596] help practitioners understand the intended
use cases and limitations of an [ai]{acronym-label="ai"
acronym-form="singular+short"} system [@Shahriari2017].\
See also: [trustAI]{acronym-label="trustAI"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"},
[explainability]{acronym-label="explainability"
acronym-form="singular+short"}, [ai]{acronym-label="ai"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [logreg]{acronym-label="logreg"
acronym-form="singular+short"},
[classification]{acronym-label="classification"
acronym-form="singular+short"},
[decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"}., first=transparency, text=transparency

name=sensitive attribute, plural=sensitive attributes,
description=[ml]{acronym-label="ml" acronym-form="singular+short"}
revolves around learning a [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} map that allows us to predict the
[label]{acronym-label="label" acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
from its [features]{acronym-label="feature"
acronym-form="plural+short"}. In some applications, we must ensure that
the output delivered by an [ml]{acronym-label="ml"
acronym-form="singular+short"} system does not allow us to infer
sensitive attributes of a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. Which part of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} is
considered a sensitive attribute is a design choice that varies across
different application domains.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"}.,
first=sensitive attribute,text=sensitive attribute

name=stochastic block model (SBM), description=The SBM is a
probabilistic generative [model]{acronym-label="model"
acronym-form="singular+short"} for an undirected
[graph]{acronym-label="graph" acronym-form="singular+short"}
$\mathcal{G} = \big( \mathcal{V}, \mathcal{E} \big)$ with a given set of
nodes $\mathcal{V}$ [@AbbeSBM2018]. In its most basic variant, the SBM
generates a [graph]{acronym-label="graph" acronym-form="singular+short"}
by first randomly assigning each node $i \in \mathcal{V}$ to a
[cluster]{acronym-label="cluster" acronym-form="singular+short"} index
$\clusteridx_{i} \in \{1,\ldots,k\}$. A pair of different nodes in the
[graph]{acronym-label="graph" acronym-form="singular+short"} is
connected by an edge with [probability]{acronym-label="probability"
acronym-form="singular+short"} $p_{i,i'}$ that depends solely on the
[labels]{acronym-label="label" acronym-form="plural+short"}
$\clusteridx_{i}, \clusteridx_{i'}$. The presence of edges between
different pairs of nodes is statistically independent.\
See also: [model]{acronym-label="model" acronym-form="singular+short"},
[graph]{acronym-label="graph" acronym-form="singular+short"},
[cluster]{acronym-label="cluster" acronym-form="singular+short"},
[probability]{acronym-label="probability"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}. , first=stochastic block model
(SBM),text=SBM

name=deep net, plural=deep nets, description=A deep net is an
[ann]{acronym-label="ann" acronym-form="singular+short"} with a
(relatively) large number of hidden layers. Deep learning is an umbrella
term for [ml]{acronym-label="ml" acronym-form="singular+short"} methods
that use a deep net as their [model]{acronym-label="model"
acronym-form="singular+short"} [@Goodfellow-et-al-2016].\
See also: [ann]{acronym-label="ann" acronym-form="singular+short"},
[ml]{acronym-label="ml" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"}.,
first=deep net,text=deep net

name=baseline, description=

Consider some [ml]{acronym-label="ml" acronym-form="singular+short"}
method that produces a learned [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} (or trained [model]{acronym-label="model"
acronym-form="singular+short"}) $\hat{\hypothesis} \in \mathcal{H}$. We
evaluate the quality of a trained [model]{acronym-label="model"
acronym-form="singular+short"} by computing the average
[loss]{acronym-label="loss" acronym-form="singular+short"} on a
[testset]{acronym-label="testset" acronym-form="singular+short"}. But
how can we assess whether the resulting
[testset]{acronym-label="testset" acronym-form="singular+short"}
performance is sufficiently good? How can we determine if the trained
[model]{acronym-label="model" acronym-form="singular+short"} performs
close to optimal and there is little point in investing more resources
(for [data]{acronym-label="data" acronym-form="singular+short"}
collection or computation) to improve it? To this end, it is useful to
have a reference (or baseline) level against which we can compare the
performance of the trained [model]{acronym-label="model"
acronym-form="singular+short"}. Such a reference value might be obtained
from human performance, e.g., the misclassification rate of
dermatologists who diagnose cancer from visual inspection of skin
[@SkinHumanAI]. Another source for a baseline is an existing, but for
some reason unsuitable, [ml]{acronym-label="ml"
acronym-form="singular+short"} method. For example, the existing
[ml]{acronym-label="ml" acronym-form="singular+short"} method might be
computationally too expensive for the intended [ml]{acronym-label="ml"
acronym-form="singular+short"} application. Nevertheless, its
[testset]{acronym-label="testset" acronym-form="singular+short"} error
can still serve as a baseline. Another, somewhat more principled,
approach to constructing a baseline is via a
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"}. In
many cases, given a [probmodel]{acronym-label="probmodel"
acronym-form="singular+short"} $p(\featurevec,\truelabel)$, we can
precisely determine the [minimum]{acronym-label="minimum"
acronym-form="singular+short"} achievable [risk]{acronym-label="risk"
acronym-form="singular+short"} among any hypotheses (not even required
to belong to the [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"} $\mathcal{H}$) [@LC]. This
[minimum]{acronym-label="minimum" acronym-form="singular+short"}
achievable [risk]{acronym-label="risk" acronym-form="singular+short"}
(referred to as the [bayesrisk]{acronym-label="bayesrisk"
acronym-form="singular+short"}) is the [risk]{acronym-label="risk"
acronym-form="singular+short"} of the
[bayesestimator]{acronym-label="bayesestimator"
acronym-form="singular+short"} for the [label]{acronym-label="label"
acronym-form="singular+short"} $\truelabel$ of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
given its [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$. Note that, for a given
choice of [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"}, the
[bayesestimator]{acronym-label="bayesestimator"
acronym-form="singular+short"} (if it exists) is completely determined
by the [probdist]{acronym-label="probdist"
acronym-form="singular+short"} $p(\featurevec,\truelabel)$ [@LC Ch. 4].
However, computing the [bayesestimator]{acronym-label="bayesestimator"
acronym-form="singular+short"} and [bayesrisk]{acronym-label="bayesrisk"
acronym-form="singular+short"} presents two main challenges:

1.  The [probdist]{acronym-label="probdist"
    acronym-form="singular+short"} $p(\featurevec,\truelabel)$ is
    unknown and needs to be estimated.

2.  Even if $p(\featurevec,\truelabel)$ is known, it can be
    computationally too expensive to compute the
    [bayesrisk]{acronym-label="bayesrisk" acronym-form="singular+short"}
    exactly [@cooper1990computational].

A widely used [probmodel]{acronym-label="probmodel"
acronym-form="singular+short"} is the [mvndist]{acronym-label="mvndist"
acronym-form="singular+short"}
$\left( \featurevec,\truelabel \right) \sim \mathcal{N}({\bm \mu},{\bm \Sigma})$
for [datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
characterized by numeric [features]{acronym-label="feature"
acronym-form="plural+short"} and [labels]{acronym-label="label"
acronym-form="plural+short"}. Here, for the
[sqerrloss]{acronym-label="sqerrloss" acronym-form="singular+short"},
the [bayesestimator]{acronym-label="bayesestimator"
acronym-form="singular+short"} is given by the posterior
[mean]{acronym-label="mean" acronym-form="singular+short"}
$\mu_{\truelabel|\featurevec}$ of the [label]{acronym-label="label"
acronym-form="singular+short"} $\truelabel$, given the
[features]{acronym-label="feature" acronym-form="plural+short"}
$\featurevec$ [@LC], [@GrayProbBook]. The corresponding
[bayesrisk]{acronym-label="bayesrisk" acronym-form="singular+short"} is
given by the posterior [variance]{acronym-label="variance"
acronym-form="singular+short"} $\sigma^{2}_{\truelabel|\featurevec}$
(see Fig. [8](#fig_post_baseline_dict){reference-type="ref"
reference="fig_post_baseline_dict"}).

<figure id="fig_post_baseline_dict">
<div class="center">

</div>
<figcaption>If the <span data-acronym-label="feature"
data-acronym-form="plural+short">features</span> and the <span
data-acronym-label="label"
data-acronym-form="singular+short">label</span> of a <span
data-acronym-label="datapoint"
data-acronym-form="singular+short">datapoint</span> are drawn from a
<span data-acronym-label="mvndist"
data-acronym-form="singular+short">mvndist</span>, we can achieve the
<span data-acronym-label="minimum"
data-acronym-form="singular+short">minimum</span> <span
data-acronym-label="risk" data-acronym-form="singular+short">risk</span>
(under <span data-acronym-label="sqerrloss"
data-acronym-form="singular+short">sqerrloss</span>) by using the <span
data-acronym-label="bayesestimator"
data-acronym-form="singular+short">bayesestimator</span> <span
class="math inline">$\mu_{\truelabel|\featurevec}$</span> to predict the
<span data-acronym-label="label"
data-acronym-form="singular+short">label</span> <span
class="math inline">$\truelabel$</span> of a <span
data-acronym-label="datapoint"
data-acronym-form="singular+short">datapoint</span> with <span
data-acronym-label="feature"
data-acronym-form="plural+short">features</span> <span
class="math inline">$\featurevec$</span>. The corresponding <span
data-acronym-label="minimum"
data-acronym-form="singular+short">minimum</span> <span
data-acronym-label="risk" data-acronym-form="singular+short">risk</span>
is given by the posterior <span data-acronym-label="variance"
data-acronym-form="singular+short">variance</span> <span
class="math inline">$\sigma^{2}_{\truelabel|\featurevec}$</span>. We can
use this quantity as a baseline for the average <span
data-acronym-label="loss" data-acronym-form="singular+short">loss</span>
of a trained <span data-acronym-label="model"
data-acronym-form="singular+short">model</span> <span
class="math inline">$\hat{\hypothesis}$</span>. <span
id="fig_post_baseline_dict"
data-label="fig_post_baseline_dict"></span></figcaption>
</figure>

See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[loss]{acronym-label="loss" acronym-form="singular+short"},
[testset]{acronym-label="testset" acronym-form="singular+short"},
[data]{acronym-label="data" acronym-form="singular+short"},
[probmodel]{acronym-label="probmodel" acronym-form="singular+short"},
[minimum]{acronym-label="minimum" acronym-form="singular+short"},
[risk]{acronym-label="risk" acronym-form="singular+short"},
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"},
[bayesrisk]{acronym-label="bayesrisk" acronym-form="singular+short"},
[bayesestimator]{acronym-label="bayesestimator"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [mvndist]{acronym-label="mvndist"
acronym-form="singular+short"}, [sqerrloss]{acronym-label="sqerrloss"
acronym-form="singular+short"}, [mean]{acronym-label="mean"
acronym-form="singular+short"}, [variance]{acronym-label="variance"
acronym-form="singular+short"}.

, first=baseline,text=baseline

name=spectrogram, description=

A spectrogram represents the time-frequency distribution of the energy
of a time signal $x(t)$. Intuitively, it quantifies the amount of signal
energy present within a specific time segment
$[t_{1},t_{2}] \subseteq \mathbb{R}$ and frequency interval
$[f_{1},f_{2}]\subseteq \mathbb{R}$. Formally, the spectrogram of a
signal is defined as the squared magnitude of its short-time Fourier
transform (STFT) [@cohen1995time]. Fig.
[9](#fig:spectrogram_dict){reference-type="ref"
reference="fig:spectrogram_dict"} depicts a time signal along with its
spectrogram.

![Left: A time signal consisting of two modulated Gaussian pulses.
Right: An intensity plot of the spectrogram. []{#fig:spectrogram_dict
label="fig:spectrogram_dict"}](assets/spectrogram.png){#fig:spectrogram_dict
width="80%"}

The intensity plot of its spectrogram can serve as an image of a signal.
A simple recipe for audio signal
[classification]{acronym-label="classification"
acronym-form="singular+short"} is to feed this signal image into
[deepnets]{acronym-label="deepnet" acronym-form="plural+short"}
originally developed for image
[classification]{acronym-label="classification"
acronym-form="singular+short"} and object detection [@Li:2022aa]. It is
worth noting that, beyond the spectrogram, several alternative
representations exist for the time-frequency distribution of signal
energy [@TimeFrequencyAnalysisBoashash], [@MallatBook].\
See also: [classification]{acronym-label="classification"
acronym-form="singular+short"}, [deepnet]{acronym-label="deepnet"
acronym-form="singular+short"}.

, first=spectrogram,text=spectrogram

name=graph clustering, description=[graph]{acronym-label="graph"
acronym-form="singular+short"} [clustering]{acronym-label="clustering"
acronym-form="singular+short"} aims at
[clustering]{acronym-label="clustering" acronym-form="singular+short"}
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} that
are represented as the nodes of a [graph]{acronym-label="graph"
acronym-form="singular+short"} $\mathcal{G}$. The edges of $\mathcal{G}$
represent pairwise similarities between
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}.
Sometimes we can quantify the extend of these similarities by an
[edgeweight]{acronym-label="edgeweight" acronym-form="singular+short"}
[@FlowSpecClustering2021], [@Luxburg2007].\
See also: [graph]{acronym-label="graph" acronym-form="singular+short"},
[clustering]{acronym-label="clustering" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[edgeweight]{acronym-label="edgeweight" acronym-form="singular+short"}.
, first=graph clustering,text=graph clustering

name=spectral clustering, description=

Spectral [clustering]{acronym-label="clustering"
acronym-form="singular+short"} is a particular instance of
[graphclustering]{acronym-label="graphclustering"
acronym-form="singular+short"}, i.e., it clusters
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
represented as the nodes $i=1,\ldots,n$ of a
[graph]{acronym-label="graph" acronym-form="singular+short"}
$\mathcal{G}$. Spectral [clustering]{acronym-label="clustering"
acronym-form="singular+short"} uses the
[eigenvectors]{acronym-label="eigenvector" acronym-form="plural+short"}
of the [LapMat]{acronym-label="LapMat" acronym-form="singular+short"}
$\LapMat{\mathcal{G}}$ to construct
[featurevecs]{acronym-label="featurevec" acronym-form="plural+short"}
$\featurevec^{(i)} \in \mathbb{R}^{\featuredim}$ for each node (i.e.,
for each [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}) $i=1,\ldots,n$. We can feed these
[featurevecs]{acronym-label="featurevec" acronym-form="plural+short"}
into [euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}-based
[clustering]{acronym-label="clustering" acronym-form="singular+short"}
methods, such as [kmeans]{acronym-label="kmeans"
acronym-form="singular+short"} or
[softclustering]{acronym-label="softclustering"
acronym-form="singular+short"} via [gmm]{acronym-label="gmm"
acronym-form="singular+short"}. Roughly speaking, the
[featurevecs]{acronym-label="featurevec" acronym-form="plural+short"} of
nodes belonging to a well-connected subset (or
[cluster]{acronym-label="cluster" acronym-form="singular+short"}) of
nodes in $\mathcal{G}$ are located nearby in the
[euclidspace]{acronym-label="euclidspace" acronym-form="singular+short"}
$\mathbb{R}^{\featuredim}$ (see Fig.
[10](#fig_lap_mtx_specclustering_dict){reference-type="ref"
reference="fig_lap_mtx_specclustering_dict"}).

<figure id="fig_lap_mtx_specclustering_dict">
<div class="center">
<div class="minipage">

</div>
<div class="minipage">
<p><span class="math display">$$\LapMat{\mathcal{G}}\!=\!
                        \begin{pmatrix}
                            2 &amp; -1 &amp; -1 &amp; 0 \\
                            -1 &amp; 1 &amp; 0 &amp; 0 \\  
                            -1 &amp; 0 &amp; 1 &amp; 0 \\
                            0 &amp; 0 &amp; 0 &amp; 0
                        \end{pmatrix}\!=\!\mathbf{V} {\bm \Lambda}
\mathbf{V}^{T}  
                        \nonumber$$</span></p>
</div>
<p><br />
</p>
<div class="minipage">

</div>
<div class="minipage">
<p><span class="math display">$$\begin{aligned}
                                            &amp; \mathbf{V} = \big(
{\bf v}^{(1)},{\bf v}^{(2)},{\bf v}^{(3)},{\bf v}^{(4)} \big) \nonumber
\\
                                            &amp;   \mathbf{v}^{(1)}\!=\!\frac{1}{\sqrt{3}}
\begin{pmatrix} 1 \\ 1 \\ 1 \\ 0 \end{pmatrix}, \,
                                                \mathbf{v}^{(2)}\!=\!\begin{pmatrix}
0 \\ 0 \\ 0 \\ 1 \end{pmatrix} \nonumber
                                                
\end{aligned}$$</span></p>
</div>
</div>
<figcaption><span id="fig_lap_mtx_specclustering_dict"
data-label="fig_lap_mtx_specclustering_dict"></span>
<span><strong>Top.</strong></span> Left: An undirected <span
data-acronym-label="graph"
data-acronym-form="singular+short">graph</span> <span
class="math inline">𝒢</span> with four nodes <span
class="math inline"><em>i</em> = 1, 2, 3, 4</span>, each representing a
<span data-acronym-label="datapoint"
data-acronym-form="singular+short">datapoint</span>. Right: The <span
data-acronym-label="LapMat"
data-acronym-form="singular+short">LapMat</span> <span
class="math inline">$\LapMat{\mathcal{G}}  \in \mathbb{R}^{4 \times
4}$</span> and its <span data-acronym-label="evd"
data-acronym-form="singular+short">evd</span>.
<span><strong>Bottom.</strong></span> Left: A <span
data-acronym-label="scatterplot"
data-acronym-form="singular+short">scatterplot</span> of <span
data-acronym-label="datapoint"
data-acronym-form="plural+short">datapoints</span> using the <span
data-acronym-label="featurevec"
data-acronym-form="plural+short">featurevecs</span> <span
class="math inline">$\featurevec^{(i)} = \big( v^{(1)}_{i},v^{(2)}_{i}
\big)^{T}$</span>. Right: Two <span data-acronym-label="eigenvector"
data-acronym-form="plural+short">eigenvectors</span> <span
class="math inline">${\bf v}^{(1)},{\bf v}^{(2)} \in
\mathbb{R}^{\featuredim}$</span> corresponding to the <span
data-acronym-label="eigenvalue"
data-acronym-form="singular+short">eigenvalue</span> <span
class="math inline"><em>λ</em> = 0</span> of the <span
data-acronym-label="LapMat"
data-acronym-form="singular+short">LapMat</span> <span
class="math inline">$\LapMat{\mathcal{G}}$</span>. </figcaption>
</figure>

See also: [clustering]{acronym-label="clustering"
acronym-form="singular+short"},
[graphclustering]{acronym-label="graphclustering"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [graph]{acronym-label="graph"
acronym-form="singular+short"},
[eigenvector]{acronym-label="eigenvector"
acronym-form="singular+short"}, [LapMat]{acronym-label="LapMat"
acronym-form="singular+short"}, [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"},
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}, [kmeans]{acronym-label="kmeans"
acronym-form="singular+short"},
[softclustering]{acronym-label="softclustering"
acronym-form="singular+short"}, [gmm]{acronym-label="gmm"
acronym-form="singular+short"}, [cluster]{acronym-label="cluster"
acronym-form="singular+short"}, [evd]{acronym-label="evd"
acronym-form="singular+short"},
[scatterplot]{acronym-label="scatterplot"
acronym-form="singular+short"}, [eigenvalue]{acronym-label="eigenvalue"
acronym-form="singular+short"}.

, first=spectral clustering,text=spectral clustering

name=flow-based clustering, description=Flow-based
[clustering]{acronym-label="clustering" acronym-form="singular+short"}
groups the nodes of an undirected [graph]{acronym-label="graph"
acronym-form="singular+short"} by applying
[kmeans]{acronym-label="kmeans" acronym-form="singular+short"}
[clustering]{acronym-label="clustering" acronym-form="singular+short"}
to node-wise [featurevecs]{acronym-label="featurevec"
acronym-form="plural+short"}. These
[featurevecs]{acronym-label="featurevec" acronym-form="plural+short"}
are built from network flows between carefully selected sources and
destination nodes [@FlowSpecClustering2021].\
See also: [clustering]{acronym-label="clustering"
acronym-form="singular+short"}, [graph]{acronym-label="graph"
acronym-form="singular+short"}, [kmeans]{acronym-label="kmeans"
acronym-form="singular+short"}, [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"}., first=flow-based
clustering,text=flow-based clustering

name=estimation error, description=Consider
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"},
each with [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"} $\featurevec$ and
[label]{acronym-label="label" acronym-form="singular+short"}
$\truelabel$. In some applications, we can model the relation between
the [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"} and the [label]{acronym-label="label"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} as
$\truelabel = \bar{\hypothesis}(\featurevec) + \varepsilon$. Here, we
use some true underlying [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\bar{\hypothesis}$ and a noise term
$\varepsilon$ which summarizes any modeling or labeling errors. The
estimation error incurred by an [ml]{acronym-label="ml"
acronym-form="singular+short"} method that learns a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\widehat{\hypothesis}$, e.g., using [erm]{acronym-label="erm"
acronym-form="singular+short"}, is defined as
$\widehat{\hypothesis}(\featurevec) - \bar{\hypothesis}(\featurevec)$,
for some [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"}. For a parametric
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"},
which consists of [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} maps determined by
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
$\vw$, we can define the estimation error as
$\Delta \vw = \widehat{\vw} - \overline{\vw}$ [@kay],
[@hastie01statisticallearning].\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}., first=estimation error,text=estimation
error

name=degree of belonging, description=Degree of belonging is a number
that indicates the extent to which a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
belongs to a [cluster]{acronym-label="cluster"
acronym-form="singular+short"} [@MLBasics Ch. 8]. The degree of
belonging can be interpreted as a soft [cluster]{acronym-label="cluster"
acronym-form="singular+short"} assignment.
[softclustering]{acronym-label="softclustering"
acronym-form="singular+short"} methods can encode the degree of
belonging by a real number in the interval $[0,1]$.
[hardclustering]{acronym-label="hardclustering"
acronym-form="singular+short"} is obtained as the extreme case when the
degree of belonging only takes on values $0$ or $1$.\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [cluster]{acronym-label="cluster"
acronym-form="singular+short"},
[softclustering]{acronym-label="softclustering"
acronym-form="singular+short"},
[hardclustering]{acronym-label="hardclustering"
acronym-form="singular+short"}., first=degree of belonging,text=degree
of belonging

name=mean squared estimation error (MSEE), description=Consider an
[ml]{acronym-label="ml" acronym-form="singular+short"} method that
learns [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} $\widehat{\vw}$ based on some
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset$. If we interpret the [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} in $\dataset$ as [iid]{acronym-label="iid"
acronym-form="singular+short"}
[realizations]{acronym-label="realization" acronym-form="plural+short"}
of an [rv]{acronym-label="rv" acronym-form="singular+short"} $\vz$, we
define the [esterr]{acronym-label="esterr"
acronym-form="singular+short"}
$\Delta \vw \defeq \widehat{w} - \overline{\vw}$. Here, $\overline{\vw}$
denotes the true [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} of the
[probdist]{acronym-label="probdist" acronym-form="singular+short"} of
$\vz$. The MSEE is defined as the
[expectation]{acronym-label="expectation" acronym-form="singular+short"}
$\expect \big\{ \big\| \Delta \vw \big\|^{2} \big\}$ of the squared
Euclidean [norm]{acronym-label="norm" acronym-form="singular+short"} of
the [esterr]{acronym-label="esterr" acronym-form="singular+short"}
[@LC], [@kay].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [iid]{acronym-label="iid"
acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [rv]{acronym-label="rv"
acronym-form="singular+short"}, [esterr]{acronym-label="esterr"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"},
[expectation]{acronym-label="expectation"
acronym-form="singular+short"}, [norm]{acronym-label="norm"
acronym-form="singular+short"}, [mean]{acronym-label="mean"
acronym-form="singular+short"}., first=mean squared estimation error
(MSEE),text=MSEE

name=generalized total variation minimization (GTVMin),
description=GTVMin is an instance of [rerm]{acronym-label="rerm"
acronym-form="singular+short"} using the [gtv]{acronym-label="gtv"
acronym-form="singular+short"} of local
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
as a [regularizer]{acronym-label="regularizer"
acronym-form="singular+short"} [@ClusteredFLTVMinTSP].\
See also: [rerm]{acronym-label="rerm" acronym-form="singular+short"},
[gtv]{acronym-label="gtv" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"},
[regularizer]{acronym-label="regularizer"
acronym-form="singular+short"}., first=generalized total variation
minimization (GTVMin),text=GTVMin

name=regression, description=Regression problems revolve around the
prediction of a numeric [label]{acronym-label="label"
acronym-form="singular+short"} solely from the
[features]{acronym-label="feature" acronym-form="plural+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
[@MLBasics Ch. 2].\
See also: [label]{acronym-label="label" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.,
first=regression,text=regression

name=accuracy, description=Consider
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
characterized by [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec \in \mathcal{X}$ and a
categorical label $\truelabel$ which takes on values from a finite
[labelspace]{acronym-label="labelspace" acronym-form="singular+short"}
$\mathcal{Y}$. The accuracy of a [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}
$\hypothesis: \mathcal{X} \rightarrow \mathcal{Y}$, when applied to the
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} in a
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset = \big\{ \big(\featurevec^{(1)}, \truelabel^{(1)} \big), \ldots, \big(\featurevec^{(m)},\truelabel^{(m)}\big) \big\}$,
is then defined as
$1 - (1/m)\sum_{r=1}^{m} \lossfunczo{\big(\featurevec^{(r)},\truelabel^{(r)}\big)}{\hypothesis}$
using the [zerooneloss]{acronym-label="zerooneloss"
acronym-form="singular+short"} $L^{(0/1)}\left(\cdot,\cdot \right)$.\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"},
[zerooneloss]{acronym-label="zerooneloss"
acronym-form="singular+short"}., first=accuracy,text=accuracy

name=expert, description=[ml]{acronym-label="ml"
acronym-form="singular+short"} aims to learn a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hypothesis$ that accurately predicts the [label]{acronym-label="label"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
based on its [features]{acronym-label="feature"
acronym-form="plural+short"}. We measure the
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
error using some [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"}. Ideally, we want to find a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
that incurs minimal [loss]{acronym-label="loss"
acronym-form="singular+short"} on any
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}. We
can make this informal goal precise via the
[iidasspt]{acronym-label="iidasspt" acronym-form="singular+short"} and
by using the [bayesrisk]{acronym-label="bayesrisk"
acronym-form="singular+short"} as the
[baseline]{acronym-label="baseline" acronym-form="singular+short"} for
the (average) [loss]{acronym-label="loss" acronym-form="singular+short"}
of a [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}. An alternative approach to obtaining a
[baseline]{acronym-label="baseline" acronym-form="singular+short"} is to
use the [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\hypothesis'$ learned by an existing
[ml]{acronym-label="ml" acronym-form="singular+short"} method. We refer
to this [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\hypothesis'$ as an expert
[@PredictionLearningGames]. [regret]{acronym-label="regret"
acronym-form="singular+short"} minimization methods learn a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
that incurs a [loss]{acronym-label="loss" acronym-form="singular+short"}
comparable to the best expert [@PredictionLearningGames], [@HazanOCO].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[lossfunc]{acronym-label="lossfunc" acronym-form="singular+short"},
[loss]{acronym-label="loss" acronym-form="singular+short"},
[iidasspt]{acronym-label="iidasspt" acronym-form="singular+short"},
[bayesrisk]{acronym-label="bayesrisk" acronym-form="singular+short"},
[baseline]{acronym-label="baseline" acronym-form="singular+short"},
[regret]{acronym-label="regret" acronym-form="singular+short"}.,
first=expert,text=expert

name=networked federated learning (NFL), description=NFL refers to
methods that learn personalized [models]{acronym-label="model"
acronym-form="plural+short"} in a distributed fashion. These methods
learn from [localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} that are related by an intrinsic network
structure.\
See also: [model]{acronym-label="model" acronym-form="singular+short"},
[localdataset]{acronym-label="localdataset"
acronym-form="singular+short"}, [fl]{acronym-label="fl"
acronym-form="singular+short"}., first=networked federated learning
(NFL),text=NFL

name=regret, description=The regret of a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hypothesis$ relative to another
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hypothesis'$, which serves as a [baseline]{acronym-label="baseline"
acronym-form="singular+short"}, is the difference between the
[loss]{acronym-label="loss" acronym-form="singular+short"} incurred by
$\hypothesis$ and the [loss]{acronym-label="loss"
acronym-form="singular+short"} incurred by $\hypothesis'$
[@PredictionLearningGames]. The [baseline]{acronym-label="baseline"
acronym-form="singular+short"} [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\hypothesis'$ is also referred to as an
[expert]{acronym-label="expert" acronym-form="singular+short"}.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [baseline]{acronym-label="baseline"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [expert]{acronym-label="expert"
acronym-form="singular+short"}., first=regret,text=regret

name=strongly convex, description=A continuously
[differentiable]{acronym-label="differentiable"
acronym-form="singular+short"} real-valued function $f(\featurevec)$ is
strongly [convex]{acronym-label="convex" acronym-form="singular+short"}
with coefficient $\sigma$ if
$f({\bf y}) \geq f({\bf x}) + \nabla f({\bf x})^{T} ({\bf y} - {\bf x}) + (\sigma/2) \normgeneric{{\bf y} - {\bf x}}{2}^{2}$
[@nesterov04],[@CvxAlgBertsekas Sec. B.1.1].\
See also: [differentiable]{acronym-label="differentiable"
acronym-form="singular+short"}, [convex]{acronym-label="convex"
acronym-form="singular+short"}., first=strongly convex,text=strongly
convex

name=differentiable, description=A real-valued function
$f: \mathbb{R}^{d} \rightarrow \mathbb{R}$ is differentiable if it can,
at any point, be approximated locally by a linear function. The local
linear approximation at the point $\mathbf{x}$ is determined by the
[gradient]{acronym-label="gradient" acronym-form="singular+short"}
$\nabla f ( \mathbf{x})$ [@RudinBookPrinciplesMatheAnalysis].\
See also: [gradient]{acronym-label="gradient"
acronym-form="singular+short"}.,
first=differentiable,text=differentiable

name=gradient, plural=gradients, description=For a real-valued function
$f: \mathbb{R}^{d} \rightarrow \mathbb{R}: \vw \mapsto f(\vw)$, if a
vector ${\bf g}$ exists such that
$\lim_{\vw \rightarrow \vw'} \frac{f(\vw) - \big(f(\vw')+ {\bf g}^{T} (\vw- \vw') \big) }{\| \vw-\vw'\|}=0$,
it is referred to as the gradient of $f$ at $\vw'$. If it exists, the
gradient is unique and denoted $\nabla f(\vw')$ or
$\nabla f(\vw)\big|_{\vw'}$ [@RudinBookPrinciplesMatheAnalysis].,
first=gradient,text=gradient

name=subgradient, plural=subgradients, description=For a real-valued
function $f: \mathbb{R}^{d} \rightarrow \mathbb{R}: \vw \mapsto f(\vw)$,
a vector ${\bf a}$ such that
$f(\vw) \geq  f(\vw') +\big(\vw-\vw' \big)^{T} {\bf a}$ is referred to
as a subgradient of $f$ at $\vw'$ [@BertCvxAnalOpt],
[@BertsekasNonLinProgr]., first=subgradient,text=subgradient

name=FedProx, description=FedProx refers to an iterative
[fl]{acronym-label="fl" acronym-form="singular+short"}
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"}
that alternates between separately training
[localmodels]{acronym-label="localmodel" acronym-form="plural+short"}
and combining the updated local
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}. In contrast to
[fedavg]{acronym-label="fedavg" acronym-form="singular+short"}, which
uses [stochGD]{acronym-label="stochGD" acronym-form="singular+short"} to
train [localmodels]{acronym-label="localmodel"
acronym-form="plural+short"}, FedProx uses a
[proxop]{acronym-label="proxop" acronym-form="singular+short"} for the
training [@FedProx2020].\
See also: [fl]{acronym-label="fl" acronym-form="singular+short"},
[algorithm]{acronym-label="algorithm" acronym-form="singular+short"},
[localmodel]{acronym-label="localmodel" acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [fedavg]{acronym-label="fedavg"
acronym-form="singular+short"}, [stochGD]{acronym-label="stochGD"
acronym-form="singular+short"}, [proxop]{acronym-label="proxop"
acronym-form="singular+short"}., first = FedProx, text=FedProx

name=rectified linear unit (ReLU), description=The ReLU is a popular
choice for the [actfun]{acronym-label="actfun"
acronym-form="singular+short"} of a neuron within an
[ann]{acronym-label="ann" acronym-form="singular+short"}. It is defined
as $\sigma(z) = \max\{0,z\}$, with $z$ being the weighted input of the
artificial neuron.\
See also: [actfun]{acronym-label="actfun"
acronym-form="singular+short"}, [ann]{acronym-label="ann"
acronym-form="singular+short"}., first = rectified linear unit (ReLU),
text=ReLU

name=hypothesis, description=A hypothesis refers to a map (or function)
$\hypothesis: \mathcal{X} \rightarrow \mathcal{Y}$ from the
[featurespace]{acronym-label="featurespace"
acronym-form="singular+short"} $\mathcal{X}$ to the
[labelspace]{acronym-label="labelspace" acronym-form="singular+short"}
$\mathcal{Y}$. Given a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} with [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$, we use a hypothesis map
$\hypothesis$ to estimate (or approximate) the
[label]{acronym-label="label" acronym-form="singular+short"}
$\truelabel$ using the [prediction]{acronym-label="prediction"
acronym-form="singular+short"}
$\hat{\truelabel} = \hypothesis(\featurevec)$. [ml]{acronym-label="ml"
acronym-form="singular+short"} is all about learning (or finding) a
hypothesis map $\hypothesis$ such that
$\truelabel \approx \hypothesis(\featurevec)$ for any
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
(having [features]{acronym-label="feature" acronym-form="plural+short"}
$\featurevec$ and [label]{acronym-label="label"
acronym-form="singular+short"} $\truelabel$).\
See also: [featurespace]{acronym-label="featurespace"
acronym-form="singular+short"}, [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}., first=hypothesis,text=hypothesis

name=Vapnik--Chervonenkis dimension (VC dimension), description=The VC
dimension of an infinite [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"} is a widely-used measure for its size. We
refer to the literature (see [@ShalevMLBook]) for a precise definition
of VC dimension as well as a discussion of its basic properties and use
in [ml]{acronym-label="ml" acronym-form="singular+short"}.\
See also: [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}., first=Vapnik--Chervonenkis dimension
(VC dimension),text=VC dimension

name=effective dimension, description=The effective dimension
$\effdim{\mathcal{H}}$ of an infinite
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"}
$\mathcal{H}$ is a measure of its size. Loosely speaking, the effective
dimension is equal to the effective number of independent tunable
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}. These
[parameters]{acronym-label="parameters" acronym-form="singular+short"}
might be the coefficients used in a linear map or the
[weights]{acronym-label="weights" acronym-form="singular+short"} and
bias terms of an [ann]{acronym-label="ann"
acronym-form="singular+short"}.\
See also: [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [parameters]{acronym-label="parameters"
acronym-form="singular+short"}, [weights]{acronym-label="weights"
acronym-form="singular+short"}, [ann]{acronym-label="ann"
acronym-form="singular+short"}., first=effective
dimension,text=effective dimension

name=label space, description=Consider an [ml]{acronym-label="ml"
acronym-form="singular+short"} application that involves
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
characterized by [features]{acronym-label="feature"
acronym-form="plural+short"} and [labels]{acronym-label="label"
acronym-form="plural+short"}. The [label]{acronym-label="label"
acronym-form="singular+short"} space is constituted by all potential
values that the [label]{acronym-label="label"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} can
take on. [regression]{acronym-label="regression"
acronym-form="singular+short"} methods, aiming at predicting numeric
[labels]{acronym-label="label" acronym-form="plural+short"}, often use
the [label]{acronym-label="label" acronym-form="singular+short"} space
$\mathcal{Y} = \mathbb{R}$. Binary
[classification]{acronym-label="classification"
acronym-form="singular+short"} methods use a
[label]{acronym-label="label" acronym-form="singular+short"} space that
consists of two different elements, e.g., $\mathcal{Y} =\{-1,1\}$,
$\mathcal{Y}=\{0,1\}$, or
$\mathcal{Y} = \{ \mbox{``cat image''}, \mbox{``no cat image''} \}$.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[regression]{acronym-label="regression" acronym-form="singular+short"},
[classification]{acronym-label="classification"
acronym-form="singular+short"}., first=label space,text=label space

name=prediction, plural=predictions, description=A prediction is an
estimate or approximation for some quantity of interest.
[ml]{acronym-label="ml" acronym-form="singular+short"} revolves around
learning or finding a [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} map $\hypothesis$ that reads in the
[features]{acronym-label="feature" acronym-form="plural+short"}
$\featurevec$ of a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} and delivers a prediction
$\widehat{\truelabel} \defeq \hypothesis(\featurevec)$ for its
[label]{acronym-label="label" acronym-form="singular+short"}
$\truelabel$.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"}.,
first=prediction,text=prediction

name=histogram, description=

Consider a [dataset]{acronym-label="dataset"
acronym-form="singular+short"} $\dataset$ that consists of $m$
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
$\vz^{(1)},\ldots,\vz^{(m)}$, each of them belonging to some cell
$[-U,U] \times \ldots \times [-U,U] \subseteq \mathbb{R}^{d}$ with side
length $U$. We partition this cell evenly into smaller elementary cells
with side length $\Delta$. The histogram of $\dataset$ assigns each
elementary cell to the corresponding fraction of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} in
$\dataset$ that fall into this elementary cell. A visual example of such
a histogram is provided in
Fig. [11](#fig:histogram){reference-type="ref"
reference="fig:histogram"}.\

<figure id="fig:histogram">

<figcaption>A histogram representing the frequency of <span
data-acronym-label="datapoint"
data-acronym-form="plural+short">datapoints</span> falling within
discrete value ranges (i.e., bins). Each bar height shows the count of
<span data-acronym-label="sample"
data-acronym-form="plural+short">samples</span> in the corresponding
interval.</figcaption>
</figure>

See also: [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [sample]{acronym-label="sample"
acronym-form="singular+short"}.

, first=histogram,text=histogram

name=bootstrap, description=For the analysis of [ml]{acronym-label="ml"
acronym-form="singular+short"} methods, it is often useful to interpret
a given set of [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}
$\dataset = \big\{ \vz^{(1)},\ldots,\vz^{(m)}\big\}$ as
[realizations]{acronym-label="realization" acronym-form="plural+short"}
of [iid]{acronym-label="iid" acronym-form="singular+short"}
[rvs]{acronym-label="rv" acronym-form="plural+short"} with a common
[probdist]{acronym-label="probdist" acronym-form="singular+short"}
$p(\vz)$. In general, we do not know $p(\vz)$ exactly, but we need to
estimate it. The bootstrap uses the
[histogram]{acronym-label="histogram" acronym-form="singular+short"} of
$\dataset$ as an estimator for the underlying
[probdist]{acronym-label="probdist" acronym-form="singular+short"}
$p(\vz)$.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[realization]{acronym-label="realization"
acronym-form="singular+short"}, [iid]{acronym-label="iid"
acronym-form="singular+short"}, [rv]{acronym-label="rv"
acronym-form="singular+short"}, [probdist]{acronym-label="probdist"
acronym-form="singular+short"}, [histogram]{acronym-label="histogram"
acronym-form="singular+short"}. , first=bootstrap,text=bootstrap

name=feature space, description= The [feature]{acronym-label="feature"
acronym-form="singular+short"} space of a given [ml]{acronym-label="ml"
acronym-form="singular+short"} application or method is constituted by
all potential values that the [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} can
take on. A widely used choice for the [feature]{acronym-label="feature"
acronym-form="singular+short"} space is the
[euclidspace]{acronym-label="euclidspace" acronym-form="singular+short"}
$\mathbb{R}^{d}$, with the dimension $\featuredim$ being the number of
individual [features]{acronym-label="feature"
acronym-form="plural+short"} of a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}.\
See also: [feature]{acronym-label="feature"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"},
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}., first=feature space,text=feature space

name=missing data, description=Consider a
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
constituted by [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} collected via some physical
[device]{acronym-label="device" acronym-form="singular+short"}. Due to
imperfections and failures, some of the
[feature]{acronym-label="feature" acronym-form="singular+short"} or
[label]{acronym-label="label" acronym-form="singular+short"} values of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
might be corrupted or simply missing. [data]{acronym-label="data"
acronym-form="singular+short"} imputation aims at estimating these
missing values [@Abayomi2008DiagnosticsFM]. We can interpret
[data]{acronym-label="data" acronym-form="singular+short"} imputation as
an [ml]{acronym-label="ml" acronym-form="singular+short"} problem where
the [label]{acronym-label="label" acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} is
the value of the corrupted [feature]{acronym-label="feature"
acronym-form="singular+short"}.\
See also: [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [device]{acronym-label="device"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}. , first=missing data,text=missing data

name=positive semi-definite (psd), description= A (real-valued)
symmetric matrix
$\mathbf{Q} = \mathbf{Q}^{T} \in \mathbb{R}^{d \times d}$ is referred to
as psd if $\featurevec^{T} \mathbf{Q} \featurevec \geq 0$ for every
vector $\featurevec \in \mathbb{R}^{d}$. The property of being psd can
be extended from matrices to (real-valued) symmetric
[kernel]{acronym-label="kernel" acronym-form="singular+short"} maps
$K: \mathcal{X} \times \mathcal{X} \rightarrow \mathbb{R}$ (with
$K(\featurevec,\featurevec') = K(\featurevec',\featurevec)$) as follows:
For any finite set of [featurevecs]{acronym-label="featurevec"
acronym-form="plural+short"}
$\featurevec^{(1)},\dots,\featurevec^{(m)}$, the resulting matrix
$\mathbf{Q} \in \mathbb{R}^{m \times m}$ with entries
$Q_{r,r'} = \kernelmap{\featurevec^{(r)}}{\featurevec^{(r')}}$ is psd
[@LearningKernelsBook].\
See also: [kernel]{acronym-label="kernel"
acronym-form="singular+short"}, [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"}., first=positive semi-definite
(psd),text=psd

name=feature, plural=features, description=A feature of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} is
one of its properties that can be measured or computed easily without
the need for human supervision. For example, if a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} is
a digital image (e.g., stored as a `.jpeg` file), then we could use the
red-green-blue intensities of its pixels as features. Domain-specific
synonyms for the term feature are \"covariate,\" \"explanatory
variable,\" \"independent variable,\" \"input (variable),\" \"predictor
(variable),\" or \"regressor\" [@Gujarati2021], [@Dodge2003],
[@Everitt2022].\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. , first=feature, text=feature

name=feature vector, plural=feature vectors,
description=[feature]{acronym-label="feature"
acronym-form="singular+short"} vector refers to a vector
${\bf x} = \big(x_{1},\ldots,x_{\featuredim}\big)^{T}$ whose entries are
individual [features]{acronym-label="feature"
acronym-form="plural+short"} $x_{1},\ldots,x_{\featuredim}$. Many
[ml]{acronym-label="ml" acronym-form="singular+short"} methods use
[feature]{acronym-label="feature" acronym-form="singular+short"} vectors
that belong to some finite-dimensional
[euclidspace]{acronym-label="euclidspace" acronym-form="singular+short"}
$\mathbb{R}^{\featuredim}$. For some [ml]{acronym-label="ml"
acronym-form="singular+short"} methods, however, it can be more
convenient to work with [feature]{acronym-label="feature"
acronym-form="singular+short"} vectors that belong to an
infinite-dimensional vector space (e.g., see
[kernelmethod]{acronym-label="kernelmethod"
acronym-form="singular+short"}).\
See also: [feature]{acronym-label="feature"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"},
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"},
[kernelmethod]{acronym-label="kernelmethod"
acronym-form="singular+short"}. , first=feature vector,text=feature
vector

name=label, plural=labels, description=A higher-level fact or quantity
of interest associated with a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. For example, if the
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} is
an image, the label could indicate whether the image contains a cat or
not. Synonyms for label, commonly used in specific domains, include
\"response variable,\" \"output variable,\" and \"target\"
[@Gujarati2021], [@Dodge2003], [@Everitt2022].\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. , first=label,text=label

name=data, description=Data refers to objects that carry information.
These objects can be either concrete physical objects (such as persons
or animals) or abstract concepts (such as numbers). We often use
representations (or approximations) of the original data that are more
convenient for data processing. These approximations are based on
different data [models]{acronym-label="model"
acronym-form="plural+short"}, with the relational data
[model]{acronym-label="model" acronym-form="singular+short"} being one
of the most widely used [@codd1970relational].\
See also: [model]{acronym-label="model" acronym-form="singular+short"}.,
text=data

name=dataset, plural=datasets, description=

A dataset refers to a collection of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}.
These [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} carry information about some quantity of
interest (or [label]{acronym-label="label"
acronym-form="singular+short"}) within an [ml]{acronym-label="ml"
acronym-form="singular+short"} application. [ml]{acronym-label="ml"
acronym-form="singular+short"} methods use datasets for
[model]{acronym-label="model" acronym-form="singular+short"} training
(e.g., via [erm]{acronym-label="erm" acronym-form="singular+short"}) and
[model]{acronym-label="model" acronym-form="singular+short"}
[validation]{acronym-label="validation" acronym-form="singular+short"}.
Note that our notion of a dataset is very flexible, as it allows for
very different types of [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}. Indeed,
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} can
be concrete physical objects (such as humans or animals) or abstract
objects (such as numbers). As a case in point,
Fig. [12](#fig_cows_dataset){reference-type="ref"
reference="fig_cows_dataset"} depicts a dataset that consists of cows as
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}.

<figure id="fig_cows_dataset">
<div class="center">
<p><span id="fig:cowsintheswissalps"
data-label="fig:cowsintheswissalps"></span> <img
src="assets/Cows_in_the_Swiss_Alps.jpg" style="width:50.0%"
alt="image" /></p>
</div>
<figcaption><span id="fig_cows_dataset"
data-label="fig_cows_dataset"></span>“Cows in the Swiss Alps” by
User:Huhu Uet is licensed under [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0/)</figcaption>
</figure>

Quite often, an [ml]{acronym-label="ml" acronym-form="singular+short"}
engineer does not have direct access to a dataset. Indeed, accessing the
dataset in Fig. [12](#fig_cows_dataset){reference-type="ref"
reference="fig_cows_dataset"} would require us to visit the cow herd in
the Alps. Instead, we need to use an approximation (or representation)
of the dataset which is more convenient to work with. Different
mathematical [models]{acronym-label="model" acronym-form="plural+short"}
have been developed for the representation (or approximation) of
datasets [@silberschatz2019database], [@abiteboul1995foundations],
[@hoberman2009data], [@ramakrishnan2002database]. One of the most widely
adopted data [model]{acronym-label="model"
acronym-form="singular+short"} is the relational
[model]{acronym-label="model" acronym-form="singular+short"}, which
organizes [data]{acronym-label="data" acronym-form="singular+short"} as
a table (or relation) [@codd1970relational],
[@silberschatz2019database]. A table consists of rows and columns:

- Each row of the table represents a single
  [datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.

- Each column of the table corresponds to a specific attribute of the
  [datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.
  [ml]{acronym-label="ml" acronym-form="singular+short"} methods can use
  attributes as [features]{acronym-label="feature"
  acronym-form="plural+short"} and [labels]{acronym-label="label"
  acronym-form="plural+short"} of the
  [datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.

For example, Table [1](#tab:cowdata){reference-type="ref"
reference="tab:cowdata"} shows a representation of the dataset in
Fig. [12](#fig_cows_dataset){reference-type="ref"
reference="fig_cows_dataset"}. In the relational
[model]{acronym-label="model" acronym-form="singular+short"}, the order
of rows is irrelevant, and each attribute (i.e., column) must be
precisely defined with a domain, which specifies the set of possible
values. In [ml]{acronym-label="ml" acronym-form="singular+short"}
applications, these attribute domains become the
[featurespace]{acronym-label="featurespace"
acronym-form="singular+short"} and the
[labelspace]{acronym-label="labelspace" acronym-form="singular+short"}.

::: {#tab:cowdata}
  **Name**    **Weight**   **Age**   **Height**   **Stomach temperature**
  ---------- ------------ --------- ------------ -------------------------
  Zenzi          100          4         100                 25
  Berta          140          3         130                 23
  Resi           120          4         120                 31

  : A relation (or table) that represents the dataset in
  Fig. [12](#fig_cows_dataset){reference-type="ref"
  reference="fig_cows_dataset"}.
:::

While the relational [model]{acronym-label="model"
acronym-form="singular+short"} is useful for the study of many
[ml]{acronym-label="ml" acronym-form="singular+short"} applications, it
may be insufficient regarding the requirements for
[trustAI]{acronym-label="trustAI" acronym-form="singular+short"}. Modern
approaches like datasheets for datasets provide more comprehensive
documentation, including details about the dataset's collection process,
intended use, and other contextual information [@DatasheetData2021].\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [validation]{acronym-label="validation"
acronym-form="singular+short"}, [data]{acronym-label="data"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"},
[featurespace]{acronym-label="featurespace"
acronym-form="singular+short"}, [labelspace]{acronym-label="labelspace"
acronym-form="singular+short"}, [trustAI]{acronym-label="trustAI"
acronym-form="singular+short"}.

,first=dataset,text=dataset

name=predictor, description=A predictor is a real-valued
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
map. Given a [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"} with [features]{acronym-label="feature"
acronym-form="plural+short"} $\featurevec$, the value
$\hypothesis(\featurevec) \in \mathbb{R}$ is used as a
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
for the true numeric [label]{acronym-label="label"
acronym-form="singular+short"} $\truelabel \in \mathbb{R}$ of the
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [feature]{acronym-label="feature"
acronym-form="singular+short"}, [prediction]{acronym-label="prediction"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}. ,first=predictor,text=predictor

name=labeled datapoint, plural=labeled datapoints, description=A
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"}
whose [label]{acronym-label="label" acronym-form="singular+short"} is
known or has been determined by some means which might require human
labor.\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [label]{acronym-label="label"
acronym-form="singular+short"}., first=labeled datapoint,text=labeled
datapoint

name=random variable (RV), plural=RVs, description=

An RV is a function that maps from a
[probspace]{acronym-label="probspace" acronym-form="singular+short"}
$\mathcal{P}$ to a value space [@GrayProbBook],
[@BillingsleyProbMeasure]. The [probspace]{acronym-label="probspace"
acronym-form="singular+short"} consists of elementary events and is
equipped with a [probability]{acronym-label="probability"
acronym-form="singular+short"} measure that assigns probabilities to
subsets of $\mathcal{P}$. Different types of RVs include

- binary RVs, which map each elementary event to an element of a binary
  set (e.g., $\{-1,1\}$ or $\{\text{cat}, \text{no cat}\}$;

- real-valued RVs, which take values in the real numbers $\mathbb{R}$;

- vector-valued RVs, which map elementary events to the
  [euclidspace]{acronym-label="euclidspace"
  acronym-form="singular+short"} $\mathbb{R}^{d}$.

[probability]{acronym-label="probability" acronym-form="singular+short"}
theory uses the concept of measurable spaces to rigorously define and
study the properties of (large) collections of RVs
[@BillingsleyProbMeasure].\
See also: [probspace]{acronym-label="probspace"
acronym-form="singular+short"},
[probability]{acronym-label="probability"
acronym-form="singular+short"},
[euclidspace]{acronym-label="euclidspace"
acronym-form="singular+short"}.

, first=random variable (RV),text=RV

name=realization, plural=realizations, description=Consider an
[rv]{acronym-label="rv" acronym-form="singular+short"} $x$ which maps
each element (i.e., outcome or elementary event)
$\omega \in \mathcal{P}$ of a [probspace]{acronym-label="probspace"
acronym-form="singular+short"} $\mathcal{P}$ to an element $a$ of a
measurable space $\mathcal{N}$ [@RudinBookPrinciplesMatheAnalysis],
[@HalmosMeasure], [@BillingsleyProbMeasure]. A realization of $x$ is any
element $a' \in \mathcal{N}$ such that there is an element
$\omega' \in \mathcal{P}$ with $x(\omega') = a'$.\
See also: [rv]{acronym-label="rv" acronym-form="singular+short"},
[probspace]{acronym-label="probspace" acronym-form="singular+short"}.,
first=realization,text=realization

name=training set, plural=training sets, description=A training set is a
[dataset]{acronym-label="dataset" acronym-form="singular+short"}
$\dataset$ which consists of some [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} used in [erm]{acronym-label="erm"
acronym-form="singular+short"} to learn a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hat{\hypothesis}$. The average [loss]{acronym-label="loss"
acronym-form="singular+short"} of $\hat{\hypothesis}$ on the training
set is referred to as the [trainerr]{acronym-label="trainerr"
acronym-form="singular+short"}. The comparison of the
[trainerr]{acronym-label="trainerr" acronym-form="singular+short"} with
the [valerr]{acronym-label="valerr" acronym-form="singular+short"} of
$\hat{\hypothesis}$ allows us to diagnose the [ml]{acronym-label="ml"
acronym-form="singular+short"} method and informs how to improve the
validation error (e.g., using a different
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"} or
collecting more [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"}) [@MLBasics Sec. 6.6].\
See also: [dataset]{acronym-label="dataset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [trainerr]{acronym-label="trainerr"
acronym-form="singular+short"}, [valerr]{acronym-label="valerr"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"}.,first=training set,text=training set

name=networked model, description=A networked
[model]{acronym-label="model" acronym-form="singular+short"} over an
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"}
$\mathcal{G} = \pair{\mathcal{V}}{\mathcal{E}}$ assigns a
[localmodel]{acronym-label="localmodel" acronym-form="singular+short"}
(i.e., a [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"}) to each node $i \in \mathcal{V}$ of the
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"}
$\mathcal{G}$.\
See also: [model]{acronym-label="model" acronym-form="singular+short"},
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"},
[localmodel]{acronym-label="localmodel" acronym-form="singular+short"},
[hypospace]{acronym-label="hypospace" acronym-form="singular+short"}.,
first=networked model,text=networked model

name=batch, description=In the context of
[stochGD]{acronym-label="stochGD" acronym-form="singular+short"}, a
batch refers to a randomly chosen subset of the overall
[trainset]{acronym-label="trainset" acronym-form="singular+short"}. We
use the [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} in this subset to estimate the
[gradient]{acronym-label="gradient" acronym-form="singular+short"} of
[trainerr]{acronym-label="trainerr" acronym-form="singular+short"} and,
in turn, to update the [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}.\
See also: [stochGD]{acronym-label="stochGD"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [gradient]{acronym-label="gradient"
acronym-form="singular+short"}, [trainerr]{acronym-label="trainerr"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}., first=batch,text=batch

name=networked data, description=Networked [data]{acronym-label="data"
acronym-form="singular+short"} consists of
[localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} that are related by some notion of pairwise
similarity. We can represent networked [data]{acronym-label="data"
acronym-form="singular+short"} using a [graph]{acronym-label="graph"
acronym-form="singular+short"} whose nodes carry
[localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} and edges encode pairwise similarities. One
example of networked [data]{acronym-label="data"
acronym-form="singular+short"} arises in [fl]{acronym-label="fl"
acronym-form="singular+short"} applications where
[localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} are generated by spatially distributed
[devices]{acronym-label="device" acronym-form="plural+short"}.\
See also: [data]{acronym-label="data" acronym-form="singular+short"},
[localdataset]{acronym-label="localdataset"
acronym-form="singular+short"}, [graph]{acronym-label="graph"
acronym-form="singular+short"}, [fl]{acronym-label="fl"
acronym-form="singular+short"}, [device]{acronym-label="device"
acronym-form="singular+short"}., first=networked data,text=networked
data

name=training error, description=The average [loss]{acronym-label="loss"
acronym-form="singular+short"} of a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
when predicting the [labels]{acronym-label="label"
acronym-form="plural+short"} of the
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} in a
[trainset]{acronym-label="trainset" acronym-form="singular+short"}. We
sometimes refer by training error also to minimal average
[loss]{acronym-label="loss" acronym-form="singular+short"} which is
achieved by a solution of [erm]{acronym-label="erm"
acronym-form="singular+short"}.\
See also: [loss]{acronym-label="loss" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[trainset]{acronym-label="trainset" acronym-form="singular+short"},
[erm]{acronym-label="erm" acronym-form="singular+short"}.,first=training
error,text=training error

name=data point, plural=data points, description=A
[data]{acronym-label="data" acronym-form="singular+short"} point is any
object that conveys information [@coverthomas].
[data]{acronym-label="data" acronym-form="singular+short"} points might
be students, radio signals, trees, forests, images,
[rvs]{acronym-label="rv" acronym-form="plural+short"}, real numbers, or
proteins. We characterize [data]{acronym-label="data"
acronym-form="singular+short"} points using two types of properties. One
type of property is referred to as a [feature]{acronym-label="feature"
acronym-form="singular+short"}. [features]{acronym-label="feature"
acronym-form="plural+short"} are properties of a
[data]{acronym-label="data" acronym-form="singular+short"} point that
can be measured or computed in an automated fashion. A different kind of
property is referred to as a [label]{acronym-label="label"
acronym-form="singular+short"}. The [label]{acronym-label="label"
acronym-form="singular+short"} of a [data]{acronym-label="data"
acronym-form="singular+short"} point represents some higher-level fact
(or quantity of interest). In contrast to
[features]{acronym-label="feature" acronym-form="plural+short"},
determining the [label]{acronym-label="label"
acronym-form="singular+short"} of a [data]{acronym-label="data"
acronym-form="singular+short"} point typically requires human experts
(or domain experts). Roughly speaking, [ml]{acronym-label="ml"
acronym-form="singular+short"} aims to predict the
[label]{acronym-label="label" acronym-form="singular+short"} of a
[data]{acronym-label="data" acronym-form="singular+short"} point based
solely on its [features]{acronym-label="feature"
acronym-form="plural+short"}.\
See also: [data]{acronym-label="data" acronym-form="singular+short"},
[rv]{acronym-label="rv" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[ml]{acronym-label="ml" acronym-form="singular+short"}. , first=data
point,text=data point

name=validation error, plural=validation errors, description=Consider a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hat{\hypothesis}$ which is obtained by some [ml]{acronym-label="ml"
acronym-form="singular+short"} method, e.g., using
[erm]{acronym-label="erm" acronym-form="singular+short"} on a
[trainset]{acronym-label="trainset" acronym-form="singular+short"}. The
average [loss]{acronym-label="loss" acronym-form="singular+short"} of
$\hat{\hypothesis}$ on a [valset]{acronym-label="valset"
acronym-form="singular+short"}, which is different from the
[trainset]{acronym-label="trainset" acronym-form="singular+short"}, is
referred to as the [validation]{acronym-label="validation"
acronym-form="singular+short"} error.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [valset]{acronym-label="valset"
acronym-form="singular+short"}, [validation]{acronym-label="validation"
acronym-form="singular+short"}.,first=validation error,text=validation
error

name=validation, description=Consider a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hat{\hypothesis}$ that has been learned via some
[ml]{acronym-label="ml" acronym-form="singular+short"} method, e.g., by
solving [erm]{acronym-label="erm" acronym-form="singular+short"} on a
[trainset]{acronym-label="trainset" acronym-form="singular+short"}
$\dataset$. Validation refers to the practice of evaluating the
[loss]{acronym-label="loss" acronym-form="singular+short"} incurred by
the [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} $\hat{\hypothesis}$ on a set of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} that
are not contained in the [trainset]{acronym-label="trainset"
acronym-form="singular+short"} $\dataset$.\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}. ,first=validation,text=validation

name=quadratic function, description=A function
$f: \mathbb{R}^{\featuredim} \rightarrow \mathbb{R}$ of the form
$$f(\vw) =  \vw^{T} \mathbf{Q} \mathbf{w} + \mathbf{q}^{T} \vw+a,$$ with
some matrix
$\mathbf{Q} \in \mathbb{R}^{\featuredim \times \featuredim}$, vector
${\bf q} \in \mathbb{R}^{\featuredim}$, and scalar $a \in \mathbb{R}$.
,first=quadratic function,text=quadratic function

name=validation set, description=A set of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} used
to estimate the [risk]{acronym-label="risk"
acronym-form="singular+short"} of a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
$\hat{\hypothesis}$ that has been learned by some
[ml]{acronym-label="ml" acronym-form="singular+short"} method (e.g.,
solving [erm]{acronym-label="erm" acronym-form="singular+short"}). The
average [loss]{acronym-label="loss" acronym-form="singular+short"} of
$\hat{\hypothesis}$ on the [validation]{acronym-label="validation"
acronym-form="singular+short"} set is referred to as the
[valerr]{acronym-label="valerr" acronym-form="singular+short"} and can
be used to diagnose an [ml]{acronym-label="ml"
acronym-form="singular+short"} method (see [@MLBasics Sec. 6.6]). The
comparison between [trainerr]{acronym-label="trainerr"
acronym-form="singular+short"} and [valerr]{acronym-label="valerr"
acronym-form="singular+short"} can inform directions for improvement of
the [ml]{acronym-label="ml" acronym-form="singular+short"} method (such
as using a different [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"}).\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [risk]{acronym-label="risk"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}, [ml]{acronym-label="ml"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [validation]{acronym-label="validation"
acronym-form="singular+short"}, [valerr]{acronym-label="valerr"
acronym-form="singular+short"}, [trainerr]{acronym-label="trainerr"
acronym-form="singular+short"}, [hypospace]{acronym-label="hypospace"
acronym-form="singular+short"}.,first=validation set,text=validation set

name=test set, description=A set of
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"} that
have been used neither to train a [model]{acronym-label="model"
acronym-form="singular+short"} (e.g., via [erm]{acronym-label="erm"
acronym-form="singular+short"}) nor in a [valset]{acronym-label="valset"
acronym-form="singular+short"} to choose between different
[models]{acronym-label="model" acronym-form="plural+short"}.\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [valset]{acronym-label="valset"
acronym-form="singular+short"}.,first=test set,text=test set

name=model selection, description=In [ml]{acronym-label="ml"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"} selection refers to the process of
choosing between different candidate [models]{acronym-label="model"
acronym-form="plural+short"}. In its most basic form,
[model]{acronym-label="model" acronym-form="singular+short"} selection
amounts to: 1) training each candidate [model]{acronym-label="model"
acronym-form="singular+short"}; 2) computing the
[valerr]{acronym-label="valerr" acronym-form="singular+short"} for each
trained [model]{acronym-label="model" acronym-form="singular+short"};
and 3) choosing the [model]{acronym-label="model"
acronym-form="singular+short"} with the smallest
[valerr]{acronym-label="valerr" acronym-form="singular+short"}
[@MLBasics Ch. 6].\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[valerr]{acronym-label="valerr"
acronym-form="singular+short"}.,first=model selection,text=model
selection

name = generalization gap, description=The difference between the
performance of a trained [model]{acronym-label="model"
acronym-form="singular+short"} on the
[trainset]{acronym-label="trainset" acronym-form="singular+short"} and
other [datapoints]{acronym-label="datapoint"
acronym-form="plural+short"} (such as those in a
[valset]{acronym-label="valset" acronym-form="singular+short"}).\
See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"},
[decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"},
[generalization]{acronym-label="generalization"
acronym-form="singular+short"}, [gdmethods]{acronym-label="gdmethods"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [models]{acronym-label="model"
acronym-form="plural+short"}, [smooth]{acronym-label="smooth"
acronym-form="singular+short"}, [lossfuncs]{acronym-label="lossfunc"
acronym-form="plural+short"}, [gd]{acronym-label="gd"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [emprisk]{acronym-label="emprisk"
acronym-form="singular+short"}, [gradient]{acronym-label="gradient"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}. , first=generalization gap,
text=generalization gap

name = concentration inequality, description=The tendency of a
[rv]{acronym-label="rv" acronym-form="singular+short"} to be close to
its [expectation]{acronym-label="expectation"
acronym-form="singular+short"} with high
[probability]{acronym-label="probability" acronym-form="singular+short"}
[@Wain2019]. , first=concentration inequality, plural=concentration
inequalities, text=concentration inequality

name = boosting, description=

Boosting is an iterative optimization method to learn an accurate
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
map (or strong learner) by sequentially combining less accurate
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
maps (referred to as weak learners) [@hastie01statisticallearning Ch.
10]. For example, weak learners are shallow
[decisiontrees]{acronym-label="decisiontree"
acronym-form="plural+short"} which are combined to obtain a deep
[decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"}. Boosting can be understood as a
[generalization]{acronym-label="generalization"
acronym-form="singular+short"} of [gdmethods]{acronym-label="gdmethods"
acronym-form="singular+short"} for [erm]{acronym-label="erm"
acronym-form="singular+short"} using parametric
[models]{acronym-label="model" acronym-form="plural+short"} and
[smooth]{acronym-label="smooth" acronym-form="singular+short"}
[lossfuncs]{acronym-label="lossfunc" acronym-form="plural+short"}
[@Friedman2001]. Just like [gd]{acronym-label="gd"
acronym-form="singular+short"} iteratively updates
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
to reduce the [emprisk]{acronym-label="emprisk"
acronym-form="singular+short"}, boosting iteratively combines (e.g., by
summation) [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} maps to reduce the
[emprisk]{acronym-label="emprisk" acronym-form="singular+short"}. A
widely-used instance of the generic boosting idea is referred to as
[gradient]{acronym-label="gradient" acronym-form="singular+short"}
boosting, which uses [gradients]{acronym-label="gradient"
acronym-form="plural+short"} of the [lossfunc]{acronym-label="lossfunc"
acronym-form="singular+short"} for combining the weak learners
[@Friedman2001].

<figure>
<div class="center">

</div>
<figcaption>Boosting methods construct a sequence of <span
data-acronym-label="hypothesis"
data-acronym-form="singular+short">hypothesis</span> maps <span
class="math inline">$\hypothesis^{(0)},\hypothesis^{(1)},\ldots$</span>
that are increasingly strong learners (i.e., incurring a smaller <span
data-acronym-label="loss"
data-acronym-form="singular+short">loss</span>).</figcaption>
</figure>

See also: [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"},
[decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"},
[generalization]{acronym-label="generalization"
acronym-form="singular+short"}, [gdmethods]{acronym-label="gdmethods"
acronym-form="singular+short"}, [erm]{acronym-label="erm"
acronym-form="singular+short"}, [models]{acronym-label="model"
acronym-form="plural+short"}, [smooth]{acronym-label="smooth"
acronym-form="singular+short"}, [lossfuncs]{acronym-label="lossfunc"
acronym-form="plural+short"}, [gd]{acronym-label="gd"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [emprisk]{acronym-label="emprisk"
acronym-form="singular+short"}, [gradient]{acronym-label="gradient"
acronym-form="singular+short"}, [loss]{acronym-label="loss"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}.

, first=boosting, text=boosting

name=generalized total variation (GTV), description=GTV is a measure of
the variation of trained [localmodels]{acronym-label="localmodel"
acronym-form="plural+short"} $\localhypothesis{i}$ (or their
[modelparams]{acronym-label="modelparams" acronym-form="singular+short"}
$\mathbf{w}^{(i)}$) assigned to the nodes $i=1,\ldots,n$ of an
undirected weighted [graph]{acronym-label="graph"
acronym-form="singular+short"} $\mathcal{G}$ with edges $\mathcal{E}$.
Given a measure $\discrepancy{\hypothesis}{\hypothesis'}$ for the
[discrepancy]{acronym-label="discrepancy" acronym-form="singular+short"}
between [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} maps $\hypothesis,\hypothesis'$, the GTV
is $$\nonumber
            \sum_{\{i,i'\}\in \mathcal{E}} \edgeweight_{i,i'} 
            \discrepancy{\localhypothesis{i}}{\localhypothesis{i'}}.$$
Here, $\edgeweight_{i,i'}>0$ denotes the weight of the undirected edge
$\{i,i'\}\in \mathcal{E}$.\
See also: [localmodel]{acronym-label="localmodel"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}, [graph]{acronym-label="graph"
acronym-form="singular+short"},
[discrepancy]{acronym-label="discrepancy"
acronym-form="singular+short"}, [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}. , first=GTV, text=GTV

name=clustered federated learning (CFL), description=CFL trains
[localmodels]{acronym-label="localmodel" acronym-form="plural+short"}
for the [devices]{acronym-label="device" acronym-form="plural+short"} in
a [fl]{acronym-label="fl" acronym-form="singular+short"} application by
using a [clustasspt]{acronym-label="clustasspt"
acronym-form="singular+short"}, i.e., the
[devices]{acronym-label="device" acronym-form="plural+short"} of an
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"} form
[clusters]{acronym-label="cluster" acronym-form="plural+short"}. Two
[devices]{acronym-label="device" acronym-form="plural+short"} in the
same [cluster]{acronym-label="cluster" acronym-form="singular+short"}
generate [localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} with similar statistical properties. CFL
pools the [localdatasets]{acronym-label="localdataset"
acronym-form="plural+short"} of [devices]{acronym-label="device"
acronym-form="plural+short"} in the same
[cluster]{acronym-label="cluster" acronym-form="singular+short"} to
obtain a [trainset]{acronym-label="trainset"
acronym-form="singular+short"} for a [cluster]{acronym-label="cluster"
acronym-form="singular+short"}-specific [model]{acronym-label="model"
acronym-form="singular+short"}. [gtvmin]{acronym-label="gtvmin"
acronym-form="singular+short"} clusters [devices]{acronym-label="device"
acronym-form="plural+short"} implicitly by enforcing approximate
similarity of [modelparams]{acronym-label="modelparams"
acronym-form="singular+short"} across well-connected nodes of the
[empgraph]{acronym-label="empgraph" acronym-form="singular+short"}.\
See also: [localmodel]{acronym-label="localmodel"
acronym-form="singular+short"}, [device]{acronym-label="device"
acronym-form="singular+short"}, [fl]{acronym-label="fl"
acronym-form="singular+short"}, [clustasspt]{acronym-label="clustasspt"
acronym-form="singular+short"}, [empgraph]{acronym-label="empgraph"
acronym-form="singular+short"}, [cluster]{acronym-label="cluster"
acronym-form="singular+short"},
[localdataset]{acronym-label="localdataset"
acronym-form="singular+short"}, [trainset]{acronym-label="trainset"
acronym-form="singular+short"}, [model]{acronym-label="model"
acronym-form="singular+short"}, [gtvmin]{acronym-label="gtvmin"
acronym-form="singular+short"},
[modelparams]{acronym-label="modelparams"
acronym-form="singular+short"}., first=clustered federated learning
(CFL), text=CFL

name=application programming interface (API), description=

An API is a formal mechanism that allows software components to interact
in a structured and modular way [@RestfulBook2013]. In the context of
[ml]{acronym-label="ml" acronym-form="singular+short"}, APIs are
commonly used to provide access to a trained [ml]{acronym-label="ml"
acronym-form="singular+short"} [model]{acronym-label="model"
acronym-form="singular+short"}. Users---whether humans or machines---can
submit the [featurevec]{acronym-label="featurevec"
acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} and
receive a corresponding [prediction]{acronym-label="prediction"
acronym-form="singular+short"}. Suppose a trained
[ml]{acronym-label="ml" acronym-form="singular+short"}
[model]{acronym-label="model" acronym-form="singular+short"} is defined
as $\widehat{\hypothesis}(\feature) \defeq 2 \feature + 1$. Through an
API, a user can input $\feature = 3$ and receive the output
$\widehat{\hypothesis}(3) = 7$ without knowledge of the detailed
structure of the [ml]{acronym-label="ml" acronym-form="singular+short"}
[model]{acronym-label="model" acronym-form="singular+short"} or its
training. In practice, the [model]{acronym-label="model"
acronym-form="singular+short"} is typically deployed on a server
connected to the internet. Clients send requests containing
[feature]{acronym-label="feature" acronym-form="singular+short"} values
to the server, which responds with the computed
[prediction]{acronym-label="prediction" acronym-form="singular+short"}
$\widehat{\hypothesis}(\featurevec)$. APIs promote modularity in
[ml]{acronym-label="ml" acronym-form="singular+short"} system design,
i.e., one team can develop and train the model, while another team
handles integration and user interaction. Publishing a trained
[model]{acronym-label="model" acronym-form="singular+short"} via an API
also offers practical advantages:

- The server can centralize computational resources which are required
  to compute [predictions]{acronym-label="prediction"
  acronym-form="plural+short"}.

- The internal structure of the [model]{acronym-label="model"
  acronym-form="singular+short"} remains hidden (which is useful for
  protecting IP or trade secrets).

However, APIs are not without [risk]{acronym-label="risk"
acronym-form="singular+short"}. Techniques such as
[modelinversion]{acronym-label="modelinversion"
acronym-form="singular+short"} can potentially reconstruct a
[model]{acronym-label="model" acronym-form="singular+short"} from its
[predictions]{acronym-label="prediction" acronym-form="plural+short"} on
carefully selected [featurevecs]{acronym-label="featurevec"
acronym-form="plural+short"}.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[model]{acronym-label="model" acronym-form="singular+short"},
[featurevec]{acronym-label="featurevec" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[feature]{acronym-label="feature" acronym-form="singular+short"},
[modelinversion]{acronym-label="modelinversion"
acronym-form="singular+short"}.

, first=application programming interface (API), text=API

name=sample size, description=The number of individual
[datapoints]{acronym-label="datapoint" acronym-form="plural+short"}
contained in a [dataset]{acronym-label="dataset"
acronym-form="singular+short"}.\
See also: [datapoint]{acronym-label="datapoint"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}.,first=sample size,text=sample size

name=random forest, description=A random forest is a set of different
[decisiontrees]{acronym-label="decisiontree"
acronym-form="plural+short"}. Each of these
[decisiontrees]{acronym-label="decisiontree"
acronym-form="plural+short"} is obtained by fitting a perturbed copy of
the original [dataset]{acronym-label="dataset"
acronym-form="singular+short"}.\
See also: [decisiontree]{acronym-label="decisiontree"
acronym-form="singular+short"}, [dataset]{acronym-label="dataset"
acronym-form="singular+short"}.,first = random forest, text=random
forest

name=bagging (or bootstrap aggregation), description=Bagging (or
bootstrap aggregation) is a generic technique to improve (the robustness
of) a given [ml]{acronym-label="ml" acronym-form="singular+short"}
method. The idea is to use the [bootstrap]{acronym-label="bootstrap"
acronym-form="singular+short"} to generate perturbed copies of a given
[dataset]{acronym-label="dataset" acronym-form="singular+short"} and
then to learn a separate [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"} for each copy. We then predict the
[label]{acronym-label="label" acronym-form="singular+short"} of a
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"} by
combining or aggregating the individual
[predictions]{acronym-label="prediction" acronym-form="plural+short"} of
each separate [hypothesis]{acronym-label="hypothesis"
acronym-form="singular+short"}. For
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
maps delivering numeric [label]{acronym-label="label"
acronym-form="singular+short"} values, this aggregation could be
implemented by computing the average of individual
[predictions]{acronym-label="prediction" acronym-form="plural+short"}.\
See also: [ml]{acronym-label="ml" acronym-form="singular+short"},
[bootstrap]{acronym-label="bootstrap" acronym-form="singular+short"},
[dataset]{acronym-label="dataset" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[label]{acronym-label="label" acronym-form="singular+short"},
[datapoint]{acronym-label="datapoint" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"}.,
first=bagging (or bootstrap aggregation), text=bagging

name=gradient descent (GD), description=

GD is an iterative method for finding the
[minimum]{acronym-label="minimum" acronym-form="singular+short"} of a
[differentiable]{acronym-label="differentiable"
acronym-form="singular+short"} function $f(\vw)$ of a vector-valued
argument $\vw \in \mathbb{R}^{\featuredim}$. Consider a current guess or
approximation $\vw^{(k)}$ for the [minimum]{acronym-label="minimum"
acronym-form="singular+short"} of the function $f(\vw)$. We would like
to find a new (better) vector $\vw^{(k+1)}$ that has a smaller objective
value $f(\vw^{(k+1)}) < f\big(\vw^{(k)}\big)$ than the current guess
$\vw^{(k)}$. We can achieve this typically by using a
[gradstep]{acronym-label="gradstep" acronym-form="singular+short"}
$$\label{equ_def_GD_step_dict}
            \vw^{(k\!+\!1)} = \vw^{(k)} - \eta \nabla f(\vw^{(k)})$$
with a sufficiently small [stepsize]{acronym-label="stepsize"
acronym-form="singular+short"} $\eta\!>\!0$. Fig.
[13](#fig_basic_GD_step_dict){reference-type="ref"
reference="fig_basic_GD_step_dict"} illustrates the effect of a single
GD step
[\[equ_def_GD_step_dict\]](#equ_def_GD_step_dict){reference-type="eqref"
reference="equ_def_GD_step_dict"}.

<figure id="fig_basic_GD_step_dict">
<div class="center">

</div>
<figcaption>A single <span data-acronym-label="gradstep"
data-acronym-form="singular+short">gradstep</span> <a
href="#equ_def_GD_step_dict" data-reference-type="eqref"
data-reference="equ_def_GD_step_dict">[equ_def_GD_step_dict]</a> towards
the minimizer <span class="math inline">$\overline{\vw}$</span> of <span
class="math inline">$f(\vw)$</span>.</figcaption>
</figure>

See also: [minimum]{acronym-label="minimum"
acronym-form="singular+short"},
[differentiable]{acronym-label="differentiable"
acronym-form="singular+short"}, [gradstep]{acronym-label="gradstep"
acronym-form="singular+short"}, [stepsize]{acronym-label="stepsize"
acronym-form="singular+short"}, [gradient]{acronym-label="gradient"
acronym-form="singular+short"}.

,first=gradient descent (GD),text=GD

name=mutual information (MI), description=The MI
$I \left( \featurevec;\truelabel\right)$ between two
[rvs]{acronym-label="rv" acronym-form="plural+short"} $\featurevec$,
$\truelabel$ defined on the same [probspace]{acronym-label="probspace"
acronym-form="singular+short"} is given by [@coverthomas]
$$I \left( \featurevec;\truelabel\right) \defeq 
    \expect \left\{ \log \frac{p (\featurevec,\truelabel)}{p(\featurevec)p(\truelabel)} \right\}.$$
It is a measure of how well we can estimate $\truelabel$ based solely on
$\featurevec$. A large value of $I \left( \featurevec;\truelabel\right)$
indicates that $\truelabel$ can be well predicted solely from
$\featurevec$. This [prediction]{acronym-label="prediction"
acronym-form="singular+short"} could be obtained by a
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"}
learned by an [erm]{acronym-label="erm"
acronym-form="singular+short"}-based [ml]{acronym-label="ml"
acronym-form="singular+short"} method.\
See also: [rv]{acronym-label="rv" acronym-form="singular+short"},
[probspace]{acronym-label="probspace" acronym-form="singular+short"},
[prediction]{acronym-label="prediction" acronym-form="singular+short"},
[hypothesis]{acronym-label="hypothesis" acronym-form="singular+short"},
[erm]{acronym-label="erm" acronym-form="singular+short"},
[ml]{acronym-label="ml" acronym-form="singular+short"}. , first=MI,
text=MI
