import streamlit as st
from PIL import Image
import io
import requests
import base64
import json
from streamlit_drawable_canvas import st_canvas

st.title("Hosted Digit Classification")
st.header("Upload or draw an image")

input_method = st.radio("Choose input method:", ["Upload Image", "Draw on Canvas"])


img_base64 = None
if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        # Convert image bytes to base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)


elif input_method == "Draw on Canvas":
    stroke_width = 30
    stroke_color = "#fff"
    bg_color = "#000"

    st.header("Draw A Digit")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=None,
        height=300,
        width=300,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data).astype("uint8"))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        st.download_button(
            label="Download Image",
            data=img_bytes,
            file_name="canvas_drawing.png",
            mime="image/png",
        )

if img_base64 and st.button("Identify Digit"):
    try:
        response = requests.post(
            "https://api-mnist-detection-196062113602.europe-west6.run.app/detect",
            json={"image": img_base64},
        )
        response = response.json()
        digit = response
        st.markdown(f"## The identified digit is **{digit}**")
    except Exception as e:
        st.error(f"Error sending image: {e}")
