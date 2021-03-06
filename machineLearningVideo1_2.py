import matplotlib.pyplot  as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()
clf=svm.SVC(gamma=0.0001,C=100)

print(len(digits.data))

x, y = digits.data[:-10], digits.data[:-10]
clf.fit(x, y)

print("prediction: ",clf.predict(digits.data[-6]))
plt.imshow(digits.images[-6], cmap=plt.cm.gray_r, interpolation="nearest")

plt.show()