import os
from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load the model once
MODEL_PATH = os.path.join(settings.BASE_DIR, 'model/model.h5')
model = load_model(MODEL_PATH)

def index(request):
    prediction = None
    predictions = []

    if request.method == 'POST' and request.FILES.get('digit_image'):
        img_file = request.FILES['digit_image']

        # Save uploaded image temporarily
        img_path = os.path.join(settings.MEDIA_ROOT, img_file.name)
        with open(img_path, 'wb+') as f:
            for chunk in img_file.chunks():
                f.write(chunk)

        # Preprocess image
        img = Image.open(img_path).convert('L').resize((28, 28))
        img_array = np.array(img) / 255.0
        img_array = img_array.reshape(1, 28, 28, 1)

        # Predict
        pred_probs = model.predict(img_array)[0]  # shape: (10,)
        prediction = int(np.argmax(pred_probs))

        # Build full list of predictions
        predictions = [(i, round(pred_probs[i] * 100, 2)) for i in range(10)]

        # Optionally delete image
        # os.remove(img_path)

    return render(request, 'predictor/index.html', {
        'prediction': prediction,
        'predictions': predictions
    })
