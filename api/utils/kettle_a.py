from org.pentaho.di.core import KettleEnvironment
from org.pentaho.di.trans import TransMeta
from org.pentaho.di.trans import Trans

# 初始化Kettle环境
KettleEnvironment.init()

# 加载已有的转换定义
transMeta = TransMeta("path_to_your_transformation.ktr")

# 创建并运行转换实例
trans = Trans(transMeta)
trans.execute(None)

# 等待转换完成
trans.waitUntilFinished()

# ...其他操作，比如获取结果等