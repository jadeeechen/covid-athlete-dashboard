import altair as alt
from m03_config import ATHLETE_DOMAIN, ATHLETE_RANGE
from m05_shared import make_athlete_radio_selection, make_weeks_slider


def build_viz3(df):
    selection = make_athlete_radio_selection()
    weeks = make_weeks_slider()

    viz = alt.Chart(df).add_selection(
        selection
    ).transform_filter(
        selection
    ).transform_filter(
        alt.FieldGTEPredicate(field="WeeksSocialDistancing", gte=weeks)
    ).transform_density(
        "LONE_TOTAL",
        as_=["LONE_TOTAL", "density"],
        extent=[0, 5],
        groupby=["is_athlete", "#inlockdownbubble"]
    ).mark_area(
        orient="horizontal",
        opacity=0.6
    ).encode(
        alt.Y("LONE_TOTAL:Q", title="Total Loneliness Score"),
        alt.Color(
            "is_athlete:N",
            title="Athlete Type: "
        ).scale(domain=ATHLETE_DOMAIN, range=ATHLETE_RANGE),
        alt.X(
            "density:Q",
            stack="center",
            impute=None,
            title=None,
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=False)
        ),
        alt.Column(
            "#inlockdownbubble:O",
            header=alt.Header(
                titleOrient="bottom",
                labelOrient="bottom",
                labelPadding=0,
                labelFontSize=10,
                titleFontSize=12
            ),
            title="People in Lockdown Bubble"
        )
    ).properties(
        width=75,
        height=400,
        title="Loneliness by Lockdown Bubble Size"
    ).add_params(
        weeks
    )

    return viz