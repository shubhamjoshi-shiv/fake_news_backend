from django.apps import AppConfig
import pickle


class CompaniesConfig(AppConfig):
    name = 'companies'
    trained_model = pickle.load(open('static/finalized_model.sav', 'rb'))
