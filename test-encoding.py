# -*- coding: utf-8 -*-
"""
测试UTF-8编码是否正常工作
"""
import sys
import os

def test_encoding():
    """测试编码设置"""
    print("=" * 50)
    print("UTF-8编码测试")
    print("=" * 50)
    
    # 检查Python版本和编码设置
    print(f"Python版本: {sys.version}")
    print(f"默认编码: {sys.getdefaultencoding()}")
    print(f"文件系统编码: {sys.getfilesystemencoding()}")
    print(f"标准输出编码: {sys.stdout.encoding}")
    print(f"标准错误编码: {sys.stderr.encoding}")
    
    # 测试中文字符输出
    print("\n测试中文字符输出:")
    test_strings = [
        "你好，世界！",
        "春儿数字人系统",
        "修复版数字人服务",
        "UTF-8编码测试",
        "中文显示正常"
    ]
    
    for i, text in enumerate(test_strings, 1):
        print(f"{i}. {text}")
    
    # 测试特殊字符
    print("\n测试特殊字符:")
    special_chars = "！@#￥%……&*（）——+{}|:<>?【】；'，。、"
    print(f"特殊字符: {special_chars}")
    
    # 测试emoji
    print("\n测试emoji表情:")
    emojis = "😀😃😄😁😆😅😂🤣😊😇"
    print(f"Emoji: {emojis}")
    
    print("\n" + "=" * 50)
    print("编码测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    # 设置控制台编码为UTF-8
    if sys.platform.startswith('win'):
        import codecs
        try:
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
            print("已设置Windows控制台编码为UTF-8")
        except Exception as e:
            print(f"设置编码时出错: {e}")
    
    test_encoding() 