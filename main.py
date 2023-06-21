import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from PyPDF2 import PdfReader, PdfWriter
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.size = (300, 400)

class WatermarkApp(App):
    title = 'PDF Watermark'

    def build(self):
        self.file1_name = ""
        self.file2_name = ""

        select1_button = Button(text="Select PDF")
        select1_button.bind(on_release=self.select_file)

        select2_button = Button(text="Select PDF/Watermark")
        select2_button.bind(on_release=self.select_water)

        watermark_button = Button(text="Add Watermark")
        watermark_button.bind(on_release=self.add_watermark)

        self.status1_label = Label()
        self.status2_label = Label()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(select1_button)
        layout.add_widget(select2_button)
        layout.add_widget(watermark_button)
        layout.add_widget(self.status1_label)
        layout.add_widget(self.status2_label)

        return layout

    def select_file(self, instance):
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.load_file)

        self.popup = Popup(title='Select a file', content=filechooser)
        self.popup.open()
        Window.size = (800, 500)

    def load_file(self, instance, selection, touch):
        if selection and selection[0].endswith('.pdf'):
            self.file1_name = selection[0]
            self.status1_label.text = f'Selected: {os.path.basename(self.file1_name)}'
        else:
            self.status1_label.text = 'Please select a .pdf file'
        self.popup.dismiss()
        Window.size = (300, 400)

    def select_water(self, instance):
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.load_water)

        self.popup = Popup(title='Select a file', content=filechooser)
        self.popup.open()
        Window.size = (800, 500)

    def load_water(self, instance, selection, touch):
        if selection and selection[0].endswith('.pdf'):
            self.file2_name = selection[0]
            self.status2_label.text = f'Selected: {os.path.basename(self.file2_name)}'
        else:
            self.status2_label.text = 'Please select a .pdf file'
        self.popup.dismiss()
        Window.size = (300, 400)


    def add_watermark(self, instance):
        if not self.file1_name:
            self.status1_label.text = 'No file selected.'
            return
        if not self.file2_name:
            self.status2_label.text = 'No watermark selected.'
            return

        watermark_obj = PdfReader(self.file2_name)
        watermark_page = watermark_obj.pages[0]

        pdf_reader = PdfReader(self.file1_name)
        pdf_writer = PdfWriter()

        for page in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[page]
            pdf_page.merge_page(watermark_page)
            pdf_writer.add_page(pdf_page)

        output_filename = os.path.splitext(self.file1_name)[0] + "_watermarked.pdf"
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        self.status1_label.text = f'Watermark added to {os.path.basename(self.file1_name)}'
        self.status2_label.text = ''

if __name__ == "__main__":
    WatermarkApp().run()