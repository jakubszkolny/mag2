import streamlit as st
from typing import List

# Definicja klasy Towar
class Towar:
    def __init__(self, nazwa: str, ilosc: int):
        self.nazwa = nazwa
        self.ilosc = ilosc

    def __str__(self):
        return f"{self.nazwa} (Ilość: {self.ilosc})"

# Inicjalizacja listy towarów w stanie sesji Streamlit (nie jest to trwały zapis)
if 'lista_towarow' not in st.session_state:
    st.session_state.lista_towarow: List[Towar] = [
        Towar("Kawa ziarnista Arabica", 50),
        Towar("Herbata czarna Earl Grey", 120),
        Towar("Cukier trzcinowy", 80),
    ]

# --- Funkcje modyfikujące listę ---

def dodaj_towar(nazwa: str, ilosc: int):
    """Dodaje lub aktualizuje towar w liście."""
    if not nazwa or ilosc <= 0:
        st.error("Wprowadź poprawną nazwę i ilość (musi być > 0).")
        return

    znaleziono = False
    for towar in st.session_state.lista_towarow:
        if towar.nazwa.lower() == nazwa.lower():
            towar.ilosc += ilosc
            znaleziono = True
            st.success(f"Zaktualizowano ilość dla **{nazwa}**. Nowa ilość: {towar.ilosc}")
            break

    if not znaleziono:
        nowy_towar = Towar(nazwa, ilosc)
        st.session_state.lista_towarow.append(nowy_towar)
        st.success(f"Dodano nowy towar: **{nowy_towar}**")

def usun_towar_po_indeksie(indeks: int):
    """Usuwa towar z listy na podstawie indeksu."""
    try:
        usuniety_towar = st.session_state.lista_towarow.pop(indeks)
        st.success(f"Usunięto towar: **{usuniety_towar.nazwa}**")
    except IndexError:
        st.error("Nieprawidłowy indeks towaru do usunięcia.")

# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Prosty Magazyn", layout="wide")

st.title("📦 Prosty System Zarządzania Magazynem")
st.markdown("Aplikacja działa bez trwałego zapisu danych.")

# --- 1. Wyświetlanie stanu magazynu ---

st.header("Aktualny Stan Magazynu")

if not st.session_state.lista_towarow:
    st.info("Magazyn jest pusty.")
else:
    dane_do_tabeli = [
        {
            "Nazwa Towaru": t.nazwa,
            "Ilość": t.ilosc
        }
        for t in st.session_state.lista_towarow
    ]
    
    st.dataframe(dane_do_tabeli, use_container_width=True, hide_index=True)


st.divider()

# --- 2. Dodawanie nowego towaru ---

st.header("➕ Dodaj / Uzupełnij Towar")
with st.form("form_dodaj_towar", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nowa_nazwa = st.text_input("Nazwa Towaru", key="input_nazwa_dodaj")
    
    with col2:
        nowa_ilosc = st.number_input("Ilość", min_value=1, value=1, step=1, key="input_ilosc_dodaj")
    
    submitted = st.form_submit_button("Dodaj Towar")
    
    if submitted:
        dodaj_towar(nowa_nazwa, nowa_ilosc)
        st.experimental_rerun() 

st.divider()

# --- 3. Usuwanie towaru ---

st.header("➖ Usuń Towar")

if st.session_state.lista_towarow:
    opcje_do_usuniecia = [
        f"[{i}] {t.nazwa} (Ilość: {t.ilosc})"
        for i, t in enumerate(st.session_state.lista_towarow)
    ]

    zaznaczony_towar = st.selectbox(
        "Wybierz towar do usunięcia (całkowicie):",
        options=opcje_do_usuniecia,
        index=0
    )

    if st.button("Usuń Zaznaczony Towar", type="primary"):
        indeks_str = zaznaczony_towar.split(']')[0].lstrip('[')
        indeks_do_usuniecia = int(indeks_str)
        
        usun_towar_po_indeksie(indeks_do_usuniecia)
        st.experimental_rerun()
else:
    st.warning("Brak towarów do usunięcia.")
