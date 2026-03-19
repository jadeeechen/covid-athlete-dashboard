import altair as alt

from m04_data_loader import load_data
from m06_viz1_happiness_by_occupation import build_viz1
from m07_viz2_happiness_anxiety_depression import build_viz2
from m08_viz3_loneliness_violin import build_viz3
from m09_viz4_psychological_wellbeing import build_viz4
from m10_legend import build_legend


def build_dashboard():
    data1, data2, df = load_data()

    jade_viz_1 = build_viz1(data1)
    jade_viz_2_3 = build_viz2(data2)
    sam_viz_4 = build_viz3(df)
    sam_viz_5 = build_viz4(df)
    legend_plot = build_legend()

    horizontal = alt.hconcat(sam_viz_5, sam_viz_4)
    vertical = alt.vconcat(jade_viz_2_3, horizontal)
    legend_binding = alt.vconcat(legend_plot, jade_viz_1)

    final = alt.hconcat(legend_binding, vertical)

    final = final.configure_axis(
        tickCount=10,
        labelFlush=False,
        ticks=False,
        domain=False,
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        padding={
            "right": 60,
            "top": 20,
            "bottom": 20,
            "left": 5
        },
        title={
            "text": [
                "During the COVID-19 pandemic, how well did athletes versus non-athletes cope?",
                "Looking at demographic information, mental well-being and general lifestyle"
            ],
            "fontSize": 20
        }
    ).configure_facet(
        spacing=35
    )

    return final


if __name__ == "__main__":
    chart = build_dashboard()
    chart.save("index.html")