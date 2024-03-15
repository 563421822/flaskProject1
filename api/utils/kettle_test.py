import subprocess

# 设置作业文件路径和参数 
trans_file = "C:\\Users\\56342\\Desktop\\abcd.ktr"
# params = "-param:username=john"

# 创建命令行命令 
cmd = ["C:\\Users\\56342\\Desktop\\data-integration\\Pan.bat", "-file", trans_file]

# 执行命令并获取输出 
process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
output, error = process.communicate()
print(output)
