import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from PyPDF2 import PdfReader, PdfWriter

class WatermarkApp(App):
    def build(self):
        self.filechooser = FileChooserIconView()
        self.filechooser.size_hint = (1, 0.8)

        select_button = Button(text="Add Watermark")
        select_button.size_hint = (1, 0.2)
        select_button.bind(on_release=self.add_watermark)

        self.status_label = Label(size_hint=(1, 0.2))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.filechooser)
        layout.add_widget(select_button)
        layout.add_widget(self.status_label)

        return layout

    def add_watermark(self, instance):
        files = self.filechooser.selection
        if not files:
            self.status_label.text = 'No file selected.'
            return

        watermark_obj = PdfReader("watermark.pdf")
        watermark_page = watermark_obj.pages[0]

        for file in files:
            pdf_reader = PdfReader(file)
            pdf_writer = PdfWriter()

            for page in range(len(pdf_reader.pages)):
                pdf_page = pdf_reader.pages[page]
                pdf_page.merge_page(watermark_page)
                pdf_writer.add_page(pdf_page)

            output_filename = os.path.splitext(file)[0] + "_watermarked.pdf"
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)

        self.status_label.text = f'Watermark added to {len(files)} file(s).'

if __name__ == "__main__":
    WatermarkApp().run()