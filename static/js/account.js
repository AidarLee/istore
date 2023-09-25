$('.change-avatar').on('click',function(){
    $('#fileToUpload').trigger('click');
})
$('#fileToUpload').on('change',function(){
    $('.saveUserAvatar').submit()
})
$(document).ready(function(){
    let notify = $('.notify');
    if(notify.length){
        callNotifyModal('Успешно', "Ваш запрос отправлен на обработку");
    }
});