#-*-coding:utf-8-*-

# 小黄鸡的ai，先自己尝试处理，没结果则交给simsimi

import plugins
import random

plugin_modules = []
for plugin_name in plugins.__all__:
    __import__('plugins.%s' % plugin_name)
    plugin_modules.append(getattr(plugins, plugin_name))

# some magic here
def magic(data, bot=None):
    for plugin_module in plugin_modules:
        try:
            if plugin_module.test(data, bot):
                return plugin_module.handle(data, bot)
        except:
            continue

    return random.choice(['呵呵', '。。。', '= =', '=。=', '傻×了吧', '砍死咸菜啊！'])

if __name__ == '__main__':
    print magic("咸菜")
