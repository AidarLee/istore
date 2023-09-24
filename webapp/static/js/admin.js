document.addEventListener("DOMContentLoaded", function (event) {
    
    let tmc = document.createElement('script');
    tmc.setAttribute('src', 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.6.2/tinymce.min.js');
    document.head.appendChild(tmc);
    let token = document.querySelectorAll('input[name="csrfmiddlewaretoken"]');
    tmc.onload = () => {
        tinymce.init({
            selector: '#id_description,#id_desc,#id_desc_for_office',
            plugins: 'image code media link',
            toolbar: 'undo redo | link image | code  | styleselect | fontsizeselect | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | tableColumn tableRow mergeTableCells',
            fontsize_formats: "2vw 4vw 6vw 8vw 10vw 12vw 14vw 8pt 9pt 10pt 11pt 12pt 14pt 18pt 24pt 30pt 36pt 48pt 60pt 72pt 96pt ",
            image_title: true,
            automatic_uploads: true,
            file_picker_types: 'image media',
            images_file_types: 'jpg,svg,webp,png,gif',
            images_upload_handler: function (blobInfo, success, failure, progress) {
                var xhr, formData;
                xhr = new XMLHttpRequest();
                xhr.withCredentials = false;
                xhr.open('POST', '/saveImage');

                xhr.upload.onprogress = function (e) {
                    progress(e.loaded / e.total * 100);
                };

                xhr.onload = function () {
                    var json;

                    if (xhr.status < 200 || xhr.status >= 300) {
                        failure('HTTP Error: ' + xhr.status);
                        return;
                    }

                    json = JSON.parse(xhr.responseText);

                    if (!json || typeof json.location != 'string') {
                        failure('Invalid JSON: ' + xhr.responseText);
                        return;
                    }

                    success(json.location);
                };

                xhr.onerror = function () {
                    failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
                };

                formData = new FormData();
                formData.append('file', blobInfo.blob(), blobInfo.filename());
                formData.append('csrfmiddlewaretoken',token[0].value);
                xhr.send(formData);
            }
        })
    }
});

django.jQuery(document).ready(function () {
    //Products
    django.jQuery('input[id^=id_specification][id$=is_active][type=checkbox]').each(function (i, el) {
        //It'll be an array of elements
        let element = django.jQuery(el).parents().eq(4).find('input[id^=id_specification][id$=price]')
        let element2 = django.jQuery(this).parents().eq(4).find('input[id^=id_specification][id$=quantity]')
        element.prop("readonly", django.jQuery(this).is(':checked'));
        element2.prop("readonly", django.jQuery(this).is(':checked'));
    });

    django.jQuery(document).on('click', "input[id^=id_specification][id$=is_active][type=checkbox]", function () {
        let element = django.jQuery(this).parents().eq(4).find('input[id^=id_specification][id$=price]')
        let element2 = django.jQuery(this).parents().eq(4).find('input[id^=id_specification][id$=quantity]')
        element.prop("readonly", django.jQuery(this).is(':checked'));
        element2.prop("readonly", django.jQuery(this).is(':checked'));
    })

    // Category
    let is_active = django.jQuery('#currency_form #id_is_active')
    let currency_field = django.jQuery('#currency_form #id_exchange_rate')
    if (is_active.is(':checked')) {
        currency_field.prop("readonly", true);
    } else {
        currency_field.prop("readonly", false);
    }
    is_active.on('click', function () {
        if (is_active.is(':checked')) {
            currency_field.prop("readonly", true);
        } else {
            currency_field.prop("readonly", false);
        }
    })
    django.jQuery('body').append("<div class='loader-background'><div class='loader'><div class='loading'></div></div></div>")
})
function spinner() {
    document.getElementsByClassName("loader-background")[0].style.display = "block";
    window.location.href = '/moysklad/get_products'
}
// $(document).on('click', '.select2', function () {
//     console.log(this)
// });
$(document).on('click','.djn-collapse-handler.grp-collapse-handler.djn-drag-handler', function(){
    setTimeout(() => {
        $('.djn-items.grp-items.ui-sortable .djn-item[data-is-initial="false"] select:not(.select2-hidden-accessible)').select2({
            width: '200px',
        });
    }, 200);
});