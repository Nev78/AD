# Лабараторна робота №3
# Наука про дані: обмін результатами та початковий аналіз
## Невмержицька Дар'я ФБ-23
### Мета роботи: ознайомитися з системою контролю версій GitHub, навчитися створювати прості веб-додатки для обміну результатами досліджень із використанням модуля spyre.
### Хід роботи:

# Імпортуємо сервер та бібліотеки
from spyre import server
import pandas as pd
import lab2
import matplotlib.pyplot as plt

# Отримуємо датасет з lab2
DATASET = lab2.get_dataset()
print(DATASET.head())

class StockExample(server.App):
    title = "NOAA data visualization"
    # Налаштування вхідних даних 
    inputs = [{
        "type": 'dropdown',
        "label": 'NOAA data dropdown',
        "options": [
            {"label": "VCI", "value": "VCI"},
            {"label": "TCI", "value": "TCI"},
            {"label": "VHI", "value": "VHI"}
        ],
        "key": 'ticker1',
        "action_id": "update_data"
    },
    {
        "type": 'dropdown',
        "label": 'Area',
        "options": [
            {"label": "Вінницька", "value": "1"},
            {"label": "Волинська", "value": "2"},
            {"label": "Дніпропетровська", "value": "3"},
            {"label": "Донецька", "value": "4"},
            {"label": "Житомирська", "value": "5"},
            {"label": "Закарпатська", "value": "6"},
            {"label": "Запорізька", "value": "7"},
            {"label": "Івано-Франківська", "value": "8"},
            {"label": "Київська", "value": "9"},
            {"label": "Кіровоградська", "value": "10"},
            {"label": "Луганська", "value": "11"},
            {"label": "Львівська", "value": "12"},
            {"label": "Миколаївська", "value": "13"},
            {"label": "Одеська", "value": "14"},
            {"label": "Полтавська", "value": "15"},
            {"label": "Рівенська", "value": "16"},
            {"label": "Сумська", "value": "17"},
            {"label": "Тернопільська", "value": "18"},
            {"label": "Харківська", "value": "19"},
            {"label": "Херсонська", "value": "20"},
            {"label": "Хмельницька", "value": "21"},
            {"label": "Черкаська", "value": "22"},
            {"label": "Чернівецька", "value": "23"},
            {"label": "Чернігівська", "value": "24"},
            {"label": "Республіка Крим", "value": "25"}
        ],
        "key": 'ticker2',
        "action_id": "update_data"
    },
    {
        "type": 'text',
        "label": 'Range of weeks',
        "value": '1-10',
        "key": 'range',
        "action_id": "update_data"
    },
    {
        "type": 'text',
        "label": 'Range of years',
        "value": '1982-2024',
        "key": 'year_range',
        "action_id": "update_data"
    }
    ]
    # Налаштування кнопки керування 
    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Update Data"
    }]
    # Налаштування вкладок
    tabs = ["Plot", "Table"]
    # Налаштування вихідних даних
    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]
    # Oтримання даних
    def getData(self, params):
        range_w = params['range']
        ranges = range_w.split('-')
        ranges = [int(ranges[0]), int(ranges[1])]
        
        year_range = params['year_range']
        year_ranges = year_range.split('-')
        year_ranges = [int(year_ranges[0]), int(year_ranges[1])]
        
        ticker1 = params['ticker1']
        ticker2 = params['ticker2']
        # Фільтруємо датасет на основі вибраних параметрів
        df = DATASET.loc[(DATASET['area'] == ticker2) &
                         (DATASET['Week'] <= ranges[1]) &
                         (DATASET['Week'] >= ranges[0]) &
                         (DATASET['Year'] >= year_ranges[0]) &
                         (DATASET['Year'] <= year_ranges[1]),
                         [ticker1, "Week", "Year"]]
        print(df)
        return df


    def getPlot(self, params):
        ticker1 = params['ticker1']
        df = self.getData(params)[[ticker1, "Year"]]
        # Фільтруємо датасет на основі вибраних параметрів
        
        
        
        df = df.set_index('Year')
        plt_obj = df.plot()
        df.plot(style='o', color='red', ax=plt_obj) 

        plt_obj.set_xlabel("Year")
        plt_obj.set_ylabel(ticker1)

        fig = plt_obj.get_figure()
        return fig


app = StockExample()
app.launch(port=8080)
