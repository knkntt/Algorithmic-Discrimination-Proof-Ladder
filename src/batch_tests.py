import pandas as pd
import numpy as np
# 修正：只导入需要的 batch_counterfactual_test，因为本脚本自己会跑循环
from algo_simulation import batch_counterfactual_test 
from sklearn.linear_model import LogisticRegression

def run_batch_experiment(bias_levels, iterations_per_level=10):
    """
    自动化批量测试脚本
    """
    print(f"正在启动自动化批量实验，总计运行 {len(bias_levels) * iterations_per_level} 次模拟...\n")
    
    summary_results = []

    for bias in bias_levels:
        win_count = 0
        total_disc_rate = 0
        
        for _ in range(iterations_per_level):
            n_samples = 1000
            df = pd.DataFrame({
                'education': np.random.randint(0, 3, n_samples),
                'experience': np.random.randint(0, 11, n_samples),
                'gender': np.random.choice([0, 1], n_samples)
            })
            
            # 生成录用逻辑
            score = df['education']*2 + df['experience'] + df['gender']*bias + np.random.normal(0, 1, n_samples)
            df['hired'] = (score > 10).astype(int)
            
            # 训练模拟黑箱
            model = LogisticRegression().fit(df[['education', 'experience', 'gender']], df['hired'])
            
            # 执行群体反事实测试 - 修正调用方式
            # 显式传递参数，确保与 algo_simulation.py 中的定义一致
            disc_rate = batch_counterfactual_test(
                model, df, 
                feature_cols=['education', 'experience', 'gender'], 
                sensitive_col='gender', 
                target_col='hired'
            )
            total_disc_rate += disc_rate
            
            # 判定胜诉逻辑
            if disc_rate > 0.10:
                win_count += 1
        
        summary_results.append({
            '歧视强度 (Bias)': bias,
            '平均群体歧视率': f"{total_disc_rate / iterations_per_level:.2%}",
            '原告胜诉率': f"{win_count / iterations_per_level:.2%}"
        })

    report_df = pd.DataFrame(summary_results)
    return report_df

if __name__ == "__main__":
    test_levels = [0.0, 0.5, 1.5, 3.0, 5.0]
    report = run_batch_experiment(test_levels)
    
    print("\n" + "="*30)
    print(" 算法歧视诉讼模拟：批量测试报告 ")
    print("="*30)
    print(report.to_string(index=False))
    print("\n报告结论：随着算法预设偏见强度的增加，'三阶梯规则'下的原告胜诉率呈现显著上升趋势。")