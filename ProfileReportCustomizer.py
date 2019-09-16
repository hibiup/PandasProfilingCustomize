import numpy as np
import pandas as pd
from pandas_profiling.view import templates


def customize_template():
    """
    修改 `pandas_profiling.view.templates.jinja2_env` 环境变量来指定新的模板所在的基本路径（template base）．
    """
    def __abspath__():
        """
        获得新模板基本路径
        """
        import sys
        from os import path
        return path.abspath(path.dirname(sys.modules[__name__].__file__)).replace("\\", "/") + "/view/templates"

    def __generate_env__():
        """
        修改路径并应设置参数
        """
        import jinja2
        # 加载模板中用到的格式化器
        from pandas_profiling.view import formatters
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=__abspath__()))
        env.filters["fmt_percent"] = formatters.fmt_percent
        env.filters["fmt_bytesize"] = formatters.fmt_bytesize
        env.filters["fmt_numeric"] = formatters.fmt_numeric
        env.filters["fmt_array"] = formatters.fmt_array
        env.filters["fmt"] = formatters.fmt
        return env

    templates.jinja2_env = __generate_env__()


def template_mapper(templates_dict):
    """
    (可选)为模板载入函数 `pandas_profiling.view.templates.template` 添加装饰器以允许我们修改模板文件名和相对路径。
    该装饰器接受一个额外 dict 类型参数，该参数将缺省模板名称映射到定制的模板名称. 该方法为可选，如果不执行这个步骤，报告
    将（从定制的模板目录下）读取缺省的模板名称。
    """
    def template_decor(function, dict):
        def wrapper(*args, **kwargs):
            return function(dict[args[0]], **kwargs)
        return wrapper

    # 应用装饰器，让 mapper 生效
    templates.template = template_decor(templates.template, templates_dict)


def deco_reporter(df, input_callback, output_callback):
    """
    (可选)如果希望进一步修改输入的数据和生成的模板，可以通过两个（输入输出）回调函数来实现。
    在 `input_callback` 中修改输入的数据集。`output_callback` 可用于进一步修改返回的报告。
    """
    # Decorate function
    def input_decor(function, in_cb, out_cb):
        def wrapper(*args, **kwargs):
            in_cb(function.__self__, *args, **kwargs)
            return out_cb(function(*args, **kwargs))       # Modified return value
        return wrapper

    # 应用输入输出装饰器
    df.profile_report = input_decor(df.profile_report, input_callback, output_callback)
    return df


if __name__ == "__main__":
    """ 修改 Templates """
    customize_template()

    """ """
    template_mapper({
        "overview.html": "overview.html",
        "freq_table.html": "freq_table.html",
        "variables/row_num_statistics.html": 'variables/row_num_statistics.html',
        'variables/row_num_histogram.html': 'variables/row_num_histogram.html',
        'variables/row_num_frequency_table.html': 'variables/row_num_frequency_table.html',
        'variables/row_num_extreme_values.html': 'variables/row_num_extreme_values.html',
        'variables/row_num.html': 'variables/row_num.html',
        'components/tabs.html': 'components/tabs.html',
        'components/list.html': 'components/list.html',
        'base.html': 'base.html',
        'wrapper.html': 'wrapper.html'
    })

    """ 准备测试数据 """
    df = pd.DataFrame(
        np.random.rand(100, 5),
        columns=['a', 'b', 'c', 'd', 'e']
    )

    # 修改测试数据(Option)
    df.drop(['a', 'c'], axis=1, inplace=True)

    """ 准备回调函数(Option) """
    def input_callback(instance, *args, **kwargs):
        print("Input =>", instance.shape, args, kwargs)         # Added side-effect

    def output_callback(output):
        print("Output <=", output)
        return output

    # 用回调函数装饰测试报告
    deco_reporter(df, input_callback, output_callback)

    """ 执行测试报告 """
    rep = df.profile_report(style={'full_width': True})
    # display(profile)  # For Jupyter notebook
    rep.to_file("output.html")
