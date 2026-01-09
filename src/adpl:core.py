import numpy as np

class FairLadder:
    def __init__(self, level="Statistical"):
        self.level = level
        self.supported_levels = ["Statistical", "Conditional", "Individual", "Counterfactual"]

    def check_bias(self, data, target, sensitive_feature):
        """
        根据阶梯层级执行偏见检测
        """
        if self.level not in self.supported_levels:
            raise ValueError(f"Level must be one of {self.supported_levels}")
        
        # 模拟检测逻辑
        # 实际开发中，这里会调用 adpl.detectors 里的具体算法
        results = {
            "level": self.level,
            "metric_name": "Demographic Parity" if self.level == "Statistical" else "Equal Opportunity",
            "score": 0.15,  # 示例数值
            "status": "Warning" if 0.15 > 0.1 else "Passed"
        }
        return Report(results)

class Report:
    def __init__(self, results):
        self.results = results

    def print_summary(self):
        print("="*30)
        print(f"ADPL 公平性检测报告")
        print("-"*30)
        print(f"检测层级: {self.results['level']}")
        print(f"核心指标: {self.results['metric_name']}")
        print(f"偏见得分: {self.results['score']}")
        print(f"最终结论: {self.results['status']}")
        print("="*30)