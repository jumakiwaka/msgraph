from common.utils import remove_non_properties_from_dict


class ResponseWrapper:
    """Generic standard wrapper class for standardizing api responses"""

    def __init__(
        self,
        status_code: int,
        status: str = None,
        message: str = None,
        error=None,
        result=None,
    ):
        self.status = status
        self.status_code = status_code
        self.message = message
        self.error = error
        self.result = result

    @property
    def data(self):
        response_data = {
            "status": self.status,
            "status_code": self.status_code,
            "message": self.message,
            "error": self.error,
            "result": self.result,
        }

        cleaned_up_res = remove_non_properties_from_dict(response_data)

        return cleaned_up_res

    @property
    def success(self):
        response_data = {
            "status": "success",
            "status_code": self.status_code,
            "message": self.message,
            "error": self.error,
            "result": self.result,
        }

        cleaned_up_res = remove_non_properties_from_dict(response_data)

        return cleaned_up_res

    @property
    def fail(self):
        response_data = {
            "status": "error",
            "status_code": self.status_code,
            "message": self.message,
            "error": self.error,
            "result": self.result,
        }

        cleaned_up_res = remove_non_properties_from_dict(response_data)

        return cleaned_up_res
