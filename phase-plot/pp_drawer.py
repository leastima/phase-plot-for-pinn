import os
import numpy as np
import matplotlib.pyplot as plt
from pp_manager import *


class PPDrawer:
    def make_phase_plot(self, pp_single_manager, store=True, output_dir='../output'):
        # 确定要绘制的 z 值数量
        num_z_values = len(pp_single_manager.z)
        num_rows = (num_z_values + 1) // 2  # 计算行数，向上取整
        num_cols = min(2, num_z_values)  # 列数固定为2

        # 创建足够的子图
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 12))

        # 确保 axs 是一维的列表
        axs = axs.flatten() if num_rows > 1 else [axs]

        for i, z_value in enumerate(pp_single_manager.z):
            # 绘制相位图
            c = axs[i].imshow(
                pp_single_manager.z_values[get_tag_with_name(z_value)],
                origin='lower'
            )
            axs[i].set_title(f'Phase Plot: {z_value}')
            axs[i].set_xlabel(pp_single_manager.x)
            axs[i].set_ylabel(pp_single_manager.y)

            # 设置 x 轴和 y 轴的刻度
            axs[i].set_xticks(range(len(pp_single_manager.x_list)))
            axs[i].set_xticklabels(pp_single_manager.x_list)
            axs[i].set_yticks(range(len(pp_single_manager.y_list)))
            axs[i].set_yticklabels(pp_single_manager.y_list)

            # 添加颜色条
            fig.colorbar(c, ax=axs[i], label='Z Values')

        # 调整子图间距
        plt.subplots_adjust(hspace=0.4, wspace=0.4)  # 增加水平和垂直间距

        # 保存图像
        if store:
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, pp_single_manager.image_name))

        # 显示图形
        plt.tight_layout()
        plt.show()