import asyncio
import json
from datetime import datetime
from services.prediction_service import PredictionService
from apps.admin.stock.params.stock_prediction import PredictionParams
import time

async def main():
    """简单预测测试"""
    request = PredictionParams(stock_code="688027", prediction_days=10, historical_days=200)
    service = PredictionService()
    historical_data = await service._get_historical_data(request.stock_code, request.historical_days)

    result = await service.predict_stock_price(request, historical_data)
    print("预测结果:", result)


async def main_backtest():
    """回测验证预测准确性"""
    stock_code = "688027"
    window_size = 60  # 使用200天历史数据进行预测
    prediction_days = 1  # 预测2天
    step = 2  # 每2天做一次预测
    max_predictions = 200  # 限制最多20次预测用于调试

    print(f"开始回测验证股票 {stock_code}")
    print(f"窗口大小: {window_size}天, 预测天数: {prediction_days}天, 步长: {step}天")
    print(f"最多预测次数: {max_predictions}")

    service = PredictionService()

    # 获取历史数据
    historical_data = await service._get_historical_data(stock_code, 200)
    print(f"获取到 {len(historical_data)} 天历史数据")

    # 打印前5条和后5条数据，确认数据顺序
    print(f"\n前5条数据（最早）:")
    for i in range(5):
        print(f"  Index {i}: date={historical_data[i]['date']}, close={historical_data[i]['close']}")
    print(f"\n后5条数据（最近）:")
    for i in range(-5, 0):
        print(f"  Index {len(historical_data) + i}: date={historical_data[i]['date']}, close={historical_data[i]['close']}")

    results = []

    # 回测循环 - 限制预测次数
    total_predictions = 0
    for i in range(0, min(max_predictions * step, len(historical_data) - window_size - prediction_days), step):
        # 取窗口数据
        window_data = historical_data[i:i + window_size]

        # 创建预测请求
        test_request = PredictionParams(
            stock_code=stock_code,
            prediction_days=prediction_days,
            historical_days=window_size
        )

            # 进行预测
        try:
            test_result = await service.predict_stock_price(test_request, window_data)

            # 打印预测返回的原始数据
            if total_predictions < 3:
                print(f"\n第 {total_predictions + 1} 次预测 - 返回的原始预测数据:")
                print("最后的窗口数据",window_data[-2:])
                for p in test_result.predictions:
                    print(f"  日期: {p.date}, 预测收盘价: {p.predicted_close}")

            # test_result 是 PredictionOut 对象，需要提取 predictions 列表
            predicted_prices = [p.predicted_close for p in test_result.predictions]



            # 获取实际值 - historical_data 是字典列表，需要取 close 价格
            actual_close_prices = [
                historical_data[i + window_size + j]['close']
                for j in range(min(prediction_days, len(historical_data) - i - window_size))
            ]
            # 打印前3次预测的详细对比
            if total_predictions < 3:
                print(f"\n第 {total_predictions + 1} 次预测:")
                print(f"  数据窗口: index {i} to {i + window_size - 1}")
                print(f"  窗口首日期: {window_data[0]['date']}, 价格: {window_data[0]['close']}")
                print(f"  窗口尾日期: {window_data[-1]['date']}, 价格: {window_data[-1]['close']}")
                print(f"  预测日期: {historical_data[i + window_size]['date']}")
                print(f"  预测值: {predicted_prices}")
                print(f"  实际值: {actual_close_prices}")
                print(f"  窗口数据统计: min={min(d['close'] for d in window_data):.2f}, max={max(d['close'] for d in window_data):.2f}, avg={sum(d['close'] for d in window_data)/len(window_data):.2f}")
            # 记录结果
            for j in range(len(predicted_prices)):
                if j < len(actual_close_prices):
                    predicted_price = predicted_prices[j]
                    actual_price = actual_close_prices[j]
                    
                    # 计算前一天的收盘价
                    if i + window_size + j - 1 >= 0:
                        prev_price = historical_data[i + window_size + j - 1]['close']
                    else:
                        prev_price = window_data[-1]['close'] if j == 0 else actual_close_prices[j - 1]
                    
                    # 计算涨跌方向
                    predicted_change = predicted_price - prev_price
                    actual_change = actual_price - prev_price
                    predicted_direction = "涨" if predicted_change > 0 else ("跌" if predicted_change < 0 else "平")
                    actual_direction = "涨" if actual_change > 0 else ("跌" if actual_change < 0 else "平")
                    direction_correct = 1 if predicted_direction == actual_direction else 0
                    
                    result = {
                        "index": i + window_size + j,
                        "date": historical_data[i + window_size + j]['date'],
                        "prev_date": historical_data[i + window_size + j - 1]['date'] if i + window_size + j - 1 >= 0 else window_data[-1]['date'],
                        "prev_price": prev_price,
                        "predicted_price": predicted_price,
                        "actual_price": actual_price,
                        "predicted_change": round(predicted_change, 2),
                        "actual_change": round(actual_change, 2),
                        "predicted_direction": predicted_direction,
                        "actual_direction": actual_direction,
                        "direction_correct": direction_correct,
                        "error": abs(predicted_price - actual_price),
                        "error_percent": abs((predicted_price - actual_price) / actual_price * 100) if actual_price > 0 else 0,
                        "window_start_date": window_data[0]['date'],
                        "window_end_date": window_data[-1]['date']
                    }
                    results.append(result)
                    total_predictions += 1

            # 打印进度
            if total_predictions % 10 == 0:
                print(f"已处理 {total_predictions} 个预测...")

        except Exception as e:
            print(f"预测失败 at index {i}: {e}")
            continue

    # 计算统计指标
    if results:
        avg_error = sum(r["error"] for r in results) / len(results)
        avg_error_percent = sum(r["error_percent"] for r in results) / len(results)
        direction_accuracy = sum(r["direction_correct"] for r in results) / len(results) * 100
        correct_count = sum(r["direction_correct"] for r in results)

        print(f"\n{'='*60}")
        print(f"回测完成！共进行 {len(results)} 次预测")
        print(f"平均误差: {avg_error:.2f} 元")
        print(f"平均误差百分比: {avg_error_percent:.2f}%")
        print(f"涨跌方向正确次数: {correct_count} / {len(results)}")
        print(f"涨跌方向准确率: {direction_accuracy:.2f}%")
        print(f"{'='*60}\n")

        # 保存详细结果
        output_file = f"backtest_results_{stock_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"详细结果已保存到: {output_file}")

        # 显示最近10次预测结果
        print("\n最近100次预测结果:")
        print(f"{'序号':<6} {'日期':<12} {'预测':<6} {'实际':<6} {'正确':<6} {'预测价':<10} {'实际价':<10} {'误差%':<8}")
        print("-" * 80)
        for i, r in enumerate(results[-100:], 1):
            direction_symbol = "✓" if r['direction_correct'] == 1 else "✗"
            print(f"{i:<6} {r['date']:<12} {r['predicted_direction']:<6} {r['actual_direction']:<6} {direction_symbol:<6} {r['predicted_price']:<10.2f} {r['actual_price']:<10.2f} {r['error_percent']:<8.2f}")


if __name__ == "__main__":
    asyncio.run(main_backtest())
