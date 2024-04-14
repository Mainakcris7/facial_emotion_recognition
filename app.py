from flask import Flask, url_for, request, redirect, render_template, jsonify
from PIL import Image
import cv2
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)
model = load_model("./models/model_conv2d.keras")   # Load the trained model

label_dict = {
    0: 'angry',
    1: 'disgusted',
    2: 'fearful',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprised'
}


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            img = request.files['image']
            img = Image.open(img)
            img = np.asarray(img)
            print(img.shape)
            try:    # To handle if the image is already in grayscale format
                # The model was trained on 48x48 grayscale images
                img = cv2.resize(img, (48, 48))
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            except:
                pass
            img = np.expand_dims(img, axis=-1)   # For channel
            img = np.expand_dims(img, axis=0)    # For batch
            res = model.predict(img)   # Getting prediction
            res = np.argmax(res, axis=1)
            res = label_dict[int(res[0])]   # Getting class name
            if res == 'angry':
                return jsonify(f"Predicted emotion: {res.title()} 😡")
            elif res == 'disgusted':
                return jsonify(f"Predicted emotion: {res.title()} 🤮")
            elif res == 'fearful':
                return jsonify(f"Predicted emotion: {res.title()} 😨")
            elif res == 'happy':
                return jsonify(f"Predicted emotion: {res.title()} 😀")
            elif res == 'neutral':
                return jsonify(f"Predicted emotion: {res.title()} 😐")
            elif res == 'sad':
                return jsonify(f"Predicted emotion: {res.title()} 😥")
            elif res == 'surprised':
                return jsonify(f"Predicted emotion: {res.title()} 😮")
        except:
            return jsonify("Something went wrong !")
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(port=8080, debug=True)
