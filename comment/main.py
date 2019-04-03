from scrapy import cmdline
import uuid

id = str(uuid.uuid4()).replace("-", "")
cmdline.execute("scrapy crawl wb -o item{0}.json".format(id).split())









