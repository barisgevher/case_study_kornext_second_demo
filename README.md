##  Proje Hakkında

Bu projenin temel amacı programa gönderilen dilekçeden  bilgi çıkarımı yapabilmektir.

###  Özellikler

* Metin ön işleme 
* Kural tabanlı bilgi çıkarımı
* Duygusal momentum takibi
* Makine öğrenmesi ile sınıflandırma
* Makine öğrenmesi için veri tabanı oluşturma algoritması

##  Kullanılan Teknolojiler

* Python 3.9
* Scikit-learn
* Pandas & NumPy
* PyCharm IDE 

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

1.  **Projeyi klonlayın:**
    ```sh
    git clone [https://github.com/barisgevher/case_study_kornext_second_demo]
    
    cd proje-adiniz
    ```

2.  **Sanal ortam (virtual environment) oluşturun ve aktifleştirin:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # Windows için: venv\Scripts\activate
    ```

3.  **Gerekli kütüphaneleri yükleyin:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Projenin kök dizininde şu komutu çalıştırın**
```sh
   python main.py
```

**Karşınıza çıkan ekrana pdf seç ve işle diyerek bir pdf seçerseniz şu şekilde bir sonuçla karşılaşırsınız**

![PDF işleme sonuçları](screenshots/uygulama_sonuc.png)

**Eğer hazırda metin halinde bir veriniz varsa hızlıca işlemek için metin giriş kısmını kullanabilirsiniz**

![Metin işleme sonuçları](screenshots/metin_taraf_sonuc.png)


