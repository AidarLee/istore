var token = $('input[name="token"]').val();
if (typeof axios !== 'undefined'){
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
}
$(document).on('click','input.remove-por',function(){
    if($(this).val() == '1'){
        $('.place-of-residence').addClass('d-none');
    }else{
        $('.place-of-residence').removeClass('d-none');
    }
});

$(document).on('click','.create_loan',function(){
    let id = $(this).attr('data-id');
    let spec = $(this).attr('data-spec')
    let form = new FormData();
    form.append('product_id', id);
    form.append('product_spec', spec);

    axios.post('/create_loan', form).then(function (resp) {
        window.location.replace("/loan");
    });
});
$(document).on('change','.loan.bank',function(){
    let option =  $(this).find('option[value='+$(this).val()+']');
    let start = parseInt(option.attr('data-start'));
    let end = parseInt(option.attr('data-end'));
    let period = $('.loan.period');
    period.html('')
    for (let i =start ; i <= end; i++) {
        if (i == 1 || i == 21){
            period.append('<option value="'+i+'">'+i+' месяц</option>');
        }
        else if(i<5){
            period.append('<option value="'+i+'">'+i+' месяца</option>');
        } else if (i < 21){
            period.append('<option value="'+i+'">'+i+' месяцев</option>');
        }else{
            period.append('<option value="' + i + '">' + i + ' месяца</option>');
        }
    }
    let bank = $('.loan.bank');
    if(bank.next().hasClass('red-alert')){
        bank.next().remove();
    }
    period.trigger('change');

});

$(document).on('click','.reserve',function(){
    let preview = $('.showPreview')[0];
    $('#reserveProduct .product-img').attr('src', preview.src);
});
$(document).on('change', '.compare-category-select', function () {
    let category = $(this).val();

    if(!category){
        category = '';
    }
    let form = new FormData();
    let first = 0;
    let second = 0;
    let third = 0;
    form.append('category', category);
    axios.post('/compareCategorySelect', form).then(function (resp) {
        $('.for-compare').html(``);
        if (resp.data.products.length < 3){
            resp.data.products[2] = resp.data.products[0]
        }
        $.each(resp.data.products, function (key, product) {
            if (key == 0){
                $('.for-compare[data-id='+1+']').attr('val',product.id)
                first = product.id
            }else if (key == 1){
                $('.for-compare[data-id='+2+']').attr('val',product.id)
                second = product.id
            }else if (key == 2){
                $('.for-compare[data-id='+3+']').attr('val',product.id)
                third = product.id
            }
            $('.for-compare').append(`
            <option class="sf-light" value="` + product.id + `">` + product.name + `</option>
            `);
        });
        let url = '/compare?category='+category;
        if(first){
            url += '&product_first='+ first;
        }
        if(second){
            url += '&product_second='+ second;
        }
        if(third){
            url += '&product_third='+ third;
        }

        window.history.replaceState({}, "",url)
        $('.for-compare').each(function(){
            $(this).val($(this).attr('val')).change();
        });
    });
});
$(document).on('change', '.for-compare', function () {
    let product = $(this).val();
    let compare = $(this).attr('data-id');
    let form = new FormData();
    form.append('product', product);

    let url = new URL(window.location.href);
    params = url.searchParams;

    if(compare == 1){
        params.set('product_first', product);
    }
    if(compare == 2){
        params.set('product_second', product);
    }
    if(compare == 3){
        params.set('product_third', product);
    }
    url.search = params.toString();

    let new_url = url.toString();

    window.history.replaceState({}, "",new_url)

    axios.post('/catalog/getProduct', form).then(function (resp) {
        $('.product-compare[data-id="' + compare + '"]').html(``);
        $('.product-compare-content[data-id="' + compare + '"]').html(``);
        let product = resp.data.product;
        let images = '';
        let product_image = '';
        $.each(resp.data.images, function (key, image) {
            if (key) {
                images += `<div class="color" data-img="` + image.image + `"><img src="` + image.color + `" alt=""></div>`
            } else {
                product_image = image.image;
                images += `<div class="color active"  data-img="` + image.image + `"><img src="` + image.color + `" alt=""></div>`
            }
        });
        $('.product-compare-content .order-' + compare +'').html('')
        $('.product-compare[data-id="' + compare + '"]').append(`
            <div class="img-container">
                <img src="` + product_image + `" class="card-img-top" alt="...">
            </div>
            <div>
                <div class="compare-color">
                    ` + images + `
                </div>
                <a class="link toBasket" data-id="` + product.id + `">
                <a class="link"  href="/catalog/product/` + product.id + `">
                    купить
                    <img src="/static/img/right-arr.svg" alt="">
                </a>
            </div>
        `);
        $.each(resp.data.specific, function (key, specific) {
            let content = $('.product-compare-content .content-'+ key +' .order-'+ compare +'')
            if(!content.length){
                $('.product-compare-content').append(`
                <div class="w-100 h-100 d-flex flex-wrap content-`+ key +`" >
                    <div class="col-lg-4 col-6 text-center px-3 order-1" order-1>
                    </div>
                    <div class="col-lg-4 col-6 text-center px-3 order-2" order-2>
                    </div>
                    <div class="col-lg-4 col-6 d-lg-block d-none text-center px-3 order-3" order-3>
                    </div>
                </div>`);
                content = $('.product-compare-content .content-' + key + ' .order-'+compare+'')
            }
            content.append(`
                <p class="sf-sem specific-title mt-5">` + specific.title + `</p>
                <p class="sf-reg specific-desc word-wrap mt-3">
                    ` + specific.desc + `
                </p>
            `);
        });

    });
});

$(document).on('input', '#page-search', function () {
    let search = $(this);
    $('.search-text-value').html('«' + search.val() + '»');
    let callBackForm = new FormData();
    callBackForm.append('search', search.val());
    axios.post('/mainSearch', callBackForm).then(function (resp) {
        $('.search-first .products-content').html('');
        $('.search-first .articles-content').html('');
        $('.search-count').html(resp.data.products.length + resp.data.articles.length);
        if (resp.data.products.length || resp.data.articles.length) {
            $('.news-and-blog').removeClass('d-none');
            $('.search-first .search-result-emtpy').removeClass('d-flex');
            $('.page-search-result.products').removeClass('d-none');
        } else {
            $('.news-and-blog').addClass('d-none');
            $('.search-first .search-result-emtpy').addClass('d-flex');
        }
        if (resp.data.products.length) {
            $.each(resp.data.products, function (key, product) {
                $('.search-first .products-content').append(`
            <div class="col-lg-6 col-12 mt-4 searched-product-card h-auto">
                <div class="card-img-wrapper d-sm-block d-none">
                    <img src="` + product.image + `" class="card-img" alt="...">
                </div>
                <div class="card-body d-flex flex-column justify-content-between bg-none mt-0 pt-0" style="width:calc(100% - 100px)">
                    <div class="">
                        <h5 class="card-title mb-1 of-ellipsis">` + product.name + `</h5>
                        <p class="card-text mb-1 of-3-ellipsis">
                            ` + product.desc + `
                        </p>
                    </div>
                    <div class="d-flex">
                        <a class="link mr-2" href="/catalog/product/` + product.id + `">
                            подробнее
                            <img src="/static/img/right-arr.svg" alt="">
                        </a>
                    </div>
                </div>
            </div>
            `);
            });
        }
        if (resp.data.articles.length) {
            $.each(resp.data.articles, function (key, article) {
                $('.search-first .articles-content').append(`
                <div class="col-lg-6 col-12 mt-lg-0 mt-2 searched-product-card">
                    <div class="card-body bg-none w-100">
                        <h5 class="card-title of-ellipsis mb-0">` + article.title + `</h5>
                        <p class="card-text mb-1 of-3-ellipsis">` + article.desc + `</p>
                        <a class="link" href="/article/` + article.id + `">
                            подробнее
                            <img src="/static/img/right-arr.svg" alt="">
                        </a>
                    </div>
                </div>
                `);
            });
        } else {
            $('.news-and-blog').addClass('d-none');
        }

    });
})
$('.main-search').keypress(function (e) {
    let key = e.which;
    if (key == 13) {
        let href = $('.goToSearch').attr('href');
        window.location.replace(href);
    }
});
$(document).on('input', '.main-search', function () {
    $("#search-result-with-text").removeClass('d-none');
    let search = $(this);
    $('.goToSearch').attr('href', '/search/' + search.val());
    let callBackForm = new FormData();
    callBackForm.append('search', search.val());
    axios.post('/mainSearch', callBackForm).then(function (resp) {
        $('.search-result .content').html(``);
        $.each(resp.data.products, function (key, product) {
            $('.search-result .content').append(`
            <a href="/catalog/product/` + product.id + `" class="sf-light searching-text of-ellipsis d-block w-100">` + boldString(product.name, search.val()) + `</a>
            `);
        });
    });
});



function boldString(str, substr) {
    let strRegExp = new RegExp(substr, 'i');
    return str.replace(strRegExp, '<span>' + substr + '</span>');
}

$(document).on('click', '.callBack-checkbox input', function () {
    $('.callBack-checkbox').next('.error').remove();
});
$(document).on('click', '.callBack', function () {
    let name = $('.callBack-name');
    let phone = $('.callBack-phone');
    let topic = $('.callBack-topic');
    let desc = $('.callBack-desc');
    let checkbox = $('.callBack-checkbox');
    let error_counter = 0;
    if (phone.val().length < 7 || phone.val().length > 20) {
        if (!phone.next().hasClass('error')) {
            phone.addClass('has-error');
            phone.after('<p class="error">Некорректный номер телефона</p>');
        }
        error_counter += 1;
    }
    if (!name.val()) {
        if (!name.next().hasClass('error')) {
            name.addClass('has-error');
            name.after('<p class="error">Введите имя</p>');
        }
        error_counter += 1;
    }
    if (!topic.val()) {
        if (!topic.next().hasClass('error')) {
            topic.addClass('has-error');
            topic.after('<p class="error">Заполните тему обращения</p>');
        }
        error_counter += 1;
    }
    if (!desc.val()) {
        if (!desc.next().hasClass('error')) {
            desc.addClass('has-error');
            desc.after('<p class="error">Введите описание</p>');
        }
        error_counter += 1;
    }
    if (!checkbox.find('input').is(":checked")) {
        checkbox.after('<p class="error mb-2">Нужно принять пользовательское соглашение</p>')
        error_counter += 1;
    }
    if (!error_counter) {
        let callBackForm = new FormData();
        callBackForm.append('name', name.val());
        callBackForm.append('phone', phone.val());
        callBackForm.append('topic', topic.val());
        callBackForm.append('desc', desc.val());
        axios.post('/callBack', callBackForm).then(function (resp) {
            name.val('');
            phone.val('');
            topic.val('');
            desc.val('');
            callNotifyModal('Успешно', "Заявка отправлена ожидайте ответ");
        });
    }
});
$(document).on('change', '.sort-from-catalog', function () {
    let val = $(this).val();
    let category = $(this).attr('data-by');
    let sortForm = new FormData();
    sortForm.append('val', val);
    sortForm.append('category', category);
    axios.post('catalog/sortFromCatalog', serviceForm).then(function (resp) {
        $('.products-content').html('');
        $.each(resp.data.products, function (key, product) {
            $('.products-content').append(`
                <div class="col-lg-3 col-md-4 col-sm-6 col-12 mt-lg-4 mt-2 recommend-card">
                        <a href="` + product.url + `" class="href">
                            <img src="` + product.image + `" class="card-img-top" alt="...">
                        </a>
                        <div class="card-body bg-none text-center">
                            <a href="` + product.url + `" class="href">
                                <h5 class="card-title mt-2">` + product.name + `</h5>
                            </a>
                            <p class="card-price-usd my-2">` + product.price + ` $</p>
                            <p class="card-price-rub my-2">` + product.converted_price + ` сом</p>
                            <a class="link toBasket" data-id="` + product.id + `">
                                <img src="/static/img/bag.svg" alt="">
                                купить
                            </a>
                        </div>
                </div>
            `);
        });

    });
});
$(document).on('click', ".submitApplication", function () {
    let category = $('.service-card.active').attr('data-category');
    let product = $('.service-product.disabled').html();
    let reason = $('.dropdown-item.service.disabled').html();
    let another = $('.service-area').val();
    let name = $('.callBackClientName').val();
    let phone = $('.callBackClientPhone').val();
    let error = 0
    if (!name) {
        name.addClass('has-error')
        error += 1
    }
    if (!phone || phone.length < 7) {
        phone.addClass('has-error')
        error += 1
    }
    if (!reason) {
        reason = '';
    }
    if (!product) {
        product = '';
    }
    if (!error) {
        $('.submitApplication').addClass('submitApplicationWaiting').removeClass('submitApplication');
        let serviceForm = new FormData();
        serviceForm.append('category', category);
        serviceForm.append('product', product);
        serviceForm.append('reason', reason);
        serviceForm.append('another', another);
        serviceForm.append('name', name);
        serviceForm.append('phone', phone);
        $('#callBack').modal('hide');
        axios.post('serviceCallBack', serviceForm).then(function (resp) {
            $('.submitApplicationWaiting').removeClass('submitApplicationWaiting').addClass('submitApplication');
            callNotifyModal('Успешно', "Заявка отправлена");
        });
    }

});
$(document).on('click', ".service-card", function () {
    let category = $(this).attr('data-category');
    $('.service-card').removeClass('active');
    $(this).addClass('active');
    let serviceForm = new FormData();
    serviceForm.append('category', category);
    axios.post('/getServiceByCategory', serviceForm).then(function (resp) {
        $('.changeCategoryOptions').html('');
        $('.service-select.main').html('Модель вашего ' + resp.data.category);

        $.each(resp.data.services, function (key, val) {
            $('.changeCategoryOptions').append(`
                <a class="dropdown-item service-product"
                                       data-id="` + val.id + `">` + val.name + `</a>
            `);
        });
    });
});
$(document).on('input', '.form-control.has-error', function () {
    $(this).removeClass('has-error');
    $(this).next('.error').remove();
});

$(document).on('click', '.reload-to-profile', function () {
    window.location.replace("/accounts/profile");
});
$(document).on('hidden.bs.modal', '.reload-to-profile', function () {
    window.location.replace("/accounts/profile");
});
$(document).on('keypress', 'input[type="number"]', function (evt) {
    let iKeyCode = (evt.which) ? evt.which : evt.keyCode
    if (iKeyCode != 46 && iKeyCode > 31 && (iKeyCode < 48 || iKeyCode > 57))
        return false;

    return true;
});
$(document).on('input', '.changeInBasket', function () {
    let unique = $(this).attr('data-unique');
    let product = $('.product-' + unique);
    let comment = product.find('.comment').val();
    let quantity = product.find('.quantity').val();
    let start = parseInt(product.find('.start-price').html()) * quantity;
    let converted = parseInt(product.find('.start-converted-price').html()) * quantity;
    product.find('.final-price').html(start);
    product.find('.converted-price').html(converted);
    if (quantity && quantity != "") {
        $('.change-quantity').addClass('.change-quantity-wait');
        let form = new FormData();
        form.append('basket_id', unique);
        form.append('quantity', quantity);
        form.append('comment', comment);
        axios.post('/changeInBasket', form).then(function (resp) {
            $('.change-quantity-wait').addClass('change-quantity').removeClass('change-quantity-wait');
        });
        calcInBasketProducts()
    }
});

function calcInBasketProducts() {
    let final_price = 0;
    let final_converted_price = 0;
    $('.product-in-basket').each(function () {
        final_price += parseInt($(this).find('.final-price').html());
        final_converted_price += parseInt($(this).find('.converted-price').html());
    });
    $('.result-price-usd span').html(final_price);
    $('.result-price-converted span').html(final_converted_price);

};
$('.main-search').on('focus input', function () {
    console.log($(this));
    $('body').addClass('overlay').css({'height':'100vh','overflow':'hidden'});
    $('.search-result').removeClass('d-none');
    $('html').css({'overflow-y':'scroll','height':'100vh'});
});
$('.overlay-wrapper').on('click', function () {
    $('body').removeClass('overlay').css({'height':'auto','overflow':'auto'});
    $('.search-result').addClass('d-none');
})
$(document).on('click', '.color', function () {
    $(this).parent().find('.active').removeClass('active');
    $(this).addClass('active');
    let img = $(this).attr('data-img');
    $(this).parent().parent().parent().find('.card-img-top').attr('src', img);

});

$(document).on('click', '.delete-from-basket', function () {
    $('.delete-from-basket').removeClass('delete-from-basket').addClass('delete-from-basket-wait');
    let unique = $(this).attr('data-unique');
    $('.product-' + unique).remove();
    let form = new FormData();
    form.append('basket_id', unique)
    let quantity = parseInt($('.shop-round').html()) - 1;
    $('.shop-round').html(quantity);
    $('.product-counter').html(quantity);
    if (!quantity) {
        $('.basket-inner').addClass('d-none');
        $('.empty-basket').addClass('d-flex').removeClass('d-none');
        $('.basket-first').removeClass('d-none');
        $('.basket-second').addClass('d-none');
    }

    axios.post('/removeFromBasket', form).then(function (resp) {
        $('.delete-from-basket-wait').addClass('delete-from-basket').removeClass('delete-from-basket-wait');
    }).catch(function (resp) {
        $('.delete-from-basket-wait').addClass('delete-from-basket').removeClass('delete-from-basket-wait');
    });
    calcInBasketProducts()
});
$(document).on('input', '.changeInBasket', function () {
    let unique = $(this).attr('data-unique');
    let quantity = $('.changeInBasket.quantity[data-unique="' + unique + '"]').val();
    let comment = $('.changeInBasket.comment[data-unique="' + unique + '"]').val();
    let form = new FormData();
    form.append('basket_id', unique)
    form.append('quantity', quantity)
    form.append('comment', comment)
    axios.post('/changeInBasket', form).then(function (resp) {
    });
});
$(document).on('click', '.toBasket', function () {
    let product_id = $(this).attr('data-id');
    let specification = $(this).attr('data-specific');
    let quantity = parseInt($('.shop-round').html()) + 1;
    $('.basket-inner').removeClass('d-none');
    $('.empty-basket').removeClass('d-flex').addClass('d-none');
    $('.shop-round').html(quantity);
    $('.product-counter').html(quantity);
    let form = new FormData();
    form.append('product_id', product_id)
    form.append('specification', specification)
    axios.post('/toBasket', form).then(function (resp) {
        let product = resp.data.product;
        callNotifyModal(...Array(5), showBtn=true);

        $('.basket-place').append(`
            <div class="dropdown-item bb-grey rounded-0 d-flex px-0 product-` + product.unique + `">
            <div class="col-3 px-1">
                <img src="` + product.image + `" alt="">
            </div>
            <div class="col-7 px-1">
                <p class="sf-light desc of-ellipsis">
                    ` + product.product_title + `
                </p>
            </div>
            <div class="col-2">
                <a class="delete-from-basket"  data-unique="` + product.unique + `">
                    <img src="/static/img/x-circle.svg" alt="">
                </a>
            </div>
        </div>
        `);
        let products = $('.products-container');
        if (products.length) {
            products.find('.count-element').before(`
                <div class="product-in-basket bb-grey d-flex flex-wrap justify-content-center w-100 my-lg-2 my-4 product-` + product.unique + `">
                        <div class="col-md-4 col-12 pl-0 d-flex align-items-center flex-wrap">
                            <div class="col-md-3 col-12 text-center">
                                <img src="` + product.image + `" alt="" class="product-img">
                            </div>
                            <div class="col-md-9 col-12 mt-md-0 mt-4 text-center">
                                <p class="sf-reg ml-2 of-2-ellipsis">` + product.product_title + `</p>
                            </div>
                        </div>
                        <div class="col-md-2 col-4 mt-md-0 mt-2 d-md-flex d-block align-items-center">
                            <p class="sf-reg d-md-none d-block title changeInBasket">Количество</p>
                            <input type="number" class="form-control mt-0 min-zero-val quantity changeInBasket"
                                   data-unique="` + product.unique + `" value="1" data-max="100">
                        </div>
                        <div class="col-md-2 col-8 mt-md-0 mt-2 d-md-flex d-block align-items-center">
                            <p class="sf-reg d-md-none d-block title comment"
                               >Комментарий</p>
                            <input type="text" class="form-control mt-0 comment changeInBasket" data-unique="` + product.unique + `" value="` + product.comment + `">
                        </div>
                        <div class="col-md-2 col-5 mt-md-0 mt-2 d-flex flex-column justify-content-center">
                            <p class="sf-reg d-md-none d-block title">Цена</p>
                            <p class="sf-medium usd-price w-100">
                                <span class="start-price">$ ` + product.price + `</span></p>
                            <p class="sf-light rub-price">
                                <span class="start-converted-price">` + product.converted + `</span>
                                сом</p>
                        </div>
                        <div class="col-md-2 col-7 mt-md-0 mt-2 d-flex align-items-center pr-0">
                            <div>
                                <p class="sf-reg d-md-none d-block title">К оплате</p>
                                <p class="sf-medium usd-price">
                                    <span class="final-price">$` + product.price + `</span>
                                </p>
                                <p class="sf-light rub-price">
                                    <span class="converted-price">` + product.converted + `</span>
                                    сом</p>
                            </div>
                            <div class="d-flex align-items-center ml-auto mr-4">
                                <a class="c-point delete-from-basket" data-id="` + product.id + `"
                                   data-unique="` + product.unique + `">
                                    <img src="/static/img/x-circle.svg" alt="">
                                </a>
                            </div>
                        </div>
                    </div>
            `);
        }
    });
});
$(document).ready(function () {
    let slider = $('.main-slider-container');
    if (slider.length != 0) {
        $('.main-slider-container').slick({
            infinite: true,
            dots: false,
            slideToShow: 1,
            autoplay: true,
            autoplaySpeed: 6000,
            adaptiveHeight: true,
            lazyLoad: 'ondemand',
            prevArrow: '<img class="rotate180 abs-center-left" src="/static/img/right.svg" alt="">',
            nextArrow: '<img class="abs-center-right" src="/static/img/right.svg" alt="">'
        });
    }
    let date = $('#edit_date');
    if (date.length) {
        var picker = new Litepicker({
            element: document.getElementById('edit_date'),
            lang: 'ru-RU',
            dropdowns: {
                "minYear": 1950, "maxYear": null, "months": true, "years": true
            },
            maxDate: new Date(),
        });
    }
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    $('.nav-icon-opener').click(function () {
        $('.mobileBasket').fadeOut(10);
        $(this).find('#nav-icon').toggleClass('open');

        if ($(this).attr('aria-expanded') == 'false') {
            $('.need-full-height').animate({'height': '200%'}, 450);
        } else {
            $('.need-full-height').animate({'height': '40px'}, 450);
        }
    });
    $('#mobileBasket').on('click', function () {
        if ($('.nav-icon-opener').attr('aria-expanded') == 'true') {
            $('.nav-icon-opener').trigger('click');
        }
        $('.mobileBasket').fadeToggle('slow');
        $('.mobileSearch').fadeOut('slow');
    });
    $('#mobileSearch').on('click', function () {
        $('.mobileSearch').fadeToggle('slow');
        $('.mobileBasket').fadeOut('slow');
    });
    let get_code = $(".getCode");
    let phone = $("#phoneNumber").val();

    if(get_code.length && phone){
        let phoneForm = new FormData();
        phoneForm.append('phone', phone)
        axios.post('/accounts/get_code_time', phoneForm).then(function (resp) {
            if(resp.data.minutes != 0){
                get_code.trigger('click');
            }
        });
    }
    $('#agreement').on('click',function(){
        if($(this).is(':checked')){
            $(this).parent().parent().find('.btn').removeAttr('disabled');
        }else{
            $(this).parent().parent().find('.btn').attr('disabled','');
        }
    });

    if($('.for-compare').length){
        $('.for-compare').each(function(){
            if($(this).attr('val')!='0'){
                $(this).val($(this).attr('val')).change();
            }
        });
    }
});

$('#source-search').on('focus input', function () {
    $('body').addClass('overlay');
    $('#search-result').removeClass('d-none');
});
$('.overlay-wrapper').on('click', function () {
    $('body').removeClass('overlay')
    $('#search-result').addClass('d-none');
})
$(document).on('click', '.click-active .el', function () {
    $(this).parent().find('.el.active').removeClass('active');
    $(this).addClass('active');
});
$('.return-none').on('keydown', function () {
    return false;
});
$('.min-zero-val').on('change', function () {
    let val = $(this).val();
    val = val.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');
    if (!val || val <= 0) {
        $(this).val(1);
    } else {
        $(this).val(parseInt(val));
    }
    let max = parseInt($(this).attr('data-max'));
    if (max && max < val) {
        $(this).val(parseInt(max));
    }
    $(this).trigger('input');
});

$(document).on('click', '.go-back', function () {
    let from_cl = $(this).attr('data-from');
    let to_cl = $(this).attr('data-to');
    $(document).find(from_cl).fadeOut(300, function () {
        $(document).find(to_cl).fadeIn(300);
    });
});
$(document).on('click', '.getCode', function () {
    $('.getCodeSecond').css({ 'display': 'none' })
    let name = $('#nameField').val();
    let password = $('#passwordField').val();
    let phone = $('#phoneNumber').val();
    if (typeof phoneMask !== 'undefined'){
        phone = phoneMask._unmaskedValue;
    }
    if ($(this).hasClass('forget-ps')){
        name = "forget"
        password = "forget123"
    }
    if (!name) {
        $('#nameField').addClass('red-alert');
        $('.register-card .info').addClass('red-alert');
        $('.register-card .info-text').html('Введите Имя');
    } if (!password) {
        $('#passwordField').addClass('red-alert');
        $('.register-card .info').addClass('red-alert');
        $('.register-card .info-text').html('Введите пароль');
    } else if (password.length < 7) {
        $('#passwordField').addClass('red-alert');
        $('.register-card .info').addClass('red-alert');
        $('.register-card .info-text').html('Пароль должен быть больше 8 символов');
    }else if (!phone) {
        $('#phoneNumber').addClass('red-alert');
        $('.register-card .info').addClass('red-alert');
        $('.register-card .info-text').html('Введите номер телефона');
    } else if (phone.length < 7) {
        $('#phoneNumber').addClass('red-alert');
        $('.register-card .info').addClass('red-alert');
        $('.register-card .info-text').html('Некорректный номер телефона');
    } else {
        let phoneForm = new FormData();
        phoneForm.append('phone', phone)
        if ($('#phoneNumber').hasClass('forget')) {
            phoneForm.append('forget', 1);
        } else {
            phoneForm.append('forget', 0);
        }
        
        axios.post('/accounts/set_code', phoneForm).then(function (resp) {
            if (resp.data.status === 'success') {
                $('.getCode').removeClass('getCode').addClass('waitCode');
                $('.register-card .info').removeClass('red-alert');
                $('.info').removeClass('opacity-0');
                $('#phoneNumber').removeClass('red-alert');
                $('.register-card .info-text').html('Повторная отправка доступна через <span class="timer">01:00</span>');
                $('.register-card').fadeOut(300, function () {
                    $('.code-card').fadeIn(300);
                });
                $('.register-card .btn-primary').html('Получить повторно');
                $('.register-card .go-back').removeClass('opacity-0');
                let duration = "01:00";
                let timer2 = "01:00";
                if(resp.data.minutes){
                    duration = "00:" + resp.data.minutes;
                    timer2 = "00:" + resp.data.minutes;
                }
                let interval = setInterval(function () {
                    let timer = duration.split(':');
                    let minutes = parseInt(timer[0], 10);
                    let seconds = parseInt(timer[1], 10);
                    --seconds;
                    minutes = (seconds < 0) ? --minutes : minutes;
                    seconds = (seconds < 0) ? 59 : seconds;
                    seconds = (seconds < 10) ? '0' + seconds : seconds;
                    minutes = (minutes < 10) ? '0' + minutes : minutes;
                    $('.timer').html(minutes + ':' + seconds);
                    if (minutes < 0) clearInterval(interval) 
                    //check if both minutes and seconds are 0
                    if ((seconds <= 0) && (minutes <= 0)) {
                        $('.waitCode').addClass('getCode').removeClass('waitCode');
                        $('.info').addClass('opacity-0');
                        $(document).find('.timer').html("01:00");
                        $('.getCodeSecond').css({ 'display': 'block' })
                        clearInterval(interval);
                    }
                    duration = minutes + ':' + seconds;
                }, 1000);
            } else if (resp.data.status === 'phone_exist') {
                $('#phoneNumber').addClass('red-alert');
                $('.register-card .info').addClass('red-alert');
                $('.register-card .info-text').html('Номер уже существует');
            } else if (resp.data.status === 'phone_not_exist') {
                $('#phoneNumber').addClass('red-alert');
                $('.register-card .info').addClass('red-alert');
                $('.register-card .info-text').html('Номер не найден');
            }

        });

    }

});
$(document).on('input change', '#verifyCode', function () {
    let code = $(this);
    let phone = $('#phoneNumber').val();
    if (typeof phoneMask !== 'undefined') {
        phone = phoneMask._unmaskedValue;
    }
    let phoneForm = new FormData();
    phoneForm.append('phone', phone)
    phoneForm.append('code', code.val())
    axios.post('/accounts/check_code', phoneForm).then(function (resp) {
        if (resp.data.status === 'success') {
            $('.join').removeAttr('disabled');
            $('#newPassword').removeClass('d-none');
            $('.waitCode').addClass('getCode').removeClass('waitCode');
            $('.info').addClass('opacity-0');
            $(document).find('.timer').html("01:00");
            $('.getCodeSecond').css({ 'display': 'none' })
        }
    });
});
$(document).on('click', ".dropdown-item", function () {
    $(this).parent().find('.disabled').removeClass('disabled');
    $(this).addClass('disabled');
    $(this).parent().parent().find('button').html($(this).html());
});

// $('#phoneNumber').on('input', function () {
//     let phone = $(this).val();
//     phone = phone.replace(/[^0-9\.]+/g, "");
//     $(this).val(phone.substring(0, 20));
// });
window.onscroll = function () {
    scrollHeader()
};

function scrollHeader() {
    if ($(window).width() > 990) {
        if (window.pageYOffset >= 40) {
            $(".nav-wrapper").addClass("hide-to-top");
        } else {
            $(".nav-wrapper").removeClass("hide-to-top");
            $('.overlay-wrapper').trigger('click');
        }
    }

}

function callNotifyModal(title = 'Успешно', desc = "Товар добавлен", btnClass = '', modalClass = '', img = '/static/img/green-mark.svg',showBtn=false) {
    if(showBtn){
        $('#notifyShow .only-continue').addClass('d-none');
        $('#notifyShow .continue-and-checkout').removeClass('d-none');
    }else{
        $('#notifyShow .only-continue').removeClass('d-none');
        $('#notifyShow .continue-and-checkout').addClass('d-none');
    }

    $('#notifyShow .notify-status').attr('src', img);
    $('#notifyShow .notify-title').html(title);
    $('#notifyShow .notify-desc').html(desc);
    $('#notifyShow .btn-primary').addClass(btnClass);
    $('#notifyShow').addClass(modalClass);
    $('#notifyShow').modal();
}


$(function () {
    $('li.nav-item a:not(.custom)').each(function () {
        var location =  window.location.href.split('?')[0];
        var link = this.href;
        if (location == link) {
            $(this).addClass('activs');
            $(this).parent().find('img').addClass('activs2');

        }
    });
});
$('#vid').on('ended', function(){
    this.playedThrough = true;
});

let video = $('#vid');
if(video.length){
    $(window).scroll(function(){
    var myVideo = document.getElementById("vid");
    if($(window).scrollTop() > 2100){
       if(!myVideo.playedThrough)
          myVideo.play();
    }
})
}
$(document).on('change', 'input[type=file]', function () {
    $(this).parent().find('.js-fileName').append('<i class="fas fa-check"></i>')
})
setTimeout(() => {
    $.getScript("//code.jivosite.com/widget/Dj8JPnwdXL");
}, 2000);


if (typeof AppleID !== 'undefined') {
    AppleID.auth.init({
        clientId: 'istore.kg',
        scope: 'name email',
        redirectURI: 'https://istore.kg/accounts/login_apple_resp',
        state: '[STATE]',
        // usePopup: true //or false defaults to false
    });
}

$('#appleid').on('click', function () {
    $('#appleid-signin').trigger('click')
});
var element = document.getElementById("phoneNumber")
var phoneMask = IMask(element, {
    mask: '{996}000000000',
    lazy: false,
});
let mask = {
    "1": '{996}000000000',
    "2": '{7}0000000000',
    "3": '{7}0000000000',
    "4": '{1}0000000000',
    "5": '{49}00000000',
    "6": '{90}00000000000',
    "7": '0000000000000',
}
$("#country").on("change", function () {
    phoneMask.updateOptions({
        mask: mask[$(this).val()],
        lazy: false,
    });
});