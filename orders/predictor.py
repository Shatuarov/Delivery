# orders/predictor.py
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
from django.conf import settings
from .services import DeliveryDataService

class DeliveryIssuePredictor:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(settings.BASE_DIR, 'models', 'delivery_issue_model.pkl')
        self.data_service = DeliveryDataService()

    def train_model(self):
        """
        Обучает модель на исторических данных.
        """
        X, y = self.data_service.prepare_training_data()
        if len(X) < 2:
            print("Недостаточно данных для обучения модели")
            return False

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)

        # Сохраняем модель
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        return True

    def load_model(self):
        """
        Загружает модель из файла.
        """
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            return True
        return False

    def predict(self, order):
        """
        Предсказывает вероятность проблемы с заказом.
        """
        if not self.model:
            if not self.load_model():
                self.train_model()

        if not self.model:
            return {"status": "error", "message": "Модель не готова"}

        features = self.data_service.prepare_features(order)
        X = [[
            features['item_count'],
            features['total_price'],
            features['hour_of_day'],
            features['distance'],
            features['duration'],
            features['temperature'],
            features['precipitation'],
            features['is_rainy']
        ]]
        probability = self.model.predict_proba(X)[0][1]  # Вероятность проблемы
        prediction = self.model.predict(X)[0]  # 1 - есть проблема, 0 - нет

        return {
            "status": "success",
            "has_issue": bool(prediction),
            "probability": float(probability),
            "features": features
        }