import sys
import os

# print(os.path.dirname(__file__))
# 将 pbc_examples 目录添加到 sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '/cpfm/pbc_examples'))

import time
import argparse
import subprocess
import cpfm
import cpfm.pbc_examples
import numpy as np
import os
import random
import torch
# from cpfm.pbc_examples.systems_pbc import *
# from cpfm.pbc_examples.choose_optimizer import *
# from cpfm.pbc_examples.net_pbc import *
import torch.backends.cudnn as cudnn
# from cpfm.pbc_examples.utils import *
# from cpfm.pbc_examples.visualize import *
import matplotlib.pyplot as plt

# from cpfm.pbc_examples.main_pbc import *

# 定义 beta 和 collocation points 的范围
beta = np.linspace(5, 15, 3)
collocation_points = np.linspace(100, 500, 5)

# 运行 script_a.py，并捕获输出
# beg_tmp = time.time_ns()
# result = subprocess.run(['python', '../cpfm/pbc_examples/main_pbc.py', '--beta', '1.0', '--N_f', '100'], capture_output=True, text=True)
# end_tmp = time.time_ns()
# print('exec cost :', end_tmp - beg_tmp)
# output = result.stdout.strip()  # 获取输出
# print("Output from script_a:", output)

# 创建训练损失和测试错误的数据
training_loss = np.outer(collocation_points, beta)
test_error = np.outer(collocation_points, beta)

# # 创建一个 1x2 的子图布局
# fig, axs = plt.subplots(1, 2, figsize=(12, 6))
#
# # 绘制训练损失
# c1 = axs[0].imshow(training_loss, aspect='auto', extent=[beta[0], beta[-1], collocation_points[0], collocation_points[-1]], origin='lower', cmap='viridis')
# axs[0].set_title('Training loss')
# axs[0].set_xlabel('Beta')
# axs[0].set_ylabel('Collocation Points')
# fig.colorbar(c1, ax=axs[0])
#
# # 绘制测试错误
# c2 = axs[1].imshow(test_error, aspect='auto', extent=[beta[0], beta[-1], collocation_points[0], collocation_points[-1]], origin='lower', cmap='viridis')
# axs[1].set_title('Test error')
# axs[1].set_xlabel('Beta')
# axs[1].set_ylabel('Collocation Points')
# fig.colorbar(c2, ax=axs[1])
#
# # 保存图像到特定目录
# # output_directory = '../output'  # 指定保存图像的目录
# # output_filename = 'training_and_test_error.png'  # 指定保存的文件名
#
# # 创建输出目录（如果不存在）
# # os.makedirs(output_directory, exist_ok=True)
#
# # 保存图像
# # plt.savefig(os.path.join(output_directory, output_filename))
#
# # 显示图形
# plt.tight_layout()
# plt.show()


## 创建数据
beta_values = [4, 5, 10, 15, 20, 25, 27, 30, 50, 70]
collocation_points = [0, 0.01, 0.02, 0.03, 0.04]  # 示例数据

# 创建子图
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# 绘制训练损失
c1 = axs[0].imshow(np.zeros((len(collocation_points), len(beta_values))), cmap='viridis', aspect='auto',
                   extent=[beta_values[0], beta_values[-1], collocation_points[0], collocation_points[-1]],
                   origin='lower')
axs[0].set_title('Training loss')
axs[0].set_xlabel('Beta')
axs[0].set_ylabel('Collocation Points')
axs[0].set_xticks(beta_values)  # 设置 x 轴刻度
axs[0].set_yticks(collocation_points)  # 设置 y 轴刻度

# 添加颜色条
fig.colorbar(c1, ax=axs[0], label='Loss Value')

# 绘制测试误差
c2 = axs[1].imshow(np.zeros((len(collocation_points), len(beta_values))), cmap='viridis', aspect='auto',
                   extent=[beta_values[0], beta_values[-1], collocation_points[0], collocation_points[-1]])
axs[1].set_title('Test error')
axs[1].set_xlabel('Beta')
axs[1].set_ylabel('Collocation Points')
axs[1].set_xticks(beta_values)  # 设置 x 轴刻度
axs[1].set_yticks(collocation_points)  # 设置 y 轴刻度

# 添加颜色条
fig.colorbar(c2, ax=axs[1], label='Error Value')

# 调整布局
plt.tight_layout()
plt.show()