import reflex as rx

from dashboard.pages import navbar

def index() -> rx.Component:
    return rx.vstack(
        navbar.top_navbar(),
        rx.spacer(),
        rx.hstack(
            navbar.left_navbar(),
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


base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
]

base_style = {
    "font_family": "Inter",
}

app = rx.App(
    style=base_style,
    stylesheets=base_stylesheets,
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="orange"
    ),
)
app.add_page(
    index,
    title="NBA Data",
    description="NBA Data for the 2015-2016 season.",
)