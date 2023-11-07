# -*- coding: utf-8 -*-
"""montly_birth.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19gOBY-fpbRrff7VdDDuUIz_VnCHtBOwD

# ***GDP가 출산율과 출생률에 미치는 영향***

# 라이브러리 불러오기
"""

# Commented out IPython magic to ensure Python compatibility.
# 라이브러리 불러오기
import numpy as np
import pandas as pd
import mpld3
import matplotlib.pyplot as plt

# %matplotlib inline

"""# 데이터 전처리

## 데이터셋 불러오기
"""

df = pd.read_csv("./world-data-2023.csv")
df.head(5)

"""## 데이터셋 열의 데이터형 확인하기"""

df.dtypes

"""## 처리해야 할 결측치 값 존재 확인하기
### .isnull() 함수로 열에 존재하는 null 값을 .sum() 함수로 개수 세기
"""

df.isnull().sum()

"""## 결측치 정리하기
### .fillna(n) 함수를 이용해 NaN 값 n으로 변경해주기
"""

df = df.fillna(0)
df.isnull().sum()

"""## object 데이터 GDP를 int 형으로 바꿔 주기
### 1) 형 변환이 쉽게 GDP 열만 꺼내서 새로운 데이터프레임 만들기
"""

gdp_df = df['GDP']
gdp_df

"""### 2) .astype(x) 함수로 데이터 형태 x로 바꾸기
### 3) .str.replace(x, y) 함수로 해당 데이터 내에 있는 x 문자를 y 문자로 바꿔 주기
### 4) 형 변환 마친 데이터 열 원래의 데이터로 넣어 주기
"""

gdp_df = gdp_df.astype('str')
gdp_df = gdp_df.str.replace(',', '')
gdp_df = gdp_df.str.replace('$', '')
gdp_df = gdp_df.astype('int64')
gdp_df
df["GDP"] = gdp_df
df["GDP"]

"""## 그래프에 사용될 값들만 꺼내 새로운 데이터프레임 만들기
### 1) 'Birth Rate', 'Fertility Rate', 'Unemployment rate', 'GDP'만 모은 데이터프레임 만들기
### 2) 'Unemployment rate' 열과 새로운 데이터프레임 데이터 형 변환하기
### 3) 사용할 새로운 데이터프레임 'new'에 'Country' 열 추가하기
"""

new_df = df[['Birth Rate', 'Fertility Rate', 'Unemployment rate', 'GDP']]
new = new_df.fillna(0)
new['Unemployment rate'] = new['Unemployment rate'].astype('str')
new['Unemployment rate'] = new['Unemployment rate'].str.replace('%', '')
new = new.astype(float)
new["GDP"] = df["GDP"].astype('int64')
new.loc[:,'Country'] = df['Country']
new

"""# 그래프 그리기
## GDP 상위/하위 20위에 따른 출산율 비교하기 (Birth Rate: Highest GDP / Birth Rate: Lowest GDP)
### 1) .sort_values() 함수를 이용해 GDP 상위/하위 20위 데이터프레임 만들기
"""

gu_df = new.sort_values(by = 'GDP', ascending = False).head(20)
gd_df = new.drop(150, axis=0).sort_values(by = 'GDP', ascending = False).tail(20)   # 해당 열 Country 값이 깨져서 drop() 함수로 삭제 후 sort 진행

gd_df

"""### 2) .subplot() 함수를 이용해 x축이나 y축을 공유하는 그래프로 만들기
### 3) .xticks(rotation=90) 함수를 이용해 x축 라벨을 90도로 꺾어서 가독성 높이기
"""

ax1 = plt.subplot(1, 2, 1)
plt.plot(gu_df['Country'], gu_df['Birth Rate'], '.-')
plt.title('Birth Rate: Highest GDP')
plt.xlabel('Top 20 Countries')
plt.ylabel('Birth Rate')
plt.xticks(rotation=90)

ax2 = plt.subplot(1, 2, 2, sharey=ax1)
plt.plot(gd_df['Country'], gd_df['Birth Rate'], '.-')
plt.title('Birth Rate: Lowest GDP')
plt.xlabel('Top 20 Countries')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()

"""## GDP에 따른 출산율/출생률 비교하기 (Birth Rate/Fertility Rate vs GDP, Top 20 Countries (without US&China))
### 1) 상위 gdp 값 확인하기
"""

gu_df

"""### 2) 그래프의 가시성을 위해 상위 값 중 극단적으로 높은 두 값(US&China) drop하기"""

re_df = df.drop(index=186)
re_df = re_df.drop(index=36)

"""### 3) .scatter() 함수를 이용해 산점도로 그래프 그리기
### 4) x 축을 GDP로 공유하고, y 축에 출산율과 출생률 두기
"""

plt.figure(figsize=(10, 6))
plt.scatter(re_df['GDP'], re_df['Birth Rate'], color='green', alpha=0.5, label='Birth Rate')
plt.scatter(re_df['GDP'], re_df['Fertility Rate'], color='red', alpha=0.5, label='Fertility Rate')
plt.title('Birth Rate/Fertility Rate vs GDP, Top 20 Countries (without US&China)')
plt.xlabel('GDP')
plt.ylabel('Fertility Rate / Birth Rate')
plt.legend()
plt.show()

"""## 글로벌 지도 상의 산점도를 통해 국가별 출산율 비교하기 (Birth Rate of Countries)
### 1) geopandas와 shapely.geometry를 통해 파이썬에서 제공하는 지도 그래프 만들기
### 2) 지도 그래프 위로 출산율을 산점도로 나타내기
"""

import geopandas as gpd
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]   # 데이터셋에 있는 위도/경도 열을 불러와 지도 그래프 위에 point(점) 찍기
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')          # 제공해주는 지도 데이터프레임 이용하기

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
fig, ax = plt.subplots(figsize=(10, 6))

world.plot(ax=ax, color='lightgrey', edgecolor='black')

scatter = plt.scatter(x = df['Longitude'], y = df['Latitude'], s = df["Birth Rate"]**2, c='#fd1132',  alpha=0.2)    # 출산율 산점도로 표시하기(s(size) 값 제곱으로 해 크기에 확실한 차이 두기)

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['Country']):
    if label in ['United States of America', 'Canada', 'Russia',
                 'China', 'Australia','Pakistan','India','Brazil', 'Kazakhstan','Algeria', 'Saudi Arabia']:         # 지도 그래프 위에 주요 국가 이름 표시하기
        ax.text(x, y, label.split(' ')[0], fontsize=8, ha='right', color='black', weight='bold', alpha=0.9)
    else:
        ax.text(x, y, '', fontsize=8, ha='right', color='darkslategrey', weight='bold', alpha=0.7)

plt.title('Birth Rate of Countries', fontsize=16, fontweight='bold')

plt.show()

