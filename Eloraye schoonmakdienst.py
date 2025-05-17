import streamlit as st
from fpdf import FPDF
from datetime import date

# Function to create the PDF invoice
def create_factuur(datum, entries, btw_percentage):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", size=12)

    pdf.cell(0, 10, "Eloraye Schoonmakdienst - Factuur", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Helvetica", size=8)
    pdf.cell(0, 10, "Developed by Semir Alemseged", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, f"Factuurdatum: {datum}", ln=True)
    pdf.ln(10)

    pdf.cell(30, 10, "Bedrijf", border=1)
    pdf.cell(30, 10, "Datum", border=1)
    pdf.cell(30, 10, "Uren", border=1)
    pdf.cell(40, 10, "Prijs per uur", border=1)
    pdf.cell(40, 10, "Totaal", border=1, ln=True)

    totaal_excl_btw = 0
    for entry in entries:
        bedrijf = entry['bedrijf']
        werkdatum = entry['werkdatum']
        uren = entry['uren']
        prijs_per_uur = entry['prijs_per_uur']
        totaal = uren * prijs_per_uur
        totaal_excl_btw += totaal

        pdf.cell(30, 10, bedrijf, border=1)
        pdf.cell(30, 10, werkdatum, border=1)
        pdf.cell(30, 10, str(uren), border=1)
        pdf.cell(40, 10, f"EUR {prijs_per_uur:.2f}", border=1)
        pdf.cell(40, 10, f"EUR {totaal:.2f}", border=1, ln=True)

    btw = totaal_excl_btw * btw_percentage / 100
    totaal_incl_btw = totaal_excl_btw + btw

    pdf.ln(10)
    pdf.cell(0, 10, f"Totaal excl. BTW: EUR {totaal_excl_btw:.2f}", ln=True)
    pdf.cell(0, 10, f"BTW ({btw_percentage}%): EUR {btw:.2f}", ln=True)
    pdf.cell(0, 10, f"Totaal incl. BTW: EUR {totaal_incl_btw:.2f}", ln=True)

    return pdf.output(dest='S').encode('latin1')


# Streamlit app
st.title("Eloraye Schoonmakdienst - Factuur Generator")
st.caption("Developed by Semir Alemseged")

st.write("Vul de gegevens in voor 5 bedrijven en genereer de factuur.")

entries = []
for i in range(1, 6):
    st.subheader(f"Bedrijf {i}")
    bedrijf = st.text_input(f"Naam bedrijf {i}", key=f"bedrijf_{i}")
    werkdatum = st.date_input(f"Datum werkzaamheden {i}", value=date.today(), key=f"datum_{i}")
    uren = st.number_input(f"Aantal gewerkte uren {i}", min_value=0.0, step=1.0, key=f"uren_{i}")
    prijs_per_uur = st.number_input(f"Prijs per uur (€) {i}", min_value=0.0, step=1.0, key=f"prijs_{i}")

    if bedrijf.strip() != "":
        entries.append({
            "bedrijf": bedrijf,
            "werkdatum": werkdatum.strftime("%d-%m-%Y"),
            "uren": uren,
            "prijs_per_uur": prijs_per_uur
        })

btw_percentage = st.number_input("BTW percentage", min_value=0.0, value=21.0, step=1.0)
factuurdatum = date.today().strftime("%d-%m-%Y")

if st.button("Genereer en download factuur"):
    if len(entries) == 0:
        st.error("Vul minimaal één bedrijf in om een factuur te genereren.")
    else:
        pdf_bytes = create_factuur(factuurdatum, entries, btw_percentage)
        st.download_button(
            label="Download factuur als PDF",
            data=pdf_bytes,
            file_name=f"Factuur_{factuurdatum}.pdf",
            mime='application/pdf'
        )
