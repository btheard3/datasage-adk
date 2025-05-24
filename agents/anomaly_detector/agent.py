# agents/anomaly_detector/agent.py

class AnomalyDetectorAgent:
    def detect(self, **kwargs):
        return {
            "anomaly": "Spending spike detected in Q2. Investigate insurance billing practices.",
            "input_params": kwargs
        }
