"""Generate report figure and table from the six completed runs."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

report = Path(__file__).resolve().parent
runs = report.parent / 'results/run-10R3a5Il/runs'
fig, axes = plt.subplots(1, 3, figsize=(9.5, 2.65), sharex=True, sharey=True)
table = []
for ax, (title, key) in zip(axes, [('AdamW', 'learning_rate'), ('SGDM', 'sgdm_learning_rate'), ('Muon', 'muon_learning_rate')]):
    handles = []
    for variant, color in [('default', '#14558a'), ('other', '#ab4927')]:
        run = runs / f'{title.lower()}-{variant}'
        cfg = json.loads((run / 'config.json').read_text())
        summary = json.loads((run / 'summary.json').read_text())
        assert (summary['status'], summary['step'], summary['tokens']) == ('completed', 5000, 92160000)
        with (run / 'metrics.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        x = [float(r['tokens']) / 1e6 for r in rows]
        lr = cfg[key]
        for field, style in [('train_loss', '--'), ('val_loss', '-')]:
            ax.plot(x, [float(r[field]) for r in rows], style, color=color, lw=1.6)
        handles.append(Line2D([], [], color=color, label=f'{lr:g}'))
        table.append(f'{title} & {lr:g} & {summary["endpoint_scores"]["loss"]:.4f} & {summary["train_seconds"]/60:.2f} ' + r'\\')
    ax.set_title(title, weight='bold', fontsize=10)
    ax.legend(handles=handles, title='Peak LR', fontsize=8, title_fontsize=8, frameon=False)
    ax.grid(axis='y', alpha=.18)
    ax.spines[['top','right']].set_visible(False)
    ax.set_xticks([0, 30, 60, 90])
axes[0].set_ylabel('Loss (nats / character)')
fig.supxlabel('Training tokens (millions)', fontsize=10)
fig.tight_layout(pad=.5, rect=(0,.06,1,1))
fig.savefig(report/'trajectories.pdf', bbox_inches='tight')
(report/'endpoints.tex').write_text('\n'.join(table)+'\n')
