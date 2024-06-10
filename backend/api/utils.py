def handle_error(message, status_code):
    """
    Constructs an error response.
    
    Args:
        message (str): The error message.
        status_code (int): The HTTP status code.
    
    Returns:
        response (dict): The error response.
        status_code (int): The HTTP status code.
    """
    response = {
        'status': 'error',
        'message': message
    }
    return response, status_code