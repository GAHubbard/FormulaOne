import reflex as rx
import global_variables as gv


class Driver(rx.Base):
    """
    This is driver variables
    """

    first_name: str
    last_name: str
    team_name: str
    race_number: int
    alias: str
    country: str
    head_shot: str
    speed: float
    position: float
    rank: int


class State(rx.State):
    """
    Display info
    """

    def refresh(self):
        pass


def index():
    return rx.vstack(
        rx.vstack(
            rx.heading('Name', font_size="2em"),
            rx.heading('Team'),
        ),
        rx.button('Refresh', color_scheme='blue',on_click=State.refresh),
    )


app = rx.App()
app.add_page(index)