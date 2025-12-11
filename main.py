from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

window = Tk()

window.title("Watermark App")
window.minsize(width=500, height=800)
window.config(padx= 50, pady= 20)

font_options = [
    "Arial",
    "Helvetica",
    "Times New Roman",
    "Courier",
    "Courier New",
    "Calibri",
    "Verdana",
    "Tahoma",
    "Trebuchet MS",
    "Comic Sans MS",
    "Georgia",
    "Impact",
    "Forte",
    "Segoe UI",
    "Consolas",
    "Lucida Console"
]

color_options = [
    "black",
    "white",
    "red",
    "green",
    "blue",
    "cyan",
    "yellow",
    "magenta",
    "gray",
    "light gray",
    "dark gray",
    "orange",
    "pink",
    "purple",
    "brown",
    "gold",
    "silver",
    "navy",
    "sky blue",
    "lime",
    "teal",
    "maroon",
    "olive"
]

font_weight_options = [
    "normal",
    "bold",
    "italic",
    "underline",
    "overstrike"
]


font_choice = StringVar()
font_weight_choice = StringVar()
color_choice = StringVar()


canvas = Canvas(width=400, height=400, bg="lightgray") 
canvas.grid(column=1, row=0, columnspan=2) 

loaded_img = None
original_img = None
watermark_id = None

def load_img():
    global loaded_img, original_img, watermark_id

    file_path = filedialog.askopenfilename(
        title='Select an Image',
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )

    if not file_path:
        return

    # Load the image
    img = Image.open(file_path)

    original_img = img.copy()

    # Get the image size
    image_width, image_height = img.size
    print("Image Width:", image_width)
    print("Image Height:", image_height)

    # Create Image Size Label
    img_size_label = Label(font=("Arial", 15, "bold"))
    img_size_label.grid(column=1, row=1)

    # Update its text whenever a new image loads
    img_size_label.config(
        text=f"Image Size: {image_width} x {image_height}"
    )


    img.thumbnail((400, 400))

    loaded_img = ImageTk.PhotoImage(img)

    # Clear previous image
    canvas.delete("all")
    watermark_id = None

    # Display new image
    canvas.create_image(200, 200, image=loaded_img)


watermark_id = None

def load_watermark():
    global watermark_id

    # Get raw values (all strings)
    watermark = watermark_entry.get().strip()
    font = font_combo.get()
    font_size = font_size_entry.get().strip()
    padx = padx_spinbox.get().strip()
    pady = pady_spinbox.get().strip()
    color = color_combo.get()
    font_weight = font_weight_combo.get()
    transparency = transparency_spinbox.get().strip()
    rotation = rotation_spinbox.get().strip()

# Validations
    if watermark == "":
        messagebox.showinfo("Oops", "Enter a watermark!")
        return
    
    if font_size == "" or padx == "" or pady == "" or transparency == "" or rotation == "":
        messagebox.showinfo("Oops", "All fields must be filled!")
        return

    # Catch invalid numbers
    try:
        size = int(font_size)
        x = int(padx)
        y = int(pady)
        transparency = int(transparency)
        angle = int(rotation)

        if not(0 <= transparency <= 100):
            messagebox.showinfo("Oops", "Transparency must be between 0 and 100.")
            return
        if not(0 <= angle <= 360):
            messagebox.showinfo("Oops", "Rotation angle must be between 0 and 360.")
            return
    except ValueError:
        messagebox.showinfo("Oops", "All values must be valid numbers!")
        return

    # ---- CREATE OR UPDATE WATERMARK ----

    if watermark_id is not None:
        # Update existing watermark
        canvas.itemconfig(
            watermark_id,
            text=watermark,
            font=(font, size, font_weight),
            fill=color,
            angle=angle
        )
        canvas.coords(watermark_id, x, y)
    else:
        # Create first watermark
        watermark_id = canvas.create_text(
            x, y,
            text=watermark,
            font=(font, size, font_weight),
            fill=color,
            angle=angle
        )

def load_new_watermark():
    global watermark_id

    watermark_id = None
    load_watermark()

def save_img():
    global original_img, watermark_id
    
    if original_img is None:
        messagebox.showwarning("No Image", "Please load an image first!")
        return
    
    transparency = transparency_spinbox.get().strip()
    rotation = rotation_spinbox.get().strip()

    try:
        alpha = int(transparency)
        angle = int(rotation)
    except:
        transparency = 100
        angle = 0

    if watermark_id is None:
        response = messagebox.askyesno("No Watermark", "No watermark has been added. Save image without watermark?")
        if not response:
            return
    
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg *.jpeg"), ("All Files", "*.*")]
    )
    
    if not save_path:
        return
    
    try:
        watermarked_img = original_img.copy()
        
        if watermark_id is not None:
            # Get watermark properties
            watermark_text = canvas.itemcget(watermark_id, 'text')
            font_info = canvas.itemcget(watermark_id, 'font')
            color = canvas.itemcget(watermark_id, 'fill')
            coords = canvas.coords(watermark_id)
            
            # Parse font info
            font_parts = font_info.split()
            font_family = font_parts[0]
            font_size = int(font_parts[1])

            # Get font weight 
            font_weight = ""
            if len(font_parts) > 2:
                font_weight = font_parts[2]
            
            # Prepare to draw
            draw = ImageDraw.Draw(watermarked_img, 'RGBA')
            
            # load the font
            try:
                # FONT MAP – full Windows paths for Window Users
                # Users can comment this if using Mac
                font_map = {
                    "Arial": r"C:\Windows\Fonts\arial.ttf",
                    "Helvetica": r"C:\Windows\Fonts\arial.ttf",     # fallback
                    "Times New Roman": r"C:\Windows\Fonts\times.ttf",
                    "Courier": r"C:\Windows\Fonts\cour.ttf",
                    "Courier New": r"C:\Windows\Fonts\cour.ttf",
                    "Calibri": r"C:\Windows\Fonts\calibri.ttf",
                    "Verdana": r"C:\Windows\Fonts\verdana.ttf",
                    "Tahoma": r"C:\Windows\Fonts\tahoma.ttf",
                    "Trebuchet MS": r"C:\Windows\Fonts\trebuc.ttf",
                    "Comic Sans MS": r"C:\Windows\Fonts\comic.ttf",
                    "Georgia": r"C:\Windows\Fonts\georgia.ttf",
                    "Impact": r"C:\Windows\Fonts\impact.ttf",
                    "Forte": r"C:\Windows\Fonts\forte.ttf",
                    "Segoe UI": r"C:\Windows\Fonts\segoeui.ttf",
                    "Consolas": r"C:\Windows\Fonts\consola.ttf",
                    "Lucida Console": r"C:\Windows\Fonts\lucon.ttf"
                }
                
                # macOS FONT MAP (Users can uncomment if using Mac)
                # mac_font_map = {
                #     "Arial": "/System/Library/Fonts/Supplemental/Arial.ttf",
                #     "Helvetica": "/System/Library/Fonts/Helvetica.ttc",
                #     "Times New Roman": "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
                #     "Courier": "/System/Library/Fonts/Courier.ttc",
                #     "Courier New": "/System/Library/Fonts/Supplemental/Courier New.ttf",
                #     "Calibri": "/System/Library/Fonts/Supplemental/Calibri.ttf",
                #     "Verdana": "/System/Library/Fonts/Supplemental/Verdana.ttf",
                #     "Tahoma": "/Library/Fonts/Tahoma.ttf",  # manually installed
                #     "Trebuchet MS": "/Library/Fonts/Trebuchet MS.ttf",
                #     "Comic Sans MS": "/Library/Fonts/Comic Sans MS.ttf",
                #     "Georgia": "/System/Library/Fonts/Supplemental/Georgia.ttf",
                #     "Impact": "/Library/Fonts/Impact.ttf",
                #     "Forte": "/Library/Fonts/Forte.ttf",
                #     "Segoe UI": "/Library/Fonts/Segoe UI.ttf",  # usually user-installed
                #     "Consolas": "/Library/Fonts/Consolas.ttf",
                #     "Lucida Console": "/System/Library/Fonts/LucidaGrande.ttc"  # closest match
                # }


                system_font = font_map.get(font_family, "arial")
                
                if font_weight == "bold":
                    font = ImageFont.truetype(f"{system_font}bd.ttf", font_size)
                elif font_weight == "italic":
                    font = ImageFont.truetype(f"{system_font}i.ttf", font_size)
                else:
                    font = ImageFont.truetype(f"{system_font}.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
            # Convert 0-100 to 0-255
            transparency_value = max(0, min(255, int(alpha * 2.55)))
            
            # Convert color to RGBA with transparency
            color_map = {
                "black": (0, 0, 0, alpha),
                "white": (255, 255, 255, alpha),
                "red": (255, 0, 0, alpha),
                "green": (0, 255, 0, alpha),
                "blue": (0, 0, 255, alpha),
                "cyan": (0, 255, 255, alpha),
                "yellow": (255, 255, 0, alpha),
                "magenta": (255, 0, 255, alpha),
                "gray": (128, 128, 128, alpha),
                "light gray": (211, 211, 211, alpha),
                "dark gray": (169, 169, 169, alpha),
                "orange": (255, 165, 0, alpha),
                "pink": (255, 192, 203, alpha),
                "purple": (128, 0, 128, alpha),
                "brown": (165, 42, 42, alpha),
                "gold": (255, 215, 0, alpha),
                "silver": (192, 192, 192, alpha),
                "navy": (0, 0, 128, alpha),
                "sky blue": (135, 206, 235, alpha),
                "lime": (0, 255, 0, alpha),
                "teal": (0, 128, 128, alpha),
                "maroon": (128, 0, 0, alpha),
                "olive": (128, 128, 0, alpha),
            }
            
            rgba_color = color_map.get(color.lower(), (transparency_value))
            
            # Scale coordinates from canvas to original image
            img_width, img_height = watermarked_img.size
            canvas_x, canvas_y = coords
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            scale_x = img_width / canvas_width
            scale_y = img_height / canvas_height
            x = canvas_x * scale_x
            y = canvas_y * scale_y
            
            # Get text dimensions
            try:
                # Create a temporary image to measure text
                temp_img = Image.new('RGBA', (1, 1))
                temp_draw = ImageDraw.Draw(temp_img)
                text_bbox = temp_draw.textbbox((0, 0), watermark_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
            except:
                text_width = font_size * len(watermark_text) * 0.6
                text_height = font_size
            
            # Handle rotation
            if angle != 0:
                text_layer = Image.new('RGBA', (int(text_width * 1.5), int(text_height * 1.5)), (0, 0, 0, 0))
                text_draw = ImageDraw.Draw(text_layer)
                text_draw.text((text_width * 0.25, text_height * 0.25), watermark_text, font=font, fill=rgba_color)
                
                rotated_text = text_layer.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
                
                # Calculate position for rotated text
                rot_width, rot_height = rotated_text.size
                paste_x = int(x - rot_width / 2)
                paste_y = int(y - rot_height / 2)
                
                # Paste rotated text onto the image
                watermarked_img.paste(rotated_text, (paste_x, paste_y), rotated_text)
            else:
                # Draw text without rotation
                draw.text((x, y), watermark_text, font=font, fill=rgba_color, anchor="mm")
        
        # Save the image
        watermarked_img.save(save_path)
        
        messagebox.showinfo("Saved", f"Watermaked Image saved successfully!\n{save_path}")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {str(e)}")
        print(f"Error details: {e}")

button = Button(text="Upload Photo", command=load_img, width=20)
button.grid(column=1, row=2, columnspan=2, pady=20)

watermark_label = Label(text='Enter the Watermark:', font=("Segoe UI", 10))
watermark_label.grid(column=0, row=3, pady=5)

watermark_entry = Entry(width=50)
watermark_entry.grid(column=1, row=3, pady=5, columnspan=2)

font_label = Label(text='Pick a Font:', font=("Segoe UI", 10))
font_label.grid(column=0, row=4, pady=5)

font_combo = ttk.Combobox(window, textvariable=font_choice, values=font_options, state="readonly")
font_combo.current(0)
font_combo.grid(column=1, row=4, pady=5)

font_weight_label = Label(text='Pick a Font Weight:', font=("Segoe UI", 10))
font_weight_label.grid(column=0, row=5, pady=5)

font_weight_combo = ttk.Combobox(window, textvariable=font_weight_choice, values=font_weight_options, state="readonly", width=30)
font_weight_combo.current(0)
font_weight_combo.grid(column=1, row=5, pady=5)

color = Label(text='Pick a Colour:', font=("Segoe UI", 10))
color.grid(column=0, row=6, pady=5)

color_combo = ttk.Combobox(window, textvariable=color_choice, values=color_options, state="readonly", width=30)
color_combo.current(0)
color_combo.grid(column=1, row=6, pady=5)

font_size_label = Label(text='Enter the Font Size:', font=("Segoe UI", 10))
font_size_label.grid(column=0, row=7, pady=5)

font_size_entry = Entry(width=30)
font_size_entry.insert(0, "20")
font_size_entry.grid(column=1, row=7, pady=5)

padx_label = Label(text='X Position:', font=("Segoe UI", 10))
padx_label.grid(column=0, row=8, sticky="w", pady=5)

padx_spinbox = Spinbox(from_=10, to=400, width=30, increment=10)
padx_spinbox.grid(column=1, row=8, pady=5)
padx_spinbox.delete(0, "end")
padx_spinbox.insert(0, "200")

pady_label = Label(text='Y Position:', font=("Segoe UI", 10))
pady_label.grid(column=0, row=9, sticky="w", pady=5)

pady_spinbox = Spinbox(from_=10, to=400, width=30, increment=10)
pady_spinbox.grid(column=1, row=9, pady=5)
pady_spinbox.delete(0, "end")
pady_spinbox.insert(0, "200")

transparency_label = Label(text="Transparency (0-100%):", font=("Segoe UI", 10))
transparency_label.grid(column=0, row=10, sticky="w", pady=5)

transparency_spinbox = Spinbox(from_=0, to=100, width=30, increment=10)
transparency_spinbox.grid(column=1, row=10, pady=5)
transparency_spinbox.delete(0, "end")
transparency_spinbox.insert(0, "100") 

rotation_label = Label(text="Rotation Angle (0-360°):", font=("Segoe UI", 10))
rotation_label.grid(column=0, row=11, sticky="w", pady=5)

rotation_spinbox = Spinbox(from_=0, to=360, width=30, increment=15)
rotation_spinbox.grid(column=1, row=11, pady=5)
rotation_spinbox.delete(0, "end")
rotation_spinbox.insert(0, "0")  

load_button = Button(text='Load Watermark', command=load_watermark, width=20)
load_button.grid(column=1, row=12, pady=5)

load_new_button = Button(text='Load New Watermark', command=load_new_watermark, width=20)
load_new_button.grid(column=1, row=13, pady=5)

save_button = Button(text='Save Picture', command=save_img, width= 40)
save_button.grid(column=1, row=14)

window.mainloop()

