import gradio as gr
import pycountry

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
        
        product_list = gr.State()
        with gr.Row():
            classify_button = gr.Button("Classify Items in Image")
            classify_button.click(
                fn = productIdentifierAgent,
                inputs = [input_image, input_prompt],
                outputs = [classified_image, product_list]
            )
        with gr.Row():
            with gr.Column(scale=4):
                product_list = gr.Button("Get Product List")
            with gr.Column(scale=1):
                region = gr.Dropdown(
                    choices=countries,
                    label="Region",
                    interactive=True
                )
            with gr.Column(scale=1):
                language = gr.Dropdown(
                    choices=['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'ko'],
                    label="Language",
                    value = 'en',
                    interactive=True
                )
        product_links_html = gr.HTML(label="Available On")

        product_list.click(
            fn = getProductListAgent,
            inputs = [product_list, region, language],
            outputs = product_links_html
        )
        return app
    

if __name__ == "__main__":
    app = styleMatch()
    app.launch()

    
