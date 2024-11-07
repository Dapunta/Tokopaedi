const domain = 'www.tokopedia.com';
const graphql = 'gql.tokopedia.com';

let productData, productOngkir, productRating;
let pos1, pos2, pos3, productRate;

class Tokopedia {
    constructor() {
        this.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Origin": `https://${domain}`
        };
    }

    // Get Product
    async productQuery(productLink) {
        const response = await fetch(productLink, { headers: this.headers });
        const redirectedUrl = response.url;
        const urlParts = redirectedUrl.split('/');
        return { shopDomain: urlParts[3], productKey: urlParts[4] };
    }

    // Get Product Information
    async info(productLink) {
        let productOverall = { status: 'failed' };
        const userLocation = { districtID: "3526" }; // Surabaya

        try {
            const productQuery = await this.productQuery(productLink);

            // Post 1
            const data1 = [{
                operationName: "PDPGetLayoutQuery",
                variables: {
                    shopDomain: productQuery.shopDomain,
                    productKey: productQuery.productKey,
                    apiVersion: 1,
                    extParam: "ivf%3Dfalse"
                },
                query:`fragment ProductVariant on pdpDataProductVariant {  errorCode  parentID  defaultChild  sizeChart  totalStockFmt  variants {    productVariantID    variantID    name    identifier    option {      picture {        urlOriginal: url        urlThumbnail: url100        __typename      }      productVariantOptionID      variantUnitValueID      value      hex      stock      __typename    }    __typename  }  children {    productID    price    priceFmt    slashPriceFmt    discPercentage    optionID    optionName    productName    productURL    picture {      urlOriginal: url      urlThumbnail: url100      __typename    }    stock {      stock      isBuyable      stockWordingHTML      minimumOrder      maximumOrder      __typename    }    isCOD    isWishlist    campaignInfo {      campaignID      campaignType      campaignTypeName      campaignIdentifier      background      discountPercentage      originalPrice      discountPrice      stock      stockSoldPercentage      startDate      endDate      endDateUnix      appLinks      isAppsOnly      isActive      hideGimmick      isCheckImei      minOrder      showStockBar      __typename    }    thematicCampaign {      additionalInfo      background      campaignName      icon      __typename    }    __typename  }  __typename}fragment ProductMedia on pdpDataProductMedia {  media {    type    urlOriginal: URLOriginal    urlThumbnail: URLThumbnail    urlMaxRes: URLMaxRes    videoUrl: videoURLAndroid    prefix    suffix    description    variantOptionID    __typename  }  videos {    source    url    __typename  }  __typename}fragment ProductCategoryCarousel on pdpDataCategoryCarousel {  linkText  titleCarousel  applink  list {    categoryID    icon    title    isApplink    applink    __typename  }  __typename}fragment ProductHighlight on pdpDataProductContent {  name  price {    value    currency    priceFmt    slashPriceFmt    discPercentage    __typename  }  campaign {    campaignID    campaignType    campaignTypeName    campaignIdentifier    background    percentageAmount    originalPrice    discountedPrice    originalStock    stock    stockSoldPercentage    threshold    startDate    endDate    endDateUnix    appLinks    isAppsOnly    isActive    hideGimmick    showStockBar    __typename  }  thematicCampaign {    additionalInfo    background    campaignName    icon    __typename  }  stock {    useStock    value    stockWording    __typename  }  variant {    isVariant    parentID    __typename  }  wholesale {    minQty    price {      value      currency      __typename    }    __typename  }  isCashback {    percentage    __typename  }  isTradeIn  isOS  isPowerMerchant  isWishlist  isCOD  preorder {    duration    timeUnit    isActive    preorderInDays    __typename  }  __typename}fragment ProductCustomInfo on pdpDataCustomInfo {  icon  title  isApplink  applink  separator  description  __typename}fragment ProductInfo on pdpDataProductInfo {  row  content {    title    subtitle    applink    __typename  }  __typename}fragment ProductDetail on pdpDataProductDetail {  content {    title    subtitle    applink    showAtFront    isAnnotation    __typename  }  __typename}fragment ProductDataInfo on pdpDataInfo {  icon  title  isApplink  applink  content {    icon    text    __typename  }  __typename}fragment ProductSocial on pdpDataSocialProof {  row  content {    icon    title    subtitle    applink    type    rating    __typename  }  __typename}fragment ProductDetailMediaComponent on pdpDataProductDetailMediaComponent {  title  description  contentMedia {    url    ratio    type    __typename  }  show  ctaText  __typename}query PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {  pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {    requestID    name    pdpSession    basicInfo {      alias      createdAt      isQA      id: productID      shopID      shopName      minOrder      maxOrder      weight      weightUnit      condition      status      url      needPrescription      catalogID      isLeasing      isBlacklisted      isTokoNow      menu {        id        name        url        __typename      }      category {        id        name        title        breadcrumbURL        isAdult        isKyc        minAge        detail {          id          name          breadcrumbURL          isAdult          __typename        }        __typename      }      txStats {        transactionSuccess        transactionReject        countSold        paymentVerified        itemSoldFmt        __typename      }      stats {        countView        countReview        countTalk        rating        __typename      }      __typename    }    components {      name      type      position      data {        ...ProductMedia        ...ProductHighlight        ...ProductInfo        ...ProductDetail        ...ProductSocial        ...ProductDataInfo        ...ProductCustomInfo        ...ProductVariant        ...ProductCategoryCarousel        ...ProductDetailMediaComponent        __typename      }      __typename    }    __typename  }}`
            }];
            const response1 = await fetch(`https://${graphql}/graphql/RecomWidget`, {
                method: 'POST',
                headers: { ...this.headers, 'X-Tkpd-Akamai': 'pdpGetLayout', 'Content-Type': 'application/json' },
                body: JSON.stringify(data1)
            });
            const pos1 = await response1.json();
            const pdpSession = (pos1[0]['data']['pdpGetLayout']['pdpSession']).replace(/\\/g, '');
            productRate = pos1[0]['data']['pdpGetLayout']['basicInfo'];

            // Post 2
            const data2 = [{
                operationName: "PDPGetDataP2",
                variables: {
                    affiliate: null,
                    productID: String(productRate.id),
                    pdpSession: pdpSession,
                    userLocation: userLocation
                },
                query:`query PDPGetDataP2($productID: String!, $pdpSession: String!, $deviceID: String, $userLocation: pdpUserLocation, $affiliate: pdpAffiliate) {  pdpGetData(productID: $productID, pdpSession: $pdpSession, deviceID: $deviceID, userLocation: $userLocation, affiliate: $affiliate) {    error {      Code      Message      DevMessage      __typename    }    callsError {      shopInfo {        Code        Message        __typename      }      cartRedirection {        Code        Message        __typename      }      nearestWarehouse {        Code        Message        __typename      }      __typename    }    productView    wishlistCount    shopFinishRate {      finishRate      __typename    }    shopInfo {      shopTier      badgeURL      closedInfo {        closedNote        reason        detail {          openDate          __typename        }        __typename      }      isOpen      favoriteData {        totalFavorite        alreadyFavorited        __typename      }      activeProduct      createInfo {        epochShopCreated        __typename      }      shopAssets {        avatar        __typename      }      shopCore {        domain        shopID        name        shopScore        url        ownerID        __typename      }      shopLastActive      location      statusInfo {        statusMessage        shopStatus        isIdle        __typename      }      isAllowManage      isOwner      ownerInfo {        id        __typename      }      isCOD      shopType      tickerData {        title        message        color        link        action        actionLink        tickerType        actionBottomSheet {          title          message          reason          buttonText          buttonLink          __typename        }        __typename      }      shopCredibility {        showOnlineStatus        showFollowButton        stats {          icon          value          __typename        }        __typename      }      partnerLabel      __typename    }    merchantVoucher {      vouchers {        voucher_id        voucher_name        voucher_type {          voucher_type          identifier          __typename        }        voucher_code        amount {          amount          amount_type          amount_formatted          __typename        }        minimum_spend        valid_thru        tnc        banner {          desktop_url          mobile_url          __typename        }        status {          status          identifier          __typename        }        in_use_expiry        __typename      }      __typename    }    nearestWarehouse {      product_id      stock      stock_wording      price      warehouse_info {        warehouse_id        is_fulfillment        district_id        postal_code        geolocation        __typename      }      __typename    }    installmentRecommendation {      data {        term        mdr_value        mdr_type        interest_rate        minimum_amount        maximum_amount        monthly_price        os_monthly_price        partner_code        partner_name        partner_icon        subtitle        __typename      }      __typename    }    productWishlistQuery {      value      __typename    }    cartRedirection {      status      error_message      data {        product_id        config_name        hide_floating_button        available_buttons {          text          color          cart_type          onboarding_message          show_recommendation          __typename        }        unavailable_buttons        __typename      }      __typename    }    shopTopChatSpeed {      messageResponseTime      __typename    }    shopRatingsQuery {      ratingScore      __typename    }    shopPackSpeed {      speedFmt      hour      __typename    }    ratesEstimate {      warehouseID      products      data {        destination        title        subtitle        chipsLabel        courierLabel        eTAText        cheapestShippingPrice        fulfillmentData {          icon          prefix          description          __typename        }        errors {          code: Code          message: Message          devMessage: DevMessage          __typename        }        __typename      }      bottomsheet {        title        iconURL        subtitle        buttonCopy        __typename      }      __typename    }    restrictionInfo {      message      restrictionData {        productID        isEligible        action {          actionType          title          description          attributeName          badgeURL          buttonText          buttonLink          __typename        }        __typename      }      __typename    }    ticker {      tickerInfo {        productIDs        tickerData {          title          message          color          link          action          actionLink          tickerType          actionBottomSheet {            title            message            reason            buttonText            buttonLink            __typename          }          __typename        }        __typename      }      __typename    }    navBar {      name      items {        componentName        title        __typename      }      __typename    }    bebasOngkir {      products {        productID        boType        __typename      }      __typename    }    __typename  }}`
            }];

            const response2 = await fetch(`https://${graphql}/graphql/PDPGetDataP2`, {
                method: 'POST',
                headers: { ...this.headers, 'X-Tkpd-Akamai': 'pdpGetData', 'Content-Type': 'application/json' },
                body: JSON.stringify(data2)
            });
            const pos2 = await response2.json();

            // Post 3
            const warehouse = pos2[0]['data']['pdpGetData']['nearestWarehouse'][0]['warehouse_info'];
            const weight = parseFloat(pdpSession.match(/"w":(.*?),/)[1]);
            const domainMatch = pdpSession.match(/"sd":"(.*?)"/)[1];
            const warehouseId = pdpSession.match(/"wid":(.*?),/)[1];
            const data3 = [{
                operationName: "ratesEstimateQuery",
                variables: {
                    weight: weight,
                    domain: domainMatch,
                    productId: String(productRate.id),
                    origin: `${warehouse.district_id}|${warehouse.postal_code}|${warehouse.geolocation}`,
                    destination: `${userLocation.districtID}|`,
                    POTime: 0,
                    isFulfillment: false,
                    deviceType: "default_v3",
                    shopTier: 2,
                    bo_metadata: "",
                    free_shipping_flag: 0,
                    warehouse_id: warehouseId
                },
                query:`query ratesEstimateQuery($weight: Float!, $domain: String!, $origin: String, $productId: String, $destination: String, $POTime: Int, $isFulfillment: Boolean, $deviceType: String, $shopTier: Int, $bo_metadata: String, $free_shipping_flag: Int, $warehouse_id: String) {  ratesEstimateV3(input: {weight: $weight, domain: $domain, origin: $origin, product_id: $productId, destination: $destination, po_time: $POTime, type: $deviceType, is_fulfillment: $isFulfillment, shop_tier: $shopTier, bo_metadata: $bo_metadata, free_shipping_flag: $free_shipping_flag, warehouse_id: $warehouse_id}) {    data {      address {        city_name        province_name        district_name        country        postal_code        address        lat        long        phone        addr_name        address_1        receiver_name        __typename      }      shop {        district_id        district_name        postal_code        origin        addr_street        latitude        longitude        province_id        city_id        city_name        __typename      }      rates {        id        rates_id        type        services {          service_name          service_id          service_order          status          range_price {            min_price            max_price            __typename          }          texts {            text_service_desc            text_service_notes            text_range_price            text_etd            text_price            __typename          }          products {            shipper_name            shipper_id            shipper_product_id            shipper_product_name            shipper_weight            price {              price              formatted_price              __typename            }            texts {              text_etd              text_range_price              text_eta_summarize              __typename            }            cod {              is_cod_available              __typename            }            eta {              text_eta              error_code              __typename            }            features {              dynamic_price {                text_label                __typename              }              __typename            }            __typename          }          service_based_shipment {            is_available            text_price            text_eta            __typename          }          cod {            is_cod            cod_text            __typename          }          order_priority {            is_now            __typename          }          etd {            min_etd            max_etd            __typename          }          range_price {            min_price            max_price            __typename          }          __typename        }        __typename      }      texts {        text_min_price        text_destination        text_eta        __typename      }      free_shipping {        flag        shipping_price        eta_text        error_code        icon_url        title        __typename      }      tokocabang_from {        title        content        icon_url        __typename      }      is_blackbox      __typename    }    __typename  }}`
            }];

            const response3 = await fetch(`https://${graphql}/graphql/ratesEstimateQuery`, {
                method: 'POST',
                headers: { ...this.headers, 'Content-Type': 'application/json' },
                body: JSON.stringify(data3)
            });
            pos3 = await response3.json();

            // Get Basic Info
            const productBasic = pos1[0]['data']['pdpGetLayout']['components'].find(component => component.name === 'product_content').data[0];
            const discount = parseInt(productBasic.campaign.percentageAmount);
            productData = {
                name: productBasic.name,
                price: parseInt(productBasic.price.value),
                real_price: discount !== 0 ? parseInt(productBasic.campaign.originalPrice) : parseInt(productBasic.price.value),
                discount: discount,
                stock: parseInt(productBasic.stock.value),
                url: productRate.url,
                picture: pos1[0]['data']['pdpGetLayout']['components'].find(component => component.name === 'product_media').data[0].media[0].urlOriginal
            };
        }

        catch (error) {
            return productOverall;
        }

        // Get Ongkir Info
        try {
            const productEstimate = pos3[0]['data']['ratesEstimateV3']['data']['rates']['services'][0];
            productOngkir = {
                ongkir: parseInt(productEstimate.range_price.min_price),
                waktu: productEstimate.texts.text_etd !== '' ? parseInt(productEstimate.texts.text_etd.match(/(\d+) hari/)[1]) : 5
            };
        }
        catch {
            productOngkir = { ongkir:20000, waktu:5 };
        }

        // Get Rating & URL
        try {
            productRating = {
                review: parseInt(productRate.stats.countReview),
                rating: parseFloat(productRate.stats.rating),
                sold: parseInt(productRate.txStats.countSold)
            };
        }
        catch {
            productRating = { review:0, rating:0, sold:0 };
        }

        // All Info
        productOverall = {
            status: 'success',
            ...productData,
            ...productOngkir,
            ...productRating
        };

        return productOverall;
        
    }
}

async function main() {
    const TP = new Tokopedia();
    try {
        const productInfo1 = await TP.info('https://www.tokopedia.com/gofficial-5/gamen-titan-v-lite-latest-titan-series-mechanical-gaming-keyboard-blue-green-blue-switch-d6226');
        console.log(productInfo1);
        const productInfo2 = await TP.info('https://www.tokopedia.com/redragon/redragon-mechanical-gaming-keyboard-60-black-fizz-k617rgb');
        console.log(productInfo2);
        const productInfo3 = await TP.info('https://www.tokopedia.com/ptnmtindo/nuphy-halo65-wireless-mechanical-keyboard-matte-black-rose-glacier-adaf1');
        console.log(productInfo3);
    } catch (error) {
        console.error('Error fetching product info:', error);
    }
}

main();