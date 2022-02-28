import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from myConvexHull import *
from sklearn import datasets

# Print pilihan dataset
print("Berikut pilihan dataset yang bisa digunakan: ")
print("1. Iris plants dataset")
print("2. Wine recognition dataset")
print("3. Breast cancer wisconsin (diagnostic) dataset")

# Prompt user memasukan integer berdasarkan pilihan dataset
try: 
    pick_dataset = int(input(f"\nMasukan 1, 2, atau 3 berdasarkan dataset yang ingin digunakan: "))
except:
    print(f"Tipe data harus integer, silahkan masukan ulang\n")

while(True):
    if(pick_dataset == 1 or pick_dataset == 2 or pick_dataset == 3):
        break
    else:
        try:
            print("Input kamu tidak sesuai, silakan kembali masukan input")
            pick_dataset = int(input(f"Masukan 1, 2, atau 3 berdasarkan dataset yang ingin digunakan: "))
            print(f"\n")
        except:
            print(f"Tipe data harus integer, silahkan masukan ulang\n")

# Meload dataset berdasarkan pilihan user
if(pick_dataset == 1):
    data = datasets.load_iris()
elif(pick_dataset == 2):
    data = datasets.load_wine()
elif(pick_dataset == 3):
    data = datasets.load_breast_cancer()

df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)

plt.figure(figsize = (10, 6))
colors = ['b','r','g', 'c', 'm', 'y', 'k', 'w']

# Menampilkan tiap feature dari dataset yang dipilih
for i in range(len(data.feature_names)):
    print(f"{i + 1}. {data.feature_names[i]}")

# Memprompt user memasukkan feature yang akan menjadi nilai pada sumbu-x dan sumbu-y
featureX = int(input(f"Masukan angka sebagai nilai pada sumbu-x (rentang 1 - {len(data.feature_names)}): "))
featureY = int(input(f"Masukan angka sebagai nilai pada sumbu-y (rentang 1 - {len(data.feature_names)}): "))

# Membuat plotting hasil
name1 = data.feature_names[featureX - 1]
name2 = data.feature_names[featureY - 1]
plt.title(name1 + " vs " + name2)
plt.xlabel(name1)
plt.ylabel(name2)

for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[featureX - 1, featureY - 1]].values
    lp, rp = leftestRightest(bucket)
    hull = convexHull(bucket, lp, rp)
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    for simplex in hull:
        plt.plot(simplex[0], simplex[1], colors[i])

namaFile = input("Masukan nama file untuk menyimpan hasil: ")
plt.savefig(f"../output/{namaFile}.jpg", bbox_inches='tight')
plt.legend()
plt.show()