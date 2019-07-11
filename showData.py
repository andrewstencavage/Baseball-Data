import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

pitchDS = pd.read_csv('./pitches.csv').drop(['ball','strike','first','second','third'],axis=1)
filteredGames = ['SEA200709261']
## Remove bad data games
pitchDSfilter = ~pitchDS['gameID'].isin(filteredGames)
pitchDS = pitchDS.where(pitchDSfilter)
print(pitchDS.head())
# # Remove Outliers
pitchDS = pitchDS[((pitchDS['scoreDiff'] - pitchDS['scoreDiff'].mean()) / pitchDS['scoreDiff'].std()).abs() < 3]

pitchDS['inning'] = (pitchDS['inning'] * 6 + pitchDS['topBottom'] * 3 + pitchDS['out'] ) / 6
pitchDS = pitchDS.drop(['topBottom','out','gameID'],axis=1)
filterHomeWin = pitchDS["home"] == 1
pitchDSHomeWins = pitchDS.where(filterHomeWin)

print(pitchDSHomeWins.head())
fullCross = (pd.crosstab(pitchDS.inning,pitchDS.scoreDiff))
homeCross = (pd.crosstab(pitchDSHomeWins.inning,pitchDSHomeWins.scoreDiff))
prob = (homeCross / fullCross)

filterLateInnings = pitchDS['inning'] >= 9.5
filterPlusScoreDiff = pitchDS['scoreDiff'] > 0
filteredBadData = pitchDS.where(filterLateInnings & filterPlusScoreDiff).dropna()
# print(filteredBadData.head())
ticklabels = [f'{"T" if x % 6 < 3 else "B"}{x // 6 + 1} Out {x % 3}' for x in range(6 * 10)]

ax = sns.heatmap(prob,cmap=sns.cubehelix_palette(8, start=2, rot=0, dark=0, light=.95),linewidth=0.5, yticklabels=ticklabels)
ax.invert_yaxis()
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places

# plt.show()