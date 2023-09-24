$('.country').on('change', function(){
    console.log($(this).val());
    if($(this).val()=='Кыргызстан'){
        $('.delivery-cost').html('Бесплатно');
        $('#cash').removeAttr('disabled').parent().removeClass('disabled');
        $('#payment_to_the_courier').removeAttr('disabled').parent().removeClass('disabled');
        $('#elsom').removeAttr('disabled').parent().removeClass('disabled');
    }else{
        $('.delivery-cost').html('1000 сом');
        $('#cash').attr('disabled','disabled').parent().addClass('disabled');
        $('#payment_to_the_courier').attr('disabled','disabled').parent().addClass('disabled');
        $('#elsom').attr('disabled','disabled').parent().addClass('disabled');

        if($('#cash').is(':checked') || $('#payment_to_the_courier').is(':checked') || $('#elsom').is(':checked')){
            $('#visa').trigger('click');
        }
    }
    $('.payment-option:checked').trigger('click');
});
$(document).on('click','.delivery-option',function(){
    let btn = $(this).attr('data-id');
    if(btn=='1'){
        $('.checkout-second .pickup').removeClass('d-none');
        $('.checkout-second .express-delivery').addClass('d-none');
        $('.country').val('Кыргызстан');
        $('.payment-option:checked').trigger('click');
    }else{
        $('.checkout-second .pickup').addClass('d-none');
        $('.checkout-second .express-delivery').removeClass('d-none');
    }
});
$(document).on('input', '#promoSearch', function () {
    let search = $(this);
    let main = $('.checkout-price');
    let converted = $('.checkout-converted-price');
    let form = new FormData();
    form.append('codeword', search.val());
    axios.post('/promoSearch', form).then(function (resp) {
        if (resp.data.status == "success") {
            let promo = resp.data.promo
            let percent = parseInt(resp.data.percent)
            $('.promo-code-area').attr('data-percent', percent);
            $('.promo-code-area').removeClass('d-none').html(promo + ' ' + percent + '%');
            let price = parseFloat(main.attr('data-price'))
            price = Math.round(price - (price * (percent / 100)))
            main.html(price).attr('data-price-with-promo',price)
            price = parseFloat(converted.attr('data-price'))
            price = Math.round(price - (price * (percent / 100)))
            converted.html(price).attr('data-price-with-promo', price)
        } else {
            $('.promo-code-area').addClass('d-none').html('');
            main.html(main.attr('data-price')).attr('data-price-with-promo', main.attr('data-price'))
            converted.html(converted.attr('data-price')).attr('data-price-with-promo', converted.attr('data-price'))
        }
        $('.payment-option:checked').trigger('click');
    });
});
$('.payment-option').on('click', function () {
    let percent = 2;
    let main = $('.checkout-price');
    let country = $('.country').val();
    let converted = $('.checkout-converted-price');
    let delivery_price = 0
    if (country == 'Казахстан'){
        delivery_price = 1000;
    }
    let delivery = Math.round(delivery_price / parseInt($('.currency').val()));
    let price = parseFloat(main.attr('data-price-with-promo'))
    if($(this).attr('id')=='visa'){
        main.html(Math.round(price + (price * (percent / 100))) + delivery)
        price = parseFloat(converted.attr('data-price-with-promo'))
        converted.html(Math.round(price + (price * (percent / 100))) + delivery_price)
    }else{
        main.html(price + delivery)
        price = parseFloat(converted.attr('data-price-with-promo'))
        converted.html(price + delivery_price)
    }
});
$('#promoSearch').trigger('input');
$('.delivery-option').trigger('click');
$('.country').trigger('change');

$('.confirm-btn').on('click', function () {
    let name = $('.register-name');
    let second_name = $('.register-second-name');
    let email = $('.register-email');
    let phone = $('.register-phone');
    let auth_phone = $('.auth-phone');
    let empty_phone = $('.empty-phone');
    let password = $('.auth-password');
    let error_counter = 0;
    let delivery = $('.delivery-option:checked');
    let payment = $('.payment-option:checked').val();
    let promo = $('.promo').val();
    let user_tab = $('#new-user');
    let address = $('.express-delivery .address');
    let country = $('.express-delivery .country');
    let modules = $('.main-btn.toBasket').attr('data-modules');
    let comment = $('.comment');
    if (user_tab.length) {
        if (user_tab.hasClass('show')) {
            if (phone.val().length < 7 || phone.val().length > 20) {
                if (!phone.next().length) {
                    phone.addClass('has-error')
                    phone.after('<p class="error">Некорректный номер телефона</p>')
                }
                error_counter += 1;
            }
            if (email.val() && !(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.val()))) {
                if (email.after().length) {
                    email.addClass('has-error')
                    email.after('<p class="error">Некорректный email</p>')
                }
                error_counter += 1;
            }
        } else {
            if (auth_phone.val().length < 7 || auth_phone.val().length > 20) {
                if (!auth_phone.next().length) {
                    auth_phone.addClass('has-error')
                    auth_phone.after('<p class="error">Некорректный номер телефона</p>')
                }
                error_counter += 1;
            }
            if (password.val().length < 7) {
                if (!password.next().length) {
                    password.addClass('has-error')
                    password.after('<p class="error">Неверный пароль</p>')
                }
                error_counter += 1;
            }
        }
    }
    if (empty_phone.length){
        if (empty_phone.val().length < 7 || empty_phone.val().length > 20) {
            if (!empty_phone.next().length) {
                empty_phone.addClass('has-error')
                empty_phone.after('<p class="error">Некорректный номер телефона</p>')
            }
            error_counter += 1;
        }
        phone = empty_phone
    }
    if(delivery.attr('data-id')=='2' && !address.val().length){
        if (!address.next().length) {
            address.addClass('has-error')
            address.after('<p class="error">Введите адрес</p>')
        }
        error_counter += 1;
    }
    
    if (!error_counter) {
        let authForm = new FormData();
        authForm.append('name', name.val())
        authForm.append('second_name', second_name.val())
        authForm.append('email', email.val())
        authForm.append('phone', phone.val())
        authForm.append('auth_phone', auth_phone.val())
        authForm.append('password', password.val())
        authForm.append('delivery', delivery.val())
        authForm.append('payment', payment)
        authForm.append('promo', promo)
        authForm.append('address', address.val())
        authForm.append('country', country.val())
        authForm.append('comment', comment.val())
        authForm.append('auth', user_tab.hasClass('show'))
        authForm.append('modules', modules)
        $('.section.bouncy').removeClass('d-none');
        axios.post('makeOrder', authForm).then(function (resp) {
            if (resp.data.status === 'phone_exist') {
                phone.trigger('input')
                phone.addClass('has-error')
                phone.after('<p class="error">Пользователь с таким номером уже существует</p>')
            } else if (resp.data.status === 'user_not_found') {
                auth_phone.trigger('input')
                auth_phone.addClass('has-error')
                auth_phone.after('<p class="error">Пользователь не найден</p>')
            } else if (resp.data.status === 'password_not_match') {
                password.trigger('input')
                password.addClass('has-error')
                password.after('<p class="error">Неверный пароль</p>')
            } else if (resp.data.status === 'success') {
                if(resp.data.check == 1){
                    console.log(resp.data);
                    window.location.replace(resp.data.url);
                }else{
                    window.location.replace(resp.data.url);
                }
            }
            
            $('.section.bouncy').addClass('d-none');
        });
    }else{
        let el = $('.form-control.has-error').first()
        if (el) {
            $('html, body').animate({
                scrollTop: el.offset().top - 200
            }, 500);
        }
    }
});

