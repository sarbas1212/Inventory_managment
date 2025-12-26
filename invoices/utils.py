from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_invoice_pdf(invoice, file_path):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50

    # Company Info
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Inventory & Billing System")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Invoice No:")
    c.drawString(150, y, invoice.invoice_number)
    y -= 20

    c.drawString(50, y, "Customer:")
    c.drawString(150, y, invoice.customer.name)
    y -= 20

    c.drawString(50, y, "Date:")
    c.drawString(150, y, invoice.created_at.strftime("%d-%m-%Y"))
    y -= 30

    # Table Header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Product")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(370, y, "Total")
    y -= 15

    c.line(50, y, 500, y)
    y -= 15

    # Items
    c.setFont("Helvetica", 10)
    for item in invoice.items.all():
        c.drawString(50, y, item.product.name)
        c.drawString(250, y, str(item.quantity))
        c.drawString(300, y, f"{item.price}")
        c.drawString(370, y, f"{item.total}")
        y -= 20

    y -= 20
    c.line(50, y, 500, y)
    y -= 20

    # Totals
    c.drawString(300, y, "Subtotal:")
    c.drawString(370, y, str(invoice.subtotal))
    y -= 20

    c.drawString(300, y, "Tax:")
    c.drawString(370, y, str(invoice.tax_amount))
    y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(300, y, "Total:")
    c.drawString(370, y, str(invoice.total_amount))

    c.showPage()
    c.save()
