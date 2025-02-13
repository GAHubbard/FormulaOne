import reflex as rx


def navbar():
    return rx.flex(
        rx.hstack(
            rx.badge(
                "2015-2016 season",
                radius="full",
                align="center",
                color_scheme="orange",
                variant="surface",
            ),
            align="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.logo(),
            rx.color_mode.button(),
            align="center",
            spacing="3",
        ),
        spacing="2",
        flex_direction=["column", "column", "row"],
        align="center",
        width="100%",
        top="0px",
    )