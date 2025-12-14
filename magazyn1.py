import streamlit as st
from typing import List

# Definicja klasy Towar
class Towar:
    def __init__(self, nazwa: str, ilosc: int):
        self.nazwa = nazwa
        self.ilosc = ilosc

    def __str__(self):
        return f"{self.nazwa} (Ilość: {self.ilosc})"

# Inicjalizacja listy towarów w stanie sesji Streamlit (bez trwałego zapisu)
if 'lista_towarow' not in st.session_state:
    st.session_state.lista_towarow: List[Towar] = [
        Towar("☕ Kawa ziarnista Arabica", 50),
        Towar("🍵 Herbata czarna Earl Grey", 120),
        Towar("🍚 Cukier trzcinowy", 80),
        Towar("🥛 Mleko UHT", 25),
    ]

# --- Funkcje modyfikujące listę ---

def dodaj_towar(nazwa: str, ilosc: int):
    """Dodaje lub aktualizuje towar w liście."""
    if not nazwa or ilosc <= 0:
        st.error("Wprowadź poprawną nazwę i ilość (musi być > 0).")
        return

    znaleziono = False
    for towar in st.session_state.lista_towarow:
        if towar.nazwa.strip().lower() == nazwa.strip().lower():
            towar.ilosc += ilosc
            znaleziono = True
            st.success(f"➕ Uzupełniono! **{towar.nazwa}**. Nowa Ilość: {towar.ilosc}")
            break

    if not znaleziono:
        nowy_towar = Towar(nazwa, ilosc)
        st.session_state.lista_towarow.append(nowy_towar)
        st.success(f"🆕 Dodano nowy towar: **{nowy_towar.nazwa}**")

def usun_towar_po_indeksie(indeks: int):
    """Usuwa towar z listy na podstawie indeksu."""
    try:
        usuniety_towar = st.session_state.lista_towarow.pop(indeks)
        st.error(f"❌ Usunięto cały stos: **{usuniety_towar.nazwa}**")
    except IndexError:
        st.warning("Nieprawidłowy indeks towaru do usunięcia.")

# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Magazyn w Stylu Gry", layout="wide")

# Użycie emotikon i kolorów w tytule
st.title("🛡️ EKWIPUNEK MAGAZYNOWY (v1.2)")
st.info("Dane są przechowywane tymczasowo (tylko w tej sesji aplikacji).")

# --- 1. Wyświetlanie stanu magazynu (Wizualizacja slotów) ---

st.header("📦 Zawartość Magazynu (Sloty)")

lista_towarow = st.session_state.lista_towarow

if not lista_towarow:
    st.info("🧱 Magazyn jest pusty. Dodaj pierwszy przedmiot!")
else:
    # Używamy siatki (grid) z 4 kolumn
    kolumny = st.columns(4) 
    
    # Funkcja do określania koloru naśladującego pasek statusu/stan
    def get_color(ilosc):
        if ilosc >= 100:
            return "green"  # Pełny (zielony)
        elif ilosc > 30:
            return "orange" # Średni (pomarańczowy/żółty)
        else:
            return "red"    # Niski stan (czerwony)

    for i, towar in enumerate(lista_towarow):
        kolumna = kolumny[i % 4] # Cykliczne umieszczanie w kolumnach
        
        with kolumna:
            # Użycie st.container z emotikonami i wyraźnym tłem, aby imitować "slot"
            with st.container(border=True):
                # Nazwa
                st.markdown(f"**{towar.nazwa}**")
                
                # Użycie st.metric do wyraźnego wyświetlenia ilości
                st.metric(
                    label="Ilość w Stosie", 
                    value=f"{towar.ilosc}", 
                )
                
                # Dodatkowy kolorowy pasek (prosta wizualizacja stanu)
                st.progress(towar.ilosc / 150, text=f"Stan krytyczny: **{get_color(towar.ilosc)}**")
            
st.divider()

# --- 2. Dodawanie nowego towaru (Blok Akcji) ---

st.header("➕ KUPNO / UZUPEŁNIENIE")

with st.form("form_dodaj_towar", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        nowa_nazwa = st.text_input("Nazwa Przedmiotu (dodaj emotikonę dla stylu!)", key="input_nazwa_dodaj")
    
    with col2:
        nowa_ilosc = st.number_input("Ilość", min_value=1, value=1, step=1, key="input_ilosc_dodaj")
    
    with col3:
        # Pusty space dla wyrównania wizualnego
        st.markdown("<br>", unsafe_allow_html=True) 
        submitted = st.form_submit_button("✅ DODAJ STOS", type="primary", use_container_width=True)
    
    if submitted:
        dodaj_towar(nowa_nazwa, nowa_ilosc)
        st.experimental_rerun() 

st.divider()

# --- 3. Usuwanie towaru (Blok Recyklingu) ---

st.header("➖ ZUŻYCIE / USUNIĘCIE")

if st.session_state.lista_towarow:
    col_sel, col_btn = st.columns([3, 1])
    
    opcje_do_usuniecia = [
        f"[{i}] {t.nazwa} (Ilość: {t.ilosc})"
        for i, t in enumerate(st.session_state.lista_towarow)
    ]

    with col_sel:
        zaznaczony_towar = st.selectbox(
            "Wybierz slot do usunięcia (całkowicie):",
            options=opcje_do_usuniecia,
            index=0,
            label_visibility="collapsed"
        )
    
    with col_btn:
        # Pusty space dla wyrównania wizualnego
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 ZUŻYJ CAŁY STOS", type="secondary", use_container_width=True):
            indeks_str = zaznaczony_towar.split(']')
