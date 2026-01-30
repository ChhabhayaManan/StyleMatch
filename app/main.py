from app.gradioUi import styleMatch

if __name__ == "__main__":
    try:
        app = styleMatch()
        app.launch(share=True, debug=True)
    except Exception:
        print("gradio execution failed")