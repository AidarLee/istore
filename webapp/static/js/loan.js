$(document).ready(function(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.get('option')){
        $(".choose-bank-option.loan").val(urlParams.get('option')).trigger('change')
    }
    if (urlParams.get('bank')) {
        $(".choose-bank.loan").val(urlParams.get('bank')).trigger('change')
    }
    
    
    setTimeout(() => {
        if (urlParams.get('period')) {
            $(".choose-period.loan").val(urlParams.get('period'))
        }
        if (urlParams.get('fee')) {
            $(".initial-fee.loan").val(urlParams.get('fee')).trigger('change')
        }
        calcLoan()
    }, 300);
})
function calcLoan(){
    let choosenProducts = []
    let url = window.location.pathname + '?'

    let ids = []
    let specs = []
    $('.loan-product .loan-result').each(function (index) {
        let id = $(this).attr('data-id');
        let spec = $(this).attr('data-spec');
        choosenProducts[index] = { id, spec };
        ids.push(id)
        specs.push(spec)
    });
    
    url += '&id=' + ids
    url += '&spec=' + specs

    
    $('#productsForPurchase').val(JSON.stringify(choosenProducts));
    let products = $(document).find('.product-converted-price')
    let price = 0
    products.each(function () {
        price += Number($(this).attr('data-price'));
    });
    let start_price = makeFloat($('.credit-start-end-price').attr('start'))
    let end_price = makeFloat($('.credit-start-end-price').attr('end'))

    $('.purchase-on-credit').removeAttr('disabled')
    $('.hint-for-disable').addClass('d-none')
    let products_price = price;
    let period = $('.choose-period');
    if (period.val() == 1 || period.val() == 21) {
        $('.credit-period').html(period.val() + ' месяц');
    } else if (period.val() < 5) {
        $('.credit-period').html(period.val() + ' месяца');
    } else if (period.val() < 21) {
        $('.credit-period').html(period.val() + ' месяцев');
    } else {
        $('.credit-period').html(period.val() + ' месяца');
    }
    let percents = JSON.parse($('.percent').attr('data-percents'));

    let last_item = 0;
    let changed = 0;
    $.each(percents, function (key, percent) {
        last_item = key;
        if (parseInt(key) >= price) {
            $('.percent').attr('data-percent', percent).attr('placeholder', percent + '%');
            changed = 1;
            return false;
        }
    });

    if (changed != 1) {
        $('.percent').attr('data-percent', percents[last_item]).attr('placeholder', percents[last_item] + '%');
    }
    let percent = makeFloat($('.percent').attr('data-percent'));
    calcFee()
    let fee_custom = makeFloat($('.initial-fee').val());
    if (fee_custom){
        price -= fee_custom 
    }else{
        fee_custom = 0
    }
    $('.credit-all-sum').html(price + ' сом');
    $('.credit-initial-fee').html(fee_custom + ' сом');
    if (price < start_price){
        notCorrectValue(products_price, price)
    }else{
        $('.purchase-on-credit').removeAttr('disabled')
        let whole_price = price;
        let pl = percent / 12 / 100
        let period_val = parseInt(period.val())
        let k = pl * Math.pow(1 + pl, period_val) / (Math.pow(1 + pl, period_val) - 1);
        let per_month = parseFloat(k * price).toFixed(2);
        let whole_interest = 0;
        for (i = 0; i < period_val; i++) {
            let interest = pl * whole_price
            whole_interest += interest;
            whole_price -= per_month - interest;
        }
        per_month = Math.round(per_month)
        price = Math.round(price + whole_interest + fee_custom)
        if (!per_month) {
            per_month = 0
        }
        if (!price) {
            price = 0
        }
        $('.credit-per-month-payment').html(per_month + ' сом');
        $('.credit-result').html(price + ' сом');
        $('.markup-result').html((price - products_price) + 'сом')
        $('.product-all-result').html(price - (price - products_price) + 'сом')

        
        url += '&option=' + $(".choose-bank-option.loan").val()
        url += '&bank=' + $(".choose-bank.loan").val()
        url += '&period=' + $(".choose-period.loan").val()
        url += '&fee=' + $(".initial-fee.loan").val()
        window.history.replaceState({}, "", url)
    }
        
};
function notCorrectValue(products_price, price){
    $('.credit-per-month-payment').html('');
    $('.credit-result').html(products_price + 'сом');
    $('.product-all-result').html(price + 'сом');
    $('.markup-result').html('')
    $('.purchase-on-credit').attr('disabled', true)
    $('.hint-for-disable').removeClass('d-none')
    
}
function  calcFee() {
    let fee = makeFloat($('.initial-fee').attr('data-fee'))
    let fee_custom = makeFloat($('.initial-fee').val())
    let before = makeFloat($('.initial-fee').attr('data-before'));
    let end_price = makeFloat($('.credit-start-end-price').attr('end'))
    let price = 0

    $('.product-converted-price').each(function () {
        price += Number($(this).attr('data-price'));
    });

    let fee_price = 0
    if (price > before) {
        fee_price = price * (fee / 100)
    }

    if (fee_price < fee_custom) {
        fee_price = fee_custom
    }

    if(fee_price > price){
        fee_price = price
    }

    if (price > end_price){
        fee_price = end_price * 0.1 + (price - end_price)
    }
    if (fee_custom > fee_price){
        fee_price = fee_custom
    }
    $('.initial-fee').val(fee_price)
    $('.credit-initial-fee').html(fee_price + ' сом')
}
$(document).on('change','.loan.bank',function(){
    let option =  $(this).find('option[value='+$(this).val()+']');
    let start = parseInt(option.attr('data-start'));
    let end = parseInt(option.attr('data-end'));
    let period = $('.loan.period');
    period.html('')

    let bank = $('.loan.bank');
    if(bank.next().hasClass('red-alert')){
        bank.next().remove();
    }
    period.trigger('change');
});
$(document).on('change','.choose-period',function(){
    calcLoan()
});

$('.choose-bank-option').on('change',function(){
    let val = $(this).val();
    if(val == 'online'){
        $('.loan.choose-bank .offline').attr('disabled','disabled');
        $('.loan.choose-bank .online').removeAttr('disabled');
        let online = $('.loan.choose-bank .online').first().val();
        $('.loan.choose-bank').val(online).trigger('change');
    }else{
        $('.loan.choose-bank .online').attr('disabled','disabled');
        $('.loan.choose-bank .offline').removeAttr('disabled');
        let offline = $('.loan.choose-bank .offline').first().val();
        $('.loan.choose-bank').val(offline).trigger('change');
    }
});

$('.initial-fee').on('change', function(){
    calcLoan()
})
$(document).on('change','.choose-bank',function(){
    let id = $(this).val();
    let period = $('.choose-period');
    let percent = $('.percent');
    let price_info = $('.credit-start-end-price');
    let guarantor_info = $('.credit-guarantor');
    let initial_fee_info = $('.credit-initial-fee-title');
    let initial_fee = $('.initial-fee');
    let period_info = $('.credit-start-end-period');
    let term_info = $('.credit-term-of-consider');
    let repayment_info = $('.credit-repayment');
    let desc = $('.credit-desc');
    let desc_in_office = $('.credit-desc-in-office');
    let img = $('.credit-bank-img');
    let form = new FormData();
    form.append('id', id);
    axios.post('/getBankData',form).then(function(response){
        let bank = response.data.bank;
        img.attr('src',bank.logo);
        price_info.html(bank.price+'-'+bank.end_price +' сом').attr('start', bank.price).attr('end', bank.end_price);
        if(bank.guarantor){
            guarantor_info.html('требуется');
        }else{
            guarantor_info.html('не требуется');
        }
        initial_fee_info.html('до '+bank.initial_fee_before+' сом без вноса');
        price_info.html(bank.price+'-'+bank.end_price +' сом');
        period_info.html(bank.start+'-'+bank.end +' месяцев');
        term_info.html(bank.term);
        repayment_info.html(bank.repayment);
        desc.html(bank.desc);
        desc_in_office.html(bank.desc_for_office);
        period.html('');

        percent.attr('placeholder', bank.percent + ' %').attr('data-percent',bank.percent).attr('data-percents',bank.percents);
        initial_fee.attr('placeholder', bank.initial_fee + ' сом').attr('data-fee', bank.initial_fee).attr('data-before', bank.initial_fee_before).val(bank.initial_fee);
        
        for (let i =bank.start ; i <= bank.end; i++) {
            if(i == 1 || i == 21){
                period.append('<option value="'+i+'">'+i+' месяц</option>');
            }else if(i < 5){
                period.append('<option value="'+i+'">'+i+' месяца</option>');
            }else if(i < 21){
                period.append('<option value="'+i+'">'+i+' месяцев</option>');
            }else{
                period.append('<option value="' + i + '">' + i + ' месяца</option>');
            }
        }
        calcLoan()
    });
});
$(document).on('click', '.addNew', function () {
    let btn = $(this);
    let product = btn.attr('data-id');
    let name = btn.html();
    let spec = btn.attr('data-spec');
    let price = parseFloat(btn.attr('data-price'));
    let price_converted = parseFloat(btn.attr('data-price-con'));
    let period = $('.loan.period');
    
    if (period.val() == 1 || period.val() == 21) {
        period = period.val() + ' месяц';
    } else if (period.val() < 5) {
        period = period.val() + ' месяца';
    } else if (period.val() < 21){
        period = period.val() + ' месяцев';
    }else{
        period = period.val() + ' месяца';
    }
    $('.loan-product').append(`
        <div class="loan-result p-3 position-relative" data-id="`+ product + `" data-spec="` + spec + `">
            <a class="remove-loan-products">
                <img src="/static/img/x-red.svg" alt="">
            </a>
            <div class="col-12">
                <p class="sf-reg loan-title">Устройство</p>
                <p class="sf-reg loan-body mt-2">`+ name + `</p>
            </div>
            <div class="d-flex flex-wrap justify-content-between">
                <div class="col-12 mt-4">
                    <p class="sf-reg loan-title">Цена устройства</p>
                    <p class="sf-reg loan-body mt-2">$`+ price + `</p>
                    <p class="sf-reg loan-title mt-2 product-converted-price" data-price="`+ price_converted + `">` + price_converted + ` сом</p>
                </div>
            </div>
        </div>
    `);
    $(".addNewProduct").val('');
    $('.search-result-product .content').addClass('d-none').html('');
    $('.purchase-on-credit').removeAttr('disabled')
    calcLoan()
    
});
$(document).on('input', '.addNewProduct', function () {
    let search = $(this).val();
    let form = new FormData();
    form.append('search', search);
    if (search) {
        axios.post('/addNewProduct', form).then(function (resp) {
            $('.search-result-product .content').html('');
            $.each(resp.data.products, function (key, product) {
                $('.search-result-product .content').append(`
                <a class="sf-light addNew" data-id="` + product.id + `" data-spec="` + product.spec + `"
                data-price="` + product.price + `"
                data-price-con="` + product.price_converted + `"
                >` + boldString(product.name, search) + `</a>
                `);
            });
            $('.search-result-product .content').removeClass('d-none');
            if (!resp.data.products) {
                $('.search-result-product .content').addClass('d-none');
            }
        });
    } else {
        $('.search-result-product .content').addClass('d-none');
        $('.search-result-product .content').html('');
    }
});

$(document).on('click', '.remove-loan-products', function () {
    $(this).parent().remove();
    if (!$('.loan-product .loan-result').length){
        $('.purchase-on-credit').attr('disabled', true)
    }
    $('.initial-fee').val(0)
    calcLoan()
});
function makeFloat(num) {
    return parseFloat(num.replace(',', '.'))
}