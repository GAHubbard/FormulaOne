import reflex as rx
from ..component.card import driver_card
from ..application import global_variables as gv


def top_navbar():
    return rx.flex(
        rx.box(
            rx.hstack(
                rx.logo(),
                rx.color_mode.button(),
                align="center",
                spacing="3",
                ),
            "hello world",
            padding="1em",
            border_width="1px",
            width="100% " 
            ),
            spacing="2",
            flex_direction=["column", "column", "row"],
            align="center",
            width="100%",
            top="0px",
    )


def left_navbar():
    return rx.flex(
        rx.vstack(
            rx.box(
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                driver_card(5),
                padding="1em",
                border_width="1px",
                
            )
        )          
    )