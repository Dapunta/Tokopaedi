import requests, re

domain = 'www.tokopedia.com'
graphql = 'gql.tokopedia.com'

class Tokopedia():

    def __init__(self) -> None:

        self.r = requests.Session()

        self.headers_web: dict[str, str] = {
            'Host':domain,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Origin':"https://{}".format(domain)}

        self.headers_graphql: dict[str, str] = {
            'Host':graphql,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Origin':"https://{}".format(domain)}

    #--> Get Product ID
    def productQuery(self, product_link:str) -> dict:
        url: list[str] = self.r.get(url=product_link, headers=self.headers_web, allow_redirects=True).url.split('/')
        return({'shopDomain':url[3], 'productKey':url[4]})

    #--> Get Ongkir
    def ongkir(self, response:list) -> int:
        try:
            unwanted_terms: set[str] = {'same', 'gosend', 'next', 'instant', 'kurir'}
            cek: list[int] = [int((i.get('range_price').get('min_price')+i.get('range_price').get('max_price'))/2) for i in response if (not any(term in i.get('service_name').lower() for term in unwanted_terms)) and (i.get('range_price').get('min_price') and i.get('range_price').get('max_price'))]
            return(int(sum(cek)/len(cek)))
        except:
            return(0)

    #--> Count Ongkir (If Error)
    def countOngkir(self, weight:int, price:int, biaya_per_kg:int=10000, persentase_harga:float=0.05) -> int:
        biaya_berat: int = (weight / 1000) * biaya_per_kg
        biaya_harga: int = price * persentase_harga
        total_biaya: int = biaya_berat + biaya_harga
        return(int(total_biaya))

    #--> Get Waktu Pengiriman
    def waktu(self, response:list) -> int:
        try:
            unwanted_terms: set[str] = {'same', 'gosend', 'next', 'instant'}
            cek: list[str] = [int(i.get('texts').get('text_etd').split(' ')[0].split('-')[-1]) for i in response if (not any(term in i.get('service_name').lower() for term in unwanted_terms)) and (i.get('texts').get('text_etd') != '')]
            return(int(sum(cek)/len(cek)))
        except:
            return(0)

    #--> Get Product Information
    def getProductInformation(self, product_link:str) -> dict:

        product_overall = {'status':'failed'}
        user_location: dict[str, str] = {"districtID":"3526"} #--> Surabaya

        try:

            product_query: dict = self.productQuery(product_link=product_link)

            #--> Post 1
            data1: list[dict[str,any]] = [{
                "operationName": "PDPGetLayoutQuery",
                "variables": {"shopDomain":product_query['shopDomain'], "productKey":product_query['productKey'], "apiVersion":1, "extParam":"ivf%3Dfalse"},
                "query": "fragment ProductVariant on pdpDataProductVariant {\n  errorCode\n  parentID\n  defaultChild\n  sizeChart\n  totalStockFmt\n  variants {\n    productVariantID\n    variantID\n    name\n    identifier\n    option {\n      picture {\n        urlOriginal: url\n        urlThumbnail: url100\n        __typename\n      }\n      productVariantOptionID\n      variantUnitValueID\n      value\n      hex\n      stock\n      __typename\n    }\n    __typename\n  }\n  children {\n    productID\n    price\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    optionID\n    optionName\n    productName\n    productURL\n    picture {\n      urlOriginal: url\n      urlThumbnail: url100\n      __typename\n    }\n    stock {\n      stock\n      isBuyable\n      stockWordingHTML\n      minimumOrder\n      maximumOrder\n      __typename\n    }\n    isCOD\n    isWishlist\n    campaignInfo {\n      campaignID\n      campaignType\n      campaignTypeName\n      campaignIdentifier\n      background\n      discountPercentage\n      originalPrice\n      discountPrice\n      stock\n      stockSoldPercentage\n      startDate\n      endDate\n      endDateUnix\n      appLinks\n      isAppsOnly\n      isActive\n      hideGimmick\n      isCheckImei\n      minOrder\n      showStockBar\n      __typename\n    }\n    thematicCampaign {\n      additionalInfo\n      background\n      campaignName\n      icon\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ProductMedia on pdpDataProductMedia {\n  media {\n    type\n    urlOriginal: URLOriginal\n    urlThumbnail: URLThumbnail\n    urlMaxRes: URLMaxRes\n    videoUrl: videoURLAndroid\n    prefix\n    suffix\n    description\n    variantOptionID\n    __typename\n  }\n  videos {\n    source\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCategoryCarousel on pdpDataCategoryCarousel {\n  linkText\n  titleCarousel\n  applink\n  list {\n    categoryID\n    icon\n    title\n    isApplink\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductHighlight on pdpDataProductContent {\n  name\n  price {\n    value\n    currency\n    priceFmt\n    slashPriceFmt\n    discPercentage\n    __typename\n  }\n  campaign {\n    campaignID\n    campaignType\n    campaignTypeName\n    campaignIdentifier\n    background\n    percentageAmount\n    originalPrice\n    discountedPrice\n    originalStock\n    stock\n    stockSoldPercentage\n    threshold\n    startDate\n    endDate\n    endDateUnix\n    appLinks\n    isAppsOnly\n    isActive\n    hideGimmick\n    showStockBar\n    __typename\n  }\n  thematicCampaign {\n    additionalInfo\n    background\n    campaignName\n    icon\n    __typename\n  }\n  stock {\n    useStock\n    value\n    stockWording\n    __typename\n  }\n  variant {\n    isVariant\n    parentID\n    __typename\n  }\n  wholesale {\n    minQty\n    price {\n      value\n      currency\n      __typename\n    }\n    __typename\n  }\n  isCashback {\n    percentage\n    __typename\n  }\n  isTradeIn\n  isOS\n  isPowerMerchant\n  isWishlist\n  isCOD\n  preorder {\n    duration\n    timeUnit\n    isActive\n    preorderInDays\n    __typename\n  }\n  __typename\n}\n\nfragment ProductCustomInfo on pdpDataCustomInfo {\n  icon\n  title\n  isApplink\n  applink\n  separator\n  description\n  __typename\n}\n\nfragment ProductInfo on pdpDataProductInfo {\n  row\n  content {\n    title\n    subtitle\n    applink\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetail on pdpDataProductDetail {\n  content {\n    title\n    subtitle\n    applink\n    showAtFront\n    isAnnotation\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDataInfo on pdpDataInfo {\n  icon\n  title\n  isApplink\n  applink\n  content {\n    icon\n    text\n    __typename\n  }\n  __typename\n}\n\nfragment ProductSocial on pdpDataSocialProof {\n  row\n  content {\n    icon\n    title\n    subtitle\n    applink\n    type\n    rating\n    __typename\n  }\n  __typename\n}\n\nfragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {\n  title\n  description\n  contentMedia {\n    url\n    ratio\n    type\n    __typename\n  }\n  show\n  ctaText\n  __typename\n}\n\nquery PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {\n  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {\n    requestID\n    name\n    pdpSession\n    basicInfo {\n      alias\n      createdAt\n      isQA\n      id: productID\n      shopID\n      shopName\n      minOrder\n      maxOrder\n      weight\n      weightUnit\n      condition\n      status\n      url\n      needPrescription\n      catalogID\n      isLeasing\n      isBlacklisted\n      isTokoNow\n      menu {\n        id\n        name\n        url\n        __typename\n      }\n      category {\n        id\n        name\n        title\n        breadcrumbURL\n        isAdult\n        isKyc\n        minAge\n        detail {\n          id\n          name\n          breadcrumbURL\n          isAdult\n          __typename\n        }\n        __typename\n      }\n      txStats {\n        transactionSuccess\n        transactionReject\n        countSold\n        paymentVerified\n        itemSoldFmt\n        __typename\n      }\n      stats {\n        countView\n        countReview\n        countTalk\n        rating\n        __typename\n      }\n      __typename\n    }\n    components {\n      name\n      type\n      position\n      data {\n        ...ProductMedia\n        ...ProductHighlight\n        ...ProductInfo\n        ...ProductDetail\n        ...ProductSocial\n        ...ProductDataInfo\n        ...ProductCustomInfo\n        ...ProductVariant\n        ...ProductCategoryCarousel\n        ...ProductDetailMediaComponent\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}]
            pos1 = self.r.post(url='https://{}/graphql/RecomWidget'.format(graphql), headers={**self.headers_graphql, 'X-Tkpd-Akamai':'pdpGetLayout'}, json=data1).json()[0]
            pdp_session = str(object=pos1.get('data').get('pdpGetLayout').get('pdpSession'))
            product_rate = pos1['data']['pdpGetLayout']['basicInfo']

            #--> Post 2
            data2: list[dict[str,any]] = [{
                "operationName":"PDPGetDataP2",
                "variables":{"affiliate":None, "productID":str(object=pos1.get('data').get('pdpGetLayout').get('basicInfo').get('id')), "pdpSession":pdp_session, "userLocation":user_location},
                "query":"query PDPGetDataP2($productID: String!, $pdpSession: String!, $deviceID: String, $userLocation: pdpUserLocation, $affiliate: pdpAffiliate) {\n  pdpGetData(productID: $productID, pdpSession: $pdpSession, deviceID: $deviceID, userLocation: $userLocation, affiliate: $affiliate) {\n    error {\n      Code\n      Message\n      DevMessage\n      __typename\n    }\n    callsError {\n      shopInfo {\n        Code\n        Message\n        __typename\n      }\n      cartRedirection {\n        Code\n        Message\n        __typename\n      }\n      nearestWarehouse {\n        Code\n        Message\n        __typename\n      }\n      __typename\n    }\n    productView\n    wishlistCount\n    shopFinishRate {\n      finishRate\n      __typename\n    }\n    shopInfo {\n      shopTier\n      badgeURL\n      closedInfo {\n        closedNote\n        reason\n        detail {\n          openDate\n          __typename\n        }\n        __typename\n      }\n      isOpen\n      favoriteData {\n        totalFavorite\n        alreadyFavorited\n        __typename\n      }\n      activeProduct\n      createInfo {\n        epochShopCreated\n        __typename\n      }\n      shopAssets {\n        avatar\n        __typename\n      }\n      shopCore {\n        domain\n        shopID\n        name\n        shopScore\n        url\n        ownerID\n        __typename\n      }\n      shopLastActive\n      location\n      statusInfo {\n        statusMessage\n        shopStatus\n        isIdle\n        __typename\n      }\n      isAllowManage\n      isOwner\n      ownerInfo {\n        id\n        __typename\n      }\n      isCOD\n      shopType\n      tickerData {\n        title\n        message\n        color\n        link\n        action\n        actionLink\n        tickerType\n        actionBottomSheet {\n          title\n          message\n          reason\n          buttonText\n          buttonLink\n          __typename\n        }\n        __typename\n      }\n      shopCredibility {\n        showOnlineStatus\n        showFollowButton\n        stats {\n          icon\n          value\n          __typename\n        }\n        __typename\n      }\n      partnerLabel\n      __typename\n    }\n    merchantVoucher {\n      vouchers {\n        voucher_id\n        voucher_name\n        voucher_type {\n          voucher_type\n          identifier\n          __typename\n        }\n        voucher_code\n        amount {\n          amount\n          amount_type\n          amount_formatted\n          __typename\n        }\n        minimum_spend\n        valid_thru\n        tnc\n        banner {\n          desktop_url\n          mobile_url\n          __typename\n        }\n        status {\n          status\n          identifier\n          __typename\n        }\n        in_use_expiry\n        __typename\n      }\n      __typename\n    }\n    nearestWarehouse {\n      product_id\n      stock\n      stock_wording\n      price\n      warehouse_info {\n        warehouse_id\n        is_fulfillment\n        district_id\n        postal_code\n        geolocation\n        __typename\n      }\n      __typename\n    }\n    installmentRecommendation {\n      data {\n        term\n        mdr_value\n        mdr_type\n        interest_rate\n        minimum_amount\n        maximum_amount\n        monthly_price\n        os_monthly_price\n        partner_code\n        partner_name\n        partner_icon\n        subtitle\n        __typename\n      }\n      __typename\n    }\n    productWishlistQuery {\n      value\n      __typename\n    }\n    cartRedirection {\n      status\n      error_message\n      data {\n        product_id\n        config_name\n        hide_floating_button\n        available_buttons {\n          text\n          color\n          cart_type\n          onboarding_message\n          show_recommendation\n          __typename\n        }\n        unavailable_buttons\n        __typename\n      }\n      __typename\n    }\n    shopTopChatSpeed {\n      messageResponseTime\n      __typename\n    }\n    shopRatingsQuery {\n      ratingScore\n      __typename\n    }\n    shopPackSpeed {\n      speedFmt\n      hour\n      __typename\n    }\n    ratesEstimate {\n      warehouseID\n      products\n      data {\n        destination\n        title\n        subtitle\n        chipsLabel\n        courierLabel\n        eTAText\n        cheapestShippingPrice\n        fulfillmentData {\n          icon\n          prefix\n          description\n          __typename\n        }\n        errors {\n          code: Code\n          message: Message\n          devMessage: DevMessage\n          __typename\n        }\n        __typename\n      }\n      bottomsheet {\n        title\n        iconURL\n        subtitle\n        buttonCopy\n        __typename\n      }\n      __typename\n    }\n    restrictionInfo {\n      message\n      restrictionData {\n        productID\n        isEligible\n        action {\n          actionType\n          title\n          description\n          attributeName\n          badgeURL\n          buttonText\n          buttonLink\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ticker {\n      tickerInfo {\n        productIDs\n        tickerData {\n          title\n          message\n          color\n          link\n          action\n          actionLink\n          tickerType\n          actionBottomSheet {\n            title\n            message\n            reason\n            buttonText\n            buttonLink\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    navBar {\n      name\n      items {\n        componentName\n        title\n        __typename\n      }\n      __typename\n    }\n    bebasOngkir {\n      products {\n        productID\n        boType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}]
            pos2 = self.r.post(url='https://{}/graphql/PDPGetDataP2'.format(graphql), headers={**self.headers_graphql, 'X-Tkpd-Akamai':'pdpGetData'}, json=data2).json()[0]

            #--> Post 3
            pdp_session = pdp_session.replace('\\','')
            warehouse = pos2.get('data').get('pdpGetData').get('nearestWarehouse')[0].get('warehouse_info')
            data3: list[dict[str,any]] = [{
                "operationName":"ratesEstimateQuery",
                "variables":{"weight":float(re.search(r'"w":(.*?),', str(pdp_session)).group(1)), "domain":str(re.search(r'"sd":"(.*?)"', str(pdp_session)).group(1)), "productId":str(pos1.get('data').get('pdpGetLayout').get('basicInfo').get('id')), "origin":"{}|{}|{}".format(warehouse['district_id'], warehouse['postal_code'], warehouse['geolocation']), "destination":"{}|".format(user_location['districtID']), "POTime":0, "isFulfillment":False, "deviceType":"default_v3", "shopTier":2, "bo_metadata":"", "free_shipping_flag":0, "warehouse_id":str(re.search(r'"wid":(.*?),', str(pdp_session)).group(1))},
                "query":"query ratesEstimateQuery($weight: Float!, $domain: String!, $origin: String, $productId: String, $destination: String, $POTime: Int, $isFulfillment: Boolean, $deviceType: String, $shopTier: Int, $bo_metadata: String, $free_shipping_flag: Int, $warehouse_id: String) {\n  ratesEstimateV3(input: {weight: $weight, domain: $domain, origin: $origin, product_id: $productId, destination: $destination, po_time: $POTime, type: $deviceType, is_fulfillment: $isFulfillment, shop_tier: $shopTier, bo_metadata: $bo_metadata, free_shipping_flag: $free_shipping_flag, warehouse_id: $warehouse_id}) {\n    data {\n      address {\n        city_name\n        province_name\n        district_name\n        country\n        postal_code\n        address\n        lat\n        long\n        phone\n        addr_name\n        address_1\n        receiver_name\n        __typename\n      }\n      shop {\n        district_id\n        district_name\n        postal_code\n        origin\n        addr_street\n        latitude\n        longitude\n        province_id\n        city_id\n        city_name\n        __typename\n      }\n      rates {\n        id\n        rates_id\n        type\n        services {\n          service_name\n          service_id\n          service_order\n          status\n          range_price {\n            min_price\n            max_price\n            __typename\n          }\n          texts {\n            text_service_desc\n            text_service_notes\n            text_range_price\n            text_etd\n            text_price\n            __typename\n          }\n          products {\n            shipper_name\n            shipper_id\n            shipper_product_id\n            shipper_product_name\n            shipper_weight\n            price {\n              price\n              formatted_price\n              __typename\n            }\n            texts {\n              text_etd\n              text_range_price\n              text_eta_summarize\n              __typename\n            }\n            cod {\n              is_cod_available\n              __typename\n            }\n            eta {\n              text_eta\n              error_code\n              __typename\n            }\n            features {\n              dynamic_price {\n                text_label\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          service_based_shipment {\n            is_available\n            text_price\n            text_eta\n            __typename\n          }\n          cod {\n            is_cod\n            cod_text\n            __typename\n          }\n          order_priority {\n            is_now\n            __typename\n          }\n          etd {\n            min_etd\n            max_etd\n            __typename\n          }\n          range_price {\n            min_price\n            max_price\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      texts {\n        text_min_price\n        text_destination\n        text_eta\n        __typename\n      }\n      free_shipping {\n        flag\n        shipping_price\n        eta_text\n        error_code\n        icon_url\n        title\n        __typename\n      }\n      tokocabang_from {\n        title\n        content\n        icon_url\n        __typename\n      }\n      is_blackbox\n      __typename\n    }\n    __typename\n  }\n}\n"}]
            pos3 = self.r.post(url='https://{}/graphql/ratesEstimateQuery'.format(graphql), headers=self.headers_graphql, json=data3).json()[0]

            #--> Get Basic Info
            product_basic = [i['data'][0] for i in pos1['data']['pdpGetLayout']['components'] if i['name']=='product_content'][0]
            discount = int(product_basic.get('campaign').get('percentageAmount'))
            hargs = int(product_basic.get('price').get('value'))
            product_data: dict[str, any] = {
                'id'         : str(product_rate.get('id')),
                'name'       : str(product_basic.get('name')),
                'price'      : hargs,
                'real_price' : int(product_basic.get('campaign').get('originalPrice')) if discount != 0 else int(product_basic.get('price').get('value')),
                'discount'   : discount,
                'stock'      : int(product_basic.get('stock').get('value')),
                'url'        : str(product_rate.get('url')),
                'picture'    : str([i['data'][0]['media'][0]['urlOriginal'] for i in pos1['data']['pdpGetLayout']['components'] if i['name']=='product_media'][0])}

        except: return(product_overall)

        #--> Get Ongkir Info
        try:
            product_estimate = pos3['data']['ratesEstimateV3']['data']['rates']
            ongkir : int = self.ongkir(response=product_estimate['services'])
            waktu  : int = self.waktu(response=product_estimate['services'])
            weight : int = int(product_estimate.get('id').split(':')[-1]) if product_estimate.get('id') else 5
            ongkim : int = ongkir if ongkir else self.countOngkir(weight, product_data['price'])
            product_ongkir: dict[str, any] = {
                'ongkir'      : ongkim,
                'total_price' : hargs + ongkim,
                'waktu'       : waktu if waktu else 5}
        except:
            product_ongkir: dict[str, any] = {'ongkir':200000, 'waktu':7} #--> Gagal Get Ongkir, Naikkan Heuristic

        #--> Get Rating & URL
        try:
            product_rating: dict[str, any] = {
                'review'  : int(product_rate.get('stats').get('countReview')),
                'rating'  : float(product_rate.get('stats').get('rating')),
                'sold'    : int(product_rate.get('txStats').get('countSold'))}
        except:
            product_rating: dict[str, any] = {'review':0, 'rating':0, 'sold':0}

        #--> All Info
        product_overall: dict[str, any] = {
            'status' : 'success',
            **product_data,
            **product_ongkir,
            **product_rating,
        }

        return(product_overall)

    #--> Search Product By Name
    def searchProductByName(self, keyword:str) -> None:

        #--> Post 1
        data1: list[dict[str,any]] = [{
            "operationName":"SearchProductV5Query",
            "variables":{
                "params":"device=desktop&l_name=sre&navsource=&ob=23&page=1&q={}&related=true&rows=60&safe_search=false&scheme=https&shipping=&show_adult=false&source=search&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&start=0&topads_bucket=true&unique_id=18d89f8cb3c0da5b7dd2c1fb75548885&user_id=0&variants=".format(str(keyword).replace(' ','%20'))},
            "query":"query SearchProductV5Query($params: String!) {\n  searchProductV5(params: $params) {\n    header {\n      totalData\n      responseCode\n      keywordProcess\n      keywordIntention\n      componentID\n      isQuerySafe\n      additionalParams\n      backendFilters\n      __typename\n    }\n    data {\n      totalDataText\n      banner {\n        position\n        text\n        applink\n        url\n        imageURL\n        componentID\n        trackingOption\n        __typename\n      }\n      redirection {\n        url\n        __typename\n      }\n      related {\n        relatedKeyword\n        position\n        trackingOption\n        otherRelated {\n          keyword\n          url\n          applink\n          componentID\n          products {\n            id\n            name\n            url\n            applink\n            mediaURL {\n              image\n              __typename\n            }\n            shop {\n              id\n              name\n              city\n              tier\n              __typename\n            }\n            badge {\n              id\n              title\n              url\n              __typename\n            }\n            price {\n              text\n              number\n              __typename\n            }\n            freeShipping {\n              url\n              __typename\n            }\n            labelGroups {\n              position\n              title\n              type\n              url\n              styles {\n                key\n                value\n                __typename\n              }\n              __typename\n            }\n            rating\n            wishlist\n            ads {\n              id\n              productClickURL\n              productViewURL\n              productWishlistURL\n              tag\n              __typename\n            }\n            meta {\n              warehouseID\n              componentID\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      suggestion {\n        currentKeyword\n        suggestion\n        query\n        text\n        componentID\n        trackingOption\n        __typename\n      }\n      ticker {\n        id\n        text\n        query\n        applink\n        componentID\n        trackingOption\n        __typename\n      }\n      violation {\n        headerText\n        descriptionText\n        imageURL\n        ctaURL\n        ctaApplink\n        buttonText\n        buttonType\n        __typename\n      }\n      products {\n        id\n        name\n        url\n        applink\n        mediaURL {\n          image\n          image300\n          videoCustom\n          __typename\n        }\n        shop {\n          id\n          name\n          url\n          city\n          tier\n          __typename\n        }\n        badge {\n          id\n          title\n          url\n          __typename\n        }\n        price {\n          text\n          number\n          range\n          original\n          discountPercentage\n          __typename\n        }\n        freeShipping {\n          url\n          __typename\n        }\n        labelGroups {\n          position\n          title\n          type\n          url\n          styles {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        labelGroupsVariant {\n          title\n          type\n          typeVariant\n          hexColor\n          __typename\n        }\n        category {\n          id\n          name\n          breadcrumb\n          gaKey\n          __typename\n        }\n        rating\n        wishlist\n        ads {\n          id\n          productClickURL\n          productViewURL\n          productWishlistURL\n          tag\n          __typename\n        }\n        meta {\n          parentID\n          warehouseID\n          isImageBlurred\n          isPortrait\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}]
        pos1 = self.r.post(url='https://{}/graphql/RecomWidget'.format(graphql), headers={**self.headers_graphql, 'Tkpd-Userid':'0'}, json=data1).json()[0]
        print(pos1)
        for i in pos1['data']['searchProductV5']['data']['products']:
            product_info = TP.getProductInformation(product_link=i['url'])
            print(product_info)
            print()

    #--> Search Product By Similarity
    def searchProductBySimilarity(self, product_link:str) -> any:

        if 'link' in str(product_link) :
            req = self.r.get(product_link, allow_redirects=True).text.replace('\\','')
            product_link = re.search(r'property="og:url" content="(.*?)\?',str(req)).group(1)

        req = self.r.get(product_link, headers=self.headers_web, allow_redirects=True).text.replace('\\','')
        product_id = re.search(r'"productID":"(.*?)"',str(req)).group(1)

        #--> Post 1
        data1: list[dict[str,any]] = [{
            "operationName":"RecomWidget",
            "variables":{"userID":0, "xDevice":"desktop", "pageName":"pdp_3", "ref":"", "productIDs":product_id},
            "query":"query RecomWidget($userID: Int!, $pageName: String!, $xSource: String!, $xDevice: String!, $productIDs: String, $LayoutPageType: String, $ref: String, $categoryIDs: String, $queryParam: String, $pageNumber: Int!) {\n  productRecommendationWidget(userID: $userID, pageName: $pageName, pageNumber: $pageNumber, xSource: $xSource, xDevice: $xDevice, productIDs: $productIDs, LayoutPageType: $LayoutPageType, ref: $ref, categoryIDs: $categoryIDs, queryParam: $queryParam) {\n    data {\n      tID\n      source\n      title\n      foreignTitle\n      seeMoreUrlLink\n      layoutType\n      pageName\n      widgetUrl\n      pagination {\n        hasNext\n        __typename\n      }\n      recommendation {\n        productSlashedPrice: slashedPrice\n        slashedPriceInt\n        productDiscountPercentage: discountPercentage\n        productReviewCount: countReview\n        isWishlist: isWishlist\n        productImageUrl: imageUrl\n        isTopads\n        clickUrl\n        trackerImageUrl\n        productUrl: url\n        productRating: rating\n        productPrice: price\n        priceInt\n        id\n        productName: name\n        categoryBreadcrumbs\n        recommendationType\n        stock\n        departmentID: departmentId\n        shop {\n          id\n          name\n          location\n          city\n          url\n          __typename\n        }\n        productLabels: labels {\n          title\n          color\n          __typename\n        }\n        labelGroup: labelgroup {\n          type\n          title\n          position\n          url\n          __typename\n        }\n        wholesalePrice {\n          price\n          quantityMax\n          quantityMin\n          priceString\n          __typename\n        }\n        badges {\n          title\n          imageUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    meta {\n      recommendation\n      size\n      failSize\n      processTime\n      experimentVersion\n      __typename\n    }\n    __typename\n  }\n}\n"}]
        pos1 = self.r.post(url='https://{}/graphql/RecomWidget'.format(graphql), headers={**self.headers_graphql, 'Tkpd-Userid':'0'}, json=data1).json()[0]

        list_product_url: list[str] = [product_link] + [i['productUrl'] for i in pos1['data']['productRecommendationWidget']['data'][0]['recommendation']]
        for url in list_product_url:
            try:
                product_info = self.getProductInformation(product_link=url)
                yield product_info
            except:
                continue

if __name__ == '__main__':

    TP = Tokopedia()

    # TP.searchProductByName(keyword='xiaomi curved monitor')
    TP.searchProductBySimilarity(product_link='https://www.tokopedia.com/bandarkomputer/monitor-xiaomi-mi-34-inch-g34wqi-wqhd-ultrawide-180hz-srgb-curved-gaming-monitor')
    TP.searchProductBySimilarity(product_link='https://www.tokopedia.com/arvinndepi/silverqueen-chunky-bar-95-g-halal-mede-almond-mede')
    TP.searchProductBySimilarity(product_link='https://www.tokopedia.com/newtechcomputer/xiaomi-mi-monitor-gaming-30-inch-curved-garansi-resmi')

    # list_url = [
    #     # 'https://www.tokopedia.com/mibo-official/xiaomi-curved-gaming-monitor-34-inch-g34wqi-garansi-resmi',
    #     'https://www.tokopedia.com/gofficial-5/gamen-titan-v-lite-latest-titan-series-mechanical-gaming-keyboard-blue-green-blue-switch-d6226',
    #     'https://www.tokopedia.com/jstoreit/plate-akrilik-fantech-maxfit61-vortexseries-vx5-pro-acrylic-plate-bawah',
    #     'https://www.tokopedia.com/ptnmtindo/nuphy-halo65-wireless-mechanical-keyboard-matte-black-rose-glacier-adaf1',
    # ]
    # for url in list_url:
    #     product_info = TP.getProductInformation(product_link=url)
    #     print(product_info)