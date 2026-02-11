import asyncio
from datetime import datetime, timedelta
from apps.admin.stock.params.stock_prediction import PredictionParams
from services.stock_service import StockService


async def test_single_prediction():
    """测试单次预测，查看返回的原始数据"""
    stock_code = "688027"
    window_size = 200
    prediction_days = 2

    print(f"测试股票 {stock_code} 的单次预测")
    print("="*60)

    # 获取股票数据
    stock_service = StockService()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=500)

    result = await stock_service.get_historical_data(
        stock_code,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    if not result or not result.get('data'):
        print("获取历史数据失败")
        return

    all_data = result['data']
    print(f"获取到 {len(all_data)} 天历史数据")

    # 取最后200天作为窗口数据
    window_data = all_data[-window_size:]
    print(f"\n使用窗口数据：")
    print(f"  起始日期: {window_data[0]['date']}, 收盘价: {window_data[0]['close']}")
    print(f"  结束日期: {window_data[-1]['date']}, 收盘价: {window_data[-1]['close']}")
    print(f"  窗口价格范围: {min(d['close'] for d in window_data):.2f} - {max(d['close'] for d in window_data):.2f}")
    print(f"  窗口平均价格: {sum(d['close'] for d in window_data)/len(window_data):.2f}")

    # 打印窗口最后5天的数据
    print(f"\n窗口最后5天的数据:")
    for d in window_data[-5:]:
        print(f"  日期: {d['date']}, 开盘: {d['open']}, 最高: {d['high']}, 最低: {d['low']}, 收盘: {d['close']}")

    # 查看窗口后2天的实际数据（用于对比）
    if len(all_data) > window_size + 2:
        print(f"\n窗口后2天的实际数据:")
        for j in range(2):
            idx = window_size + j
            d = all_data[idx]
            print(f"  日期: {d['date']}, 开盘: {d['open']}, 最高: {d['high']}, 最低: {d['low']}, 收盘: {d['close']}")

    print("\n" + "="*60)
    print("开始调用预测服务...")
    print("="*60 + "\n")

    # 调用预测服务
    from services.prediction_service import PredictionService
    prediction_service = PredictionService()

    test_request = PredictionParams(
        stock_code=stock_code,
        prediction_days=prediction_days,
        historical_days=window_size
    )

    try:
        pred_result = await prediction_service.predict_stock_price(test_request, window_data)

        print("="*60)
        print("预测结果:")
        print("="*60)
        print(f"股票代码: {pred_result.stock_code}")
        print(f"预测天数: {pred_result.prediction_days}")
        print(f"历史数据天数: {pred_result.historical_data_count}")

        print(f"\n预测详情:")
        for i, p in enumerate(pred_result.predictions, 1):
            print(f"  第{i}天:")
            print(f"    日期: {p.date}")
            print(f"    预测收盘价: {p.predicted_close}")

        if len(all_data) > window_size + 2:
            print(f"\n对比预测值和实际值:")
            for i, p in enumerate(pred_result.predictions):
                actual_idx = window_size + i
                if actual_idx < len(all_data):
                    actual_data = all_data[actual_idx]
                    print(f"  日期: {p.date}")
                    print(f"    预测: {p.predicted_close:.2f}")
                    print(f"    实际: {actual_data['close']:.2f}")
                    print(f"    误差: {abs(p.predicted_close - actual_data['close']):.2f}")
                    print(f"    误差%: {abs((p.predicted_close - actual_data['close']) / actual_data['close'] * 100):.2f}%")

    except Exception as e:
        print(f"预测失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_single_prediction())
