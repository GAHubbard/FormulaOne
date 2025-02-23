import reflex as rx
from dashboard.component.navbar import left_navbar, top_navbar
from dashboard.component.race_screen import race_screen


def index() -> rx.Component:
    return rx.hstack(
        left_navbar(),
        rx.vstack(
            top_navbar(),
            race_screen(),
            width="100%",
            align="center"
        ),
        width="100%",
        padding_x="1em",
        padding_y="1em",
    )