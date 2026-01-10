import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from ucimlrepo import fetch_ucirepo 
import warnings

warnings.filterwarnings('ignore')

# ==========================================
# 核心证明工具：通用反事实测试函数
# ==========================================
def batch_counterfactual_test(model, df, feature_cols, sensitive_col, target_col, is_classification=True):
    """
    通用反事实证明器：支持分类（招聘）与回归（定价）
    法律逻辑：剥离中性因素，锁定单一属性的因果贡献
    """
    # 筛选受损群体（在定价场景中，所有“老用户”都是潜在受损群体）
    if is_classification:
        disadvantaged = df[(df[sensitive_col] == 0) & (df[target_col] == 0)].copy()
    else:
        disadvantaged = df[df[sensitive_col] == 0].copy() # 假设 0 代表老用户/被歧视特征
        
    if disadvantaged.empty: return 0.0
    
    # 构造反事实：强行改变敏感属性
    cf_samples = disadvantaged.copy()
    cf_samples[sensitive_col] = 1 # 0->1: 女性变男性 / 老用户变新用户
    
    # 执行预测
    cf_preds = model.predict(cf_samples[feature_cols])
    
    if is_classification:
        # 统计在改变性别后，有多少人从“落选”变成了“录用”
        discrimination_rate = (cf_preds == 1).mean()
    else:
        # 统计在改变身份后，有多少订单的价格下降了
        orig_preds = model.predict(disadvantaged[feature_cols])
        # 法律意义：如果 cf_price < orig_price，说明存在基于身份的溢价
        discrimination_rate = (cf_preds < orig_preds).mean()
        
    return discrimination_rate

# ==========================================
# 场景一：招聘歧视实证 (基于 UCI 真实数据集)
# ==========================================
def run_hiring_case():
    print(f"\n{'='*20} 场景一：招聘歧视 (三阶梯证明实证) {'='*20}")
    try:
        # 1. 获取证据 (Evidence Acquisition)
        adult = fetch_ucirepo(id=2)
        X, y = adult.data.features, adult.data.targets
        df = pd.concat([X, y], axis=1).dropna(subset=['sex', 'income'])
        
        # 预处理：映射法律上的敏感属性
        df['gender_binary'] = df['sex'].map({'Female': 0, 'Male': 1})
        df['target'] = df['income'].str.contains('>50K').astype(int)
        
        # --- 第一阶梯：初步举证 (Prima Facie Case) ---
        # 法律逻辑：原告展示统计上的不平等，动摇“算法中立”推定
        female_rate = df[df['gender_binary'] == 0]['target'].mean()
        male_rate = df[df['gender_binary'] == 1]['target'].mean()
        di_ratio = female_rate / male_rate if male_rate > 0 else 0
        
        print(f"【第一阶梯】统计证据：")
        print(f" - 女性高薪率: {female_rate:.2%}, 男性高薪率: {male_rate:.2%}")
        print(f" - 差别性影响系数 (DI): {di_ratio:.4f}")
        
        # 判定是否触发第二阶梯（通常 DI < 0.8 触发）
        if di_ratio < 0.8:
            print(f">>> 结论：DI 低于 0.8，初步证明成立。举证责任转移至被告。")
            
            # --- 第二阶梯：技术反证与因果剥离 (Causal Inference) ---
            # 法律逻辑：被告辩称是基于“教育”等中性因素。我们通过反事实检验其真伪。
            feature_cols = ['age', 'education-num', 'hours-per-week', 'gender_binary']
            model = LogisticRegression().fit(df[feature_cols], df['target'])
            
            # 执行核心的反事实测试
            rate = batch_counterfactual_test(model, df, feature_cols, 'gender_binary', 'target')
            
            print(f"\n【第二阶梯】反事实验证报告：")
            print(f" - 在固定年龄、教育、工时后，算法对性别的纯因果依赖率为: {rate:.2%}")
            
            # --- 第三阶梯：最终司法裁量 (Judicial Decision) ---
            # 法律逻辑：法官综合判断歧视强度是否超出社会容忍度
            print(f"\n【第三阶梯】最终审查结果：")
            threshold = 0.05  # 假设司法实践中 5% 为非法歧视红线
            if rate > threshold:
                print(f" >>> 判决：【原告胜诉】。反事实歧视率 ({rate:.2%}) 超过法定阈值 ({threshold:.2%})。")
                print(" >>> 结论：算法在决策逻辑中非法使用了性别属性，被告反证失败。")
            else:
                print(f" >>> 判决：【被告胜诉】。虽然存在统计差异，但因果歧视率较低。")
                print(" >>> 结论：结果不平等主因归于教育等中性变量，算法逻辑基本合规。")
        else:
            print("\n>>> 结论：统计差异不显著，驳回原告起诉。")

    except Exception as e:
        print(f"场景一运行失败: {e}")
# ==========================================
# 场景二：大数据杀熟 (模拟算法回归检验)
# ==========================================
def run_pricing_case(bias_strength=15.0):
    """
    场景模拟：算法定价中的“新老差价”
    bias_strength: 平台对老用户的加价幅度
    """
    print(f"\n{'='*20} 场景二：大数据杀熟 (参数化回归检验) {'='*20}")
    
    # 1. 构造高保真模拟数据
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'urgency': np.random.rand(n),               # 需求紧急度 (0-1)
        'is_old_user': np.random.choice([0, 1], n)  # 0: 老用户, 1: 新用户
    })
    
    # 法律模拟定价逻辑：Price = β0 + β1*Urgency + β2*Is_Old + ε
    # 其中 β2 即为我们要证明的“歧视权重”
    df['price'] = 50 + df['urgency']*100 + (1 - df['is_old_user'])*bias_strength + np.random.normal(0, 2, n)
    
    # 2. 建立回归模型 (模拟法院获取的算法黑箱镜像)
    feature_cols = ['urgency', 'is_old_user']
    model = LinearRegression().fit(df[feature_cols], df['price'])
    
    # 3. 第一阶梯：统计证据
    avg_old = df[df['is_old_user'] == 0]['price'].mean()
    avg_new = df[df['is_old_user'] == 1]['price'].mean()
    print(f"【第一阶梯】均价统计：老用户 {avg_old:.2f} 元, 新用户 {avg_new:.2f} 元")
    
    # 4. 第二阶梯：因果剥离
    if avg_old > avg_new * 1.05:
        print(">>> 触发举证责任转移：启动反事实价格敏感度分析...")
        
        # 调用回归模式下的反事实测试
        discrimination_rate = batch_counterfactual_test(
            model, df, feature_cols, 'is_old_user', 'price', is_classification=False
        )
        
        print(f"【第二阶梯】技术报告：{discrimination_rate:.2%} 的老用户订单存在纯身份溢价。")
        
        # 5. 第三阶梯：法官裁量
        if discrimination_rate > 0.8:
            print("【最终裁定】胜诉。算法对“老用户”身份存在系统性加价，构成大数据杀熟。")
        else:
            print("【最终裁定】败诉。差价主因由“紧急度”等合理因素解释。")
    else:
        print(">>> 差价未达法律显著性门槛，驳回起诉。")

if __name__ == "__main__":
    # 同时运行两个场景，展现框架的通用性
    run_hiring_case()
    run_pricing_case(bias_strength=15.0) # 模拟杀熟存在
    run_pricing_case(bias_strength=1.0)  # 模拟正常定价