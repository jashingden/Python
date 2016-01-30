# -*- coding: utf-8 -*-
import pysvn

svn_server = 'https://svn-server.mitake.com.tw/svn/RD2/android/trunk/'
project_folder = 'D:\MITAKE\Git'

client = pysvn.Client()

def checkout(name, ver='', isTrunk=True):
    if isTrunk:
        path = "%s/%s/trunk" % (svn_server, name)
        folder = "%s\\%s" % (project_folder, name)
    else:
        path = "%s/%s/tags/%s" % (svn_server, name, ver)
        folder = "%s\\%s_%s" % (project_folder, name, ver)
    print(path, folder)
    client.checkout(path, folder)


'''
#Phone一階
checkout('com_mitake_finance_chart')
checkout('com_mitake_jni')
checkout('com_mitake_telegram')
checkout('com_mitake_appwidget')
checkout('com_mitake_loginflow')
checkout('com_mitake_network')
checkout('com_mitake_finance_sqlite')
checkout('com_mitake_widget')
checkout('com_mitake_variable')
checkout('com_mitake_securities')
checkout('com_mitake_trade')
checkout('com_mitake_function')
checkout('Android_Phone_MTK')
'''

'''
#Phone一階
checkout('MitakeStock_Phone_V5', 'V6.181.730')
checkout('com_mitake_finance_phone_core', 'v4.8.37')
'''

