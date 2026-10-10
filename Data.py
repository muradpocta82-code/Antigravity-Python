import re
import pandas as pd

raw_document = """
ТРАНСПОРТНАЯ НАКЛАДНАЯ № ЖД-88492
Отправитель: ООО "ТехноПром", г. Москва
Получатель: ЗАО "УралСтиль", г. Екатеринбург
Номер вагона: 52890144
Масса груза: 45 тонн
Груз: Стальные трубы
"""


def extract_entities(text):
  data = {}
  data['doc_id'] = (
      re.search(r'НАКЛАДНАЯ №\s*([\w-]+)', text).group(1)
      if re.search(r'НАКЛАДНАЯ №\s*([\w-]+)', text)
      else None
  )
  data['sender'] = (
      re.search(r'Отправитель:\s*(.+)', text).group(1).strip()
      if re.search(r'Отправитель:\s*(.+)', text)
      else None
  )
  data['vagon_number'] = (
      re.search(r'Номер вагона:\s*(\d+)', text).group(1)
      if re.search(r'Номер вагона:\s*(\d+)', text)
      else None
  )
  data['weight'] = (
      re.search(r'Масса груза:\s*(.+)', text).group(1).strip()
      if re.search(r'Масса груза:\s*(.+)', text)
      else None
  )
  return data


parsed_data = extract_entities(raw_document)
df = pd.DataFrame([parsed_data])

# СОХРАНЯЕМ В НАСТОЯЩИЙ EXCEL-ФАЙЛ (.xlsx)
df.to_excel('parsed_report.xlsx', index=False)

print('=== ТАБЛИЦА УСПЕШНО СОХРАНЕНА В parsed_report.xlsx ===')
print(df)