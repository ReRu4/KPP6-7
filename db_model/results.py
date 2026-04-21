from datetime import datetime, timezone
import base64
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime

Base = declarative_base()


class Predictions(Base):
    __tablename__ = 'Predictions'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=True)           # Оригинальное имя файла
    image_data = Column(Text, nullable=False)               # Изображение в base64
    predicted_class = Column(String(50), nullable=False)    # Предсказанный класс
    confidence = Column(Float, nullable=False)              # Уверенность
    probabilities_circle = Column(Float, nullable=True)     # Вероятность круга
    probabilities_square = Column(Float, nullable=True)     # Вероятность квадрата
    probabilities_triangle = Column(Float, nullable=True)   # Вероятность треугольника
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Время создания

    def __init__(self, filename, image_data, predicted_class, confidence,
                 probabilities_circle, probabilities_square, probabilities_triangle):
        """
        Прямой инициализатор с явными параметрами
        """
        self.filename = filename
        self.image_data = image_data
        self.predicted_class = predicted_class
        self.confidence = confidence
        self.probabilities_circle = probabilities_circle
        self.probabilities_square = probabilities_square
        self.probabilities_triangle = probabilities_triangle

    def __repr__(self):
        """Строковое представление объекта"""
        return (f"<Prediction(id={self.id}, filename='{self.filename}',"
                f" class='{self.predicted_class}', confidence={self.confidence:.2%})>")

    @staticmethod
    def image_to_base64(image_bytes):
        """Конвертирует изображение в base64 строку"""
        return base64.b64encode(image_bytes).decode('utf-8')

    @staticmethod
    def base64_to_image(base64_str):
        """Конвертирует base64 строку обратно в байты"""
        return base64.b64decode(base64_str.encode('utf-8'))
