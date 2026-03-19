import altair as alt


def build_viz1(data1):
    chart_athlete = alt.Chart(data1).mark_circle(
        color="#f59505",
        size=100,
        opacity=1
    ).encode(
        alt.Y("y:N", title="Category"),
        alt.X("Athlete:Q", title="Average Happiness"),
        tooltip=[
            alt.Tooltip("Athlete:Q", title="Average Happiness (Athlete)")
        ],
        color=alt.condition(
            alt.datum["Athlete"] == alt.datum["Non-Athlete"],
            alt.value("red"),
            alt.value("#f59505")
        )
    )

    chart_non_athlete = alt.Chart(data1).mark_circle(
        color="#a105f5",
        size=100,
        opacity=1
    ).encode(
        alt.Y("y:N", title="Occupational Category"),
        alt.X("Non-Athlete:Q"),
        tooltip=[
            alt.Tooltip("Non-Athlete:Q", title="Average Happiness (Non-Athlete)")
        ],
        color=alt.condition(
            alt.datum["Athlete"] == alt.datum["Non-Athlete"],
            alt.value("red"),
            alt.value("#a105f5")
        )
    )

    chart_line = alt.Chart(data1).mark_line(size=2).encode(
        alt.Y("y:N", title="Category"),
        alt.X("x1:Q", scale=alt.Scale(domain=[0.0, 5.1])),
        alt.X2("x2:Q"),
        tooltip=[
            alt.Tooltip("Difference:Q", title="Difference")
        ]
    )

    viz = (chart_line + chart_athlete + chart_non_athlete).properties(
        height=850,
        title="Average Happiness by Occupation"
    )

    return viz