import random
import numpy as np


class DataAnalyzer:
    def __init__(self, random_data):
        random.seed(1)
        self.random_data = random_data

        # Set upper and lower limit to 3 standard deviation
        self.std = np.std(self.random_data)
        self.mean = np.mean(self.random_data)
        self.anomaly_cut_off = self.std * 2.3

        self.lower_limit = self.mean - self.anomaly_cut_off
        self.upper_limit = self.mean + self.anomaly_cut_off

    def find_anomalies(self):
        anomalies = []
        for i, outlier in enumerate(self.random_data):
            if outlier < self.lower_limit or outlier > self.upper_limit:
                anomalies.append((i, outlier))
        return anomalies
