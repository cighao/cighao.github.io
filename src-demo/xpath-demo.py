# python xpath 使用示例

from lxml import etree

html = '''
<div id="content">
   <ul id="useful">
      <li>有效信息1</li>
      <li>有效信息2</li>
      <li>有效信息3</li>
   </ul>
   <ul id="useless">
      <li>无效信息1</li>
      <li>无效信息2</li>
      <li>无效信息3</li>
   </ul>
</div>
<div id="url">
   <a href="http://cighao.com">陈浩的博客</a>
   <a href="http://cighao.com.photo" title="陈浩的相册">点我打开</a>
</div>
'''
selector = etree.HTML(html)

# 提取 li 中的有效信息123
content = selector.xpath('//ul[@id="useful"]/li/text()')
for each in content:
    print(each)

#提取 a 中的属性
link = selector.xpath('//a/@href')
for each in link:
    print(each)

title = selector.xpath('//a/@title')
for each in title:
    print(each)
