import requests
from lxml import etree


def detect_ip(ip, port, http_type):
    """检测ip地址是否可用,验证的地址为 百度"""
    url = 'https://www.baidu.com'
    # 检测是否为ｈｔｔｐｓ还是ｈｔｔｐ

    http_types = http_type.lower()
    if http_types == 'http':
        proxies = {
            "http": ip.strip()+":"+port.strip(),
        }
    else:
        proxies = {
            "https": ip.strip()+":"+port.strip(),
        }

    print(proxies)
    try:
        response = requests.get(url, proxies=proxies, timeout=3)
        print(response.status_code)
        if response.status_code == 200:
            return True
    except:
        return False


# 爬去西刺代理的地址
def get_proxy():

    url = 'https://www.xicidaili.com/wn/'
    # headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    data = requests.get(url, headers=headers)
    # s = data.content.body
    s = data.content.decode()
    # print(type(s))
    with open('s.txt', 'w') as f:
        f.write(s)
    html = etree.parse('s.txt', etree.HTMLParser())
    print(html)

    ip_port_list = html.xpath('//*[@id="ip_list"]/tr[position()>1]')

    for i in ip_port_list:
        ip = i.xpath('./td[2]/text()')
        port = i.xpath('./td[3]/text()')
        # types为代理ip的分类
        types = i.xpath('./td[5]/text()')
        http_type = i.xpath('./td[6]/text()')

        if types[0] == '高匿':
            # 检测代理ｉｐ是否为高匿，不是的话舍弃
            print(ip[0], port[0], http_type[0])
            if detect_ip(ip[0], port[0], http_type[0]):
                yield ip[0], port[0], http_type[0]


s = get_proxy()
for i in s:
    print(i, '*******')

