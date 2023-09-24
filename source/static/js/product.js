$(document).on('click', '.showPreview', function () {
    
    $('#imagePreviewModal').css({
        'display': 'block'
    });
})
$(document).on('click', '.close-preview', function () {
    $('#imagePreviewModal').css({
        'display': 'none'
    });
});
$(document).ready(function () {
    $('.thumbnail-images').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 3,
        lazyLoad: 'ondemand',
        responsive: [
            {
                breakpoint: 480,
                settings: {
                    centerPadding: '50px',
                    slidesToShow: 2,
                    slidesToScroll: 2,
                }
            }
        ],
        prevArrow: '<img class="rotate180 abs-center-left" src="/static/img/right.svg" alt="">',
        nextArrow: '<img class="abs-center-right" src="/static/img/right.svg" alt="">'
    });
    $('.change-slide-img.active').trigger('click');
    let color = $('.color');
    if(color.length){
        $(function () {
          $('.color').tooltip()
        })
    }
});

let data = JSON.parse($('.product-data').val())
let selected_items = []
$(document).on('click', '.change-data', function () {
    $(this).parent().find('.change-data.active').not(this).removeClass('active')
    $(this).toggleClass('active')
    if ($(this).hasClass('active')){
        selected_items[$(this).attr('data-key')] = $(this).attr('data-value')
    }else{
        delete selected_items[$(this).attr('data-key')]
    }
    changeData()
});
$(document).ready(function(){
    selected_items["color_hex"] = $('.specification-color').first().attr('data-value')
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let entries = urlParams.entries();
    for (const entry of entries) {
        $(".change-data[data-key=" + entry[0] + "][data-value=" + entry[1] + "]").trigger("click")
    }
    changeData()
})
function changeData(){
    let sorted = Object.values(data)
    for (let value in selected_items) {
        sorted = sorted.filter(item => item[value] == selected_items[value]);
    }
    sorted = sorted.sort((a, b) => a.price > b.price)
    let selected_product = sorted[0]
    $(document).find('.change-data').addClass('not-active')
    if (selected_product){
        $('.create_loan').attr('data-spec', selected_product.id)
    }
    let url = window.location.pathname + '?'
    let to_url = []
    let exclude_word = ["images", "is_valid", "price", "quantity", "is_active", "code", "secondary_price", "products", "id"]
    
    for (let specification in sorted) {
        for (let value in sorted[specification]) {
            let active = ''
            if (selected_product[value] == sorted[specification][value]) {
                active = 'active'
            }
            if (sorted[specification][value] != null && !exclude_word.includes(value) && active == "active"){
                to_url[value] = sorted[specification][value]
            }
            $('.change-data.not-active[data-key="' + value + '"][data-value="' + sorted[specification][value] + '"]').removeClass('not-active').addClass(active)
        }
    }
    for (let key in to_url) {
        url += '&' + key + '=' + to_url[key];
    }
    
    window.history.replaceState({}, "", url)
    $(document).find('.change-data.not-active').removeClass('active')
    
    let slider = $('.product-img-slider');
    slider.find('.productSlide').remove();
    $('.thumbnail-images').slick('removeSlide', null, null, true);
    $.each(selected_product.images, function (key, img) {
        let display = '';
        if (key == 0) {
            display = 'active';
        }
        slider.find('.carousel-inner').append(`
            <div class="productSlide carousel-item ` + display + `">
                <img src="/media/` + img + `" class="showPreview" data-target="#imagePreviewModal" data-slide-to="` + key + `">
            </div>
        `);
        slider.find('.thumbnail-images').append(`
            <div class="column cursor" data-target="#productCarousel" data-slide-to="` + key + `">
                <img class="productSlideImg " src="/media/` + img + `">
            </div>
        `);
    });
    $('.toBasket').attr('data-specific', selected_product.id)
    $('.product_specification').val(selected_product.id)
    $('.thumbnail-images')[0].slick.refresh();
    $('.product-price-main span').html(parseFloat(selected_product.price).toFixed(2)).attr('data-price', (selected_product.price).toFixed(2));
    $('.product-price-secondary span').html(parseInt(selected_product.secondary_price)).attr('data-price', selected_product.secondary_price);
    if (parseInt(selected_product.quantity) > 0) {
        $('.product-in-stock').html('Товар в наличии');
        $('.product-in-stock').removeClass('outOfStock');
        $('.toBasketParent').removeClass('d-none');
        $('.createLoanParent').removeClass('d-none').addClass('d-lg-flex d-block');
    } else {
        $('.product-in-stock').html('Нет в наличии');
        $('.product-in-stock').addClass('outOfStock');
        $('.toBasketParent').addClass('d-none');
        $('.createLoanParent').addClass('d-none').removeClass('d-lg-flex d-block');
    }
}