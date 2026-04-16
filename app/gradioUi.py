import html

import gradio as gr

from app.Workflows.ImgProcessingWorkflow import WORKFLOW_ACTIVITY_STEPS, stream_img_processing

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

.activity-shell {
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 24px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 248, 250, 0.92));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
    padding: 20px;
}

.activity-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px;
}

.activity-kicker {
    margin: 0;
    color: #94a3b8;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.activity-title {
    margin: 6px 0 4px;
    color: #111827;
    font-size: 1.08rem;
    font-weight: 700;
}

.activity-summary {
    margin: 0;
    color: #6b7280;
    font-size: 0.94rem;
    line-height: 1.6;
}

.activity-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    white-space: nowrap;
}

.activity-badge::before {
    content: "";
    width: 9px;
    height: 9px;
    border-radius: 999px;
    background: currentColor;
}

.activity-badge--ready {
    background: rgba(226, 232, 240, 0.7);
    color: #64748b;
}

.activity-badge--live {
    background: rgba(254, 242, 242, 0.95);
    color: #f43f5e;
}

.activity-badge--done {
    background: rgba(236, 253, 245, 0.95);
    color: #15803d;
}

.activity-badge--error {
    background: rgba(255, 241, 242, 0.95);
    color: #be123c;
}

.activity-progress-track {
    height: 10px;
    margin-top: 18px;
    border-radius: 999px;
    background: rgba(226, 232, 240, 0.8);
    overflow: hidden;
}

.activity-progress-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(135deg, #22c55e 0%, #f97316 56%, #ec4899 100%);
    transition: width 0.3s ease;
}

.activity-meta {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 10px;
    margin-top: 10px;
    color: #6b7280;
    font-size: 0.88rem;
}

.activity-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 14px;
    margin-top: 18px;
}

.activity-card {
    min-height: 164px;
    border-radius: 20px;
    border: 1px solid rgba(226, 232, 240, 0.92);
    background: rgba(255, 255, 255, 0.9);
    padding: 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.activity-card--done {
    border-color: rgba(134, 239, 172, 0.9);
    background: linear-gradient(180deg, rgba(240, 253, 244, 0.96), rgba(236, 253, 245, 0.92));
}

.activity-card--active {
    border-color: rgba(251, 146, 60, 0.5);
    background: linear-gradient(180deg, rgba(255, 247, 237, 0.98), rgba(253, 242, 248, 0.96));
    box-shadow: 0 18px 32px rgba(249, 115, 22, 0.14);
    transform: translateY(-2px);
}

.activity-card--error {
    border-color: rgba(251, 113, 133, 0.7);
    background: linear-gradient(180deg, rgba(255, 241, 242, 0.98), rgba(255, 247, 237, 0.94));
}

.activity-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.activity-card-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.activity-card-status::before {
    content: "";
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: currentColor;
}

.activity-card-index {
    color: #cbd5e1;
    font-size: 0.82rem;
    font-weight: 700;
}

.activity-card-title {
    margin-top: 22px;
    color: #111827;
    font-size: 1.04rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.activity-card-copy {
    margin-top: 8px;
    color: #64748b;
    font-size: 0.92rem;
    line-height: 1.55;
}

.activity-card-note {
    margin-top: 16px;
    color: #475569;
    font-size: 0.84rem;
    font-weight: 600;
}

.activity-card--pending .activity-card-status {
    color: #cbd5e1;
}

.activity-card--done .activity-card-status {
    color: #22c55e;
}

.activity-card--active .activity-card-status {
    color: #f97316;
}

.activity-card--error .activity-card-status {
    color: #f43f5e;
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

    .activity-header {
        flex-direction: column;
    }
}
"""

HERO_HTML = """
<div class="hero">
    <div class="hero-kicker">Fashion Discovery Studio</div>
    <h1 class="hero-title">StyleMatch</h1>
    <p class="hero-copy">
        Upload a look, name the piece you want to match, and follow each agent live while
        StyleMatch builds the labeled image and shopping-ready recommendations.
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

_ACTIVITY_STEP_MAP = {step["id"]: step for step in WORKFLOW_ACTIVITY_STEPS}


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
        raw_errors = [errors]
    else:
        raw_errors = list(errors)

    cleaned_errors = []
    for error in raw_errors:
        text = str(error).strip()
        if text and text not in cleaned_errors:
            cleaned_errors.append(text)

    return "\n".join(cleaned_errors)


def _render_activity_panel(active_node=None, completed_nodes=None, failed_node=None, message=None) -> str:
    completed_nodes = completed_nodes or []
    completed_set = set(completed_nodes)
    total_steps = len(WORKFLOW_ACTIVITY_STEPS)
    completed_count = len([step for step in WORKFLOW_ACTIVITY_STEPS if step["id"] in completed_set])
    remaining_count = max(total_steps - completed_count, 0)

    if failed_node:
        badge_label = "Issue"
        badge_class = "activity-badge activity-badge--error"
        summary_text = message or "The workflow stopped before all agents could finish."
        progress_ratio = completed_count / total_steps if total_steps else 0
    elif active_node:
        badge_label = "Live"
        badge_class = "activity-badge activity-badge--live"
        active_title = _ACTIVITY_STEP_MAP.get(active_node, {}).get("title", active_node)
        summary_text = f"{completed_count} of {total_steps} agents complete. Running {active_title} now."
        progress_ratio = min((completed_count + 0.45) / total_steps, 1) if total_steps else 0
    elif completed_count == total_steps and total_steps:
        badge_label = "Done"
        badge_class = "activity-badge activity-badge--done"
        summary_text = f"All {total_steps} agents finished. Your annotated image and matches are ready."
        progress_ratio = 1
    else:
        badge_label = "Ready"
        badge_class = "activity-badge activity-badge--ready"
        summary_text = message or "Upload an image and start StyleMatch to watch each agent step through the workflow."
        progress_ratio = 0

    pending_ids = [
        step["id"]
        for step in WORKFLOW_ACTIVITY_STEPS
        if step["id"] not in completed_set and step["id"] != active_node and step["id"] != failed_node
    ]
    next_pending = pending_ids[0] if pending_ids else None
    progress_percent = round(progress_ratio * 100, 1)

    card_html = []
    for index, step in enumerate(WORKFLOW_ACTIVITY_STEPS, start=1):
        step_id = step["id"]
        if step_id == failed_node:
            status_class = "activity-card activity-card--error"
            status_text = "Error"
            note_text = "Needs attention"
        elif step_id in completed_set:
            status_class = "activity-card activity-card--done"
            status_text = "Done"
            note_text = "Completed"
        elif step_id == active_node:
            status_class = "activity-card activity-card--active"
            status_text = "Live"
            note_text = "Running now"
        else:
            status_class = "activity-card activity-card--pending"
            status_text = "Queued"
            note_text = "Up next" if step_id == next_pending else "Waiting"

        card_html.append(
            f"""
            <div class="{status_class}">
                <div class="activity-card-top">
                    <span class="activity-card-status">{html.escape(status_text)}</span>
                    <span class="activity-card-index">{index:02d}</span>
                </div>
                <div class="activity-card-title">{html.escape(step['title'])}</div>
                <div class="activity-card-copy">{html.escape(step['description'])}</div>
                <div class="activity-card-note">{html.escape(note_text)}</div>
            </div>
            """
        )

    return f"""
    <div class="activity-shell">
        <div class="activity-header">
            <div>
                <p class="activity-kicker">Agent Activity</p>
                <p class="activity-title">Workflow status</p>
                <p class="activity-summary">{html.escape(summary_text)}</p>
            </div>
            <div class="{badge_class}">{html.escape(badge_label)}</div>
        </div>
        <div class="activity-progress-track">
            <div class="activity-progress-fill" style="width: {progress_percent}%;"></div>
        </div>
        <div class="activity-meta">
            <span>{completed_count} complete</span>
            <span>{remaining_count} to go</span>
        </div>
        <div class="activity-grid">
            {''.join(card_html)}
        </div>
    </div>
    """


EMPTY_ACTIVITY_HTML = _render_activity_panel()


def _build_ui_update(workflow_update, error_text="", failed_node=None):
    completed_nodes = workflow_update.get("completed_nodes", [])
    completed_set = set(completed_nodes)
    state = workflow_update.get("state", {})
    activity_html = _render_activity_panel(
        active_node=workflow_update.get("active_node"),
        completed_nodes=completed_nodes,
        failed_node=failed_node,
        message=error_text or None,
    )

    classified_image = state.get("img") if "ImageLabeling" in completed_set else None
    products_value = (
        _format_products(state.get("products"))
        if "ProductRecognition" in completed_set
        else EMPTY_PRODUCTS_TEXT
    )
    results_html = (
        state.get("html_shopping") or EMPTY_RESULTS_HTML
        if "HTMLBlockGenerator" in completed_set
        else EMPTY_RESULTS_HTML
    )

    return (
        activity_html,
        results_html,
        classified_image,
        products_value,
        gr.update(value=error_text, visible=bool(error_text)),
    )


def _reset_ui():
    return (
        None,
        "",
        EMPTY_ACTIVITY_HTML,
        None,
        EMPTY_RESULTS_HTML,
        EMPTY_PRODUCTS_TEXT,
        gr.update(value="", visible=False),
    )


def _run_stylematch(input_image, input_prompt):
    if input_image is None:
        error_text = "Upload an image before submitting."
        yield (
            EMPTY_ACTIVITY_HTML,
            EMPTY_RESULTS_HTML,
            None,
            EMPTY_PRODUCTS_TEXT,
            gr.update(value=error_text, visible=True),
        )
        return

    prompt = input_prompt.strip() if input_prompt and input_prompt.strip() else "Fashion"
    latest_update = {"active_node": None, "completed_nodes": [], "state": {}}

    try:
        for workflow_update in stream_img_processing(input_image, prompt):
            latest_update = workflow_update
            error_text = _format_errors(workflow_update.get("state", {}).get("errors"))
            yield _build_ui_update(workflow_update, error_text=error_text)
    except Exception as exc:
        error_text = f"StyleMatch could not process this request.\n{exc}"
        failed_node = latest_update.get("active_node") or WORKFLOW_ACTIVITY_STEPS[0]["id"]
        yield _build_ui_update(
            latest_update,
            error_text=error_text,
            failed_node=failed_node,
        )


def styleMatch():
    with gr.Blocks(theme=gr.themes.Soft(), css=APP_CSS, title="StyleMatch") as app:
        with gr.Column(elem_id="app-shell"):
            gr.Markdown(HERO_HTML)

            with gr.Column(elem_classes="panel"):
                gr.Markdown("<p class='section-title'>Agent Activity</p>")
                gr.Markdown(
                    "<p class='section-copy'>Track which agent is currently running and how many are still left in the queue.</p>"
                )
                activity_board = gr.HTML(value=EMPTY_ACTIVITY_HTML)

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
                        "<p class='section-copy'>The labeled image and detected product details will populate here as the workflow finishes later agents.</p>"
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
                        "<p class='section-copy'>Curated shopping cards appear here once the workflow reaches the final gallery step.</p>"
                    )
                    product_links_html = gr.HTML(value=EMPTY_RESULTS_HTML)

            classify_button.click(
                fn=_run_stylematch,
                inputs=[input_image, input_prompt],
                outputs=[activity_board, product_links_html, classified_image, products_box, errors],
            )

            reset_button.click(
                fn=_reset_ui,
                outputs=[
                    input_image,
                    input_prompt,
                    activity_board,
                    classified_image,
                    product_links_html,
                    products_box,
                    errors,
                ],
            )

        app.queue()
        return app


if __name__ == "__main__":
    app = styleMatch()
    app.launch()
