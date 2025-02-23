import reflex as rx
from dashboard.component import navbar


def index() -> rx.Component:
    return rx.hstack(
        navbar.left_navbar(),
        rx.hstack(
            navbar.top_navbar(),
            width="100%",
            spacing="6",
            padding_x=["1.5em", "1.5em", "3em", "5em"],
            padding_y=["1.25em", "1.25em", "2em"],
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em", "5em"],
        padding_y=["1.25em", "1.25em", "2em"],
    )