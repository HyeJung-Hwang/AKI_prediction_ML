import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, roc_auc_score, f1_score, precision_recall_curve, auc
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from collections import Counter

def train_test(df_path: str = "", save_path: str = "" ):
    df = pd.read_csv(df_path)
    y = df["AKI"].values.flatten()
    df = df.drop(['AKI'],axis = 1)
    x = df.values
    train_x, test_x, train_y, test_y = train_test_split(x , y, test_size = 0.3, random_state = 42)
    print('{} (event {:.1f}%) training, {} testing (event {:.1f} %) samples'.format(train_x.shape[0], np.mean(train_y) * 100 , test_x.shape[0], np.mean(test_y) * 100))
    ros = RandomOverSampler(random_state = 42)
    x_res , y_res = ros.fit_resample(train_x,train_y)
    print('before resample %s' % Counter(train_y))
    print('after resample %s' % Counter(y_res))
    model = xgb.XGBClassifier(
        objective="binary:logistic",
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(x_res , y_res)
    # model.save_model(save_path + f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.model")
    pred_y = model.predict_proba(test_x)[:, 1].ravel()

    fpr, tpr, thvals = roc_curve(test_y, pred_y)
    auroc = auc(fpr, tpr)
    precision, recall, _ = precision_recall_curve(test_y, pred_y)
    auprc = auc(recall, precision)
    optimal_idx = np.argmax(tpr - fpr)
    thval = thvals[optimal_idx]

    print('optimal thval: {}'.format(thval))
    pred_y= pred_y > thval
    f1 = f1_score(test_y, pred_y)
    acc = accuracy_score(test_y, pred_y)
    tn, fp, fn, tp = confusion_matrix(test_y, pred_y).ravel()
    print('auroc: {:.3f}, auprc: {:.3f}\tacc: {:.3f}\tf1: {:.3f}\tTN {}\tfp {}\tfn {}\tTP {}'.format(auroc, auprc, acc, f1, tn, fp, fn, tp))

if __name__ == "__main__":
    train_test()