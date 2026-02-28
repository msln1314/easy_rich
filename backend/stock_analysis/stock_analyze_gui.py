import sys
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import multiprocessing
import queue
import re
from datetime import datetime
import traceback
import importlib.util

# 尝试导入 stock_analyze
stock_analyze = None
import_error_msg = ""

def load_stock_analyze_dynamic():
    global stock_analyze, import_error_msg
    
    # 查找候选路径
    candidates = []
    if getattr(sys, 'frozen', False):
        # Frozen: look in _MEIPASS and executable dir
        if hasattr(sys, '_MEIPASS'):
            candidates.append(os.path.join(sys._MEIPASS, 'stock_analyze.py'))
        candidates.append(os.path.join(os.path.dirname(sys.executable), 'stock_analyze.py'))
    else:
        # Dev: look in current dir
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stock_analyze.py'))
        candidates.append('stock_analyze.py')

    found_path = None
    for p in candidates:
        if os.path.exists(p):
            found_path = p
            break
            
    if found_path:
        try:
            # Use a unique name to avoid conflicts with existing sys.modules entries
            module_name = "stock_analyze_dynamic"
            spec = importlib.util.spec_from_file_location(module_name, found_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # Do not register in sys.modules to avoid side effects if possible, 
                # or register with the unique name
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                stock_analyze = module
                return True
        except Exception as e:
            import_error_msg += f"Dynamic load from {found_path} failed: {e}\n{traceback.format_exc()}\n"
    else:
        import_error_msg += f"stock_analyze.py not found in candidates: {candidates}\n"
    
    return False

# First try standard import
try:
    import stock_analyze
    # Check if it has main
    if not hasattr(stock_analyze, 'main'):
        import_error_msg += f"Standard import successful but 'main' not found. Module file: {getattr(stock_analyze, '__file__', 'unknown')}\n"
        stock_analyze = None # Discard invalid module
    else:
        pass # Good to go
except ImportError as e:
    import_error_msg += f"Standard import failed: {e}\n"

# If standard import failed or returned invalid module, try dynamic load
if not stock_analyze:
    load_stock_analyze_dynamic()



class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # miliseconds
        self.wraplength = 300   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffe0", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class MultiSelectDropdown(ttk.Frame):
    def __init__(self, master=None, textvariable=None, values=None, **kwargs):
        super().__init__(master, **kwargs)
        self.textvariable = textvariable
        self.values = values or []
        
        self.entry = ttk.Entry(self, textvariable=self.textvariable, state="readonly")
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Button-1>", self.show_popup)
        
        self.btn = ttk.Button(self, text="▼", width=3, command=self.show_popup)
        self.btn.pack(side=tk.RIGHT, fill=tk.Y)

    def show_popup(self, event=None):
        popup = tk.Toplevel(self)
        popup.title("")
        popup.overrideredirect(True)
        
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        w = self.winfo_width()
        popup.geometry(f"{w}x250+{x}+{y}")
        
        # Main layout
        list_frame = ttk.Frame(popup)
        list_frame.pack(side="top", fill="both", expand=True)
        
        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=w-20)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_frame = ttk.Frame(popup)
        btn_frame.pack(side="bottom", fill="x")
        ttk.Button(btn_frame, text="确定", command=lambda: self.confirm(popup)).pack(fill="x")
        
        self.check_vars = {}
        current_val = self.textvariable.get()
        current_parts = current_val.split()
        is_all = "所有" in current_parts or not current_parts
        
        # "所有" option
        var_all = tk.BooleanVar(value=is_all)
        cb_all = ttk.Checkbutton(scrollable_frame, text="所有", variable=var_all)
        cb_all.pack(anchor="w", padx=5, pady=2)
        self.check_vars["所有"] = var_all
        
        def on_all_click():
            if var_all.get():
                for k, v in self.check_vars.items():
                    if k != "所有": v.set(False)
        cb_all.config(command=on_all_click)

        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", padx=5, pady=2)
        
        # Other options
        for val in self.values:
            if val == "所有": continue
            is_checked = val in current_parts and not is_all
            var = tk.BooleanVar(value=is_checked)
            cb = ttk.Checkbutton(scrollable_frame, text=val, variable=var)
            cb.pack(anchor="w", padx=5, pady=2)
            self.check_vars[val] = var
            
            def on_item_click(v=var):
                if v.get():
                    var_all.set(False)
            cb.config(command=on_item_click)
            
        popup.focus_set()
        popup.grab_set()
        
        # Close on click outside
        def on_click_outside(event):
            try:
                x, y = event.x_root, event.y_root
                x1 = popup.winfo_rootx()
                y1 = popup.winfo_rooty()
                x2 = x1 + popup.winfo_width()
                y2 = y1 + popup.winfo_height()
                
                if not (x1 <= x <= x2 and y1 <= y <= y2):
                    self.confirm(popup)
            except Exception:
                pass
        
        popup.bind("<Button-1>", on_click_outside)
        
    def confirm(self, popup):
        selected = []
        if self.check_vars["所有"].get():
            selected = ["所有"]
        else:
            for val in self.values:
                if val == "所有": continue
                if self.check_vars[val].get():
                    selected.append(val)
        
        if not selected:
            selected = ["所有"]
            
        self.textvariable.set(" ".join(selected))
        popup.destroy()

class StockAnalyzeGUI:
    def __init__(self, root):
        self.root = root
        self.version = "1.0.1"
        self.author = "sam.wan@qq.com"
        self.root.title(f"股票分析工具 GUI v{self.version} - 作者: {self.author}")
        self.root.geometry("1000x800")
        
        self.process = None
        self.queue = queue.Queue()
        self.stop_event = threading.Event()

        self.create_widgets()
        self.load_config_content()

        # Check queue for output
        self.root.after(100, self.check_queue)

    def create_widgets(self):
        # Main layout
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_basic = ttk.Frame(notebook)
        self.tab_filter = ttk.Frame(notebook)
        self.tab_advanced = ttk.Frame(notebook)
        self.tab_financial = ttk.Frame(notebook)
        self.tab_config = ttk.Frame(notebook)

        notebook.add(self.tab_basic, text="基础设置")
        notebook.add(self.tab_filter, text="筛选条件")
        notebook.add(self.tab_advanced, text="高级选项")
        notebook.add(self.tab_financial, text="财务/其他")
        notebook.add(self.tab_config, text="配置文件")

        self.create_basic_tab()
        self.create_filter_tab()
        self.create_advanced_tab()
        self.create_financial_tab()
        self.create_config_tab()

        # Bottom area: Buttons and Log
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        self.btn_run = ttk.Button(btn_frame, text="开始分析", command=self.run_analysis)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        self.btn_stop = ttk.Button(btn_frame, text="停止", command=self.stop_analysis, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_clear = ttk.Button(btn_frame, text="清空日志", command=self.clear_log)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        # Log area
        log_frame = ttk.LabelFrame(bottom_frame, text="运行日志")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, state='disabled', height=15, font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tags for coloring
        self.log_text.tag_config('INFO', foreground='black')
        self.log_text.tag_config('ERROR', foreground='red')
        self.log_text.tag_config('WARNING', foreground='orange')

    def create_basic_tab(self):
        frame = self.tab_basic
        
        # Grid layout helper
        def add_entry(parent, label, row, col, var_type=tk.StringVar, default="", tooltip=""):
            lbl = ttk.Label(parent, text=label)
            lbl.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
            if tooltip:
                ToolTip(lbl, tooltip)
            
            var = var_type(value=default)
            entry = ttk.Entry(parent, textvariable=var)
            entry.grid(row=row, column=col+1, sticky=tk.EW, padx=5, pady=5)
            if tooltip:
                ToolTip(entry, tooltip)
            return var

        self.vars = {}

        # Codes
        self.vars['codes'] = add_entry(frame, "股票代码 (逗号分隔):", 0, 0, tooltip="指定要分析的股票代码，多个代码用逗号分隔")
        
        # Days
        self.vars['days'] = add_entry(frame, "分析天数 (-d):", 1, 0, default="30", tooltip="分析的历史数据天数，默认30天（最少5个交易日）")
        
        # Start/End Date
        self.vars['start_date'] = add_entry(frame, "开始日期 (YYYYMMDD):", 2, 0, tooltip="指定分析开始日期，格式YYYYMMDD。不能与分析天数同时使用")
        self.vars['end_date'] = add_entry(frame, "结束日期 (YYYYMMDD):", 3, 0, tooltip="指定分析结束日期，格式YYYYMMDD。不能与分析天数同时使用")
        
        # Top K
        self.vars['k'] = add_entry(frame, "显示前K只 (-k):", 4, 0, default="10", tooltip="分析完成后，只显示排名前K只股票")
        
        # Parallel
        self.vars['parallel'] = add_entry(frame, "并行进程数 (-p):", 5, 0, default="8", tooltip="并行处理的进程数，根据CPU核心数调整")

        # Checkboxes
        self.vars['all'] = tk.BooleanVar()
        cb_all = ttk.Checkbutton(frame, text="分析所有股票 (--all)", variable=self.vars['all'])
        cb_all.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_all, "分析所有上证和深证股票（耗时较长）")

        self.vars['topgains'] = tk.BooleanVar()
        cb_topgains = ttk.Checkbutton(frame, text="按涨幅排序 (-g)", variable=self.vars['topgains'])
        cb_topgains.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_topgains, "结果按照区间涨幅排序（仅在分析多只股票时有效）")

        frame.columnconfigure(1, weight=1)

    def create_filter_tab(self):
        frame = self.tab_filter
        
        def add_entry(parent, label, row, col, default="", tooltip=""):
            lbl = ttk.Label(parent, text=label)
            lbl.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
            if tooltip:
                ToolTip(lbl, tooltip)
            var = tk.StringVar(value=default)
            entry = ttk.Entry(parent, textvariable=var)
            entry.grid(row=row, column=col+1, sticky=tk.EW, padx=5, pady=5)
            if tooltip:
                ToolTip(entry, tooltip)
            return var

        self.vars['sector_filter'] = tk.StringVar(value="所有")
        lbl_sector = ttk.Label(frame, text="板块筛选:")
        lbl_sector.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(lbl_sector, "指定热门板块筛选（如AI,芯片,航天,人工智能,半导体,军工）\n选择'所有'则不进行板块筛选")
        
        sector_values = ["所有", "AI", "芯片", "航天", "人工智能", "半导体", "军工", "能源", "可控核聚变", "通讯模块", "光纤", "新能源", "电子模块"]
        combo_sector = MultiSelectDropdown(frame, textvariable=self.vars['sector_filter'], values=sector_values)
        combo_sector.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        ToolTip(combo_sector.entry, "点击选择板块，支持多选。\n选择'所有'则不进行板块筛选")
        self.vars['min_avg_volume'] = add_entry(frame, "最小平均成交量:", 1, 0, tooltip="过滤平均成交量过低的股票（单位：手，按所选区间平均）")
        self.vars['max_rsi'] = add_entry(frame, "最大 RSI:", 2, 0, tooltip="过滤末值RSI过高（超买）的股票")
        self.vars['max_volatility'] = add_entry(frame, "最大波动率 (%):", 3, 0, tooltip="过滤区间波动率过高的股票（单位：百分比）")
        
        # Breakout
        self.vars['breakout'] = tk.BooleanVar()
        cb_breakout = ttk.Checkbutton(frame, text="启用突破过滤 (--breakout)", variable=self.vars['breakout'])
        cb_breakout.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_breakout, "启用突破过滤（新高+量能放大+MACD为正）")
        
        self.vars['breakout_window'] = add_entry(frame, "突破窗口天数:", 5, 0, default="10", tooltip="突破窗口天数（默认10）")
        self.vars['breakout_vol_mult'] = add_entry(frame, "突破量能倍数:", 6, 0, default="1.3", tooltip="突破量能放大倍数阈值（默认1.3）")

        frame.columnconfigure(1, weight=1)

    def create_advanced_tab(self):
        frame = self.tab_advanced
        
        # Checkboxes
        row = 0
        self.vars['ai'] = tk.BooleanVar()
        cb_ai = ttk.Checkbutton(frame, text="启用 AI 分析 (--ai)", variable=self.vars['ai'])
        cb_ai.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_ai, "启用AI分析功能, 需要在 config.toml 中配置 [llm] 部分")
        
        self.vars['fast'] = tk.BooleanVar()
        cb_fast = ttk.Checkbutton(frame, text="快速模式 (--fast)", variable=self.vars['fast'])
        cb_fast.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_fast, "快速模式：跳过东财实时与历史接口，优先使用腾讯与缓存")
        row += 1

        self.vars['cache'] = tk.BooleanVar()
        cb_cache = ttk.Checkbutton(frame, text="使用缓存 (--cache)", variable=self.vars['cache'])
        cb_cache.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_cache, "启用缓存（parquet/csv），命令行优先于配置文件")
        
        self.vars['refresh_cache'] = tk.BooleanVar()
        cb_refresh = ttk.Checkbutton(frame, text="刷新缓存 (--refresh-cache)", variable=self.vars['refresh_cache'])
        cb_refresh.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_refresh, "分析前刷新所选区间的历史数据缓存")
        row += 1

        self.vars['force'] = tk.BooleanVar()
        cb_force = ttk.Checkbutton(frame, text="强制运行 (--force)", variable=self.vars['force'])
        cb_force.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_force, "预检失败仍然强制运行")
        
        self.vars['debug'] = tk.BooleanVar()
        cb_debug = ttk.Checkbutton(frame, text="调试模式 (--debug)", variable=self.vars['debug'])
        cb_debug.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_debug, "启用调试模式，输出更多日志信息")
        row += 1

        self.vars['industry_neutral'] = tk.BooleanVar()
        cb_ind = ttk.Checkbutton(frame, text="行业中性化 (--industry-neutral)", variable=self.vars['industry_neutral'])
        cb_ind.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_ind, "启用行业中性化排名（按行业内z-score排序后再合并）")

        self.vars['rank_expected'] = tk.BooleanVar()
        cb_rank = ttk.Checkbutton(frame, text="按期望分排序 (--rank-expected)", variable=self.vars['rank_expected'])
        cb_rank.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_rank, "按风险调整后的期望分排序")
        row += 1

        self.vars['strict'] = tk.BooleanVar()
        cb_strict = ttk.Checkbutton(frame, text="严格模式 (--strict)", variable=self.vars['strict'])
        cb_strict.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_strict, "严格模式：强制正收益、trend命中、期望分排序并扩大候选集")
        
        self.vars['forward'] = tk.BooleanVar()
        cb_forward = ttk.Checkbutton(frame, text="前瞻模式 (--forward)", variable=self.vars['forward'])
        cb_forward.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_forward, "前瞻模式：仅生成analysis_results与图表，不执行验证")
        row += 1

        # Entries
        lbl_mins = ttk.Label(frame, text="分钟周期 (1/5/15/30/60):")
        lbl_mins.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(lbl_mins, "分钟级分析周期，支持1/5/15/30/60分钟")
        self.vars['mins'] = tk.StringVar()
        mins_combo = ttk.Combobox(frame, textvariable=self.vars['mins'], values=['1', '5', '15', '30', '60'])
        mins_combo.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
        ToolTip(mins_combo, "推荐使用5或15分钟周期")
        row += 1

        self.vars['minute_sim'] = tk.BooleanVar()
        cb_minsim = ttk.Checkbutton(frame, text="日线模拟分钟数据 (--minute-sim)", variable=self.vars['minute_sim'])
        cb_minsim.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_minsim, "允许在分钟数据不可用时使用日线模拟分钟数据")
        row += 1

        self.vars['minute_chart'] = tk.BooleanVar()
        cb_minchart = ttk.Checkbutton(frame, text="生成分钟图表 (--minute-chart)", variable=self.vars['minute_chart'])
        cb_minchart.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_minchart, "为分钟级分析生成图表（仅在启用 -m 或 -d 5 时生效）")
        row += 1

        lbl_trend = ttk.Label(frame, text="趋势验证天数:")
        lbl_trend.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(lbl_trend, "趋势验证天数，表示预期在N天内出现上涨")
        self.vars['trend_day'] = tk.StringVar()
        entry_trend = ttk.Entry(frame, textvariable=self.vars['trend_day'])
        entry_trend.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
        ToolTip(entry_trend, "趋势验证天数")
        row += 1

        lbl_val = ttk.Label(frame, text="验证窗口天数:")
        lbl_val.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(lbl_val, "验证窗口天数，用于评估所选股票在后续区间的表现")
        self.vars['validate_days'] = tk.StringVar()
        entry_val = ttk.Entry(frame, textvariable=self.vars['validate_days'])
        entry_val.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
        ToolTip(entry_val, "验证窗口天数")
        row += 1

    def create_financial_tab(self):
        frame = self.tab_financial
        
        row = 0
        self.vars['use_financial'] = tk.BooleanVar()
        cb_fin = ttk.Checkbutton(frame, text="启用财务因子调整 (--use-financial)", variable=self.vars['use_financial'])
        cb_fin.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_fin, "启用财务因子调整得分")
        row += 1

        self.vars['pe'] = tk.BooleanVar()
        cb_pe = ttk.Checkbutton(frame, text="市盈率 PE", variable=self.vars['pe'])
        cb_pe.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_pe, "启用市盈率(PE)评分")
        
        self.vars['pb'] = tk.BooleanVar()
        cb_pb = ttk.Checkbutton(frame, text="市净率 PB", variable=self.vars['pb'])
        cb_pb.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_pb, "启用市净率(PB)评分")
        row += 1

        self.vars['volume'] = tk.BooleanVar()
        cb_vol = ttk.Checkbutton(frame, text="成交量评分", variable=self.vars['volume'])
        cb_vol.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_vol, "启用成交量评分")
        
        self.vars['turnover'] = tk.BooleanVar()
        cb_turn = ttk.Checkbutton(frame, text="成交额评分", variable=self.vars['turnover'])
        cb_turn.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_turn, "启用成交额评分")
        row += 1

        self.vars['news'] = tk.BooleanVar()
        cb_news = ttk.Checkbutton(frame, text="新闻分析 (--news)", variable=self.vars['news'])
        cb_news.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_news, "启用新闻热度分析，从互联网搜索股票相关新闻并分析关键词")
        
        lbl_region = ttk.Label(frame, text="地区 (cn/intl):")
        lbl_region.grid(row=row, column=1, sticky=tk.E, padx=5, pady=5)
        ToolTip(lbl_region, "新闻搜索地区")
        self.vars['region'] = tk.StringVar(value="cn")
        region_combo = ttk.Combobox(frame, textvariable=self.vars['region'], values=['cn', 'intl'], width=10)
        region_combo.grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(region_combo, "cn: 中国(使用百度)，intl: 国际(使用DuckDuckGo)")
        row += 1

        self.vars['expert_filter'] = tk.BooleanVar()
        cb_expert = ttk.Checkbutton(frame, text="专家规则筛选 (--expert-filter)", variable=self.vars['expert_filter'])
        cb_expert.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ToolTip(cb_expert, "启用经验规则筛选")

    def create_config_tab(self):
        frame = self.tab_config
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="加载 config.toml", command=self.load_config_content).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存 config.toml", command=self.save_config_content).pack(side=tk.LEFT, padx=5)
        
        self.config_text = scrolledtext.ScrolledText(frame, height=20, font=('Consolas', 10))
        self.config_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_config_content(self):
        try:
            if os.path.exists("config.toml"):
                with open("config.toml", "r", encoding="utf-8") as f:
                    content = f.read()
                    self.config_text.delete(1.0, tk.END)
                    self.config_text.insert(tk.END, content)
                    self.log("INFO", "已加载 config.toml")
            elif os.path.exists("config.example.toml"):
                 with open("config.example.toml", "r", encoding="utf-8") as f:
                    content = f.read()
                    self.config_text.delete(1.0, tk.END)
                    self.config_text.insert(tk.END, content)
                    self.log("INFO", "已加载 config.example.toml (config.toml 不存在)")
        except Exception as e:
            self.log("ERROR", f"加载配置文件失败: {e}")

    def save_config_content(self):
        try:
            content = self.config_text.get(1.0, tk.END)
            with open("config.toml", "w", encoding="utf-8") as f:
                f.write(content)
            self.log("INFO", "config.toml 已保存")
        except Exception as e:
            self.log("ERROR", f"保存配置文件失败: {e}")

    def log(self, level, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {message}\n", level)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')

    def clear_log(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

    def build_command(self):
        # Build command list
        cmd = [sys.executable]
        
        # In a frozen environment, sys.executable is the exe.
        # If we are running this script as an exe, we need to pass args to it to trigger stock_analyze.main()
        # But wait, if we use subprocess with sys.executable, we are spawning a new process of the SAME exe.
        # We need to ensure that the new process enters stock_analyze.main().
        # We can detect this by checking if arguments are present.
        
        # However, if we are in dev mode (python script), sys.executable is python.exe.
        # So we need to pass the script name.
        if getattr(sys, 'frozen', False):
            # Running as EXE
            pass 
        else:
            # Running as script
            # cmd.append(os.path.abspath(__file__)) # Call self
            # Or call stock_analyze.py directly if it exists
             if os.path.exists("stock_analyze.py"):
                 cmd.append("stock_analyze.py")
             else:
                 # Should not happen in dev
                 pass

        # Add arguments
        codes_val = self.vars['codes'].get()
        if codes_val:
            cmd.extend(['-c', codes_val])
            # Check if K needs adjustment
            try:
                k_val = int(self.vars['k'].get())
                codes_list = codes_val.split(',')
                # If codes are provided and count < K, use count as K
                if len(codes_list) < k_val:
                     # We don't change the GUI value, but we pass the adjusted value or let the backend handle it.
                     # However, user asked to "automatically set -k".
                     # It's better to let the backend handle this logic to be consistent, 
                     # but since we are generating the command here, we can also be explicit.
                     # Actually, the user's request implies backend logic adjustment, which we did.
                     # But to be safe and clear in the log command, we can also adjust it here if we want.
                     # Let's rely on the backend logic we just added to stock_analyze.py.
                     pass
            except ValueError:
                pass
        
        if self.vars['days'].get():
            cmd.extend(['-d', self.vars['days'].get()])
            
        if self.vars['start_date'].get():
            cmd.extend(['--start-date', self.vars['start_date'].get()])
            
        if self.vars['end_date'].get():
            cmd.extend(['--end-date', self.vars['end_date'].get()])
            
        if self.vars['k'].get():
            cmd.extend(['-k', self.vars['k'].get()])
            
        if self.vars['parallel'].get():
            cmd.extend(['-p', self.vars['parallel'].get()])

        if self.vars['all'].get():
            cmd.append('--all')
            
        if self.vars['topgains'].get():
            cmd.append('--topgains')

        if self.vars['sector_filter'].get() and self.vars['sector_filter'].get() != "所有":
            cmd.append('--sector-filter')
            cmd.extend(self.vars['sector_filter'].get().split())

        if self.vars['min_avg_volume'].get():
            cmd.extend(['--min-avg-volume', self.vars['min_avg_volume'].get()])
            
        if self.vars['max_rsi'].get():
            cmd.extend(['--max-rsi', self.vars['max_rsi'].get()])
            
        if self.vars['max_volatility'].get():
            cmd.extend(['--max-volatility', self.vars['max_volatility'].get()])

        if self.vars['breakout'].get():
            cmd.append('--breakout')
            if self.vars['breakout_window'].get():
                cmd.extend(['--breakout-window', self.vars['breakout_window'].get()])
            if self.vars['breakout_vol_mult'].get():
                cmd.extend(['--breakout-vol-mult', self.vars['breakout_vol_mult'].get()])

        if self.vars['ai'].get():
            cmd.append('--ai')
            
        if self.vars['fast'].get():
            cmd.append('--fast')
            
        if self.vars['cache'].get():
            cmd.append('--cache')
            
        if self.vars['refresh_cache'].get():
            cmd.append('--refresh-cache')
            
        if self.vars['force'].get():
            cmd.append('--force')
            
        if self.vars['debug'].get():
            cmd.append('--debug')

        if self.vars['industry_neutral'].get():
            cmd.append('--industry-neutral')
            
        if self.vars['rank_expected'].get():
            cmd.append('--rank-expected')
            
        if self.vars['strict'].get():
            cmd.append('--strict')
            
        if self.vars['forward'].get():
            cmd.append('--forward')

        if self.vars['mins'].get():
            cmd.extend(['-m', self.vars['mins'].get()])
            
        if self.vars['minute_sim'].get():
            cmd.append('--minute-sim')
            
        if self.vars['minute_chart'].get():
            cmd.append('--minute-chart')
            
        if self.vars['trend_day'].get():
            cmd.extend(['--trend-day', self.vars['trend_day'].get()])
            
        if self.vars['validate_days'].get():
            cmd.extend(['--validate-days', self.vars['validate_days'].get()])

        if self.vars['use_financial'].get():
            cmd.append('--use-financial')

        if self.vars['pe'].get():
            cmd.append('--pe')
        if self.vars['pb'].get():
            cmd.append('--pb')
        if self.vars['volume'].get():
            cmd.append('--volume')
        if self.vars['turnover'].get():
            cmd.append('--turnover')

        if self.vars['news'].get():
            cmd.append('--news')
            # 只有在启用新闻分析时，才添加地区参数
            if self.vars['region'].get():
                cmd.extend(['--region', self.vars['region'].get()])
            
        if self.vars['expert_filter'].get():
            cmd.append('--expert-filter')

        # GUI模式参数 - 已移除
        # cmd.append('--gui')
        # cmd.append('--gui-no-progress') 


        return cmd

    def run_analysis(self):
        if self.process and self.process.poll() is None:
            messagebox.showinfo("提示", "程序正在运行中...")
            return

        cmd = self.build_command()
        self.log("INFO", f"执行命令: {' '.join(cmd)}")
        
        self.btn_run.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.stop_event.clear()

        def target():
            try:
                # hide console window on windows
                startupinfo = None
                creationflags = 0
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    creationflags = subprocess.CREATE_NO_WINDOW
                
                # 使用 CREATE_NEW_CONSOLE 可以在单独的控制台窗口运行，性能最好，但无法在 GUI 中显示日志
                # 这里我们尝试优化管道缓冲区，或者使用线程读取
                
                # 关键修改：不再重定向 stderr，让其混合在 stdout 中，减少管道竞争
                # 并且不使用 text=True (universal_newlines)，使用二进制读取再手动解码，避免编解码开销
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, 
                    # text=False, # 二进制模式
                    # encoding=None,
                    # bufsize=-1, # 使用系统默认缓冲区
                    text=True, # 保持文本模式以便处理，但依赖 bufsize 优化
                    encoding='utf-8',
                    bufsize=1, # 行缓冲
                    startupinfo=startupinfo,
                    creationflags=creationflags
                )

                import time
                last_progress_time = 0
                progress_interval = 0.1 # GUI mode progress is already throttled, so we can be more responsive

                for line in self.process.stdout:
                    if self.stop_event.is_set():
                        break
                    
                    # Handle tqdm progress output
                    if '分析进度' in line:
                        current_time = time.time()
                        if current_time - last_progress_time < progress_interval:
                            continue # Skip this update if too frequent
                        last_progress_time = current_time
                        
                        self.queue.put(("OUTPUT", line))
                        continue

                    self.queue.put(("OUTPUT", line))

                
                self.process.wait()
                self.queue.put(("DONE", self.process.returncode))

            except Exception as e:
                self.queue.put(("ERROR", str(e)))

        self.thread = threading.Thread(target=target)
        self.thread.daemon = True
        self.thread.start()

    def stop_analysis(self):
        if self.process and self.process.poll() is None:
            self.stop_event.set()
            self.process.terminate()
            self.log("WARNING", "正在停止进程...")
            # We don't wait here to keep UI responsive, check_queue will handle done state

    def check_queue(self):
        # Batch process output to improve performance
        batch_output = []
        batch_limit = 1000 # Max lines per update
        
        while not self.queue.empty():
            try:
                msg_type, content = self.queue.get_nowait()
                if msg_type == "OUTPUT":
                    batch_output.append(content)
                    if len(batch_output) >= batch_limit:
                        break
                elif msg_type == "DONE":
                    self.flush_output(batch_output)
                    batch_output = []
                    self.log("INFO", f"分析结束，返回码: {content}")
                    self.btn_run.config(state=tk.NORMAL)
                    self.btn_stop.config(state=tk.DISABLED)
                    if content == 0:  # Only open on success
                        self.open_output_dir()
                elif msg_type == "ERROR":
                    self.flush_output(batch_output)
                    batch_output = []
                    self.log("ERROR", f"执行出错: {content}")
                    self.btn_run.config(state=tk.NORMAL)
                    self.btn_stop.config(state=tk.DISABLED)
            except queue.Empty:
                break
        
        self.flush_output(batch_output)
        self.root.after(100, self.check_queue)

    def open_output_dir(self):
        base_dir = "data_archive"
        if not os.path.exists(base_dir):
            return
            
        try:
            # Get all subdirectories
            subdirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
            if not subdirs:
                return
                
            # Find the latest one
            latest_dir = max(subdirs, key=os.path.getmtime)
            
            # Open it
            os.startfile(latest_dir)
            self.log("INFO", f"已打开结果目录: {latest_dir}")
        except Exception as e:
            self.log("ERROR", f"无法打开结果目录: {e}")

    def flush_output(self, lines):
        if not lines:
            return
            
        self.log_text.configure(state='normal')
        
        # Smart filtering for GUI progress bars
        filtered_lines = []
        last_progress_idx = -1
        
        # Check if lines are GUI progress updates
        is_progress = ['分析进度:' in line for line in lines]
        
        # Find the last progress line index
        for i in range(len(lines) - 1, -1, -1):
            if is_progress[i]:
                last_progress_idx = i
                break
        
        for i, line in enumerate(lines):
            # If this is a progress line but not the last one in this batch, skip it
            if is_progress[i] and i != last_progress_idx:
                continue
            
            # If we are keeping a progress line, try to delete the previous line 
            if is_progress[i]:
                # Get the last line in the text widget
                last_line_idx = self.log_text.index("end-2c linestart")
                last_line_text = self.log_text.get(last_line_idx, "end-1c")
                if '分析进度:' in last_line_text:
                    self.log_text.delete(last_line_idx, "end-1c")
            
            filtered_lines.append(line)

        # Join and insert
        text_to_insert = "".join(filtered_lines)
        self.log_text.insert(tk.END, text_to_insert)
        
        # Only scroll to end if we inserted something
        if text_to_insert:
            self.log_text.see(tk.END)
            
        self.log_text.configure(state='disabled')

def main():
    # 检测是否是通过命令行传递了参数（除了脚本本身）
    # 如果是冻结应用 (EXE)，sys.argv[0] 是 exe 路径
    # 如果 sys.argv 长度 > 1，说明有参数传入
    
    is_frozen = getattr(sys, 'frozen', False)
    
    if is_frozen:
        if len(sys.argv) > 1:
            # CLI mode
            # 必须调用 stock_analyze.main()
            if stock_analyze:
                # multiprocessing freeze support
                multiprocessing.freeze_support()
                stock_analyze.main()
            else:
                print("Error: stock_analyze module not found.")
                print("Diagnostic Info:")
                print(import_error_msg)
            return
    
    # GUI Mode
    root = tk.Tk()
    app = StockAnalyzeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
