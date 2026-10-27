"""Generate report tables/matrices directly from recorded numerical evidence."""
from pathlib import Path
import csv
import json

b = Path(__file__).resolve().parents[1]
r = b/'results/run-20261027'
out = b/'report'
p2 = json.loads((r/'p2-checks.json').read_text())['checks']
p3 = json.loads((r/'p3-checks.json').read_text())['checks']

def matrix(a, digits=10):
    return r'\begin{pmatrix}' + r'\\'.join(' & '.join(f'{v:.{digits}f}' for v in row) for row in a) + r'\end{pmatrix}'

def sci(x, digits=3):
    if x == 0:
        return '0'
    mantissa, exponent = f'{x:.{digits}e}'.split('e')
    return rf'{mantissa}\times10^{{{int(exponent)}}}'

s = r'''\textbf{Gradient check.} The supplied four-sample input, labels and parameter matrix were used:
\[
X=\begin{pmatrix}1&-1&1\\2&0.5&1\\-1&2&1\\0.5&0.2&1\end{pmatrix},\quad
Y=\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\\0&1&0\end{pmatrix},\quad
\Th=\begin{pmatrix}0.1&-0.2&0.05\\0.3&-0.1&0.2\\0.02&0.1&-0.1\end{pmatrix}.
\]
For each entry, the central difference is
\[
(G_{\rm FD})_{ab}=\frac{L(\Th+10^{-6}E_{ab})-L(\Th-10^{-6}E_{ab})}{2\times10^{-6}}.
\]
The computed analytic and numerical matrices are, respectively,
'''
s += '\\[G_{\\rm analytic}='+matrix(p2['gradient']['analytic'])+'\\]'
s += '\n\\[G_{\\rm FD}='+matrix(p2['gradient']['central_difference'])+'\\]\n'
s += rf'The maximum entrywise absolute difference, before rounding the displayed matrices, is ${sci(p2["gradient"]["max_absolute_difference"],6)}$. This is below $10^{{-8}}$ and supports agreement with the mean-loss gradient in part (a).'
s += r'''

\textbf{One accelerated update.} Set $\Th_{\rm previous}=\Th-0.02$ entrywise, $\mu=0.05$, $\beta=0.90$, $k=3$ and $G(A)=2A$. Momentum evaluates $G$ at the current matrix $\Th$ displayed above and returns
'''
s += '\\[\\Th^+_{\\rm Momentum}='+matrix(p2['momentum']['computed_update'],4)+'\\].\n'
s += r'Nesterov uses $(k-1)/(k+2)=2/5$, so its recorded gradient point is'
s += '\\[W=\\Th+0.008='+matrix(p2['nesterov']['computed_gradient_point'],4)+'\\],\n'
s += r'and its computed updated parameter is'
s += '\\[\\Th^+_{\\rm Nesterov}='+matrix(p2['nesterov']['computed_update'],4)+'\\].\n'
s += r'''These match the separate formula calculations $0.9\Th+0.018$ and $0.9(\Th+0.008)$. Both gradient points match their expectations exactly in the check; both update discrepancies are $2.776\times10^{-17}$ (rounding), with one gradient call each. Momentum uses the current point and adds the previous displacement afterward. Nesterov extrapolates first and evaluates the gradient at that extrapolated point.

\textbf{Additional checks.} All seven supplied P2 tests passed before the full runs. The loss on logits $(1000,-1000)$ with the second class true is $2000$ (expected $2000$); zero logits with three classes give $\log3=1.0986122887$. Stability, shift invariance, first-update equality and unchanged inputs also passed. The included \method{p2/verify.py} prints these numerical checks without downloading a dataset.
'''
(out/'p2-checks.tex').write_text(s)

summary = list(csv.DictReader((r/'p2/summary.csv').open()))
s = r'''\textbf{Dataset sizes.} Digits has 1437 training and 360 test examples, with no exact duplicates removed. Dry Bean has 10834 training and 2709 test examples after removing 68 duplicates (13543 remaining). These sizes and the train/test hashes were recorded by the unmodified framework.

\begin{table}[htbp]\centering\small
\caption{Metrics after exactly 1000 updates. CE denotes mean cross-entropy; accuracy is a percentage.}\label{tab:p2}
\begin{tabular}{@{}llrrrr@{}}\toprule
Dataset & Method & Train CE & Test CE & Train acc. & Test acc.\\\midrule
'''
for row in summary:
    ds={'digits':'Digits','dry_bean':'Dry Bean'}[row['dataset']]
    method={'gd':'GD','momentum':'Momentum','nesterov':'Nesterov'}[row['method']]
    vals=[f"{float(row[k]):.6f}" for k in ['train_loss','test_loss']]
    vals += [f"{100*float(row[k]):.3f}\\%" for k in ['train_accuracy','test_accuracy']]
    s+=' & '.join([ds,method]+vals)+r'\\'+'\n'
s+=r'''\bottomrule\end{tabular}\end{table}

\textbf{(i) Which method reduces training loss faster?} In these runs, Nesterov eventually reduces training loss fastest, Momentum is next, and GD is slowest on both datasets. At update 100, the training CE values for GD/Momentum/Nesterov are $0.439801/0.108877/0.086856$ on Digits and $0.734252/0.294142/0.262083$ on Dry Bean. The final training losses have the same ordering. This is a comparison at equal gradient-update budgets, rather than a claim that one curve is lower at every early iteration.

\textbf{(ii) Which method has the best final test metrics?} On Digits, Momentum has the lowest test CE ($0.115559$), while Nesterov has the highest test accuracy ($96.944\%$). Nesterov has the lowest training CE but a higher test CE ($0.167670$) than both other methods. Accuracy measures only the winning class; CE also penalizes confident incorrect predictions, so their rankings can differ. On Dry Bean, Nesterov has the lowest test CE ($0.218661$), and Nesterov and Momentum tie for the highest test accuracy ($92.174\%$, exactly the same accuracy before rounding). Thus the lowest-training-loss method is best on test CE for Dry Bean, but not for Digits.

\textbf{(iii) Is there evidence of overfitting?} On Digits, Nesterov's smallest recorded test CE is $0.115969$ at update 185; its training CE there is $0.041322$. By update 1000, training CE falls to $0.002176$ while test CE rises to $0.167670$. Momentum has a weaker instance: after its test CE minimum of $0.114851$ at update 730, training CE falls from $0.036272$ to $0.029333$, while test CE increases to $0.115559$. The loss curves therefore show a divergence between continued fitting of training examples and held-out log-loss performance. In the last 100 updates, test CE increases by $0.004749$ for Nesterov and $0.000392$ for Momentum while each training CE decreases.

For Dry Bean, no sustained late training/test loss divergence is observed. All three methods attain their lowest recorded test CE at update 1000, and both losses decrease over the last 100 updates. This does not prove that the models cannot overfit with a different training duration or setting. Test minima above are descriptive observations only; the prescribed final update remains 1000 and no stopping rule or hyperparameter was selected using the test set.
'''
(out/'p2-results.tex').write_text(s)

s = r'''\textbf{Implementation.} The fitting function uses least squares directly on the raw Legendre design. The population-error function pads only the degree axis with zeros and sums squared coefficient differences with weights $1/(2q+1)$. For a batch, it returns one risk for each column. Inputs are not modified and targets are not normalized again.

\textbf{Fitting verification.} Use $x_i$ as 40 equally spaced points from $-0.95$ to $0.95$ and noiseless labels $y_i=0.3L_0(x_i)-0.7L_1(x_i)+0.2L_2(x_i)$. The expected degree-2 coefficients are $(0.3,-0.7,0.2)$; degree 10 has the same first three coefficients and eight zeros. Actual fitted coefficients are:
\begin{center}\small
\begin{tabular}{@{}rrrr@{}}\toprule
Degree index & Expected & Computed $K=2$ & Computed $K=10$\\\midrule
'''
w2=p3['noiseless_degree_2']['computed_coefficients'];w10=p3['noiseless_degree_10']['computed_coefficients']
for i,v in enumerate(w10):
    expected=[.3,-.7,.2][i] if i<3 else 0
    v2=f'{w2[i]:.16f}' if i<3 else '--'
    v10=f'{v:.16f}' if i<3 else '$'+sci(v,6)+'$'
    s+=f'{i} & {expected:g} & {v2} & {v10}'+r'\\'+'\n'
s += r'''\bottomrule\end{tabular}\end{center}
The largest coefficient differences are $1.221\times10^{-15}$ ($K=2$) and $2.498\times10^{-15}$ ($K=10$), below $10^{-11}$. The expected clean-target risk is zero; the computed risks are $3.024\times10^{-31}$ and $6.495\times10^{-30}$. Recovery checks the fitting function without noise or missing target terms.

\textbf{Error verification.} Use model coefficients $w=(0.5,-0.3,0.2)$ and an already-normalized target $c=(0.1,0.2,-0.1,0.4)$. The expected error is
\[
0.4^2+\frac{(-0.5)^2}{3}+\frac{0.3^2}{5}+\frac{(-0.4)^2}{7}
=0.2841904761904762.
\]
The implemented analytic result is $0.2841904761904762$. Independent 80-point Gauss--Legendre quadrature of $(f-g)^2/2$ gives $0.28419047619047905$, a difference of $2.831\times10^{-15}$, below $10^{-10}$. This compares evaluation in input space with the coefficient formula, including the missing degree-3 term and the uniform density. Additional scalar checks give expected/computed values $1/1$ for constant residual one, $4/7\,/\,4/7$ for a target-only tail, and $9/5\,/\,9/5$ for a model-only tail. All eight supplied P3 tests and batched-column checks passed.

\textbf{Fixed full experiment.} The two original grids were run with seed 666 and 1000 independent trial rows per cell. Each pair of models fits exactly the same labels. Across cells, the provided random bank reuses input/coefficient prefixes and noise to form paired comparisons. Each cell reports the arithmetic mean of all 1000 values of $\rho_e=\Eout(f_{10})-\Eout(f_2)$. No trial was discarded, no regularization was added, and no numerical error was clipped or smoothed. Across all fits, the recorded maximum violation of $\Ein(f_{10})\le\Ein(f_2)$ was $0$.
'''
(out/'p3-checks.tex').write_text(s)

# Keep punctuation inside displayed equations.
for name in ("p2-checks.tex", "p3-checks.tex"):
    path=out/name
    path.write_text(path.read_text().replace("\\].", ".\\]").replace("\\],", ",\\]"))
