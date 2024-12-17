'''
import logging.config
import os
from app.dependencies import get_settings

settings = get_settings()
def setup_logging():
    """
    Sets up logging for the application using a configuration file.
    This ensures standardized logging across the entire application.
    """
    # Construct the path to 'logging.conf', assuming it's in the project's root.
    logging_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
    # Normalize the path to handle any '..' correctly.
    normalized_path = os.path.normpath(logging_config_path)
    # Apply the logging configuration.
    logging.config.fileConfig(normalized_path, disable_existing_loggers=False)
'''

import logging.config
import os
from app.dependencies import get_settings

settings = get_settings()

def setup_logging():
    """
    Sets up logging for the application using a configuration file.
    This ensures standardized logging across the entire application.
    """
    # Construct the path to 'logging.conf', assuming it's in the project's root.
    logging_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
    # Normalize the path to handle any '..' correctly.
    normalized_path = os.path.normpath(logging_config_path)
    # Apply the logging configuration.
    logging.config.fileConfig(normalized_path, disable_existing_loggers=False)

    # Add custom loggers for profile updates and status changes if needed
    logger = logging.getLogger('user_profile')
    logger.setLevel(logging.INFO)  # or ERROR, depending on your requirements
    
    # Example of logging profile update actions
    def log_profile_update(user_id: str, updated_fields: list):
        logger.info(f"User {user_id} updated their profile. Fields updated: {', '.join(updated_fields)}")
    
    # Example of logging status upgrade actions
    def log_status_upgrade(user_id: str, new_status: str):
        logger.info(f"User {user_id} upgraded to {new_status} professional status.")
    
    # Optionally, return these logging functions for use elsewhere
    return log_profile_update, log_status_upgrade
