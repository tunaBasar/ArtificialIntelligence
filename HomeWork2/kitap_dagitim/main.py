import folium
import streamlit as st
import numpy as np
import pandas as pd
import googlemaps
import matplotlib.pyplot as plt
from algoritma import AntColonyOptimization
from streamlit_folium import st_folium

st.set_page_config(page_title="Kitap Dağıtımı", layout="wide")

st.markdown("""
Ad Soyad: Hilmi Tunahan BAŞAR
Okul No: 2112721019
Senaryo: Kitap Dağıtımı
""")
st.markdown("---")

st.sidebar.header("Parametreleri buradan değiştirebilirsiniz")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = st.sidebar.text_input("Google Maps API Key", type="password")
    st.sidebar.warning("API Key secrets.toml dosyasında bulunamadı.")

n_ants = st.sidebar.slider("Karınca Sayısı", 10, 100, 30)
n_iterations = st.sidebar.slider("İterasyon Sayısı", 10, 200, 50)
alpha = st.sidebar.slider("Alpha (Feromon Önemi)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta (Mesafe Önemi)", 0.1, 5.0, 2.0)
evaporation = st.sidebar.slider("Buharlaşma Oranı", 0.1, 0.99, 0.5)

lokasyonlar = [
    "İzmir İl Milli Eğitim Müdürlüğü",
    "Çiğli Teğmen Ali Rıza Akıncı Anadolu Lisesi",
    "İzmir Fen Lisesi",
    "Bornova Anadolu Lisesi",
    "İzmir Yunus Emre Anadolu Lisesi",
    "Çiğli 75.Yıl Mesleki ve Teknik Anadolu Lisesi",
    "Karşıyaka 15 Temmuz Şehitler Anadolu Lisesi",
    "Karşıyaka Atakent Anadolu Lisesi",
    "Cemil Meriç Ortaokulu",
    "İzmir-Karabağlar Şehit Muhtar Mete Sertbaş Ortaokulu",
    "İzmir-Konak Osman Kibar Ortaokulu",
    "Karşıyaka Lisesi",
    "Şehit Fazıl Bey İlköğretim Okulu",
    "Emlakbank Süleyman Demirel Anadolu Lisesi",
    "Nazire Merzeci İlkokulu",
    "Limontepe Seniye Hasan Saray İlkokulu" 
]

st.title("Kitap Dağıtım")
st.info(f"{len(lokasyonlar)} farklı noktaya kitap dağıtımı için en kısa rota hesaplanıyor.")

st.subheader("Dağıtım Noktaları")
st.dataframe(pd.DataFrame(lokasyonlar, columns=["Okul Adı / Lokasyon"]))

if st.button("Rota_Hesapla"):
    if not api_key:
        st.error("api anahtarı bulunamadı hocam")
    else:
        try:
            gmaps = googlemaps.Client(key=api_key)
            
            status_text = st.empty() 
            status_text.info("Lokasyonların koordinatları alınıyor")
            
            temp_koordinatlar = [] 
            temp_valid_locations = [] 
            
            progress_bar = st.progress(0)
            
            for idx, loc in enumerate(lokasyonlar):
                try:
                    geocode_result = gmaps.geocode(loc)
                    if geocode_result:
                        lat = geocode_result[0]['geometry']['location']['lat']
                        lng = geocode_result[0]['geometry']['location']['lng']
                        temp_koordinatlar.append({"lat": lat, "lon": lng, "isim": loc})
                        temp_valid_locations.append(loc)
                    else:
                        st.warning(f"'{loc}' bulunamadı.")
                except Exception as e:
                    st.error(f"Hata ({loc}): {e}")
                progress_bar.progress((idx + 1) / len(lokasyonlar))
            
            status_text.info('Mesafeler hesaplanıyor')
            n = len(temp_valid_locations)
            temp_matrix = np.zeros((n, n))
            
            api_error_occurred = False
            
            for i in range(n):
                for j in range(n):
                    if i != j:
                        try:
                            result = gmaps.distance_matrix(temp_valid_locations[i], temp_valid_locations[j], mode="driving")
                            if result['rows'][0]['elements'][0]['status'] == 'OK':
                                temp_matrix[i][j] = result['rows'][0]['elements'][0]['distance']['value']
                            else:
                                error_msg = result['rows'][0]['elements'][0].get('status', 'Unknown Error')
                                st.error(f"API Hatası: {error_msg} -> {temp_valid_locations[i]} - {temp_valid_locations[j]}")
                                temp_matrix[i][j] = 999999
                                api_error_occurred = True
                        except Exception as e:
                            st.error(f"Bağlantı Hatası: {e}")
                            temp_matrix[i][j] = 999999
                    else:
                        temp_matrix[i][j] = np.inf
            
            if api_error_occurred:
                st.warning("Api reddetti izin kontrol et")

            status_text.success("Algoritma çalıştırılıyor")

            aco = AntColonyOptimization(
                distances=temp_matrix, 
                n_ants=n_ants, 
                n_best=int(n_ants/4), 
                n_iterations=n_iterations, 
                decay=evaporation, 
                alpha=alpha, 
                beta=beta
            )
            
            best_path, history = aco.run()
            
            st.session_state['hesaplandi'] = True
            st.session_state['best_path'] = best_path
            st.session_state['history'] = history
            st.session_state['koordinatlar'] = temp_koordinatlar
            st.session_state['valid_locations'] = temp_valid_locations
            
            status_text.empty()
            progress_bar.empty()

        except Exception as e:
            st.error(f"Genel Hata: {e}")

if st.session_state.get('hesaplandi'):
    
    best_path = st.session_state['best_path']
    history = st.session_state['history']
    koordinatlar = st.session_state['koordinatlar']
    valid_locations = st.session_state['valid_locations']
    
    best_indices = [x[0] for x in best_path[0]]
    total_dist_km = best_path[1] / 1000

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"Toplam: {total_dist_km:.2f} km")
        st.markdown("Optimize Rota:")
        for step, idx in enumerate(best_indices):
            st.write(f"{step + 1}. {valid_locations[idx]}")
        st.write(f"Dönüş: {valid_locations[best_indices[0]]}")

    with col2:
        st.subheader("Gelişim Grafiği")
        fig, ax = plt.subplots()
        ax.plot(history, color='blue')
        ax.set_title("Yakınsama")
        ax.grid(True)
        st.pyplot(fig)

    st.markdown("Rota Haritası")
    
    if len(best_indices) > 0 and len(koordinatlar) > 0:
        start_lat = koordinatlar[best_indices[0]]['lat']
        start_lon = koordinatlar[best_indices[0]]['lon']
        m = folium.Map(location=[start_lat, start_lon], zoom_start=10)

        route_coords = []
        for i, idx in enumerate(best_indices):
            loc_data = koordinatlar[idx]
            loc_coord = [loc_data['lat'], loc_data['lon']]
            route_coords.append(loc_coord)
            
            icon_color = 'red' if i == 0 else 'blue'
            icon_type = 'star' if i == 0 else 'info-sign'
            
            folium.Marker(
                location=loc_coord,
                popup=f"{i+1}. {loc_data['isim']}",
                tooltip=loc_data['isim'],
                icon=folium.Icon(color=icon_color, icon=icon_type)
            ).add_to(m)

        route_coords.append([koordinatlar[best_indices[0]]['lat'], koordinatlar[best_indices[0]]['lon']])

        folium.PolyLine(
            route_coords,
            color="red",
            weight=4,
            opacity=0.7,
            tooltip="En Kısa Rota"
        ).add_to(m)

        st_folium(m, width=725)