from utils.Templates.schemas import ImageState


class StopWorkflowAgent:
    _NON_ERROR_MESSAGES = {
        "Workflow stopped by StopWorkflowAgent",
    }

    def run(self, imageState: ImageState) -> dict:
        """Leaves the workflow state untouched unless it needs error cleanup."""

        cleaned_errors = [
            str(error).strip()
            for error in (imageState.errors or [])
            if str(error).strip() and str(error).strip() not in self._NON_ERROR_MESSAGES
        ]

        if cleaned_errors != list(imageState.errors or []):
            return {"errors": cleaned_errors}

        return {}
