import streamlit as st
from typing import List

# Definicja klasy Towar (przedmiot)
class Towar:
    def __init__(self, nazwa: str, ilosc: int):
        self.nazwa = nazwa
        self.ilosc = ilosc

    def __str__(self):
        return f"{self.nazwa} (Stosów: {self.ilosc // 64}, Reszta: {self.ilosc % 64})"

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
        if towar.nazwa.strip().lower() == nazwa.strip().lower():
            towar.ilosc += ilosc
            znaleziono = True
            st.success(f"➕ Uzupełniono! **{towar.nazwa}** - Dodano: {ilosc} szt.")
            break

    if not znaleziono:
        nowy_towar = Towar(nazwa, ilosc)
        st.session_state.lista_towarow.append(nowy_towar)
        st.success(f"🆕 Znaleziono nowy przedmiot: **{nowy_towar.nazwa}**!")

def usun_towar_po_indeksie(indeks: int):
    """Usuwa towar z listy na podstawie indeksu."""
    try:
        usuniety_towar = st.session_state.lista_towarow.pop(indeks)
        st.error(f"🔥 Zniszczono cały stos: **{usuniety_towar.nazwa}**!")
    except IndexError:
        st.warning("Nieprawidłowy indeks przedmiotu do zniszczenia.")

# --- Interfejs użytkownika Streamlit ---

st.set_page_config(page_title="Minecraft Inventory", layout="wide")

st.title("🎒 EKWIPUNEK: Baza Materiałów")
st.markdown("### ✨ Twoje Slot'y Magazynowe")
st.caption("Aplikacja działa bez trwałego zapisu (dane znikają po odświeżeniu/redeployu).")

# --- 1. Wyświetlanie stanu magazynu (Wizualizacja slotów) ---

st.header("🖼️ Slot'y z Przedmiotami")

lista_towarow = st.session_state.lista_towarow

if not lista_towarow:
    st.info("❌ Ekwipunek jest pusty. Ruszaj na wykopaliska!")
else:
    # Tworzenie siatki (grid) na wzór ekwipunku (5 slotów w rzędzie)
    kolumny = st.columns(5) 
    
    # Funkcja do dodawania wizualnego ostrzeżenia
    def get_status_icon(ilosc):
        if ilosc >= 64:
            return "✔️" # Dobry stan/pełny stos
        elif ilosc > 10:
            return "⚠️" # Średni stan/uwaga
        else:
            return "🔴"   # Niski stan/krytycznie

    for i, towar in enumerate(lista_towarow):
        kolumna = kolumny[i % 5] # Umieszczanie w kolumnach cyklicznie
        
        with kolumna:
            # Użycie kontenera z obramowaniem, aby imitować slot
            with st.container(border=True):
                status_icon = get_status_icon(towar.ilosc)
                # Nazwa przedmiotu z ikoną statusu
                st.markdown(f"**{status_icon} {towar.nazwa}**")
                
                # Ilość jako wyraźny metric
                st.metric(
                    label="Całkowita Ilość", 
                    value=f"{towar.ilosc}", 
                    # --- BŁĄD POPRAWIONY: Usunięto problematyczny delta_color ---
                )
                
                # Wyświetlenie stosów i reszty (dla lepszego wrażenia Minecraft)
                st.markdown(f"Stosy 64: **{towar.ilosc // 64}** | Reszta: **{towar.ilosc % 64}**")
            
st.divider()

# --- 2. Dodawanie nowego towaru (Blok Wykopalisk/Craftingu) ---

st.header("⛏️ WYKOPALISKA / CRAFTING: Dodaj Przedmiot")
st.caption("Jeśli przedmiot istnieje, dodana ilość trafi do obecnego stosu.")

with st.form("form_dodaj_towar", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        nowa_nazwa = st.text_input("Nazwa Przedmiotu (np. 🌳 Dąb)", key="input_nazwa_dodaj")
    
    with col2:
        nowa_ilosc = st.number_input("Ilość (np. 1-64)", min_value=1, value=1, step=1, key="input_ilosc_dodaj")
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True) 
        submitted = st.form_submit_button("✅ DODAJ / UZUPEŁNIJ STOS", type="primary", use_container_width=True)
    
    if submitted:
        dodaj_towar(nowa_nazwa, nowa_ilosc)
        st.experimental_rerun() 

st.divider()

# --- 3. Usuwanie towaru (Blok Niszczenia/Wyrzucania) ---

st.header("🔥 NISZCZENIE: Wyrzuć Cały Stos")

if st.session_state.lista_towarow:
    col_sel, col_btn = st.columns([3, 1])
    
    opcje_do_usuniecia = [
        f"[{i}] {t.nazwa} (Ilość: {t.ilosc})"
        for i, t in enumerate(st.session_state.lista_towarow)
    ]

    with col_sel:
        zaznaczony_towar = st.selectbox(
            "Wybierz slot, który chcesz zniszczyć (całkowicie):",
            options=opcje_do_usuniecia,
            index=0,
            label_visibility="collapsed" 
        )
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚫 ZNISZCZ CAŁY STOS", type="secondary", use_container_width=True):
            indeks_str = zaznaczony_towar.split(']')[0].lstrip('[')
            indeks_do_usuniecia = int(indeks_str)
            
            usun_towar_po_indeksie(indeks_do_usuniecia)
            st.experimental_rerun()
else:
    st.warning("Brak przedmiotów do zniszczenia. Ekwipunek pusty.")
