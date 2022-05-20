"""
Module responsible for starting and ending selenium based chrome and viewing the video
"""
from returns.result import Result, Success, Failure



def watch(url: str, how_long: int = 100, quality: int = None) -> Result[str, str]:
    """
    Function that completes the task of:
    1. Starting the chrome from selenium
    2. Adding the extensions to chrome (on start)
      2.1. AddBlock extension to avoid advertisement
      2.2. JS extension to collect StatsForNerds
    3. Stops Chrome by timeout
    :param url: valid http/s youtube url to video
    :param how_long: seconds, for timeout of video viewing. None for "till the end of video"
    :param quality: None for auto, int ~240-1024 for specific quality selection
    :return: 1 for success
    """
    if not (quality is None):
        raise NotImplementedError(f"Quality selection not implemented yet,"
                                  f" use None for automatic quality selection")

    return Success("End of video")
