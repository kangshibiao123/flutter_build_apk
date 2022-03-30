import os
import requests
import webbrowser
from requests_toolbelt.multipart import encoder
import sys
# 执行脚本 python3 apk.py
# 依赖  requests_toolbelt  执行pip3 install  requests_toolbelt
# 依赖  requests  执行pip3 install  requests


# 华为渠道release包 flutter build apk  --flavor huawei --release
packaging = 'flutter build apk  --flavor huawei --release'

# 文件名
fileName = 'app-huawei-release.apk'

# 获取路径
currentPath = os.getcwd()

# 拼接文件路径
filePath = currentPath + '/build/app/outputs/flutter-apk/app-huawei-release.apk'

# 获取文件大小
fileLength = os.path.getsize(filePath)

# 蒲公英上传地址
url = 'https://www.pgyer.com/apiv2/app/upload'

# 蒲公英_api_key
apiKey = ''


def buildAPK():
    try:
        print('开始打包' + packaging)
        os.system(packaging)
        print('打包完成 -- 开始上传')
        uploadFile()
    except KeyError as e:
        print(e)

# 上传到蒲公英
def uploadFile():
    file = open(filePath, 'rb')
    e = encoder.MultipartEncoder(
        fields={
            '_api_key': apiKey,
            'file': (fileName, file, 'application/x-www-form-urlencoded'),
        },
    )
    m = encoder.MultipartEncoderMonitor(e, my_callback,)
    res = requests.post(url, data=m, headers={'Content-Type': m.content_type}).json()
    print(res)
    code = res['code']
    if code == 0 :
        webbrowser.open(url=res['data']['buildQRCodeURL'])



def my_callback( monitor):
    total = 50
    fileLength = os.path.getsize(filePath)
    pro = int((monitor.bytes_read * 1.0) / fileLength * 1.0 * total)
    unit = 1000 * 1000.0
    sys.stdout.write(
        '\r' + str(pro * '\033[46;34m \033[0m') + str((total - pro) * '\033[40;30m \033[0m') + '[{0}M/{1}M]'.format(
            round(monitor.bytes_read / unit, 2), round(fileLength / unit, 2)))
    sys.stdout.flush()


if __name__ == '__main__':
    buildAPK()
