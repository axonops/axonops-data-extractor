#  © 2024 AxonOps Limited. All rights reserved.

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging
import sys
from colorlog import ColoredFormatter


def setup_logger(name='AxonOpsLogger', level=logging.INFO):
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    # Define a colored formatter
    formatter = ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    console_handler.setFormatter(formatter)

    # Clear existing handlers, and add new ones
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
