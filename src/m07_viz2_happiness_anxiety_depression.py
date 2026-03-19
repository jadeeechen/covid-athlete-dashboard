import altair as alt
from m03_config import ATHLETE_DOMAIN, ATHLETE_RANGE


def build_viz2(data2):
    brush = alt.selection_interval(encodings=["x"], name="brush")
    click = alt.selection_point(encodings=["color"])

    line_chart = alt.Chart(data2).mark_line(point=True).encode(
        alt.X("SurveyDate:T", axis=alt.Axis(format="%m/%d"), title="Survey Date"),
        alt.Y("average(Happy):Q", scale=alt.Scale(domain=[0.75, 5.0]), title="Average Happiness"),
        alt.Color("is_athlete:N", legend=None).scale(domain=ATHLETE_DOMAIN, range=ATHLETE_RANGE)
    ).properties(
        width=500,
        height=320
    ).add_params(
        brush
    ).transform_filter(
        click
    )

    bar_chart_anxiety = alt.Chart(data2).mark_bar().encode(
        alt.Column("Anxiety Severity:N", title=None),
        alt.X("is_athlete:N", axis=alt.Axis(title=None, labelAngle=0)),
        alt.Y("count()", title="Count", scale=alt.Scale(domain=[0, 300])),
        alt.Color(
            "is_athlete:N",
            legend=None,
            scale=alt.Scale(domain=ATHLETE_DOMAIN, range=ATHLETE_RANGE)
        ),
        opacity=alt.condition(click, alt.value(1), alt.value(0.3))
    ).properties(
        width=120,
        height=110,
        title="Anxiety Severity Counts"
    )

    bar_chart_depression = alt.Chart(data2).mark_bar().encode(
        alt.Column("Depression Severity:N", title=None),
        alt.X("is_athlete:N", axis=alt.Axis(title=None, labelAngle=0)),
        alt.Y("count()", title="Count", scale=alt.Scale(domain=[0, 300])),
        alt.Color(
            "is_athlete:N",
            legend=None,
            scale=alt.Scale(domain=ATHLETE_DOMAIN, range=ATHLETE_RANGE)
        ),
        opacity=alt.condition(click, alt.value(1), alt.value(0.3))
    ).properties(
        width=120,
        height=110,
        title="Depression Severity Counts"
    )

    combined_bar = alt.vconcat(bar_chart_anxiety, bar_chart_depression).transform_filter(
        brush
    ).add_params(
        click
    )

    viz = alt.hconcat(line_chart, combined_bar, spacing=50).properties(
        title="Happiness, Anxiety, and Depression Over Time"
    )

    return viz