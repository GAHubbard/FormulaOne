import reflex as rx
from dashboard.pages import index

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
        appearance="dark", has_background=True, radius="large", accent_color="orange"
    ),
)
app.add_page(
    index.index,
    title="Formula1",
    description="Dashboard for Formula1 races.",
)