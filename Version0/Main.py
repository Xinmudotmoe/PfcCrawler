import urllib2
f=open("C.html",'w+')
f.write(urllib2.urlopen("http://www.pfc.cn/Awebsite/CollegeAll.aspx").read())
f.close()
