import matplotlib.pyplot as plt
import numpy as np

# Sample data (replace with your actual data)
gnbs = ['gNB1', 'gNB2', 'gNB3', 'gNB4', 'gNB5', 'gNB6']
ue_counts = [4, 8, 12]
colors = plt.cm.get_cmap('Set2')(np.linspace(0, 1, len(gnbs)))

# Sample delays for each UE in each gNB for each experiment (replace with your actual data)
# Structure: list of lists of lists
# First level: experiments (4, 8, 12 UEs)
# Second level: gNBs
# Third level: delays for each UE in that gNB for that experiment
delays = [
    # 4 UEs experiment
    [[np.random.uniform(5, 15, 4) for _ in range(6)]],
    # 8 UEs experiment
    [[np.random.uniform(5, 15, 8) for _ in range(6)]],
    # 12 UEs experiment
    [[np.random.uniform(5, 15, 12) for _ in range(6)]]
]

fig, axes = plt.subplots(3, 1, figsize=(12, 18), sharex=True)
fig.suptitle('Average Delay for Each UE in Different gNBs', fontsize=16)

for exp, (ax, ue_count) in enumerate(zip(axes, ue_counts)):
    x = np.arange(ue_count)
    width = 0.8 / len(gnbs)
    
    for i, gnb_delays in enumerate(delays[exp][0]):
        ax.bar(x + i*width, gnb_delays, width, label=gnbs[i], color=colors[i], alpha=0.7)
    
    ax.set_ylabel('Average Delay')
    ax.set_title(f'Experiment with {ue_count} UEs')
    ax.set_xticks(x + width * (len(gnbs) - 1) / 2)
    ax.set_xticklabels([f'UE{i+1}' for i in range(ue_count)])
    ax.legend(title='gNBs', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.7)

plt.xlabel('UEs')
plt.tight_layout()
plt.show()
