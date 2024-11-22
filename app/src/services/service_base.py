
def _create_response(status: str, message, data=None):
	response = {
		"status": status,
		"message": message,
		"data": data
	}
	return response
