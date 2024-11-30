import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageCropperTab:
    def __init__(self, parent):
        self.parent = parent
        self.image_path = None
        self.img = None
        self.canvas = tk.Canvas(parent)
        self.canvas.pack()
        self.load_button = tk.Button(parent, text="打开图片", command=self.load_image)
        self.load_button.pack()
        self.crop_button = tk.Button(parent, text="裁剪或处理", command=self.crop_and_save)
        self.crop_button.pack()
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rectangle = None
        self.parent.bind('<Control-s>', self.crop_and_save)  # 绑定 Ctrl+S 事件
        self.parent.bind('<Control-o>', self.load_image)
        self.tip = tk.Label(parent, text="在图片框选区域住可以裁剪")
        self.tip.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.img = Image.open(self.image_path)
            if self.img.width > 500 or self.img.height > 500:  # 如果图片尺寸过大，则缩小图片
                self.img = self.img.resize((int(self.img.width * 0.3), int(self.img.height * 0.3)), Image.LANCZOS)  # 缩小图片便于显示
            self.photo = ImageTk.PhotoImage(self.img)
            self.canvas.config(width=self.img.width, height=self.img.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rectangle:
            self.rectangle = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rectangle, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rectangle, self.start_x, self.start_y, self.end_x, self.end_y)

    def crop_and_save(self, event=None):
        if self.img and self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            try:
                box = (min(self.start_x, self.end_x), min(self.start_y, self.end_y),
                       max(self.start_x, self.end_x), max(self.start_y, self.end_y))
                cropped_img = self.img.crop(box)
                target_width = 100
                target_height = int(target_width * 0.25)
                resized_cropped_img = cropped_img.resize((target_width, target_height), Image.LANCZOS)
                save_path = filedialog.asksaveasfilename(
                    title='Save Cropped Image',
                    initialfile='cropped_image.png',
                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
                )
                if save_path:
                    resized_cropped_img.save(save_path)
                    print(f"Image saved to {save_path}")
            except FileNotFoundError as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Could not save the image: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        else:
            if self.image_path is None:
                messagebox.showwarning("Warning", "Please load an image first.")
            else:
                target_width = 100
                target_height = int(target_width * 0.25)
                resized_cropped_img = self.img.resize((target_width, target_height), Image.LANCZOS)
                save_path = filedialog.asksaveasfilename(
                    title='Save Cropped Image',
                    initialfile='cropped_image.png',
                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
                )
                if save_path:
                    resized_cropped_img.save(save_path)
                    print(f"Image saved to {save_path}")


class CppGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.load_button = tk.Button(parent, text="打开图片", command=self.load_image)
        self.load_button.pack()
        self.tip = tk.Label(parent, text="请打开处理好图片")
        self.tip.pack()
        self.image_path = None

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            output_file = filedialog.asksaveasfilename(
                title='保存 C++ 程序',
                initialdir=r'.',
                initialfile='colorful.cpp',
                filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")]
            )
            if output_file:
                generate_cpp_program(self.image_path, output_file)
                messagebox.showinfo("C++ 程序已生成", f"C++ 程序已生成并保存到 {output_file}")

def generate_cpp_program(image_path, output_file):
    with Image.open(image_path) as img:
        width, height = img.size
        img = img.convert('RGB')
        image_data = []
        for y in range(height):
            row = []
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                row.append({"r": r, "g": g, "b": b})
            image_data.append(row)

    with open(output_file, 'w') as f:
        f.write('#include <iostream>\n#include <vector>\n#include <string>\n\n')
        f.write('struct Color {\n    int r, g, b;\n};\n\n')
        f.write('const std::vector<std::vector<Color>> img = {{\n')
        for y in range(height):
            f.write('    {')
            f.write(', '.join(f'{{ {color["r"]}, {color["g"]}, {color["b"]} }}' for color in image_data[y]))
            f.write('},\n')
        f.write('}};\n\n')
        f.write('void print_img(const std::vector<std::vector<Color>>& img_data) {\n')
        f.write('    for (const auto& row : img_data) {\n')
        f.write('        for (const auto& color : row) {\n')
        f.write('            std::cout << "\\033[38;2;" << color.r << ";" << color.g << ";" << color.b << "m#" << "\\033[0m";\n')
        f.write('        }\n')
        f.write('        std::cout << std::endl;\n')
        f.write('    }\n')
        f.write('}\n\n')
        f.write('int main() {\n    system("color");\n    print_img(img);\n    return 0;\n}\n')

class ImageToAsciiTab:
    def __init__(self, parent):
        self.parent = parent
        self.load_button = tk.Button(parent, text="打开图片", command=self.get_ascii_img)
        self.load_button.pack()
        self.text_area = tk.Text(parent)
        self.text_area.pack()
        self.image_path = None

    def get_ascii_img(self):
        img = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        ascii_char = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z', 'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 'i', '!', 'l', 'I', ';', ':', ',', '"', '^', '`', "'", '.', ' ']
        im=Image.open(img)  
        im=im.convert("RGB")
        self.text_area.config(width=im.width)
        txt=""  
        for i in range(im.height):  
            for j in range(im.width):  
                r,g,b = im.getpixel((j,i))
                gray=int((r+g+b)/3)
                gray = round((69 / 256) * gray + (186 / 256))
                txt+=ascii_char[int(gray)] 
            txt+='\n'
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, txt)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ANSL转义打印图片")

    notebook = ttk.Notebook(root)
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text="图片处理")
    notebook.add(tab2, text="生成c++文件")
    notebook.add(tab3, text="图片转字符")
    notebook.pack(expand=1, fill="both")

    image_cropper_tab = ImageCropperTab(tab1)
    cpp_generator_tab = CppGeneratorTab(tab2)
    image_to_ascii_tab = ImageToAsciiTab(tab3)

    root.mainloop()
