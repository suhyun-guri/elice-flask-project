import pandas as pd
data = pd.read_csv('엘리스 도서관 책 정보 리스트.csv', header=0)

import os
data['img_path']='temp'
for i in range(1,len(data)+1):
    file = os.path.isfile(f"./static/image/{i}.png")
    if file:
        data["img_path"][i-1] = f"/image/{i}.png"
    else:
        data["img_path"][i-1] = f"/image/{i}.jpg"

import pymysql
con = pymysql.connect(host='localhost', user='root', password='0903', db='library')
cur = con.cursor()

for index, row in data.iterrows():
    data1 = (row['Unnamed: 0'], row['book_name'], row['publisher'], row['author'], row['publication_date'], row['pages'], row['isbn'], row['description'], row['link'], 5, 0, row['img_path'])
    # print(data1)
    cur.execute("INSERT INTO Book_info VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",data1)
    
con.commit()
con.close()