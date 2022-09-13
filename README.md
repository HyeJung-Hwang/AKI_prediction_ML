# Acute Kidney Injury Detection from Bio-Signals using Machine Learning

## Overview

Acute Kidney Injury 는 급성 신장 손상으로 , 신장에서 혈액에서 노폐물을 걸러내는 능력이 급격하게 감소하는 증상입니다. 급성증상이지만, 악화되는 속도가 빠르고 만성 신부전으로 이어질 수 있는 질병입니다. 
기존의 Acute Kidney Injury 진단의 경우 , blood test 기반으로 이루어지는데 , 진단 시간이 소요되고 , 환자의 경우에 소변검사나, 초음파검사등의 따라 추가 검사를 진행하기도 하여 번거롭고 진단까지 시간이 소요됩니다.
그래서 기존 방식을 대체하여 머신러닝 활용하여 시간을 단축시켜 예측이 필요합니다. 그리고 , 환자의 바이오 데이터와 Acute Kidney Injury 발병사이에는 인과관계가 복잡한데 이 복잡한 인과관계의 경우, 머신러닝을 활용하여 예측하는 것이 필요합니다.

## My Goal

제가 하고자하는 머신러닝을 활용한 Acute Kidney Injury 발병 예측의 목표는 다음과 같습니다.
환자의 심전도 데이터나 , 혈압데이터 , 산소포화도 등의 bio signal을 인풋으로 들어오는 환자가 Acute Kidney Injury normal 이면 0 , malignant 이면 1을 예측하는 Acute Kidney Injury detection 함수 f 를 찾는 것입니다. 

![image](https://user-images.githubusercontent.com/79091824/188569040-b1c7d54e-cc9a-441b-9f34-e0792da1cdb5.png)

## Machine Learning-based Acute Kidney Injury Detection

머신러닝 기반 Acute Kidney Injury detection 의 프로세스는 아래 사진과 같습니다. 수술중인 환자에게 Acute Kidney Injury 가 발생했을 때 , 신체 이상이 생기면  biosignal의 변화가 생길 것이고 , 인공지능을 활용하여 이 변화를 감지하면 , Acute Kidney Injury 발생 예측이 가능할 것입니다. 바이오 시그널의 변화는 highly complex 하여 머신러닝으로의 예측을 하고자 했습니다.

![image](https://user-images.githubusercontent.com/79091824/188569104-a9e8b1ad-baf8-4a9f-a344-55d5d2b887b1.png)

## Raw Data

예측에 활용할 raw dataset 은 다음과 같습니다. 총 1568 명의 환자가 있고, Acute Kidney Injury 가 음성인 환자는 1463명 , 123 명이고 환자당 약 x 개의 bio signal 이 있습니다.
Vital Data와 Non-Vital Data로 나눌 수 있고 이때 , Vital Data의 경우 500 Hz 로 high resolution이었습니다.

![image](https://user-images.githubusercontent.com/79091824/188571900-4bdbf0c2-2df3-45a1-8c04-fd01668612ac.png)

## Data Refinement 

### 1️⃣ Vital Sign 종류 선정 -> Blood Pressure Data

논문에서 확인한 , 환자의 혈압과 Acute Kidney Injury 발생의 연관성을 바탕으로 , mean blood pressure ,  systolic blood pressure , diastolic blood pressure 총 3가지 혈압데이터를 사용하기로 결정하였습니다. 혈압 데이터의 경우 ,  dimension 이 약 30000으로 커서 , 차원을 줄이는 것이 필요했습니다.

### 2️⃣ Vital sign Data -> 1 factor

vital sign data를 1개의Factor로 줄이는 Refinement를 진행했습니다.
Ratio 와 Average Real Variability , 총 2 종류의 Factor를 구하여 사용하였습니다.

- **Ratio ( R )**

![image](https://user-images.githubusercontent.com/79091824/188573224-3f9ab7d4-bcc9-4628-9113-7cc7561b8f9a.png)

- **Average Real Variability ( ARV )**

![image](https://user-images.githubusercontent.com/79091824/188573284-cb0557ee-ce0d-4a21-b7a1-b4aaa9b537e0.png)

### 3️⃣ Random Over Sampling

Raw Dataset의 경우 , Acute Kidney Injury가 양성인 환자와 음성인 환자의 비율이 
약 12 : 1로 불균형이 심하여 , train set에 대해 , Random Over Sampling을 진행하여 
Data Imbalance Problem을 해결하고자 했습니다.

## Data

앞서 구한 R ( Ratio ) 와 ARV ( Average Real Variability ) 와 Non-Vital Data
를 최종 데이터셋으로 사용하였습니다.

![image](https://user-images.githubusercontent.com/79091824/188577172-57be505a-3ba8-4d99-b7cd-dca857965188.png)

## Models and Learning Parameter Setting

- XGBClassifier Model
- max_depth = 10 , n_estimators = 100 

## Results

auroc 가 0.703 ,  auprc 가 0.293 , sensitivity 가 0.58 , specificity가 0.77 , f1-score가 0.275 , accuracy가 0.759 로 나왔습니다.

![image](https://user-images.githubusercontent.com/79091824/189907345-bd55fd35-7b18-43df-8548-c88d797da39a.png)


## Conclusion & Discussion

낮은 모델의 성능에 대해 분석해본 결과 , 제 application 의 3가지 문제점을 낮은 모델의 성능으로 꼽을 수 있었습니다.

첫 번째로 , Data Imbalance Problem 을 완전히 해결하지 못했습니다. Random Over Sampling 외에 Loss Ratio를 조절하는 방법을 사용해보고자 합니다.

두 번째로 , 학습 Feature 개수의 부족입니다. 본 application 과 유사하게 ,  Bio-Signals를 기반으로 Acute Kidney Injury를 예측하는 타 논문의 경우 , 78 개의 feature를 사용한 것을 참고하여 , 추가 feature 를 사용하고자 합니다.

세 번째로 , vital sign 의 시계열적 특성을 살리기 위한 딥러닝 approach 를 사용해보고자합니다.

## Reference 
- [Predicting Acute Kidney Injury via Interpretable
Ensemble Learning and Attention Weighted
Convoutional-Recurrent Neural Networks]( https://engineering.jhu.edu/nsa/wp-content/uploads/2021/02/YPeng_CISS_2021_preprint.pdf )
- [Vital DB Examples ]( https://github.com/vitaldb/examples/blob/master/comments_in_Korean/mbp_aki.ipynb )


