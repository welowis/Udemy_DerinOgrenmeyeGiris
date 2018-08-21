# -*- coding: utf-8 -*-
"""Titanic_Veri_Gorsellestirme.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ET6xL3NPCIlNuwK8hKsOZkl-YV9LhUMt

# **TITANIC Verisi için Python'da Veri Görselleştirme**


---

Kaynak:[Pandas & Seaborn - A guide to handle & visualize data in Python](https://)


---


[<img align="left" width="100" height="100" src="http://www.i2symbol.com/images/symbols/style-letters/circled_latin_capital_letter_a_u24B6_icon_128x128.png">](https://www.ayyucekizrak.com/)
[<img align="right" width="200" height="50"  src="https://raw.githubusercontent.com/deeplearningturkiye/pratik-derin-ogrenme-uygulamalari/944a247d404741ba37b9ef74de0716acff6fd4f9/images/dltr_logo.png">](https://deeplearningturkiye.com/)

**Colab **için kimlik doğrulama işlemleri...
"""

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}
!mkdir -p drive
!google-drive-ocamlfuse drive

!mkdir -p drive
!google-drive-ocamlfuse drive

import os
os.chdir("/content/drive/Udemy_DerinOgrenmeyeGiris/Titanic Gorsellestirme ve Siniflama")
!pwd

"""Neden **Pandas** kütüphanesi kullanıyoruz? Çünkü **NumPy** üzerinde inşa edilmiştir. Manipülasyon ve analiz için daha yüksek seviyeli yöntemler sağlamak için çok boyutlu dizileri ve hızlı operasyonları dahili olarak kullanır. **Seaborn**'u da ***Titatic*** verisini çekmek için kullanıyoruz."""

import numpy as np
import pandas as pd
import seaborn as sns
import timeit

# Veri kümseini yükle
titanic = sns.load_dataset('titanic')

"""### Veri setine bir gözatalım :)"""

titanic.info()

"""### *Örnek bir sorgu yapalım* ve aynı cinsiyet grubuna ait 1. ve 3. sınıf ve yaşamıyor olan yolcuların bilet ücretlerini, yolculukta yalnız olup olmadıklarını, hangi şehirden olduklarını gözlemleyelim."""

titanic[
    (titanic.sex == 'female')
    & (titanic['class'].isin(['First', 'Third']))
    & (titanic.age > 30)
    & (titanic.survived == 0)
]

"""Veriden bir grup çekelim: Hangi ülke ve şehirden geldikleri bilgisi olsun."""

# Datadan küçük bir parça çekelim, yaşadıkları şehir, şehirde yaşadıkları süre ve şehir yaşı bilgileri olsun
towns_dic = {
    'name': ['Southampton', 'Cherbourg', 'Queenstown', 'Montevideo'],
    'country': ['United Kingdom', 'France', 'United Kingdom', 'Uruguay'],
    'population': [236900, 37121, 12347, 1305000],
    'age': [np.random.randint(500, 1000) for _ in range(4)]
}
towns_df = pd.DataFrame(towns_dic)

(titanic.merge(
  towns_df, 
  left_on='embark_town', right_on='name', 
  how='left',
  indicator=True,
  suffixes=('_passenger', '_city')
)).head()
# 'head' takes the last n elements of the DataFrame

"""**distplot:** Verilerinizi keşfederken görmek istediğiniz ilk şey, değişkenlerinizin dağılımıdır. 
Örneğin, Titanic’in yolcularının yaş dağılımını görelim.
"""

sns.distplot(titanic.age.dropna())
sns.plt.show()

"""**FacetGrid:** Bir grafiği (örneğin sonuncusu) bazı kategorilerden ayırmak isteyebiliriz!"""

g = sns.FacetGrid(titanic, row='survived', col='class')
g.map(sns.distplot, "age")
sns.plt.show()

"""**jointplot:** Bu metot, veri değişkenlerinin hem dağılımları hem de çekirdek yoğunluğu tahmin edicileri ve verilere uyan bir opsiyonel regresyon ile birlikte iki değişkene göre görüntülenmesi için kullanılır. **Reg** ile, verilere uygun bir regresyon istediğimizi belirtiyoruz.
Bu durumda, regresyonun gösterdiği yukarı doğru küçük bir eğilim olduğu görünse de, ***Pearson korelasyon katsayısı*** ile gösterildiği gibi *“yaş”* ve *“ücret”* değişkenleri arasında hemen hemen hiçbir ilişki yoktur.
"""

sns.jointplot(data=titanic, x='age', y='fare', kind='reg', color='g')
sns.plt.show()

"""Son olarak bir veri ile ilgili oluşturulabilecek en havalı şey korelasyon matrisidir :)
Sütunlarının tüm çiftleri arasındaki Pearson'ları (bir başka  yöntem de olabilir) korelasyon katsayısını hesaplayan bir düzeltme yöntemine sahiptir.
"""

df = titanic.pivot_table(index='embark_town', columns='age_group', values='fare', aggfunc=np.median)
sns.heatmap(df, annot=True, fmt=".1f")