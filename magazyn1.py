import streamlit as st
from typing import List

# Definicja klasy Towar
class Towar:
    def __init__(self, nazwa: str, ilosc: int):
        self.nazwa = nazwa
        self.ilosc = ilosc

    def __str__(self):
        return f"{self.nazwa} (Ilość: {self.ilosc})"

# Inicjalizacja listy towarów (bez trwałego zapisu)
if 'lista_towarow' not in st.session_state:
    st.session_state.lista_towarow: List[Towar] = [
        Towar("🧱 Kamień", 64),
        Towar("🌲 Drewno Dębowe", 32),
        Towar("💎 Diament", 5),
        Towar("🍞 Chleb", 10),
    ]

# --- Funkcje modyfikujące listę ---

def dodaj_towar(nazwa: str, ilosc: int):
    """Dodaje lub aktualizuje towar w liście."""
    if not nazwa or ilosc <= 0:
        st.error("Wprowadź poprawną nazwę i ilość (musi być > 0).")
        return

    znaleziono = False
    for towar in st.session_state.lista_towarow:
        # Porównanie bez uwzględniania wielkości liter
        if towar.nazwa.strip().lower() == nazwa.strip().lower():
            towar.ilosc += ilosc
            znaleziono = True
            st.success(f"➕ Uzupełniono: **{towar.nazwa}**! Nowa Ilość: {towar.ilosc}")
            break

    if not znaleziono:
        nowy_towar = Towar(nazwa, ilosc)
        st.session_state.lista_towarow.append(nowy_towar)
        st.success(f"🆕 Dodano nowy przedmiot: **{nowy_towar.nazwa}**!")

def usun_towar_po_nazwie(nazwa: str):
    """Usuwa towar z listy na podstawie nazwy."""
    
    # Znajdź indeks, ignorując emotikony i formatowanie
    lista = st.session_state.lista_towarow
    index_do_usuniecia = -1
    
    for i, towar in enumerate(lista):
        # Usuwamy formatowanie Streamlitowe, aby znaleźć czystą nazwę.
        # W tym przypadku jest to prostsze, bo usuwamy po nazwie z obiektu.
        if towar.nazwa == nazwa:
            index_do_usuniecia = i
            break
            
    if index_do_usuniecia != -1:
        usuniety_towar = st.session_state.lista_towarow.pop(index_do_usuniecia)
        st.error(f"❌ Usunięto cały stos: **{usuniety_towar.nazwa}**!")
    else:
        st.warning("Nie znaleziono towaru do usunięcia.")


# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Magazyn Minecraft", layout="wide")

# Użycie kolorowego kontenera (box) dla tytułu
st.title("🎒 EQWIPUNEK: Baza Materiałów")
st.markdown("### ✨ Twoje Slot'y Magazynowe")

# --- 1. Wyświetlanie stanu magazynu (Wizualizacja slotów) ---

st.subheader("Aktualne Stosy (Sloty)")

lista_towarow = st.session_state.lista_towarow

if not lista_towarow:
    st.info("❌ Ekwipunek jest pusty. Idź kopać!")
else:
    # Tworzenie siatki (grid) na wzór ekwipunku (4 sloty w rzędzie)
    kolumny = st.columns(4) 
    
    # Określenie stylu koloru baneru w zależności od ilości
    def get_color(ilosc):
        if ilosc >= 64:
            return "success" # Zielony (pełny stos)
        elif ilosc > 20:
            return "warning" # Żółty (częściowy stos)
        else:
            return "info"   # Niebieski (niski stan)

    for i, towar in enumerate(lista_towarow):
        kolumna = kolumny[i % 4] # Umieszczanie w kolumnach cyklicznie
        
        with kolumna:
            # Używamy st.metric lub st.container z emotikonami, 
            # aby naśladować blokowy, wyraźny slot
            
            # W Streamlit 1.29 i wyżej można użyć st.status/st.container, 
            # ale st.metric daje wyraźne tło
            st.metric(
                label=f"📦 {towar.nazwa}", 
                value=f"{towar.ilosc}", 
                help=f"Stan na magazynie: {towar.ilosc}",
                delta_color=get_color(towar.ilosc) # Używamy koloru do podkreślenia stanu
            )
            # Użycie pustego markdowna z wyraźnym tłem, aby stworzyć wizualny blok
            st.markdown(f'<div style="background-color: #333333; color: white; padding: 5px; border-radius: 5px; text-align: center;">ID: {i+1}</div>', unsafe_allow_html=True)
            
st.divider()

# --- 2. Dodawanie nowego towaru (Blok Uzupełniania) ---

st.header("⛏️ WYKOPALISKA: Dodaj/Uzupełnij Stos")
st.caption("Jeśli przedmiot już istnieje, jego ilość zostanie dodana do obecnego stosu.")

with st.form("form_dodaj_towar", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Sugestia: Podaj nazwę towaru wraz z emotikoną!
        nowa_nazwa = st.text_input("Nazwa Przedmiotu (np. 🌳 Dąb)", key="input_nazwa_dodaj")
    
    with col2:
        nowa_ilosc = st.number_input("Ilość (Max Stos 64)", min_value=1, value=1, max_value=64, step=1, key="input_ilosc_dodaj")
    
    # Duży, wyraźny przycisk dodawania
    submitted = st.form_submit_button("✅ DODAJ / UZUPEŁNIJ STOS", type="primary")
    
    if submitted:
        dodaj_towar(nowa_nazwa, nowa_ilosc)
        st.experimental_rerun() 

st.divider()

# --- 3. Usuwanie towaru (Blok Recyklingu/Zużycia) ---

st.header("🔥 ZUŻYCIE: Usuń Cały Stos")

if st.session_state.lista_towarow:
    
    # Tworzenie listy nazw towarów do wyboru
    nazwy_do_usuniecia = [t.nazwa for t in st.session_state.lista_towarow]

    zaznaczony_towar_nazwa = st.selectbox(
        "Wybierz, który stos chcesz zużyć/wyrzucić (całkowicie):",
        options=nazwy_do_usuniecia,
        index=0
    )

    # Czerwony, wyraźny przycisk usuwania
    if st.button("🚫 USUŃ CAŁY STOS Z EKWIPUNKU", type="secondary"):
        usun_towar_po_nazwie(zaznaczony_towar_nazwa)
        st.experimental_rerun()
else:
    st.warning("Ekwipunek jest pusty. Brak przedmiotów do zużycia.")
