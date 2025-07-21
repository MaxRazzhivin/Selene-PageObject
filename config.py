import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    base_url: str = 'https://demoqa.com'
    driver_name: str = 'chrome'
    hold_driver_at_exit: bool = False
    window_width: int = 1169
    window_height: int = 1800
    timeout: float = 4.0
