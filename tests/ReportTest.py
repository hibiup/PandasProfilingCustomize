from unittest import TestCase
import numpy as np
import pandas as pd
import pandas_profiling

from PandasProfileCustomization import deco_reporter, customize_template, template_mapper


def reporting(df, output):
    """ Profiling method """
    rep = df.profile_report(style={'full_width': True})
    # display(profile)  # For Jupyter notebook
    output(rep)


class ReportTest(TestCase):
    def test_report_generation(self):
        """ 修改 Templates """
        customize_template()

        """ 修改模板映射 """
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
        from concurrent import futures
        with futures.ProcessPoolExecutor(5) as executor:
            done = executor.submit(reporting(df, lambda out: out.to_file("output.html")))
            futures.as_completed(done)
