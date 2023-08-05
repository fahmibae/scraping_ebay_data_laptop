import requests
from bs4 import BeautifulSoup
import csv


def scrape_ebay_data(url, start_page=1, max_pages=5, max_rows=240, total_rows=0):
    
    # Inisialisasi list untuk menyimpan data
    data_all = []

    for page_number in range(start_page, start_page + max_pages):
        response = requests.get(f"{url}&_pgn={page_number}")

        if response.status_code != 200:
            print(f"Failed to access eBay website: {url}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        # Mengambil elemen yang mengandung informasi produk
        products = soup.find_all('div', class_='s-item__wrapper clearfix')

        if not products:
            break  # Keluar dari loop jika sudah tidak ada data lagi

        for product in products:
            # Cari semua elemen yang memiliki class "s-item__discount"
            manufacturer = get_manufacturer_from_ebay_product(url)
            image_url = product.find('img').get('src', 'No image')
            title = product.find('div', class_='s-item__title').text.strip()
            url = product.find('a', class_='s-item__link').get('href', 'No URL')
            price = get_price_from_ebay_product(url)
            shipping_cost = get_shipping_cost_from_ebay_product(url)
            # Cari Shipping Cost dari product ebay
            # shipping_cost_element = product.find('span', class_='s-item__shipping s-item__logisticsCost')
            # if shipping_cost_element:
            #     shipping_cost = shipping_cost_element.text.strip()
            # else:
            #     shipping_cost = 'No shipping cost'  # Set a default value or handle the absence of shipping cost

            ram = get_ram_from_ebay_product(url)
            gpu = get_gpu_from_ebay_product(url)
            processor = get_processor_from_ebay_product(url)
            screen_size = get_screen_size_from_ebay_product(url)
            screen_resolution = get_screen_resolution_from_ebay_product(url)
            product_weight = get_product_weight_from_ebay_product(url)
            ssd_ext = get_ssd_from_ebay_product(url)
            hdd_ext = get_ssd_from_ebay_product(url)

            ssd = ssd_ext if ssd_ext else ""
            hdd = hdd_ext if hdd_ext else ""
            
            # Cari Feedback Supplier
            feedback_data = get_feedback_data(url)

            ssd_hdd = ssd + " | " + hdd

            # Cari Kondisi dari URL
            condition = get_condition_from_ebay_product(url)

            # Cari item number dari URL
            ein = extract_item_number(url)

            # Cari stok barang dari deskripsi produk
            stock = get_product_stock(url)

            # Cari informasi supplier dari deskripsi produk
            supplier = get_product_supplier(url)

            # Menambahkan data ke dalam list
            data_all.append([image_url, ein, title, manufacturer, url, shipping_cost, price, stock, condition, ram, gpu, processor, ssd_hdd, screen_size, screen_resolution, product_weight, supplier, feedback_data])

            total_rows += 1
            if total_rows >= max_rows:
                break

        if total_rows >= max_rows:
            break

    return data_all, total_rows

def get_manufacturer_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return None

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi EAN (misalnya, label "EAN", atau atribut data-ean)
    manufacturer_element = product_soup.find('span', class_='ux-textspans', string='Brand')
    if manufacturer_element:
        manufacturer = manufacturer_element.find_next('span', class_='ux-textspans').text.strip()
        return manufacturer

    print(f"Manufacturer tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_feedback_data(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return None

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi EAN (misalnya, label "ISBN" atau atribut data-ean)
    feedback_element = product_soup.find('span', class_='ux-textspans', string=') ')
    if feedback_element:
        feedback = feedback_element.find_next('span', class_='ux-textspans').text.strip()
        return feedback

    print(f"Feedback tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_price_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return 'Unknown Price'

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi EAN (misalnya, label "ISBN" atau atribut data-ean)
    price_element = product_soup.find('span', class_='ux-textspans', string='Price:')
    if price_element:
        price = price_element.find_next('span', class_='ux-textspans').text.strip()
        return price

    print(f"Price tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_shipping_cost_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return 'Unknown Shipping Cost'

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi EAN (misalnya, label "ISBN" atau atribut data-ean)
    shipping_cost_element = product_soup.find('span', class_='ux-textspans', string='Shipping:')
    if shipping_cost_element:
        shipping_cost = shipping_cost_element.find_next('span', class_='ux-textspans ux-textspans--BOLD').text.strip()
        return shipping_cost

    print(f"Shipping cost tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_ram_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return 'Unknown RAM'

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi RAM (misalnya, label "RAM Size" atau atribut data-ram)
    ram_element = product_soup.find('span', class_='ux-textspans', string='RAM Size')
    if ram_element:
        ram = ram_element.find_next('span', class_='ux-textspans').text.strip()
        return ram

    print(f"RAM tidak ditemukan pada halaman produk eBay: {url}")
    return None


def get_gpu_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return 'Unknown GPU'

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi Tipe buku (misalnya, label "Format" atau atribut data-format)
    gpu_element = product_soup.find('span', class_='ux-textspans', string='GPU')
    if gpu_element:
        # Jika elemen format ditemukan, ambil teks dari elemen 'span' berikutnya
        gpu = gpu_element.find_next('span', class_='ux-textspans').text.strip()
        return gpu
    print(f"GPU Type tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_processor_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return 'Unknown Processor'

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi bahasa (misalnya, label "Language" atau atribut data-language)
    processor_element = product_soup.find('span', class_='ux-textspans', string='Processor')
    if processor_element:
        # Jika elemen bahasa ditemukan, ambil teks dari elemen 'span' berikutnya
        processor = processor_element.find_next('span', class_='ux-textspans').text.strip()
        return processor

    print(f"Processor Produk tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_screen_size_from_ebay_product(url):
    # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return 'Unknown Screen Size'

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi pengarang (misalnya, label "Author:" atau atribut data-authors)
    screen_size_element = product_soup.find('span', class_='ux-textspans', string='Screen Size')
    if screen_size_element:
        # Jika elemen pengarang ditemukan, ambil teks dari elemen 'td' berikutnya
        screen_size = screen_size_element.find_next('span', class_='ux-textspans').text.strip()
        return screen_size

    print(f"Screen Size Produk tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_screen_resolution_from_ebay_product(url):
    # Mengakses halaman produk untuk mencari informasi jumlah stok terjual
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown screen resolution'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi Screen Resolution (misalnya, label "Screen Resolution" atau atribut data-resolution)
    screen_resolution_element = soup.find('span', class_='ux-textspans', string='Maximum Resolution')
    if screen_resolution_element:
        # Jika elemen pengarang ditemukan, ambil teks dari elemen 'td' berikutnya
        screen_resolution = screen_resolution_element.find_next('span', class_='ux-textspans').text.strip()
        return screen_resolution

    print(f"Screen Resolution Produk tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_ssd_from_ebay_product(url):
    # Mengakses halaman produk untuk mencari informasi jumlah stok terjual
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown SSD'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi Screen Resolution (misalnya, label "Screen Resolution" atau atribut data-resolution)
    ssd_element = soup.find('span', class_='ux-textspans', string='SSD Capacity')
    if ssd_element:
        # Jika elemen pengarang ditemukan, ambil teks dari elemen 'td' berikutnya
        ssd = ssd_element.find_next('span', class_='ux-textspans').text.strip()
        return ssd

    print(f"SSD Produk tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_hdd_from_ebay_product(url):
    # Mengakses halaman produk untuk mencari informasi jumlah stok terjual
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown HDD'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi Screen Resolution (misalnya, label "Screen Resolution" atau atribut data-resolution)
    hdd_element = soup.find('span', class_='ux-textspans', string='Hard Drive Capacity')
    if hdd_element:
        # Jika elemen pengarang ditemukan, ambil teks dari elemen 'td' berikutnya
        hdd = hdd_element.find_next('span', class_='ux-textspans').text.strip()
        return hdd

    print(f"HDD Produk tidak ditemukan pada halaman produk eBay: {url}")
    return None
    
def get_condition_from_ebay_product(url):
    # Mengakses halaman produk untuk mencari informasi kondisi produk
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown condition product'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen HTML yang mengandung informasi kondisi product
    condition_element = soup.find('span', {'class': 'ux-icon-text__text'})

    if condition_element:
        return condition_element.text.strip()
    else:
        return 'Unknown condition product'
    
def get_product_weight_from_ebay_product(url):
    # Mengakses halaman produk untuk mencari informasi kondisi produk
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown product weight'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi Screen Resolution (misalnya, label "Screen Resolution" atau atribut data-resolution)
    product_weight_element = soup.find('span', class_='ux-textspans', string='Item Weight')
    if product_weight_element:
        # Jika elemen pengarang ditemukan, ambil teks dari elemen 'td' berikutnya
        product_weight = product_weight_element.find_next('span', class_='ux-textspans').text.strip()
        return product_weight

    print(f"Product Weight Produk tidak ditemukan pada halaman produk eBay: {url}")
    return None

def get_product_supplier(url):
    # Mengakses halaman produk untuk mencari informasi supplier
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown supplier'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen HTML yang mengandung informasi supplier
    # Ubah sesuai dengan struktur halaman eBay yang Anda scraping
    supplier_element = soup.find('span', {'class': 'ux-textspans ux-textspans--PSEUDOLINK ux-textspans--BOLD'})

    if supplier_element:
        return supplier_element.text.strip()
    else:
        return 'Unknown supplier'

def extract_item_number(url):
     # Mengakses halaman produk eBay
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk eBay: {url}")
        return None

    # Menginisialisasi objek BeautifulSoup untuk halaman produk
    product_soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen yang mengandung informasi EAN (misalnya, label "EAN", "UPC", "GTIN", atau atribut data-ean)
    item_number_element = product_soup.find('span', class_='ux-textspans ux-textspans--SECONDARY', string='eBay item number:')
    if item_number_element:
        item_number = item_number_element.find_next('span', class_='ux-textspans ux-textspans--BOLD').text.strip()
        return item_number

    print(f"Item Number tidak ditemukan pada halaman produk eBay: {url}")
    return None
    
def get_product_stock(url):
    # Mengakses halaman produk untuk mencari informasi stok barang
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Gagal mengakses halaman produk: {url}")
        return 'Unknown stock'

    soup = BeautifulSoup(response.text, 'html.parser')

    # Cari elemen HTML yang mengandung informasi stok
    stock_element = soup.find('div', {'class': 'd-quantity__availability'})

    if stock_element:
        return stock_element.text.strip()
    else:
        return 'Stok tidak ada'
    

def save_to_csv(data_list, filename):
    # Menyimpan data dalam format CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        
        csv_writer.writerow(['Image URL', 'Artiker Number', 'Title', 'Manufacturer', 'URL', 'Shipping Cost', 'Price', 'Stock', 'Condition', 'RAM', 'GPU', 'Processor', 'SSD vs HDD', 'Screen Size', 'Screen Resolution', 'Product Weight', 'Supplier', 'Positive Feedback'])
        csv_writer.writerows(data_list)

if __name__ == '__main__':
   
    ebay_urls = [
        'https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptop&_sacat=177&_fcid=1&_sop=15&rt=nc&LH_ItemCondition=1000%7C2010&Type=Notebook%252FLaptop&_dcat=177&_ipg=240&_pgn=4',
    ]

    # Inisialisasi list untuk menyimpan data
    scraped_data = []

    # Inisialisasi variabel untuk menghitung jumlah data yang telah diambil
    total_data = 0

    # Loop untuk mengambil data hingga mencapai 240 baris
    for url in ebay_urls:
        data_per_page, total_data = scrape_ebay_data(url, max_rows=240, total_rows=total_data)

        if not data_per_page:
            # Jika tidak ada data yang diambil, keluar dari loop
            break

        # Menambahkan data_per_page ke dalam scraped_data
        scraped_data += data_per_page

        if total_data >= 240:
            # Jika total_data sudah mencapai 240 baris, keluar dari loop
            break

    if scraped_data:
        # Menghapus data yang berlebih jika total_data melebihi 240 baris
        scraped_data = scraped_data[:240]

        save_to_csv(scraped_data, f'page/ebay_data_4.csv')
        print(f"Data berhasil disimpan dalam file ebay_data_4.csv")
    else:
        print("Tidak ada data yang berhasil diambil.")