class Heuristic():

    def __init__(self, list_product:list) -> None:
        
        self.list_product : list = list_product
        self.bobot: dict[str, float] = {
            'total_price': 0.85,
            'price': 0.5,
            'ongkir': 0.5,
            'waktu': 0.2,
            'review': 0.2,
            'rating': 0.25,
            'sold': 0.25,
            'stock': 0.01}

        self.sortByPrice()

    def sortByPrice(self):
        self.rata_rata = self.list_product[0]['total_price']
        self.temp_list_product = []
        for item in self.list_product:
            diskon = self.countDiscount()
            max_range = self.rata_rata + diskon
            min_range = self.rata_rata - diskon
            if min_range <= item['total_price'] <= max_range:
                self.temp_list_product.append(item)
                self.rata_rata = sum(p['total_price'] for p in self.temp_list_product) / len(self.temp_list_product)
        self.list_product = self.temp_list_product

    def countDiscount(self) -> float:
        batas = [10000, 20000, 30000, 200000, 500000, 1000000, 2000000, float('inf')]
        diskon = [0.35, 0.25, 0.20, 0.20, 0.20, 0.15, 0.10, 0.06]
        index = next(i for i, b in enumerate(batas) if self.rata_rata <= b)
        selisih_harga = self.rata_rata * diskon[index]
        return(selisih_harga)

    def scoreByHeuristic(self, produk:dict, min_total:int, min_price:int, min_ongkir:int) -> float:

        skor : any = (
            (min_total / produk['total_price']) * self.bobot['total_price'] +
            (min_price / produk['price']) * self.bobot['price'] +
            (min_ongkir / produk['ongkir']) * self.bobot['ongkir'] +
            (1 / produk['waktu']) * self.bobot['waktu'] +
            (produk['review'] / max(p['review'] for p in self.list_product)) * self.bobot['review'] +
            (produk['rating'] / 5) * self.bobot['rating'] +
            (produk['sold'] / max(p['sold'] for p in self.list_product)) * self.bobot['sold'] +
            (produk['stock'] / max(p['stock'] for p in self.list_product)) * self.bobot['stock']
        )

        return skor

    def search(self, count:int) -> list[dict]:

        produk_terbaik = []
        min_total = min(p['total_price'] for p in self.list_product)
        min_price = min(p['price'] for p in self.list_product)
        min_ongkir = min(p['ongkir'] for p in self.list_product)

        for produk in self.list_product:
            skor = self.scoreByHeuristic(produk=produk, min_total=min_total, min_price=min_price, min_ongkir=min_ongkir)
            produk_terbaik.append({**produk, 'score':skor})

        produk_terbaik.sort(key=lambda x: x['score'], reverse=True)
        
        if len(produk_terbaik) < count:
            produk_terbaik = produk_terbaik
        else:
            produk_terbaik = produk_terbaik[:count]

        return(produk_terbaik)

# produk_data : list[dict[str,any]] = [
#     {"status":"success", "id":"13513232415", "name":"Monitor Xiaomi Mi 34 Inch G34WQi WQHD Ultrawide 180Hz SRGB Curved Gaming Monitor",                        "price":3935000, "real_price":3935000, "discount":0,  "stock":94,  "url":"https://www.tokopedia.com/bandarkomputer/monitor-xiaomi-mi-34-inch-g34wqi-wqhd-ultrawide-180hz-srgb-curved-gaming-monitor",                      "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/22/fc274d42-ac08-4d36-88da-e86a916a446c.png", "ongkir":250000, "waktu":3, "review":31,  "rating":5.0, "sold":93},
#     {"status":"success", "id":"13395288395", "name":"Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi 3 Tahun - Packing Bubble", "price":3930000, "real_price":6000000, "discount":35, "stock":45,  "url":"https://www.tokopedia.com/tokobaru-s/xiaomi-mi-monitor-34-g34wqi-wqhd-ultrawide-180hz-curved-gaming-garansi-resmi-3-tahun-packing-bubble-bf6b5", "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/15/7d2eb422-cf14-4665-8b66-0d3a8e2fa4de.png", "ongkir":67250,  "waktu":4, "review":3,   "rating":5.0, "sold":8},
#     {"status":"success", "id":"14536475851", "name":"Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",                   "price":3880000, "real_price":3880000, "discount":0,  "stock":100, "url":"https://www.tokopedia.com/multifungsiharco/xiaomi-mi-monitor-34-g34wqi-wqhd-ultrawide-180hz-curved-gaming-g34wqi-tanpa-kayu-6a34a",              "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/7/22/75499b70-ba58-4a60-992f-a0109245d552.jpg", "ongkir":280133, "waktu":4, "review":101, "rating":4.9, "sold":252},
#     {"status":"success", "id":"13218062038", "name":"Xiaomi Curved Gaming Monitor 34 Inch G34WQi Garansi Resmi",                                               "price":3989000, "real_price":4499000, "discount":11, "stock":10,  "url":"https://www.tokopedia.com/mibo-official/xiaomi-curved-gaming-monitor-34-inch-g34wqi-garansi-resmi",                                              "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/3/2184b436-fe66-481c-9e30-48ce4e2f8a0a.png",  "ongkir":267400, "waktu":4, "review":12,  "rating":5.0, "sold":33},
#     {"status":"success", "id":"13384642944", "name":"Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi 3 Tahun - bubble",         "price":3885000, "real_price":5000000, "discount":22, "stock":26,  "url":"https://www.tokopedia.com/tokojbc/xiaomi-mi-monitor-34-g34wqi-wqhd-ultrawide-180hz-curved-gaming-garansi-resmi-3-tahun-bubble-59fd4",            "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/14/a1161b77-91db-401f-92e2-143b734b8f8f.png", "ongkir":174750, "waktu":4, "review":5,   "rating":5.0, "sold":5},
#     {"status":"success", "id":"13734382201", "name":"Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming",                                        "price":3950000, "real_price":3950000, "discount":0,  "stock":86,  "url":"https://www.tokopedia.com/jayakomputa-1/xiaomi-mi-monitor-34-g34wqi-wqhd-ultrawide-180hz-curved-gaming",                                         "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/6/6/a21cf667-5c95-457e-9248-bf11bd0b6812.jpg",  "ongkir":93216,  "waktu":4, "review":4,   "rating":5.0, "sold":13},
#     {"status":"success", "id":"13371434839", "name":"Xiaomi Mi Monitor 34 Inch G34WQi WQHD Ultrawide 180Hz Curved Gaming Monitor - +Kayu JNE/Sicpt",           "price":4000000, "real_price":4199000, "discount":5,  "stock":17,  "url":"https://www.tokopedia.com/getonlines/xiaomi-mi-monitor-34-inch-g34wqi-wqhd-ultrawide-180hz-curved-gaming-monitor-kayu-jne-sicpt-28a25",          "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/6/13/2ea1f54a-d0ef-46d4-bf23-3d77744480d0.png", "ongkir":347750, "waktu":4, "review":33,  "rating":5.0, "sold":56},
#     {"status":"success", "id":"14709155115", "name":"Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",                   "price":3880000, "real_price":3880000, "discount":0,  "stock":100, "url":"https://www.tokopedia.com/shingushop/xiaomi-mi-monitor-34-g34wqi-wqhd-ultrawide-180hz-curved-gaming-g34wqi-tanpa-kayu-424d5",                    "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/7/22/cd1023a2-922a-4fd8-a3fb-3b9240137df1.jpg", "ongkir":260700, "waktu":4, "review":12,  "rating":5.0, "sold":20},
#     {"status":"success", "id":"13382127665", "name":"Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming ",                                       "price":3972000, "real_price":3972000, "discount":0,  "stock":9,   "url":"https://www.tokopedia.com/starcomporigin/xiaomi-mi-monitor-34-g34wqi-wqhd-ultrawide-180hz-curved-gaming",                                        "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/14/b2a32c2f-932b-4bf2-88b3-d39cae6aebdd.png", "ongkir":158250, "waktu":4, "review":3,   "rating":5.0, "sold":5},
#     {"status":"success", "id":"13420414905", "name":"Xiaomi Monitor Curved Gaming Monitor 34 Inch 180Hz 34\" WQHD G34WQi 34inch",                              "price":3899000, "real_price":4170000, "discount":6,  "stock":97,  "url":"https://www.tokopedia.com/venusmobile/xiaomi-monitor-curved-gaming-monitor-34-inch-180hz-34-wqhd-g34wqi-34inch",                                 "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/16/8386ab25-4fe1-4012-8b17-3ce313213066.jpg", "ongkir":192500, "waktu":3, "review":3,   "rating":5.0, "sold":4},
#     {"status":"success", "id":"15179557817", "name":"Monitor Xiaomi Mi 34 Inch G34WQi WQHD Ultrawide 180Hz SRGB Curved Gaming Monitor",                        "price":3935000, "real_price":3935000, "discount":0,  "stock":11,  "url":"https://www.tokopedia.com/gamingpcstore/monitor-xiaomi-mi-34-inch-g34wqi-wqhd-ultrawide-180hz-srgb-curved-gaming-monitor",                       "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/9/19/9f82cc0e-ac80-4074-95a3-bff843769d3c.jpg", "ongkir":208666, "waktu":4, "review":1,   "rating":5.0, "sold":1},
#     {"status":"success", "id":"13229846913", "name":"Xiaomi Mi Monitor 34 Inch G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi",                       "price":4150000, "real_price":4150000, "discount":0,  "stock":1,   "url":"https://www.tokopedia.com/globel-com/xiaomi-mi-monitor-34-inch-g34wqi-wqhd-ultrawide-180hz-curved-gaming-garansi-resmi",                         "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/5/4/a3c3c896-7b26-4ff2-9eaf-bd897518bbd7.jpg",  "ongkir":479500, "waktu":5, "review":2,   "rating":5.0, "sold":2},
#     {"status":"success", "id":"15076881340", "name":"Xiaomi Mi Monitor G34WQi 34 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",              "price":3985500, "real_price":3985500, "discount":0,  "stock":33,  "url":"https://www.tokopedia.com/ecomputex/xiaomi-mi-monitor-g34wqi-34-inch-wqhd-ultrawide-180hz-srgb-curved-gaming-resmi-wrapping-a5eea",              "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/9/10/f272da34-aedc-4496-8cae-079ede3f774b.jpg", "ongkir":232116, "waktu":8, "review":1,   "rating":5.0, "sold":1},
#     {"status":"success", "id":"15076881340", "name":"Xiaomi Mi Monitor G28WQi 30 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",              "price":3985500, "real_price":3985500, "discount":0,  "stock":33,  "url":"https://www.tokopedia.com/ecomputex/xiaomi-mi-monitor-g34wqi-34-inch-wqhd-ultrawide-180hz-srgb-curved-gaming-resmi-wrapping-a5eea",              "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/9/10/f272da34-aedc-4496-8cae-079ede3f774b.jpg", "ongkir":232116, "waktu":8, "review":1,   "rating":5.0, "sold":1},
#     {"status":"success", "id":"15076881340", "name":"Xiaomi Mi Monitor G34WQi 34 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",              "price":3985500, "real_price":3985500, "discount":0,  "stock":33,  "url":"https://www.tokopedia.com/ecomputex/xiaomi-mi-monitor-g34wqi-34-inch-wqhd-ultrawide-180hz-srgb-curved-gaming-resmi-wrapping-a5eea",              "picture":"https://images.tokopedia.net/img/cache/700/VqbcmM/2024/9/10/f272da34-aedc-4496-8cae-079ede3f774b.jpg", "ongkir":232116, "waktu":8, "review":1,   "rating":5.0, "sold":1},
# ]



# list_nama = [
#     "Monitor Xiaomi Mi 34 Inch G34WQi WQHD Ultrawide 180Hz SRGB Curved Gaming Monitor",                      
#     "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi 3 Tahun - Packing Bubble"
#     "Xiaomi Mi Monitor 30\" G34WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",                 
#     "Xiaomi Curved Gaming Monitor 34 Inch G34WQi Garansi Resmi",                                             
#     "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi 3 Tahun - bubble",       
#     "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming",                                      
#     "Xiaomi Mi Monitor 34 Inch G34WQi WQHD Ultrawide 180Hz Curved Gaming Monitor - +Kayu JNE/Sicpt",         
#     "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming - G34WQi, TANPA KAYU",                 
#     "Xiaomi Mi Monitor 34\" G34WQi WQHD Ultrawide 180Hz Curved Gaming ",                                     
#     "Xiaomi Monitor Curved Gaming Monitor 34 Inch 180Hz 34\" WQHD G34WQi 34inch",                            
#     "Monitor Xiaomi Mi 34 Inch G34WQi WQHD Ultrawide 180Hz SRGB Curved Gaming Monitor",                      
#     "Xiaomi Mi Monitor 34 Inch G34WQi WQHD Ultrawide 180Hz Curved Gaming Garansi Resmi",                     
#     "Xiaomi Mi Monitor G34WQi 34 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",            
#     "Xiaomi Mi Monitor G30WQi 30 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",            
#     "Samsung Mi Monitor G34WQi 34 Inch WQHD Ultrawide 180Hz SRGB Curved Gaming Resmi - +Wrapping",            
# ]

# produk_data = [
#     {"status": "success", "id": "12736802529", "name": "VGA Card MSI GeForce RTX 3050 VENTUS 2X 6G OC - 6GB GDDR6", "price": 3049000, "real_price": 3320000, "discount": 8, "stock": 7, "url": "https://www.tokopedia.com/nvidiageforce/vga-card-msi-geforce-rtx-3050-ventus-2x-6g-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/8/13/7144a396-a7b3-428d-a3cf-5a059adec981.jpg", "ongkir": 35000, "waktu": 3, "review": 32, "rating": 5.0, "sold": 49},
#     {"status": "success", "id": "12747408212", "name": "VGA MSI GEFORCE RTX 3050 VENTUS 2X OC 6GB GDDR6", "price": 3090000, "real_price": 3090000, "discount": 0, "stock": 2, "url": "https://www.tokopedia.com/tokoexpert/vga-msi-geforce-rtx-3050-ventus-2x-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/2/16/b5af6bac-3797-4061-8e89-0ed208314b9b.jpg", "ongkir": 40133, "waktu": 4, "review": 2, "rating": 5.0, "sold": 11},
#     {"status": "success", "id": "14185544923", "name": "VGA MSI GeForce RTX 3050 6GB GDDR6 VENTUS 2X 6G OC", "price": 3249000, "real_price": 3249000, "discount": 0, "stock": 6, "url": "https://www.tokopedia.com/eseskomputer/vga-msi-geforce-rtx-3050-6gb-gddr6-ventus-2x-6g-oc", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/7/3/ed24211a-6386-4d8e-b62c-5731f0f3d7c0.jpg", "ongkir": 38833, "waktu": 3, "review": 1, "rating": 5.0, "sold": 3},
#     {"status": "success", "id": "12738517087", "name": "VGA MSI GeForce RTX 3050 VENTUS 2X 6G OC | RTX3050 6GB GDDR6", "price": 3013000, "real_price": 3013000, "discount": 0, "stock": 4, "url": "https://www.tokopedia.com/youngscom/vga-msi-geforce-rtx-3050-ventus-2x-6g-oc-rtx3050-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/8/30/d5389a88-8828-405b-9f6a-a2b89be113e0.png", "ongkir": 33000, "waktu": 4, "review": 6, "rating": 5.0, "sold": 11},
#     {"status": "success", "id": "14155038699", "name": "VGA Card MSI GeForce RTX 3050 VENTUS 2X 6G OC - 6GB GDDR6", "price": 3099000, "real_price": 3099000, "discount": 0, "stock": 49, "url": "https://www.tokopedia.com/ascaryacomputer-1/vga-card-msi-geforce-rtx-3050-ventus-2x-6g-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/7/16/24d9199d-90d4-4783-852a-f2975f8f3a46.png", "ongkir": 38800, "waktu": 4, "review": 2, "rating": 5.0, "sold": 3},
#     {"status": "success", "id": "14199165958", "name": "VGA MSI GeForce RTX 3050 6GB GDDR6 VENTUS 2X 6G OC", "price": 3249000, "real_price": 3249000, "discount": 0, "stock": 2, "url": "https://www.tokopedia.com/eseskomputertasikmalaya/vga-msi-geforce-rtx-3050-6gb-gddr6-ventus-2x-6g-oc", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/7/4/178eeacf-8533-4ebf-833d-500a5ebec316.jpg", "ongkir": 42933, "waktu": 4, "review": 1, "rating": 5.0, "sold": 2},
#     {"status": "success", "id": "12833101770", "name": "VGA MSI GeForce RTX 3050 VENTUS 2X OC 6GB GDDR6", "price": 3320000, "real_price": 3320000, "discount": 0, "stock": 4, "url": "https://www.tokopedia.com/hexacomputer/vga-msi-geforce-rtx-3050-ventus-2x-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/3/1/148eb0b2-9f70-411e-b6e9-f958d13c7a90.jpg", "ongkir": 23000, "waktu": 3, "review": 1, "rating": 5.0, "sold": 1},
#     {"status": "success", "id": "12813926979", "name": "Vga Card Msi GeForce RTX\u2122 3050 Ventus 2X 8G OC", "price": 3995000, "real_price": 3995000, "discount": 0, "stock": 9, "url": "https://www.tokopedia.com/agrapana-tech/vga-card-msi-geforce-rtx-3050-ventus-2x-8g-oc", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/3/1/3a3a59b7-a6a6-4773-94f0-dd5c08135060.jpg", "ongkir": 39000, "waktu": 3, "review": 1, "rating": 5.0, "sold": 1},
#     {"status": "success", "id": "12769471625", "name": "VGA MSI GeForce RTX 3050 VENTUS 2X 6G OC 6GB GDDR6", "price": 2999000, "real_price": 2999000, "discount": 0, "stock": 4, "url": "https://www.tokopedia.com/oneitgadget/vga-msi-geforce-rtx-3050-ventus-2x-6g-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/hDjmkQ/2024/10/10/7668a63b-6390-4afa-b333-8505dc506817.jpg", "ongkir": 17500, "waktu": 4, "review": 1, "rating": 5.0, "sold": 1},
#     {"status": "success", "id": "12770264189", "name": "VGA MSI GeForce RTX 3050 VENTUS 2X 6G OC 6GB GDDR6", "price": 2999000, "real_price": 2999000, "discount": 0, "stock": 5, "url": "https://www.tokopedia.com/oneitoffice/vga-msi-geforce-rtx-3050-ventus-2x-6g-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/hDjmkQ/2024/5/1/1e3a2c21-8634-4727-8f5e-ab0edac70ec0.jpg", "ongkir": 17500, "waktu": 4, "review": 1, "rating": 5.0, "sold": 1},
#     {"status": "success", "id": "13163381536", "name": "VGA MSI GeForce RTX 3050 VENTUS 2X 6G OC | RTX3050 6GB GDDR6", "price": 3299000, "real_price": 3299000, "discount": 0, "stock": 98, "url": "https://www.tokopedia.com/point99/vga-msi-geforce-rtx-3050-ventus-2x-6g-oc-rtx3050-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/4/26/4a4fb988-872e-4b57-bc8b-3e7d2d1713f6.jpg", "ongkir": 44033, "waktu": 3, "review": 1, "rating": 5.0, "sold": 2},
#     {"status": "success", "id": "14282435331", "name": "VGA Card MSI GeForce RTX 3050 VENTUS 2X 6G OC - 6GB GDDR6", "price": 3320000, "real_price": 3320000, "discount": 0, "stock": 8, "url": "https://www.tokopedia.com/gtcomputer/vga-card-msi-geforce-rtx-3050-ventus-2x-6g-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/VqbcmM/2024/7/9/08e9003b-02c9-40e4-a7ce-7495e38a85a2.png", "ongkir": 37466, "waktu": 4, "review": 1, "rating": 5.0, "sold": 1},
#     {"status": "success", "id": "12769471476", "name": "VGA MSI GeForce RTX 3050 VENTUS 2X 6G OC 6GB GDDR6", "price": 2999000, "real_price": 2999000, "discount": 0, "stock": 4, "url": "https://www.tokopedia.com/oneitgaming/vga-msi-geforce-rtx-3050-ventus-2x-6g-oc-6gb-gddr6", "picture": "https://images.tokopedia.net/img/cache/700/hDjmkQ/2024/10/10/d411238b-472a-4b63-a9f5-04ace794ae80.jpg", "ongkir": 17500, "waktu": 4, "review": 1, "rating": 5.0, "sold": 1}
# ]

# HS = Heuristic(list_product=produk_data)
# best = HS.search(count=3)
# print(best)

# print(f"Produk Terbaik: {produk_terbaik[1]} , Skor: {produk_terbaik[0]:.2f}")