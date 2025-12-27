from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

def generate_invoice_pdf(invoice, file_obj, logo_path=None):
    width, height = A4
    c = canvas.Canvas(file_obj, pagesize=A4)
    y = height - 50

    # -------------------
    # Company Logo
    # -------------------
    if logo_path:
        c.drawImage(logo_path, 50, y - 50, width=1.5*inch, height=1.5*inch)
    
    # -------------------
    # Header: Company Name & Invoice
    # -------------------
    c.setFont("Helvetica-Bold", 16)
    c.drawString(220, y, "Inventory & Billing System")
    y -= 50

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

    # -------------------
    # Table Header
    # -------------------
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Product")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(370, y, "Total")
    y -= 15
    c.line(50, y, 500, y)
    y -= 15

    # -------------------
    # Table Items
    # -------------------
    c.setFont("Helvetica", 10)
    for item in invoice.items.all():
        if y < 100:  # Start new page if low space
            draw_footer(c, invoice, c.getPageNumber())
            c.showPage()
            y = height - 50
            draw_header(c, invoice, logo_path)
        c.drawString(50, y, item.product.name)
        c.drawString(250, y, str(item.quantity))
        c.drawString(300, y, f"{item.price}")
        c.drawString(370, y, f"{item.total}")
        y -= 20

    y -= 20
    c.line(50, y, 500, y)
    y -= 20

    # -------------------
    # Totals
    # -------------------
    c.drawString(300, y, "Subtotal:")
    c.drawString(370, y, str(invoice.subtotal))
    y -= 20

    c.drawString(300, y, "Tax:")
    c.drawString(370, y, str(invoice.tax_amount))
    y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(300, y, "Total:")
    c.drawString(370, y, str(invoice.total_amount))

    # -------------------
    # Footer
    # -------------------
    draw_footer(c, invoice, 1)

    c.showPage()
    c.save()


# -------------------
# Helper functions
# -------------------
def draw_header(c, invoice, logo_path=None):
    width, height = A4
    y = height - 50
    if logo_path:
        c.drawImage(logo_path, 50, y - 50, width=1.5*inch, height=1.5*inch)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(220, y, "Inventory & Billing System")
    y -= 50
    return y

def draw_footer(c, invoice, page_number):
    width, _ = A4
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 20, f"Invoice: {invoice.invoice_number}")
    c.drawRightString(width - 50, 20, f"Page {page_number}")
