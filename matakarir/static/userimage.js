odoo.define('matakarir.avatar', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');

    var _t = core._t;

    var lastsearch;

    $('.o_karir_profile_pic_edit').on('click', function(ev) {
        ev.preventDefault();
        $(this).closest('form').find('.o_karir_file_upload').trigger('click');
    });

    $('.o_karir_file_upload').on('change', function() {
        if (this.files.length) {
            var $form = $(this).closest('form');
            var reader = new window.FileReader();
            reader.onload = function(ev) {
                $form.find('.o_karir_avatar_img').attr('src', ev.target.result);
            };
            reader.readAsDataURL(this.files[0]);
            $form.find('#karir_clear_image').remove();
        }
    });

    $('.o_karir_profile_pic_clear').click(function() {
        var $form = $(this).closest('form');
        $form.find('.o_karir_avatar_img').attr("src", "/web/static/src/img/placeholder.png");
        $form.append($('<input/>', {
            name: 'clear_image',
            id: 'karir_clear_image',
            type: 'hidden',
        }));
    });
    
});