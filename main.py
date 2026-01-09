import tkinter as tk
import pandas as pd
import os

# ==================== 全局参数配置 ====================
# 字体配置
FONT_FAMILY = "Microsoft YaHei"  # 微软雅黑作为主要字体

# 标题字体 - 用于周期表主标题
FONT_TITLE = (FONT_FAMILY, 18, "bold")      # 18号加粗，用于主标题

# 副标题字体 - 用于详情面板标题
FONT_SUBTITLE = (FONT_FAMILY, 16, "bold")   # 16号加粗，用于副标题

# 正常字体 - 用于主要文本内容
FONT_NORMAL = (FONT_FAMILY, 14)             # 14号常规，用于重要文本显示

# 小号字体 - 用于普通辅助文本
FONT_SMALL = (FONT_FAMILY, 8)               # 8号常规，用于小号文本

# 极小字体 - 用于元素单元格中的原子序数等极小文本
FONT_TINY = (FONT_FAMILY, 6)                # 6号常规，与FONT_SMALL相同但用途不同

# 元素符号字体 - 专门用于元素符号显示
FONT_ELEMENT_SYMBOL = (FONT_FAMILY, 12, "bold")  # 12号加粗，突出元素符号

# 状态栏字体 - 用于底部状态栏文本
FONT_STATUS = (FONT_FAMILY, 9)              # 9号常规，用于状态栏提示信息

# 颜色方案
COLOR_SCHEME = {
    'alkali_metal': '#FF6666',
    'alkaline_earth': '#FFDEAD',
    'transition_metal': '#FFB6C1',
    'basic_metal': '#CCCCCC',
    'metalloid': '#99CC99',
    'nonmetal': '#87CEEB',
    'halogen': '#FFFF99',
    'noble_gas': '#FFB7C5',
    'lanthanide': '#FFA07A',  # 镧系元素颜色
    'actinide': '#E6E6FA',  # 锕系元素颜色
    'unknown': '#D3D3D3',
    'status_bg': '#e0e0e0',
    'detail_bg': 'white',
    'text_bg': '#f5f5f5',
    'separator': 'gray'
}

# 新增镧系和锕系颜色（与上面不同，便于区分）
COLOR_LANTHANIDE = '#FF9966'  # 更鲜艳的橙色
COLOR_ACTINIDE = '#CC99FF'  # 更鲜艳的紫色

# 窗口和布局参数
WINDOW_TITLE = "元素周期表"
WINDOW_SIZE = "1300x800"  # 增加高度以容纳下方两行
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
DETAIL_PANEL_WIDTH = 300
ELEMENT_CELL_WIDTH = 50
ELEMENT_CELL_HEIGHT = 60
TEXT_AREA_HEIGHT = 20
TEXT_AREA_WIDTH = 35
STATUS_BAR_HEIGHT = 25
LANTHANIDE_ROW_HEIGHT = 70  # 镧系行高度
ACTINIDE_ROW_HEIGHT = 70  # 锕系行高度
SEPARATOR_HEIGHT = 20  # 分隔行高度

# 文本内容
TEXT_ELEMENTS = "元素总数: {}"
TEXT_HINT = "提示：点击元素查看详细信息"
TEXT_DETAIL_TITLE = "元素详情"
TEXT_CLICK_TO_VIEW = "点击元素查看详情"
TEXT_INITIAL_PROMPT = "请点击周期表中的元素查看详细信息"
TEXT_ERROR_LOADING = "无法加载数据文件"
TEXT_LANTHANIDE = "镧系元素"
TEXT_ACTINIDE = "锕系元素"
TEXT_SEPARATOR = "══════════════════════════════════════════"


# ==================== 参数配置结束 ====================


class SimplePeriodicTable:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # 加载数据
        self.data = self.load_data()

        # 分离主族元素和镧系/锕系元素
        self.main_elements = []
        self.lanthanides = []
        self.actinides = []
        self.separate_elements()

        # UI 组件
        self.detail_text = None
        self.current_element = None  # 在这里声明

        # 构建界面
        self.build_ui()

    def load_data(self):
        """加载元素数据"""
        csv_path = os.path.join(os.path.dirname(__file__), "elements.csv")
        df = pd.read_csv(csv_path)
        return df


    def separate_elements(self):
        """分离主族元素、镧系和锕系元素"""
        if not self.data.empty:
            # 获取所有元素数据
            all_elements = [self.data.iloc[i].to_dict() for i in range(len(self.data))]

            for element in all_elements:
                atomic_num = element.get('atomic_number', 0)

                # 镧系元素：原子序数57-71
                if 57 <= atomic_num <= 71:
                    self.lanthanides.append(element)
                # 锕系元素：原子序数89-103
                elif 89 <= atomic_num <= 103:
                    self.actinides.append(element)
                # 其他元素
                else:
                    self.main_elements.append(element)

            # 按原子序数排序
            self.lanthanides.sort(key=lambda x: x['atomic_number'])
            self.actinides.sort(key=lambda x: x['atomic_number'])
            self.main_elements.sort(key=lambda x: x['atomic_number'])

    def find_element_by_position(self, period, group):
        """根据周期和族查找元素"""
        if not self.data.empty:
            mask = (self.data['period'] == period) & (self.data['group'] == group)
            result = self.data[mask]
            if len(result) > 0:
                element = result.iloc[0].to_dict()
                symbol = element.get('symbol', '')

                # 如果是La（周期6，族3）或Ac（周期7，族3），返回特殊标记
                if symbol == 'La' and period == 6 and group == 3:
                    return {'symbol': '57-71', 'name': '镧系', 'atomic_number': '',
                            'is_special': True, 'bg_color': COLOR_LANTHANIDE}
                elif symbol == 'Ac' and period == 7 and group == 3:
                    return {'symbol': '89-103', 'name': '锕系', 'atomic_number': '',
                            'is_special': True, 'bg_color': COLOR_ACTINIDE}

                return element
        return None

    def build_ui(self):
        """构建主界面"""
        # 创建主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 创建左侧周期表区域
        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建右侧详情区域
        right_frame = tk.Frame(main_container, width=DETAIL_PANEL_WIDTH, bg=COLOR_SCHEME['detail_bg'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 10), pady=10)
        right_frame.pack_propagate(False)  # 固定宽度

        # 在左侧添加周期表
        self.create_periodic_table(left_frame)

        # 在右侧添加元素详情
        self.create_detail_panel(right_frame)

        # 底部状态栏
        self.create_status_bar()

    def create_periodic_table(self, parent):
        """创建周期表网格（包含主表和镧系/锕系）"""
        # 创建滚动条容器
        canvas_container = tk.Frame(parent)
        canvas_container.pack(fill=tk.BOTH, expand=True)

        # 创建画布和滚动条
        canvas = tk.Canvas(canvas_container)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)

        # 创建滚动区域框架
        scrollable_frame = tk.Frame(canvas)

        # 配置滚动区域
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 创建窗口
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 布局画布和滚动条
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 标题
        title_label = tk.Label(scrollable_frame, text=WINDOW_TITLE, font=FONT_TITLE)
        title_label.pack(pady=(0, 10))

        # 创建主周期表框架
        main_table_frame = tk.Frame(scrollable_frame)
        main_table_frame.pack(fill=tk.X, pady=(0, 10))

        # 创建7个周期的主要框架
        for period in range(1, 8):
            period_frame = tk.Frame(main_table_frame)
            period_frame.pack(fill=tk.X, pady=2)

            # 创建该周期的元素框架
            elements_frame = tk.Frame(period_frame)
            elements_frame.pack(fill=tk.X, expand=True)

            # 根据周期确定族范围
            if period == 1:
                groups = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18]
            else:
                groups = list(range(1, 19))

            # 创建该周期的元素按钮
            for group in groups:
                cell_frame = tk.Frame(elements_frame,
                                      width=ELEMENT_CELL_WIDTH,
                                      height=ELEMENT_CELL_HEIGHT,
                                      relief=tk.RAISED,
                                      bd=1)
                cell_frame.pack(side=tk.LEFT, padx=1, pady=1)
                cell_frame.pack_propagate(False)

                if group != 0:  # 不是空位置
                    element = self.find_element_by_position(period, group)
                    if element is not None:
                        self.create_element_cell(cell_frame, element, False)

        # 添加分隔线
        separator_frame = tk.Frame(scrollable_frame, height=2, bg=COLOR_SCHEME['separator'])
        separator_frame.pack(fill=tk.X, pady=10)

        # 镧系元素行
        lanthanide_frame = tk.Frame(scrollable_frame)
        lanthanide_frame.pack(fill=tk.X, pady=5)

        # 镧系标题
        lanthanide_label = tk.Label(lanthanide_frame,
                                    text=TEXT_LANTHANIDE,
                                    font=FONT_NORMAL,
                                    fg=COLOR_LANTHANIDE)
        lanthanide_label.pack(anchor='w', padx=5)

        # 镧系元素容器
        lanthanide_container = tk.Frame(lanthanide_frame)
        lanthanide_container.pack(fill=tk.X, pady=5)

        # 创建镧系元素（共15个，从La到Lu）
        for i in range(15):  # 镧系有15个元素
            cell_frame = tk.Frame(lanthanide_container,
                                  width=ELEMENT_CELL_WIDTH,
                                  height=ELEMENT_CELL_HEIGHT,
                                  relief=tk.RAISED,
                                  bd=1)
            cell_frame.pack(side=tk.LEFT, padx=1, pady=1)
            cell_frame.pack_propagate(False)

            # 如果存在对应的镧系元素数据
            if i < len(self.lanthanides):
                element = self.lanthanides[i]
                self.create_element_cell(cell_frame, element, True, COLOR_LANTHANIDE)
            else:
                # 空单元格
                cell_frame.config(bg='white')

        # 锕系元素行
        actinide_frame = tk.Frame(scrollable_frame)
        actinide_frame.pack(fill=tk.X, pady=5)

        # 锕系标题
        actinide_label = tk.Label(actinide_frame,
                                  text=TEXT_ACTINIDE,
                                  font=FONT_NORMAL,
                                  fg=COLOR_ACTINIDE)
        actinide_label.pack(anchor='w', padx=5)

        # 锕系元素容器
        actinide_container = tk.Frame(actinide_frame)
        actinide_container.pack(fill=tk.X, pady=5)

        # 创建锕系元素（共15个，从Ac到Lr）
        for i in range(15):  # 锕系有15个元素
            cell_frame = tk.Frame(actinide_container,
                                  width=ELEMENT_CELL_WIDTH,
                                  height=ELEMENT_CELL_HEIGHT,
                                  relief=tk.RAISED,
                                  bd=1)
            cell_frame.pack(side=tk.LEFT, padx=1, pady=1)
            cell_frame.pack_propagate(False)

            # 如果存在对应的锕系元素数据
            if i < len(self.actinides):
                element = self.actinides[i]
                self.create_element_cell(cell_frame, element, True, COLOR_ACTINIDE)
            else:
                # 空单元格
                cell_frame.config(bg='white')

    def create_element_cell(self, parent, element, is_series=False, series_color=None):
        """创建单个元素格子"""
        # 检查是否是特殊框（表示镧系或锕系范围）
        is_special = element.get('is_special', False)

        if is_special:
            # 特殊框：显示镧系或锕系范围
            bg_color = element.get('bg_color', COLOR_SCHEME['unknown'])
            parent.config(bg=bg_color)

            # 不显示原子序数
            # 直接显示范围符号（居中大号字体）
            symbol = tk.Label(parent,
                              text=element['symbol'],
                              bg=bg_color,
                              font=FONT_TINY)
            symbol.pack(expand=True)

            # 显示系列名称
            name = tk.Label(parent,
                            text=element['name'],
                            bg=bg_color,
                            font=FONT_TINY)
            name.pack(side='bottom', pady=2)

            # 特殊框不可点击，不绑定事件
            return

        # 以下是原来的普通元素代码
        # 根据元素类别获取颜色
        if is_series and series_color:
            bg_color = series_color
        else:
            category = element.get('category', 'unknown')
            bg_color = COLOR_SCHEME.get(category, COLOR_SCHEME['unknown'])

        # 设置框架背景色
        parent.config(bg=bg_color)

        # 原子序数（小号）
        atomic_num = tk.Label(parent,
                              text=str(element['atomic_number']),
                              bg=bg_color,
                              font=FONT_TINY)
        atomic_num.pack(anchor='ne', padx=2)

        # 元素符号（大号）
        symbol = tk.Label(parent,
                          text=element['symbol'],
                          bg=bg_color,
                          font=FONT_ELEMENT_SYMBOL)
        symbol.pack(expand=True)

        # 元素名称（小号）
        name = tk.Label(parent,
                        text=element['name'],
                        bg=bg_color,
                        font=FONT_TINY)
        name.pack(side='bottom', pady=2)

        # 绑定点击事件
        for widget in [parent, atomic_num, symbol, name]:
            widget.bind('<Button-1>', lambda e, el=element: self.show_element_detail(el))
    def create_detail_panel(self, parent):
        """创建元素详情面板"""
        # 标题
        detail_title = tk.Label(parent,
                                text=TEXT_DETAIL_TITLE,
                                font=FONT_SUBTITLE,
                                bg=COLOR_SCHEME['detail_bg'])
        detail_title.pack(pady=10)

        # 当前选中元素
        self.current_element = tk.StringVar(value=TEXT_CLICK_TO_VIEW)
        element_label = tk.Label(parent,
                                 textvariable=self.current_element,
                                 font=FONT_NORMAL,
                                 bg=COLOR_SCHEME['detail_bg'])
        element_label.pack(pady=5)

        # 分隔线
        separator = tk.Frame(parent, height=2, bg=COLOR_SCHEME['separator'])
        separator.pack(fill=tk.X, pady=10, padx=10)

        # 详细信息文本框
        detail_frame = tk.Frame(parent, bg=COLOR_SCHEME['detail_bg'])
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # 使用Text控件显示详细信息
        self.detail_text = tk.Text(detail_frame,
                                   height=TEXT_AREA_HEIGHT,
                                   width=TEXT_AREA_WIDTH,
                                   font=FONT_SMALL,
                                   bg=COLOR_SCHEME['text_bg'],
                                   relief=tk.FLAT)
        self.detail_text.pack(fill=tk.BOTH, expand=True)


        # 初始提示
        self.detail_text.insert(tk.END, TEXT_INITIAL_PROMPT)
        self.detail_text.config(state=tk.DISABLED)

    def create_status_bar(self):
        """创建状态栏"""
        status_bar = tk.Frame(self.root, height=STATUS_BAR_HEIGHT, bg=COLOR_SCHEME['status_bg'])
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 计算所有元素数量（包括镧系和锕系）
        total_elements = len(self.main_elements) + len(self.lanthanides) + len(self.actinides)
        count_text = TEXT_ELEMENTS.format(total_elements) if self.data is not None else "数据加载失败"

        count_label = tk.Label(status_bar, text=count_text, bg=COLOR_SCHEME['status_bg'])
        count_label.pack(side=tk.RIGHT, padx=10)

        # 提示信息
        hint_label = tk.Label(status_bar,
                              text=TEXT_HINT,
                              bg=COLOR_SCHEME['status_bg'],
                              font=FONT_STATUS)
        hint_label.pack(side=tk.LEFT, padx=10)

    def show_element_detail(self, element):
        """显示元素详细信息"""
        # 更新当前元素标题
        self.current_element.set(f"{element['symbol']} - {element['name']}")

        # 更新详细信息
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete(1.0, tk.END)

        # 基本信息
        details = f"【基本信息】\n"
        details += f"元素符号: {element['symbol']}\n"
        details += f"元素名称: {element['name']}\n"
        details += f"原子序数: {element['atomic_number']}\n"
        details += f"相对原子质量: {element.get('mass', 'N/A')}\n"
        details += f"周期: {element.get('period', 'N/A')}\n"
        details += f"族: {element.get('group', 'N/A')}\n"


        atomic_num = element.get('atomic_number', 0)
        if 57 <= atomic_num <= 71:
            details += f"所属系列: 镧系元素\n"
        elif 89 <= atomic_num <= 103:
            details += f"所属系列: 锕系元素\n"
        elif 21 <= atomic_num <= 30 or 39 <= atomic_num <= 48 or 72<= atomic_num <= 80 or 104<= atomic_num <=112:
            details += f"所属系列: 副族元素\n"
        else:
            details += f"所属系列: 主族元素\n"

        # 物理性质
        details += f"\n【物理性质】\n"
        details += f"密度: {element.get('density', 'N/A')} g/cm³\n"
        details += f"熔点: {element.get('melting_point', 'N/A')} K\n"
        details += f"沸点: {element.get('boiling_point', 'N/A')} K\n"
        details += f"状态: {element.get('state_room_temp', 'N/A')}\n"

        # 化学性质
        details += f"\n【化学性质】\n"
        details += f"电负性: {element.get('electronegativity', 'N/A')}\n"
        details += f"原子半径: {element.get('atomic_radius', 'N/A')} pm\n"

        # 其他信息
        details += f"\n【其他信息】\n"
        details += f"类别: {element.get('category', 'N/A')}\n"
        details += f"发现年份: {element.get('discovery_year', 'N/A')}\n"

        self.detail_text.insert(tk.END, details)
        self.detail_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    SimplePeriodicTable(root)
    root.mainloop()


if __name__ == "__main__":
    main()