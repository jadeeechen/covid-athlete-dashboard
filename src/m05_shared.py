import altair as alt
from m03_config import ATHLETE_DOMAIN


def make_athlete_radio_selection():
    input_dropdown = alt.binding_radio(
        options=[None, "Athlete", "Non-Athlete"],
        labels=["Both", "Athlete", "Non-Athlete"],
        name="Athlete type: "
    )

    selection = alt.selection_point(
        fields=["is_athlete"],
        bind=input_dropdown
    )

    return selection


def make_weeks_slider():
    slider = alt.binding_range(
        min=1,
        max=19,
        step=3,
        name="Minimum Weeks Spent Social Distancing: "
    )
    weeks = alt.param(value=0, bind=slider)
    return weeks


def make_demographic_dropdown():
    dropdown = alt.binding_select(
        options=[
            "AgeGroup",
            "Gender",
            "CountryDuringLockdown",
            "MaritalStatus",
            "SmokingStatus",
            "FiveFruitandVeg",
            "Hourssleep",
        ],
        labels=[
            "Age Group",
            "Gender",
            "Country Inhabited During Lockdown",
            "Marital Status",
            "Smoking Status",
            "Eat Five Fruits and Vegetables",
            "Average Maximum Hours of Sleep",
        ],
        name="Ridgeline plot Y-axis - Demograpic information: "
    )

    row_param = alt.param(
        value="AgeGroup",
        bind=dropdown
    )

    return row_param