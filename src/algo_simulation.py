import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
import warnings

warnings.filterwarnings('ignore')


def batch_counterfactual_test(model, df, feature_cols=['education', 'experience', 'gender'], sensitive_col='gender', target_col='hired', is_classification=True):
    """
    对所有落选/受损群体进行批量反事实干预，计算系统性偏见概率
    """
    # 筛选受损群体
    if is_classification:
        disadvantaged = df[(df[sensitive_col] == 0) & (df[target_col] == 0)].copy()
    else:
        disadvantaged = df[(df[sensitive_col] == 0)].copy()
        
    if disadvantaged.empty:
        return 0.0
    
    # 构造反事实样本
    cf_samples = disadvantaged.copy()
    cf_samples[sensitive_col] = 1
    
    # 执行预测
    # 注意：这里需要确保只选取特征列
    cf_preds = model.predict(cf_samples[feature_cols])
    
    if is_classification:
        discrimination_rate = (cf_results == 1).mean() if 'cf_results' in locals() else (cf_preds == 1).mean()
    else:
        orig_preds = model.predict(disadvantaged[feature_cols])
        discrimination_rate = (cf_preds < orig_preds).mean()
        
    return discrimination_rate

# 场景一：招聘算法歧视模拟 (分类模型)

def simulate_hiring_case(bias_strength):
    print(f"\n{'='*20} 场景模拟：招聘算法歧视 (权重={bias_strength}) {'='*20}")
    
    # 1. 数据模拟 (模拟黑箱平台) 
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'education': np.random.randint(0, 3, n),
        'experience': np.random.randint(0, 11, n),
        'gender': np.random.choice([0, 1], n) # 0:女, 1:男
    })
    # 歧视逻辑：录取分 = 能力 + 性别溢价
    score = df['education']*2 + df['experience'] + df['gender']*bias_strength + np.random.normal(0, 1, n)
    df['hired'] = (score > 10).astype(int)
    
    model = LogisticRegression().fit(df[['education', 'experience', 'gender']], df['hired'])

    # 第一阶梯：初步举证 
    male_rate = df[df['gender'] == 1]['hired'].mean()
    female_rate = df[df['gender'] == 0]['hired'].mean()
    di = female_rate / (male_rate if male_rate > 0 else 1)
    print(f"【第一阶梯】差别性影响比值: {di:.2f} (女 {female_rate:.2%} vs 男 {male_rate:.2%})")

    if di < 0.8:
        print(">>> 触发举证责任转移。")
        # 第二、三阶梯：反事实验证 
        group_bias = batch_counterfactual_test(model, df, ['education', 'experience', 'gender'], 'gender', 'hired')
        print(f"【第二阶梯】技术验证报告：系统性反事实歧视率为 {group_bias:.2%}")
        
        # 模拟个案
        plaintiff = pd.DataFrame({'education':[2], 'experience':[5], 'gender':[0]})
        is_discriminated = model.predict(plaintiff)[0] != model.predict(plaintiff.assign(gender=1))[0]
        
        print(f"【第三阶梯】法院判决：{'原告胜诉' if is_discriminated else '被告胜诉'} (个案因果关系检验)")
    else:
        print(">>> 证据不足，驳回起诉。")


# 场景二：大数据杀熟模拟 (回归模型)

def simulate_pricing_case(bias_strength):
    print(f"\n{'='*20} 场景模拟：大数据杀熟 (权重={bias_strength}) {'='*20}")
    
    # 1. 数据模拟 (模拟定价算法) [cite: 14]
    np.random.seed(123)
    n = 1000
    df = pd.DataFrame({
        'urgency': np.random.rand(n),      # 需求紧急度
        'is_old_user': np.random.choice([0, 1], n) # 0:老用户, 1:新用户 (模拟对老用户加价)
    })
    # 定价逻辑：价格 = 紧急度*100 + (1-是否新用户)*bias_strength (老用户加价)
    df['price'] = df['urgency']*100 + (1 - df['is_old_user'])*bias_strength + np.random.normal(0, 2, n)
    
    model = LinearRegression().fit(df[['urgency', 'is_old_user']], df['price'])

    # 第一阶梯 
    avg_old = df[df['is_old_user'] == 0]['price'].mean()
    avg_new = df[df['is_old_user'] == 1]['price'].mean()
    print(f"【第一阶梯】统计证据：老用户均价 {avg_old:.2f}, 新用户均价 {avg_new:.2f}")

    if avg_old > avg_new * 1.05: # 老用户贵5%以上触发
        print(">>> 触发举证责任转移。")
        # 第二、三阶梯 
        group_bias = batch_counterfactual_test(model, df, ['urgency', 'is_old_user'], 'is_old_user', 'price', False)
        print(f"【第二阶梯】技术验证报告：{group_bias:.2%} 的老用户订单在反事实干预（转为新用户）下价格下降。")
        
        # 个案检验
        p_price = 80
        p_cf_price = model.predict([[0.7, 1]])[0] # 同样紧急度，换成新用户身份
        
        print(f"【第三阶梯】最终审查：{'原告胜诉' if group_bias > 0.5 else '被告胜诉'}")
    else:
        print(">>> 差价在合理范围内，驳回起诉。")


# 执行全案模拟

if __name__ == "__main__":
    # 模拟招聘歧视：重度偏见
    simulate_hiring_case(bias_strength=5.0)
    # 模拟招聘歧视：算法中性
    simulate_hiring_case(bias_strength=0.0)
    # 模拟大数据杀熟
    simulate_pricing_case(bias_strength=15.0)