import seaborn as sns
from data import getRawData

data_tailed = getRawData()
sns.lmplot(x="Time", y="OLR", data=data_tailed)
