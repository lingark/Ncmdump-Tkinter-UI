import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class NCMConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NCM文件转换器")
        self.root.geometry("400x250")

        # 设置ncmdump工具路径
        self.ncmdump_path = os.path.join(os.path.dirname(__file__), 'ncmdump')

        # 创建选择NCM文件按钮
        self.select_file_button = tk.Button(root, text="选择NCM文件", command=self.select_ncm_file)
        self.select_file_button.pack(pady=10)

        # 创建选择输出文件夹按钮
        self.select_output_button = tk.Button(root, text="选择输出文件夹", command=self.select_output_folder)
        self.select_output_button.pack(pady=10)

        # 创建转换按钮
        self.convert_button = tk.Button(root, text="开始转换", command=self.convert_ncm_file)
        self.convert_button.pack(pady=10)

        # 创建标签显示文件路径
        self.ncm_file_path_label = tk.Label(root, text="未选择NCM文件")
        self.ncm_file_path_label.pack(pady=5)

        self.output_folder_label = tk.Label(root, text="未选择输出文件夹")
        self.output_folder_label.pack(pady=5)

        # 存储选择的文件路径
        self.ncm_file_path = None
        self.output_folder_path = None

    def select_ncm_file(self):
        # 打开文件对话框选择NCM文件
        self.ncm_file_path = filedialog.askopenfilename(filetypes=[("NCM Files", "*.ncm")])
        if self.ncm_file_path:
            if os.path.exists(self.ncm_file_path):
                self.ncm_file_path_label.config(text=f"已选择文件: {self.ncm_file_path}")
            else:
                messagebox.showerror("错误", "指定的NCM文件未找到，请检查路径是否正确")
                self.ncm_file_path = None
                self.ncm_file_path_label.config(text="未选择NCM文件")
        else:
            self.ncm_file_path = None
            self.ncm_file_path_label.config(text="未选择NCM文件")

    def select_output_folder(self):
        # 打开文件夹对话框选择输出文件夹
        self.output_folder_path = filedialog.askdirectory()
        if self.output_folder_path:
            self.output_folder_label.config(text=f"已选择输出文件夹: {self.output_folder_path}")
        else:
            self.output_folder_path = None
            self.output_folder_label.config(text="未选择输出文件夹")

    def select_ncmdump_file(self):
        # 打开文件对话框选择ncmdump工具
        self.ncmdump_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe *.py *.sh")])
        if self.ncmdump_path:
            if os.path.exists(self.ncmdump_path):
                messagebox.showinfo("成功", "已选择ncmdump工具")
            else:
                messagebox.showerror("错误", "指定的ncmdump工具未找到，请检查路径是否正确")
                self.ncmdump_path = None
        else:
            self.ncmdump_path = None

    def convert_ncm_file(self):
        if not self.ncm_file_path:
            messagebox.showerror("错误", "请先选择一个NCM文件")
            return

        if not self.output_folder_path:
            messagebox.showerror("错误", "请先选择输出文件夹")
            return

        if not os.path.exists(self.ncm_file_path):
            messagebox.showerror("错误", "指定的NCM文件未找到，请检查路径是否正确")
            return

        if not os.path.exists(self.ncmdump_path):
            messagebox.showerror("错误", "ncmdump工具未找到，请选择ncmdump工具")
            self.select_ncmdump_file()
            return

        try:
            # 使用ncmdump命令行工具进行转换
            subprocess.run([self.ncmdump_path, '-o', self.output_folder_path, self.ncm_file_path], check=True)
            messagebox.showinfo("成功", "文件转换成功")
        except subprocess.CalledProcessError:
            messagebox.showerror("错误", "文件转换失败，请确保ncmdump已正确安装")
        except FileNotFoundError:
            messagebox.showerror("错误", "指定的文件未找到，请检查路径是否正确")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NCMConverterGUI(root)
    root.mainloop()
