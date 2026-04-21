import base64
import io

import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
from sqlalchemy import select
from PIL import Image

from db_model.results import Predictions
from database.database import db_session, init_db, engine
from model import nn

app = Flask(__name__)

# Инициализируем базу данных
init_db()

# Загружаем модель при старте
model = nn.get_model()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Проверяем, есть ли файл в запросе
            if 'file' not in request.files:
                return jsonify({'error': 'Файл не найден'}), 400

            file = request.files['file']

            # Проверяем, выбран ли файл
            if file.filename == '':
                return jsonify({'error': 'Файл не выбран'}), 400

            # Читаем файл
            image_bytes = file.read()

            # Открываем изображение
            img = Image.open(io.BytesIO(image_bytes)).convert('L')
            img = img.resize((20, 20))

            # Предобработка
            img_array = np.array(img) / 255.0
            img_flattened = img_array.flatten().reshape(1, -1)

            # Предсказание
            predictions = model.predict(img_flattened, verbose=0)[0]

            # Классы
            classes = ['circle', 'triangle', 'square']
            class_index = np.argmax(predictions)
            confidence = float(predictions[class_index])
            predicted_class = classes[class_index]

            print(predictions)

            # СОХРАНЯЕМ В БАЗУ ДАННЫХ
            # Конвертируем изображение в base64 для сохранения
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            # Создаём запись в БД
            new_prediction = Predictions(
                filename=file.filename,
                image_data=image_base64,
                predicted_class=predicted_class,
                confidence=confidence,
                probabilities_circle=float(predictions[0]),   # круг
                probabilities_square=float(predictions[2]),   # квадрат
                probabilities_triangle=float(predictions[1])  # треугольник
            )

            # Сохраняем в базу
            db_session.add(new_prediction)
            db_session.commit()

            # Возвращаем JSON для JavaScript
            return jsonify({
                'class': predicted_class,
                'confidence': confidence
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # GET запрос — показываем страницу
    return render_template('index.html')


@app.route('/history', methods=['GET'])
def history():
    stmt = select(Predictions).order_by(Predictions.id.desc())
    predictions = db_session.execute(stmt).scalars().all()
    db_session.commit()
    return render_template('history.html', predictions=predictions)


@app.route('/image/<int:prediction_id>')
def get_image(prediction_id):
    #Возвращает изображение по ID предсказания
    prediction = db_session.query(Predictions).get(prediction_id)
    if prediction and prediction.image_data:
        # Декодируем base64 в байты
        image_bytes = base64.b64decode(prediction.image_data)
        return send_file(
            io.BytesIO(image_bytes),
            mimetype='image/png',
            as_attachment=False
        )
    return "Image not found", 404


# Закрывать сессию
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
