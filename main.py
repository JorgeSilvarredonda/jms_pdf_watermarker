import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from PyPDF2 import PdfReader, PdfWriter
from kivy.uix.popup import Popup

class WatermarkApp(App):
    def build(self):
        self.file_name = ""

        select_button = Button(text="Select PDF")
        select_button.bind(on_release=self.select_file)

        watermark_button = Button(text="Add Watermark")
        watermark_button.bind(on_release=self.add_watermark)

        self.status_label = Label()

        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(select_button)
        layout.add_widget(watermark_button)
        layout.add_widget(self.status_label)

        return layout

    def select_file(self, instance):
        filechooser = FileChooserIconView()
        filechooser.bind(on_submit=self.load_file)

        self.popup = Popup(title='Select a file', content=filechooser)
        self.popup.open()


    def load_file(self, instance, selection, touch):
        if selection and selection[0].endswith('.pdf'):
            self.file_name = selection[0]
            self.status_label.text = f'Selected: {os.path.basename(self.file_name)}'
        else:
            self.status_label.text = 'Please select a .pdf file'
        #sself.popup.dismiss()

    def add_watermark(self, instance):
        if not self.file_name:
            self.status_label.text = 'No file selected.'
            return

        watermark_obj = PdfReader("watermark.pdf")
        watermark_page = watermark_obj.pages[0]

        pdf_reader = PdfReader(self.file_name)
        pdf_writer = PdfWriter()

        for page in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[page]
            pdf_page.merge_Page(watermark_page)
            pdf_writer.add_Page(pdf_page)

        output_filename = os.path.splitext(self.file_name)[0] + "_watermarked.pdf"
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        self.status_label.text = f'Watermark added to {os.path.basename(self.file_name)}'

if __name__ == "__main__":
    WatermarkApp().run()