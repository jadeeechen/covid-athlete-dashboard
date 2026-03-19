import altair as alt
from m03_config import ATHLETE_DOMAIN, ATHLETE_RANGE
from m05_shared import make_athlete_radio_selection, make_demographic_dropdown


def build_viz4(df):
    selection = make_athlete_radio_selection()
    row_param = make_demographic_dropdown()

    step = 13
    overlap = 3

    nearest = alt.selection_point(
        nearest=True,
        on="mouseover",
        fields=["PsychologicalWellbeing"],
        empty=False
    )

    selectors = alt.Chart(df).mark_point().encode(
        x="PsychologicalWellbeing:Q",
        opacity=alt.value(0)
    ).add_params(
        nearest
    )

    line = alt.Chart(df).add_selection(
        selection
    ).transform_filter(
        selection
    ).mark_line(
        interpolate="monotone",
        strokeWidth=1,
        opacity=1
    ).encode(
        x="PsychologicalWellbeing:Q",
        y="count():Q",
        color=alt.Color("is_athlete:N").legend(None).scale(domain=ATHLETE_DOMAIN, range=ATHLETE_RANGE)
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, "count():Q", alt.value(" "))
    )

    rules = alt.Chart(df).mark_rule(color="gray").encode(
        x="PsychologicalWellbeing:Q"
    ).transform_filter(
        nearest
    )

    demographic_vis = alt.Chart(df, height=step).add_selection(
        selection
    ).transform_filter(
        selection
    ).mark_area(
        interpolate="monotone",
        fillOpacity=0.5,
        strokeWidth=0.5
    ).encode(
        alt.X("PsychologicalWellbeing:Q").title("Psychological Wellbeing"),
        alt.Y("count()", title="", stack=None).axis(None).scale(range=[step, -step * overlap]),
        alt.Fill(
            "is_athlete:N",
            scale=alt.Scale(range=ATHLETE_RANGE, domain=ATHLETE_DOMAIN),
            title="Athlete Type: "
        ).legend()
    )

    viz = alt.layer(
        demographic_vis, line, selectors, points, rules, text
    ).transform_calculate(
        row=f"datum[{row_param.name}]"
    ).facet(
        bounds="flush",
        row=alt.Row("row:N", sort=alt.Sort()).title("").header(labelAngle=0, labelAlign="left")
    ).properties(
        title={
            "text": ["Psychological Wellbeing by Demographic"],
            "align": "left",
            "anchor": "start",
            "frame": "group"
        },
        align="none"
    ).add_params(
        row_param
    )

    return viz