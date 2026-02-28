from gm.api import *

# 设置Token（需要替换为实际的Token）
set_token("2d2a05e9ba6eac1de131cea8a509fd3216efd9af")

# 获取股票历史行情
# symbol: 股票代码格式为 交易所.股票代码，如 SHSE.688039 或 SZSE.000001
# frequency: 周期类型，1d=日线, 1w=周线, 1m=月线
# start_time: 开始时间
# end_time: 结束时间
# adjust: 复权类型，0=不复权, 1=前复权, 2=后复权
data = history(
    symbol='SHSE.688039',
    frequency='1d',
    start_time='2024-01-01 00:00:00',
    end_time='2026-02-24 23:59:59',
    adjust=1,
    df=True
)

print(data)