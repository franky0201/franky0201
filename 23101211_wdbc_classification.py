import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
from sklearn.ensemble import RandomForestClassifier  
from matplotlib.lines import Line2D

def load_wdbc_data(filename):
    class WDBCData:
        data          = []  # Shape: (569, 30)
        target        = []  # Shape: (569, )
        target_names  = ['malignant', 'benign']
        feature_names = [
            'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 
            'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
            'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 
            'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
            'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 
            'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension'
        ]
    
    wdbc = WDBCData()
    with open(filename) as f:
        for line in f.readlines():
            items = line.strip().split(',')
            wdbc.target.append(0 if items[1] == 'M' else 1)  # TODO #1: "M"을 0, 다른 값은 1로 설정
            wdbc.data.append([float(i) for i in items[2:]])  # TODO #1: 30개의 속성을 실수형으로 변환하여 추가
    
    wdbc.data = np.array(wdbc.data)
    wdbc.target = np.array(wdbc.target)
    return wdbc

if __name__ == '__main__':
    # 데이터셋 로드
    wdbc = load_wdbc_data('C:/Users/Administrator/Downloads/ml01_lab/data/wdbc.data')  # TODO #1: 'load_wdbc_data()' 함수 구현

    # 모델 훈련
    model = RandomForestClassifier(random_state=42)  # TODO #2: 더 나은 분류기 사용 (RandomForestClassifier)
    model.fit(wdbc.data, wdbc.target)

    # 모델 테스트
    predict = model.predict(wdbc.data)
    accuracy = metrics.balanced_accuracy_score(wdbc.target, predict)

    # 혼동 행렬 시각화
    cm = metrics.confusion_matrix(wdbc.target, predict)
    disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=wdbc.target_names)
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix')
    plt.show()

    # 테스트 결과 시각화
    cmap = np.array([(1, 0, 0), (0, 1, 0)])
    clabel = [Line2D([0], [0], marker='o', lw=0, label=wdbc.target_names[i], color=cmap[i]) for i in range(len(cmap))]
    for (x, y) in [(0, 1)]:  # [(i, i+1) for i in range(0, 30, 2)]도 가능
        plt.figure()
        plt.title(f'My Classifier (Accuracy: {accuracy:.3f})')
        plt.scatter(wdbc.data[:, x], wdbc.data[:, y], c=cmap[wdbc.target], edgecolors=cmap[predict])
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
    plt.show()
