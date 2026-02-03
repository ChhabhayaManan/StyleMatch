import gradio as gr
import pycountry
from app.Workflows.ImgProcessingWorkflow import ImgProcessing
countries = [
    (f"{country.name} ({country.alpha_2.lower()})", country.alpha_2.lower())
    for country in pycountry.countries
]



def styleMatch():
    with gr.Blocks() as app:
        gr.Markdown("<div align='center'><h1>StyleMatch</h1></div>")

        with gr.Row():
            with gr.Column():
                input_image = gr.Image(label="Upload an Image")
                input_prompt = gr.Textbox(label="Specify Item (e.g., 'red dress')")
            
            with gr.Column():
                classified_image = gr.Image()
        
        with gr.Row():
            product_links_html = gr.HTML(label="Recommended Products")

        with gr.Row():
            classify_button = gr.Button("Submit")
            classify_button.click(
                fn = ImgProcessing,
                inputs = [input_image, input_prompt],
                outputs = [product_links_html, classified_image]
            )
              

        return app
    

if __name__ == "__main__":
    app = styleMatch()
    app.launch()

    
