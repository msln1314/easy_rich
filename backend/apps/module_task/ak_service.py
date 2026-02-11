async def sync_board_concept_from_akshare(db: AsyncSession) -> dict:
    """
    从akshare同步概念板块数据
    先获取当天所有的概念板块信息，判断是更新还是插入
    :return: 操作结果
    """
    try:
        print("开始获取概念板块数据...")

        # 获取概念板块数据
        board_concept_df = ak.stock_board_concept_ths()

        # 字段映射
        column_mapping = {
            "序号": "sequence",
            "板块": "board_name",
            "涨跌幅": "change_percent",
            "总成交量": "total_volume",
            "总成交额": "total_amount",
            "净流入": "net_inflow",
            "上涨家数": "up_count",
            "下跌家数": "down_count",
            "均价": "average_price",
            "领涨股": "leading_stock",
            "领涨股-最新价": "leading_stock_price",
            "领涨股-涨跌幅": "leading_stock_change",
        }

        # 重命名列
        board_concept_df = board_concept_df.rename(columns=column_mapping)

        # 获取当前日期
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 获取数据库中当天已有的概念板块名称
        existing_board_names = await get_board_concept_by_date(db, current_date)
        existing_set = set(existing_board_names)

        # 分离需要新增和更新的数据
        boards_to_add = []
        boards_to_update = []

        for _, row in board_concept_df.iterrows():
            try:
                board_name = row["board_name"] if pd.notna(row["board_name"]) else ""
                if not board_name:
                    continue

                # 构建数据
                board_data = {
                    "board_name": board_name,
                    "board_code": None,  # 同花顺接口不提供板块代码
                    "sequence": int(row["sequence"])
                    if pd.notna(row["sequence"])
                    else None,
                    "change_percent": float(row["change_percent"])
                    if pd.notna(row["change_percent"])
                    else None,
                    "average_price": float(row["average_price"])
                    if pd.notna(row["average_price"])
                    else None,
                    "total_volume": float(row["total_volume"])
                    if pd.notna(row["total_volume"])
                    else None,
                    "total_amount": float(row["total_amount"])
                    if pd.notna(row["total_amount"])
                    else None,
                    "net_inflow": float(row["net_inflow"])
                    if pd.notna(row["net_inflow"])
                    else None,
                    "up_count": int(row["up_count"])
                    if pd.notna(row["up_count"])
                    else None,
                    "down_count": int(row["down_count"])
                    if pd.notna(row["down_count"])
                    else None,
                    "leading_stock": row["leading_stock"]
                    if pd.notna(row["leading_stock"])
                    else None,
                    "leading_stock_price": float(row["leading_stock_price"])
                    if pd.notna(row["leading_stock_price"])
                    else None,
                    "leading_stock_change": float(row["leading_stock_change"])
                    if pd.notna(row["leading_stock_change"])
                    else None,
                    "leading_stock_code": None,  # 同花顺接口不提供领涨股代码
                    "date_at": current_date,
                    "data_time": datetime.now(),
                    "data_from": "akshare_ths",
                }

                # 判断是新增还是更新
                if board_name in existing_set:
                    board_data["updated_at"] = datetime.now()
                    boards_to_update.append(board_data)
                else:
                    boards_to_add.append(board_data)

            except Exception as e:
                print(f"处理概念板块数据失败: {str(e)}")
                continue

        # 执行批量新增
        add_count = 0
        if boards_to_add:
            board_models = [StockBoardConcept(**data) for data in boards_to_add]
            await batch_board_concept_add(db, board_models)
            add_count = len(board_models)

        # 执行批量更新
        update_count = 0
        if boards_to_update:
            await batch_board_concept_update(db, boards_to_update)
            update_count = len(boards_to_update)

        message = f"成功同步：新增 {add_count} 条，更新 {update_count} 条概念板块数据"
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        raise e
