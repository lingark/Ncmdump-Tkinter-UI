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

        # 检查ncmdump工具是否存在
        if not os.path.exists(self.ncmdump_path):
            self.ncmdump_path = self.select_ncmdump_file()

        # 创建选择NCM文件按钮
        self.select_file_button = tk.Button(root, text="选择单个NCM文件", command=self.select_ncm_file)
        self.select_file_button.pack(pady=10)

        # 创建选择NCM文件夹按钮
        self.select_folder_button = tk.Button(root, text="选择NCM文件夹", command=self.select_ncm_folder)
        self.select_folder_button.pack(pady=10)

        # 创建选择输出文件夹按钮
        self.select_output_button = tk.Button(root, text="选择输出文件夹", command=self.select_output_folder)
        self.select_output_button.pack(pady=10)

        # 创建转换按钮
        self.convert_button = tk.Button(root, text="开始转换", command=self.convert_ncm_file)
        self.convert_button.pack(pady=10)

        # 创建标签显示文件路径
        self.ncm_file_path_label = tk.Label(root, text="未选择NCM文件")
        self.ncm_file_path_label.pack(pady=5)

        self.ncm_folder_path_label = tk.Label(root, text="未选择NCM文件夹")
        self.ncm_folder_path_label.pack(pady=5)

        self.output_folder_label = tk.Label(root, text="未选择输出文件夹")
        self.output_folder_label.pack(pady=5)

        # 存储选择的文件路径
        self.ncm_file_path = None
        self.ncm_folder_path = None
        self.output_folder_path = None

    def select_ncmdump_file(self):
        # 打开文件对话框选择ncmdump工具
        ncmdump_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe *.py *.sh")])
        if ncmdump_path:
            if os.path.exists(ncmdump_path):
                messagebox.showinfo("成功", "已选择ncmdump工具")
                return ncmdump_path
            else:
                messagebox.showerror("错误", "指定的ncmdump工具未找到，请检查路径是否正确")
        else:
            messagebox.showerror("错误", "请先选择ncmdump工具")

        # 如果用户没有选择有效的ncmdump工具，则显示错误并再次提示选择
        return self.select_ncmdump_file()

    def select_ncm_file(self):
        # 打开文件对话框选择单个NCM文件
        self.ncm_file_path = filedialog.askopenfilename(filetypes=[("NCM Files", "*.ncm")])
        if self.ncm_file_path:
            if os.path.exists(self.ncm_file_path):
                self.ncm_file_path_label.config(text=f"已选择文件: {self.ncm_file_path}")
                self.ncm_folder_path = None
                self.ncm_folder_path_label.config(text="未选择NCM文件夹")
            else:
                messagebox.showerror("错误", "指定的NCM文件未找到，请检查路径是否正确")
                self.ncm_file_path = None
                self.ncm_file_path_label.config(text="未选择NCM文件")
        else:
            self.ncm_file_path = None
            self.ncm_file_path_label.config(text="未选择NCM文件")

    def select_ncm_folder(self):
        # 打开文件夹对话框选择NCM文件夹
        self.ncm_folder_path = filedialog.askdirectory()
        if self.ncm_folder_path:
            if os.path.exists(self.ncm_folder_path):
                self.ncm_folder_path_label.config(text=f"已选择文件夹: {self.ncm_folder_path}")
                self.ncm_file_path = None
                self.ncm_file_path_label.config(text="未选择NCM文件")
            else:
                messagebox.showerror("错误", "指定的NCM文件夹未找到，请检查路径是否正确")
                self.ncm_folder_path = None
                self.ncm_folder_path_label.config(text="未选择NCM文件夹")
        else:
            self.ncm_folder_path = None
            self.ncm_folder_path_label.config(text="未选择NCM文件夹")

    def select_output_folder(self):
        # 打开文件夹对话框选择输出文件夹
        self.output_folder_path = filedialog.askdirectory()
        if self.output_folder_path:
            self.output_folder_label.config(text=f"已选择输出文件夹: {self.output_folder_path}")
        else:
            self.output_folder_path = None
            self.output_folder_label.config(text="未选择输出文件夹")

    def convert_ncm_file(self):
        if not self.ncm_file_path and not self.ncm_folder_path:
            messagebox.showerror("错误", "请先选择一个NCM文件或一个NCM文件夹")
            return

        if not self.output_folder_path:
            messagebox.showerror("错误", "请先选择输出文件夹")
            return

        if self.ncm_file_path:
            if not os.path.exists(self.ncm_file_path):
                messagebox.showerror("错误", "指定的NCM文件未找到，请检查路径是否正确")
                return
            ncm_files = [self.ncm_file_path]
        elif self.ncm_folder_path:
            if not os.path.exists(self.ncm_folder_path):
                messagebox.showerror("错误", "指定的NCM文件夹未找到，请检查路径是否正确")
                return
            ncm_files = [os.path.join(self.ncm_folder_path, f) for f in os.listdir(self.ncm_folder_path) if f.endswith('.ncm')]

        if not ncm_files:
            messagebox.showerror("错误", "未找到任何NCM文件")
            return

        if not os.path.exists(self.ncmdump_path):
            messagebox.showerror("错误", "ncmdump工具未找到，请选择ncmdump工具")
            self.ncmdump_path = self.select_ncmdump_file()
            if not self.ncmdump_path:
                return

        for ncm_file in ncm_files:
            try:
                # 使用ncmdump命令行工具进行转换
                subprocess.run([self.ncmdump_path, '-o', self.output_folder_path, ncm_file], check=True)
            except subprocess.CalledProcessError:
                messagebox.showerror("错误", f"文件 {ncm_file} 转换失败，请确保ncmdump已正确安装")
                return
            except FileNotFoundError:
                messagebox.showerror("错误", f"指定的文件 {ncm_file} 未找到，请检查路径是否正确")
                return
            except Exception as e:
                messagebox.showerror("错误", f"转换文件 {ncm_file} 时发生错误: {e}")
                return

        messagebox.showinfo("成功", "所有文件转换成功")

if __name__ == "__main__":
    root = tk.Tk()
    app = NCMConverterGUI(root)
    root.mainloop()
