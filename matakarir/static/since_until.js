odoo.define('input.since_until', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var time = require('web.time');
    var core = require('web.core');

    $(document).ready(function() {
        $('select[name="status"]').on("change", 'select[value="progress"]', function () {
            $("input[name='until']").parent('tr').hide();
        });
    });
});

