import subprocess
import os
import pandas as pd
from io import StringIO


home_path = os.environ['HOME']
cwd_path = os.getcwd()
password = "jj"

# 清理之前的 mininet 进程
os.system(f"echo {password} | sudo mn -c")
get_servertest_cmd = f"echo {password} | sudo pgrep -f servertest"
os.system(f"echo {password} | sudo kill -9 $({get_servertest_cmd})")

# 自动测试脚本，运行子进程
# command = f'echo {password} | sudo -S python3 topo-3.py'
# subprocess.run(command, shell=True, check=True, text=True, cwd=cwd_path)

# 处理生成的 MPDTrace
get_score_cmd = "python3 ../tools/get_score.py MPDTrace_00010203040506070809101112131415161718cb.txt"
score_process = subprocess.run(get_score_cmd, shell=True, check=True, text=True, cwd=cwd_path, capture_output=True)
score_text = score_process.stdout

print(score_text)

lines = score_text.splitlines()

result = pd.DataFrame(columns=["Key", "Value"])

for line in lines:
    if(":" not in line):
        continue
    line_split = line.split(",")
    final_line = [item.split(":") for item in line_split]
    df = pd.DataFrame(final_line, columns=["Key", "Value"])
    result = pd.concat([result, df])


print(result)
