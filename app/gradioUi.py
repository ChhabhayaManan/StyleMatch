import gradio as gr

from app.Workflows.ImgProcessingWorkflow import ImgProcessing

APP_CSS = """
body {
    background: linear-gradient(135deg, #fff8f2 0%, #fff4f7 48%, #fffdf8 100%);
}

.gradio-container {
    background:
        radial-gradient(circle at top, rgba(251, 146, 60, 0.16), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(236, 72, 153, 0.12), transparent 22%),
        linear-gradient(180deg, #fffaf5 0%, #fff6f9 52%, #fffdf9 100%);
}

#app-shell {
    max-width: 1180px;
    margin: 0 auto;
    padding: 24px 16px 48px;
}

.hero {
    text-align: center;
    padding: 18px 16px 10px;
}

.hero-kicker {
    display: inline-block;
    margin-bottom: 12px;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(236, 72, 153, 0.18);
    color: #be185d;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.hero-title {
    margin: 0;
    color: #111827;
    font-size: 3.4rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
}

.hero-copy {
    max-width: 760px;
    margin: 16px auto 0;
    color: #4b5563;
    font-size: 1.05rem;
    line-height: 1.7;
}

.panel {
    height: 100%;
    border: 1px solid rgba(236, 72, 153, 0.12);
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.88);
    box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
    backdrop-filter: blur(10px);
    padding: 22px;
}

.section-title {
    margin: 0 0 8px;
    color: #111827;
    font-size: 1.08rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}

.section-copy {
    margin: 0 0 18px;
    color: #6b7280;
    font-size: 0.96rem;
    line-height: 1.6;
}

#submit-btn {
    min-height: 48px;
    border: none;
    background: linear-gradient(135deg, #f97316 0%, #ec4899 100%);
    color: white;
    font-weight: 700;
}

#reset-btn {
    min-height: 48px;
    border: 1px solid #fbcfe8;
    background: white;
    color: #111827;
    font-weight: 600;
}

#error-box textarea {
    background: #fff1f2 !important;
    color: #9f1239 !important;
}

#error-box label {
    color: #9f1239 !important;
    font-weight: 700 !important;
}

.empty-state {
    padding: 28px 24px;
    border: 1px dashed rgba(244, 114, 182, 0.35);
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(255, 247, 237, 0.9), rgba(253, 242, 248, 0.9));
    text-align: center;
}

.empty-state h3 {
    margin: 8px 0 10px;
    color: #111827;
    font-size: 1.2rem;
}

.empty-state p {
    margin: 0;
    color: #6b7280;
    line-height: 1.6;
}

.empty-state-kicker {
    color: #be185d;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

@media (max-width: 900px) {
    #app-shell {
        padding: 18px 12px 36px;
    }

    .hero-title {
        font-size: 2.6rem;
    }

    .panel {
        padding: 18px;
    }
}
"""

HERO_HTML = """
<div class="hero">
    <div class="hero-kicker">Fashion Discovery Studio</div>
    <h1 class="hero-title">StyleMatch</h1>
    <p class="hero-copy">
        Upload a look, name the piece you want to match, and get a labeled result with
        shopping-ready recommendations in one place.
    </p>
</div>
"""

EMPTY_RESULTS_HTML = """
<div class="empty-state">
    <div class="empty-state-kicker">Shopping Matches</div>
    <h3>Your recommendations will appear here.</h3>
    <p>Upload an image and run StyleMatch to generate product cards and related shopping links.</p>
</div>
"""

EMPTY_PRODUCTS_TEXT = "Detected items will appear here after StyleMatch finishes processing your image."


def _format_products(products) -> str:
    if not products:
        return EMPTY_PRODUCTS_TEXT

    lines = []
    for index, product in enumerate(products, start=1):
        product_name = getattr(product, "productDisplayName", None)
        brand = getattr(product, "Brand", None)
        category = getattr(product, "subCategory", None) or getattr(product, "masterCategory", None)
        color = getattr(product, "Color", None)

        if isinstance(product, dict):
            product_name = product.get("productDisplayName", product_name)
            brand = product.get("Brand", brand)
            category = product.get("subCategory") or product.get("masterCategory") or category
            color = product.get("Color", color)

        details = [detail for detail in [brand, category, color] if detail]
        label = product_name or f"Item {index}"
        lines.append(f"{index}. {label}")

        if details:
            lines.append(f"   {' | '.join(details)}")

    return "\n".join(lines)


def _format_errors(errors) -> str:
    if not errors:
        return ""

    if isinstance(errors, str):
        cleaned_errors = [errors.strip()] if errors.strip() else []
    else:
        cleaned_errors = [str(error).strip() for error in errors if str(error).strip()]

    return "\n".join(cleaned_errors)


def _reset_ui():
    return None, "", None, EMPTY_RESULTS_HTML, EMPTY_PRODUCTS_TEXT, gr.update(value="", visible=False)


def _run_stylematch(input_image, input_prompt):
    if input_image is None:
        return (
            EMPTY_RESULTS_HTML,
            None,
            EMPTY_PRODUCTS_TEXT,
            gr.update(value="Upload an image before submitting.", visible=True),
        )

    prompt = input_prompt.strip() if input_prompt and input_prompt.strip() else "Fashion"

    try:
        product_links_html, classified_image, products, errors = ImgProcessing(input_image, prompt)
    except Exception as exc:
        return (
            EMPTY_RESULTS_HTML,
            None,
            EMPTY_PRODUCTS_TEXT,
            gr.update(value=f"StyleMatch could not process this request.\n{exc}", visible=True),
        )

    error_text = _format_errors(errors)
    rendered_html = product_links_html or EMPTY_RESULTS_HTML

    return (
        rendered_html,
        classified_image,
        _format_products(products),
        gr.update(value=error_text, visible=bool(error_text)),
    )


def styleMatch():
    with gr.Blocks(theme=gr.themes.Soft(), css=APP_CSS, title="StyleMatch") as app:
        with gr.Column(elem_id="app-shell"):
            gr.Markdown(HERO_HTML)

            with gr.Row(equal_height=True):
                with gr.Column(scale=5, elem_classes="panel"):
                    gr.Markdown("<p class='section-title'>Upload & describe</p>")
                    gr.Markdown(
                        "<p class='section-copy'>Start with an outfit photo and tell StyleMatch what item you want to find.</p>"
                    )
                    input_image = gr.Image(
                        label="Upload an image",
                        type="pil",
                        sources=["upload"],
                        height=420,
                    )
                    input_prompt = gr.Textbox(
                        label="Specify item",
                        placeholder="Examples: red dress, denim jacket, white sneakers",
                    )

                    with gr.Row():
                        classify_button = gr.Button("Find Matches", variant="primary", elem_id="submit-btn")
                        reset_button = gr.Button("Reset", elem_id="reset-btn")

                with gr.Column(scale=5, elem_classes="panel"):
                    gr.Markdown("<p class='section-title'>Results</p>")
                    gr.Markdown(
                        "<p class='section-copy'>Review the labeled output image, detected product details, and any workflow feedback.</p>"
                    )
                    classified_image = gr.Image(
                        label="Annotated image",
                        type="pil",
                        interactive=False,
                        height=420,
                    )
                    products_box = gr.Textbox(
                        label="Detected products",
                        value=EMPTY_PRODUCTS_TEXT,
                        lines=6,
                        interactive=False,
                    )
                    errors = gr.Textbox(
                        label="Errors",
                        lines=4,
                        interactive=False,
                        visible=False,
                        elem_id="error-box",
                    )

            with gr.Row():
                with gr.Column(elem_classes="panel"):
                    gr.Markdown("<p class='section-title'>Recommended Products</p>")
                    gr.Markdown(
                        "<p class='section-copy'>Curated shopping cards will show up here after processing.</p>"
                    )
                    product_links_html = gr.HTML(value=EMPTY_RESULTS_HTML)

            classify_button.click(
                fn=_run_stylematch,
                inputs=[input_image, input_prompt],
                outputs=[product_links_html, classified_image, products_box, errors],
            )

            reset_button.click(
                fn=_reset_ui,
                outputs=[input_image, input_prompt, classified_image, product_links_html, products_box, errors],
            )

        return app


if __name__ == "__main__":
    app = styleMatch()
    app.launch()
