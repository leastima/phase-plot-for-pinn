import json

from numpy.ma.extras import apply_along_axis


class PPConfigLoader:
    def __init__(self, path='config.json'):
        """
        初始化 PPConfigLoader 类并加载配置文件。

        :parameter path: 配置文件的路径（默认: config.json）
        """
        self.config = self.get_config_for_pp(path)
        self.count = len(self.config)

    ### public
    def description(self):
        print('plot count :', self.count)
        print('total config :', self.config)

    ### private
    def get_config_for_pp(self, path):
        """
        加载配置文件并返回配置内容。

        :parameter path: 配置文件的路径
        :return: json
        """
        with open(path, 'r') as f:
            pp_config = json.load(f)
            return pp_config

