from utils.Templates.schemas import ImageState


class StopWorkflowAgent:
    def run(self, imageState: ImageState) -> dict:
        """Stops the workflow and displays the final confidence score"""

        if imageState.products is not None:
            for product in imageState.products:
                print(product)

        err = imageState.errors if imageState.errors is not None else []
        err.append("Workflow stopped by StopWorkflowAgent")
        
        return {
            "errors": err
        }