from validation_pipeline import CaptureLogContext
import logging


def test_log_capturing():
    logger = logging.getLogger("matchms")

    with CaptureLogContext() as log_capture:
        logger.warning("Added bonus info")
    for log_message in log_capture:
        print(log_message)