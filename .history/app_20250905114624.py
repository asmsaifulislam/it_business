
# -------------------- Invoice Report --------------------
@app.route('/invoice-report')
def invoice_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    total_invoices = Invoice.query.count()
    paid = Invoice.query.filter_by(status='Paid').count()
    unpaid = Invoice.query.filter_by(status='Unpaid').count()
    overdue = Invoice.query.filter_by(status='Overdue').count()

    return render_template('invoice_report.html',
                           total_invoices=total_invoices,
                           paid=paid,
                           unpaid=unpaid,
                           overdue=overdue)


# -------------------- Run --------------------
if __name__ == '__main__':
    app.run(debug=True)
