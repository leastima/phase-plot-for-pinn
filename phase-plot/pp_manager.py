import json
import time
import subprocess
import numpy as np
from numpy.ma.extras import apply_along_axis

def value_to_str(value):
    if type(value) is str:
        return str(value)
    if isinstance(value, float) and value.is_integer():
        # 将浮点数转换为整数，再转换为字符串
        return str(int(value))
    else:
        # 如果不是整数，直接转换为字符串
        return str(value)

def get_tag_with_name(name):
    if name == 'relative_error':
        return 'Error u rel: '
    elif name == 'abs_error':
        return 'Error u abs: '
    elif name == 'linf_error':
        return 'Error u linf: '
    elif name == 'training_loss':
        return 'Training loss: '
    elif name == 'running_cost':
        return 'Total cost : '
    return None

class PPManager:
    def __init__(self, config):
        """
        初始化 PPManager 类并读取相关参数。

        :parameter config : 单个phase plot配置项
        """
        self.config = config

        # set default value
        self.image_type = 'phase plot'
        self.image_name = ''
        self.seed_count = 2
        self.default_param = []

        self.x = ''
        self.x_list = []
        self.y = ''
        self.y_list = []
        self.z = ['relative_error']
        self.z_values = {}

        self.output = None

        # load params
        self.parse_image_config()
        self.parse_default_param()
        self.calculate_axis_list()

    ### public
    def description(self):
        print('image config :', {'type':self.image_type, 'name':self.image_name, 'seed_count':self.seed_count})
        print(self.default_param)
        print('x_list :', self.x_list)
        print('y_list :', self.y_list)
        print('target function :', self.z)

    def generate_image(self):
        tags = [get_tag_with_name(zname) for zname in self.z]
        print('tags :', tags)

        # 创建一个字典来存储每个 tag 对应的数组
        z_values = {tag: np.zeros((len(self.y_list), len(self.x_list))) for tag in tags}

        for x_index in range(len(self.x_list)):
            x_value = self.x_list[x_index]
            for y_index in range(len(self.y_list)):
                y_value = self.y_list[y_index]
                for seed in range(self.seed_count):
                    commands = self.default_param + [self.x, value_to_str(x_value), self.y, value_to_str(y_value), '--seed', str(seed)]
                    # print('commands :', commands)
                    output = self.exec_script(commands)
                    z_value = self.get_zvalue_from_output(output, tags)
                    print('seed =', seed, 'x =', x_value, 'y =', y_value, 'z =', z_value)

                    for tag in tags:
                        z_values[tag][y_index][x_index] = z_values[tag][y_index][x_index] + z_value[tag]

                for tag in tags:
                    z_values[tag][y_index][x_index] = z_values[tag][y_index][x_index] / self.seed_count

        self.z_values = z_values
        print('z_values :', z_values)

    ### private
    def parse_image_config(self):
        self.image_type = self.config.get('type')
        self.image_name = self.config.get('name')
        self.seed_count = self.config.get('seed_count')

        if self.image_name is None or len(self.image_name) == 0:
            self.image_name = self.config.get('x') + '_' + self.config.get('y') + '_' + self.config.get('z') + '_' + str(int(time.time()))
        self.image_name = self.image_name + '.png'

    def parse_default_param(self):
        if self.image_type == 'phase plot':
            self.default_param = ['python', '../cpfm/pbc_examples/main_pbc.py']

        # 将 extra_param 转换为一维列表
        extra_param = [item for sublist in self.config.get('default', {}).items() for item in
                       ['--' + sublist[0], str(sublist[1])]]

        # 直接将一维列表 extra_param 添加到 self.default_param 中
        self.default_param = self.default_param + extra_param

    def calculate_axis_list(self):
        self.x = '--' + self.config.get('x')
        x_region = self.config.get('x_region')
        x_count = self.config.get('x_count')
        if x_region != None and len(x_region) > 0:
            if type(x_region[0]) is str or x_count == None:
                self.x_list = x_region
            else:
                x_min = x_region[0]
                x_max = x_region[-1]
                self.x_list = np.linspace(x_min, x_max, x_count).tolist()

        # 处理 y
        self.y = '--' + self.config.get('y')
        y_region = self.config.get('y_region')
        y_count = self.config.get('y_count')
        if y_region is not None and len(y_region) > 0:
            if isinstance(y_region[0], str) or y_count == None:
                self.y_list = y_region
            else:
                y_min = y_region[0]
                y_max = y_region[-1]
                self.y_list = np.linspace(y_min, y_max, y_count).tolist()

        self.z = self.config.get('z')

    def exec_script(self, commands = ['python', '../cpfm/pbc_examples/main_pbc.py']):
        result = subprocess.run(commands, capture_output=True,
                                text=True)
        output = result.stdout.strip()  # 获取输出
        return output

    def get_zvalue_from_output(self, output, tags):
        print(output)

        # 初始化结果字典
        results = {}

        # 按行分割输出
        lines = output.splitlines()

        for line in lines:
            for tag in tags:
                # 查找标签并提取后面的浮点数
                if tag in line:
                    # 取出标签及其后面的浮点数
                    start_index = line.index(tag) + len(tag) - 1
                    value_part = line[start_index:].strip()

                    parts = value_part.split(',')
                    if len(parts) > 0:
                        value = float(parts[0])  # 取第一个浮点数
                        results[tag] = value

        return results