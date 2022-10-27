import pandas as pd

# Убрать из файла квадратные скобки, так как в дальнейшем они мешают обработке данных
file = open('events.log', 'r')
data = file.read()
data = data.replace('[', '').replace(']', '')
file.close()
file = open('events.log', 'w')
file.write(data)
file.close()

# Преобразовать файл в формат pandas, создать столбцы date, time, status
df = pd.read_csv('events.log', sep=" ", header=None)
df.columns = ["date", "time", "status"]
# Создать новый столбец datetime, убрать лишние столбцы, переместить datetime на 1е место
df["datetime"] = df["date"] + ' ' + df["time"]
df = df.drop(df.columns[[0, 1]], axis=1)
new_col = ["datetime", "status"]
df = df[new_col]
# Преобразовать столбец datetime в формат данных - дата
df.datetime = pd.to_datetime(df.datetime)

# Сгруппировать время по минутам, посчитать количество NOK и OK за каждую минуту
counts = (df.groupby(df['datetime'].map(lambda x: x.replace(second=0)))['status']
          .value_counts()
          .unstack(fill_value=0)
          .reset_index()
          )
# Вывести количество только NOK за каждую минуту
print(counts[['datetime', 'NOK']])
