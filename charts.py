import matplotlib.pyplot as plt

def plot_charts(x,y,bias_flags,threshold, col_name):
    plt.figure(figsize=(10, 6))
    bars =plt.bar(x, y, color = ["red" if flag else "green" for flag in bias_flags])
    plt.axhline(y=threshold, color = 'grey', linestyle = '--', label = 'Bias Threshold')
    plt.xlabel(col_name.title())
    plt.ylabel("Success Rate (%)")
    plt.title(f"Bias Detection for {col_name.title()}")
    plt.legend()
    plt.xticks(rotation = 45, ha = "right")
    plt.tight_layout()
    plt.savefig(f"chart_{col_name}.png")
    plt.show()

def plot_bias_charts(all_findings):
    demographic_groups = set(f["demographic_col"] for f in all_findings)
    for cols in demographic_groups:
        group_findings = [f for f in all_findings if f["demographic_col"] == cols]
        groups = [f["group"] for f in group_findings]
        rates = [f["rate"] for f in group_findings]
        bias_flags = [f["bias_detected"] for f in group_findings]
        threshold = max(rates) * 0.80
        plot_charts(groups, rates, bias_flags, threshold, cols)
