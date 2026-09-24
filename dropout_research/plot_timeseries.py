# dropout_timeseries.csv から主要な時系列をグラフ化する（検証済み値のみ）
import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("dropout_timeseries.csv")
df = df[df["status"].str.startswith("V")]
series = [
    ("USA", "IPEDS 6-year graduation rate (first-time full-time bachelor)", "US IPEDS 6-yr graduation (%)"),
    ("USA", "NSC persistence rate (2nd fall any institution)", "US NSC persistence (%)"),
    ("USA", "NSC retention rate (2nd fall same institution)", "US NSC retention (%)"),
]
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for c, ind, label in series:
    s = df[(df.country == c) & (df.indicator == ind)].astype({"cohort_or_year": int}).sort_values("cohort_or_year")
    axes[0].plot(s.cohort_or_year, s.value, marker="o", label=label)
axes[0].set_title("USA (entry cohort)"); axes[0].xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True)); axes[0].legend(fontsize=8); axes[0].set_ylim(50, 85)

for ind, label in [("MEXT annual dropout rate (univ+junior college+KOSEN)", "univ+JC+KOSEN"),
                   ("MEXT annual dropout rate (incl. graduate schools)", "incl. graduate schools")]:
    s = df[(df.country == "Japan") & (df.indicator == ind)].astype({"cohort_or_year": int}).sort_values("cohort_or_year")
    axes[1].plot(s.cohort_or_year, s.value, marker="o", label=label)
axes[1].set_title("Japan MEXT annual dropout rate (%)"); axes[1].legend(fontsize=8); axes[1].set_ylim(0, 3.5)

s = df[df.country == "OECD"]
for ind, label in [("bachelor completion within theoretical duration (EAG B5)", "within N"),
                   ("bachelor completion within theoretical duration +3y (EAG B5)", "within N+3")]:
    t = s[s.indicator == ind]
    axes[2].plot(t.cohort_or_year, t.value, marker="o", label=label)
axes[2].set_title("OECD avg bachelor completion (%)"); axes[2].legend(fontsize=8); axes[2].set_ylim(0, 100)
plt.tight_layout()
plt.savefig("dropout_timeseries.png", dpi=120)
print("saved")
