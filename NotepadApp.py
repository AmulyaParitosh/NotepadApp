from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QMessageBox,
    QFontDialog,
    QColorDialog,
)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QFileInfo, Qt

from ui_notepad import Ui_Notepad


class Notepad(QMainWindow, Ui_Notepad):
    def __init__(self,) -> None:
        super().__init__()
        self.setupUi(self)
        self.show()

        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_Preview.triggered.connect(self.print_preview)
        self.actionExport_PDF.triggered.connect(self.export_PDF)
        self.actionQuit.triggered.connect(self.close)

        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)

        self.actionBold.triggered.connect(self.text_bold)
        self.actionItalic.triggered.connect(self.text_italic)
        self.actionUnderline.triggered.connect(self.text_underline)

        self.actionLeft.triggered.connect(self.allign_left)
        self.actionRight.triggered.connect(self.allign_right)
        self.actionCenter.triggered.connect(self.allign_center)
        self.actionJustify.triggered.connect(self.allign_justify)

        self.actionFont.triggered.connect(self.set_font)
        self.actionColor.triggered.connect(self.set_color)

        self.actionAbout_App.triggered.connect(self.about)

    def to_save(self) -> bool:
        if not self.textEdit.document().isModified():
            return False

        ret = QMessageBox.warning(
            self,
            "To Save",
            "Document was Modefied. Do you want to save it?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )

        if ret is QMessageBox.StandardButton.Save:
            return self.save_file()

        elif ret is QMessageBox.StandardButton.Discard:
            return False

        return True

    def save_file(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(self, "Save File")

        if not filename:
            return

        try:
            text = self.textEdit.toPlainText()
            with open(filename, "w") as file:
                file.write(text)

            QMessageBox.information(self, "Save message", "File saved sucessfuly!")

        except Exception as exc:
            QMessageBox.critical(self, "Error", str(exc))

    def new_file(self) -> None:
        if self.to_save():
            return

        self.textEdit.clear()

    def open_file(self) -> None:
        if self.to_save():
            return

        filename, _ = QFileDialog.getOpenFileName(self, "Open File")

        self.textEdit.clear()

        with open(filename, "r") as file:
            data = file.read()
            self.textEdit.setText(data)

    def print_file(self) -> None:
        if self.to_save():
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.print_textEdit(printer)

    def print_preview(self) -> None:

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_textEdit)
        previewDialog.exec()

    def print_textEdit(self, printer: QPrinter) -> None:
        self.textEdit.print(printer)

    def export_PDF(self):
        filename, _ = QFileDialog().getSaveFileName(
            self, "Export to PDF", filter="PDF files (.pdf) ;; All Files ()"
        )

        if not filename:
            return

        if QFileInfo(filename).suffix() != "pdf":
            filename += ".pdf"

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filename)

        self.print_textEdit(printer)

    def text_bold(self):

        font = self.textEdit.font()
        font.setBold(not font.bold())
        self.textEdit.setFont(font)

    def text_italic(self):
        font = self.textEdit.font()
        font.setItalic(not font.italic())
        self.textEdit.setFont(font)

    def text_underline(self):
        font = self.textEdit.font()
        font.setUnderline(not font.underline())
        self.textEdit.setFont(font)

    def allign_left(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def allign_right(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def allign_center(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def allign_justify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def set_font(self):
        font, ok = QFontDialog.getFont()

        if not ok:
            return

        self.textEdit.setFont(font)

    def set_color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def about(self):
        QMessageBox.about(self, "About App", "This is my notepad aap.")


def main():
    import sys

    app = QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
