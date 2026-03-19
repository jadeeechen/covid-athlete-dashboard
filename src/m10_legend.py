import pandas as pd
import altair as alt
from m03_config import LEGEND_DOMAIN, LEGEND_RANGE


def build_legend():
    legend_data = pd.DataFrame(["Athlete", "Non-Athlete", "Both"], columns=["is_athlete"])

    legend_plot = alt.Chart(legend_data).mark_rect(
        filled=True,
        size=100
    ).encode(
        y=alt.Y("is_athlete:N", title="").axis(orient="right").sort(["Athlete", "Non-Athlete", "Both"]),
        color=alt.Color("is_athlete:N", scale=alt.Scale(range=LEGEND_RANGE, domain=LEGEND_DOMAIN)).legend(None)
    ).properties(
        width=110,
        height=90,
        title="Legend:"
    )

    return legend_plot