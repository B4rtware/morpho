import logging

# setup logger
logging.basicConfig(
    format="[{asctime}] [ {name} ] [ {levelname:<7} ] {message}",
    datefmt="%d.%m.%Y %H:%M:%S",
    level=0,
    style="{",
)
