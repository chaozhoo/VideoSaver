import os

def load_style(style_name):
    try:
        style_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'styles', 
            style_name
        )
        with open(style_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"加载样式文件失败: {str(e)}")
        return None 