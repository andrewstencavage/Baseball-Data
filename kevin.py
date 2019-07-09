import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pitchDS = pd.read_csv('./andrew.csv')

# # Remove Outliers
pitchDS = pitchDS[((pitchDS['scoreDiff'] - pitchDS['scoreDiff'].mean()) / pitchDS['scoreDiff'].std()).abs() < 3]
pitchDS = pitchDS[pitchDS['scoreDiff'] != 0]

pitchDS['subinning'] = ((pitchDS['inning']) * 6 + pitchDS['topBottom'] * 3 + pitchDS['out']) / 6

fullCross = (pd.crosstab(pitchDS.subinning,pitchDS.scoreDiff))

# Home win filter
homeWin = pitchDS[pitchDS['home'] == 1]
homeCross = (pd.crosstab(homeWin.subinning,pitchDS.scoreDiff))

# Away win filter
awayWin = pitchDS[pitchDS['home'] == 0]
awayCross = (pd.crosstab(awayWin.subinning,pitchDS.scoreDiff))

winner = (homeCross - awayCross)

# np.nan != np.nan, so the value will not be equal to itself
winner[winner != winner] = -awayCross
winner[winner != winner] = homeCross

prob = winner / fullCross

ticklabels = [f'{"T" if x % 6 < 3 else "B"}{x // 6 + 1} Out {x % 3 + 1}' for x in range(6 * 10)]

ax = sns.heatmap(prob,linewidth=0.5,annot=True, yticklabels=ticklabels)
ax.invert_yaxis()
plt.show()