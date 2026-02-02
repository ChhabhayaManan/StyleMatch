import gradio as gr
import pycountry

countries = [
    (f"{country.name} ({country.alpha_2.lower()})", country.alpha_2.lower())
    for country in pycountry.countries
]

css_temp =""".product-card {
  max-width: 320px;
  width: 100%;
  font-family: Inter, Arial, sans-serif;
}

.product-card a {
  text-decoration: none;
  color: inherit;
}

.product-box {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.product-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

/* Image */
.product-image {
  aspect-ratio: 1 / 1;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Content */
.product-content {
  padding: 14px;
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.3;
  margin-bottom: 6px;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
}

.product-stars {
  color: #f5a623;
}

.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.product-seller {
  height: 24px;
  object-fit: contain;
}

.product-price {
  font-size: 18px;
  font-weight: 700;
  color: #111;
}

/* Responsive tweak */
@media (max-width: 480px) {
  .product-title {
    font-size: 15px;
  }
  .product-price {
    font-size: 16px;
  }
}
"""

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
        
        product_links_html = gr.HTML(label="Available On", css_template=css_temp)

        product_list.click(
            fn = getProductListAgent,
            inputs = [product_list, region, language],
            outputs = product_links_html
        )
        return app
    

if __name__ == "__main__":
    app = styleMatch()
    app.launch()

    
