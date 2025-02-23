import reflex as rx

def race_screen():
    return rx.flex(
        rx.box(
            "Video or audio and a map go here",
            text_align="center",
            border_width="1px",
            width="100%",
        ),
        width="100%",
        align="center"
    )