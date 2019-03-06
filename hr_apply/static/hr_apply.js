odoo.define('hr_apply.hr_apply', function (require) {
'use strict';
    
    require('web.dom_ready');
    
    if ($('.o_required_exp').length) {
        $('.o_required_exp').on('click', "a[id='new_department']", function () {
            $("a[id='new_department']").parent().hide();
            $("td[id='input_department']").show();
        });
        $('.o_required_exp').on('click', "a[id='new_industry']", function () {
            $("a[id='new_industry']").parent().hide();
            $("td[id='input_industry']").show();
        });
        $('.o_required_exp').on('click', "a[id='new_level']", function () {
            $("a[id='new_level']").parent().hide();
            $("td[id='input_level']").show();
        });
    }

    if ($('.o_required_univ').length) {
        var major_options = $("select[name='major_id']:enabled option:not(:first)");
        $('.o_required_univ').on('change', "select[name='faculty_id']", function () {
            var select = $("select[name='major_id']");
            major_options.detach();
            var displayed_major = major_options.filter("[data-faculty="+($(this).val() || 0)+"]");
            var nb = displayed_major.appendTo(select).show().size();
            select.parent().toggle(nb>=1);
        });
        $('.o_required_univ').on('click', "a[id='new_degree']", function () {
            $("a[id='new_degree']").parent().hide();
            $("td[id='input_degree']").show();
        });
        $('.o_required_univ').on('click', "a[id='new_faculty']", function () {
            $("a[id='new_faculty']").parent().hide();
            $("td[id='input_faculty']").show();
        });
        $('.o_required_univ').on('click', "a[id='new_major']", function () {
            $("a[id='new_major']").parent().hide();
            $("td[id='input_major']").show();
        });
        $('.o_required_univ').find("select[name='faculty_id']").change();
        $('.o_required_univ').find("select[name='major_id']").change();
    }

    if ($('.o_add_exp_level').length) {
        $('.o_add_exp_level').on('click', "a[id='new_exp_level']", function () {
            $("td[id='input_exp_level']").show();
            $("a[id='new_exp_level']").parent().hide();
            });
    }
        
    if ($('.o_add_exp_industry').length) {
        $('.o_add_exp_industry').on('click', "a[id='new_exp_industry']", function () {
            $("td[id='input_exp_industry']").show();
            $("a[id='new_exp_industry']").parent().hide();
            });
    }
        
    if ($('.o_add_v_object').length) {
        $('.o_add_v_object').on('click', "a[id='new_v_object']", function () {
            $("td[id='input_v_object']").show();
            $("a[id='new_v_object']").parent().hide();
            });
    }
        
    if ($('.o_search_area').length) {
        var state_options = $("select[name='state']:enabled option:not(:first)");
        var city_options = $("select[name='city']:enabled option:not(:first)");
        var district_options = $("select[name='district']:enabled option:not(:first)");
        var village_options = $("select[name='village']:enabled option:not(:first)");
        var area_options = $("select[name='area']:enabled option:not(:first)");
        var zipcode_options = $("select[name='zipcode']:enabled option:not(:first)");
        var company_options = $("select[name='company']:enabled option:not(:first)");
        
        $('.o_search_area').ready(function () {
            var select_country = $("select[name='country']");
            var select_company = $("select[name='company']");
            company_options.detach();
            var displayed_company = company_options.filter("[data-country="+($(select_country).val() || 0)+"]");
            var nb_company = displayed_company.appendTo(select_company).show().size();
        });
        
        $('.o_search_area').on('change', "select[name='country']", function () {
            var select_state = $("select[name='state']");
            var select_city = $("select[name='city']");
            var select_district = $("select[name='district']");
            var select_village = $("select[name='village']");
            var select_area = $("select[name='area']");
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            state_options.detach();
            city_options.detach();
            district_options.detach();
            village_options.detach();
            area_options.detach();
            zipcode_options.detach();
            company_options.detach();
            var displayed_state = state_options.filter("[data-country="+($(this).val() || 0)+"]");
            var displayed_city = city_options.filter("[data-country="+($(this).val() || 0)+"]").filter("[data-state="+($(select_state).val() || 0)+"]");
            var displayed_district = district_options.filter("[data-country="+($(this).val() || 0)+"]").filter("[data-state="+($(select_state).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]");
            var displayed_village = village_options.filter("[data-country="+($(this).val() || 0)+"]").filter("[data-state="+($(select_state).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]");
            var displayed_area = area_options.filter("[data-country="+($(this).val() || 0)+"]").filter("[data-state="+($(select_state).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]");
            var displayed_zipcode = zipcode_options.filter("[data-country="+($(this).val() || 0)+"]").filter("[data-state="+($(select_state).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]").filter("[data-area="+($(select_area).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-country="+($(this).val() || 0)+"]");
            var nb_state = displayed_state.appendTo(select_state).show().size();
            var nb_city = displayed_city.appendTo(select_city).show().size();
            var nb_district = displayed_district.appendTo(select_district).show().size();
            var nb_village = displayed_village.appendTo(select_village).show().size();
            var nb_area = displayed_area.appendTo(select_area).show().size();
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_state.parent().toggle(nb_state>=1);
            select_city.parent().toggle(nb_city>=1);
            select_district.parent().toggle(nb_district>=1);
            select_village.parent().toggle(nb_village>=1);
            select_area.parent().toggle(nb_area>=1);
            select_zipcode.parent().toggle(nb_zipcode>=1);
        });
        $('.o_search_area').on('change', "select[name='state']", function () {
            var select_city = $("select[name='city']");
            var select_district = $("select[name='district']");
            var select_village = $("select[name='village']");
            var select_area = $("select[name='area']");
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            city_options.detach();
            district_options.detach();
            village_options.detach();
            area_options.detach();
            zipcode_options.detach();
            company_options.detach();
            var displayed_city = city_options.filter("[data-state="+($(this).val() || 0)+"]");
            var displayed_district = district_options.filter("[data-state="+($(this).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]");
            var displayed_village = village_options.filter("[data-state="+($(this).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]");
            var displayed_area = area_options.filter("[data-state="+($(this).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]");
            var displayed_zipcode = zipcode_options.filter("[data-state="+($(this).val() || 0)+"]").filter("[data-city="+($(select_city).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]").filter("[data-area="+($(select_area).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-state="+($(this).val() || 0)+"]");
            var nb_city = displayed_city.appendTo(select_city).show().size();
            var nb_district = displayed_district.appendTo(select_district).show().size();
            var nb_village = displayed_village.appendTo(select_village).show().size();
            var nb_area = displayed_area.appendTo(select_area).show().size();
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_city.parent().toggle(nb_city>=1);
            select_district.parent().toggle(nb_district>=1);
            select_village.parent().toggle(nb_village>=1);
            select_area.parent().toggle(nb_area>=1);
            select_zipcode.parent().toggle(nb_zipcode>=1);
        });
        $('.o_search_area').on('change', "select[name='city']", function () {
            var select_district = $("select[name='district']");
            var select_village = $("select[name='village']");
            var select_area = $("select[name='area']");
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            district_options.detach();
            village_options.detach();
            area_options.detach();
            zipcode_options.detach();
            company_options.detach();
            var displayed_district = district_options.filter("[data-city="+($(this).val() || 0)+"]");
            var displayed_village = village_options.filter("[data-city="+($(this).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]");
            var displayed_area = area_options.filter("[data-city="+($(this).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]");
            var displayed_zipcode = zipcode_options.filter("[data-city="+($(this).val() || 0)+"]").filter("[data-district="+($(select_district).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]").filter("[data-area="+($(select_area).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-city="+($(this).val() || 0)+"]");
            var nb_district = displayed_district.appendTo(select_district).show().size();
            var nb_village = displayed_village.appendTo(select_village).show().size();
            var nb_area = displayed_area.appendTo(select_area).show().size();
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_district.parent().toggle(nb_district>=1);
            select_village.parent().toggle(nb_village>=1);
            select_area.parent().toggle(nb_area>=1);
            select_zipcode.parent().toggle(nb_zipcode>=1);
        });
        $('.o_search_area').on('change', "select[name='district']", function () {
            var select_village = $("select[name='village']");
            var select_area = $("select[name='area']");
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            village_options.detach();
            area_options.detach();
            zipcode_options.detach();
            company_options.detach();
            var displayed_village = village_options.filter("[data-district="+($(this).val() || 0)+"]");
            var displayed_area = area_options.filter("[data-district="+($(this).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]");
            var displayed_zipcode = zipcode_options.filter("[data-district="+($(this).val() || 0)+"]").filter("[data-village="+($(select_village).val() || 0)+"]").filter("[data-area="+($(select_area).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-district="+($(this).val() || 0)+"]");
            var nb_village = displayed_village.appendTo(select_village).show().size();
            var nb_area = displayed_area.appendTo(select_area).show().size();
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_village.parent().toggle(nb_village>=1);
            select_area.parent().toggle(nb_area>=1);
            select_zipcode.parent().toggle(nb_zipcode>=1);
        });
        $('.o_search_area').on('change', "select[name='village']", function () {
            var select_area = $("select[name='area']");
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            area_options.detach();
            zipcode_options.detach();
            company_options.detach();
            var displayed_area = area_options.filter("[data-village="+($(this).val() || 0)+"]");
            var displayed_zipcode = zipcode_options.filter("[data-village="+($(this).val() || 0)+"]").filter("[data-area="+($(select_area).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-village="+($(this).val() || 0)+"]");
            var nb_area = displayed_area.appendTo(select_area).show().size();
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_area.parent().toggle(nb_area>=1);
            select_zipcode.parent().toggle(nb_zipcode>=1);
        });
        $('.o_search_area').on('change', "select[name='area']", function () {
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            zipcode_options.detach();
            company_options.detach();
            var displayed_zipcode = zipcode_options.filter("[data-area="+($(this).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-area="+($(this).val() || 0)+"]");
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_zipcode.parent().toggle(nb_zipcode>=1);
        });        

        $('.o_search_area').find("select[name='country']").change();
        $('.o_search_area').find("select[name='state']").change();
        $('.o_search_area').find("select[name='city']").change();
        $('.o_search_area').find("select[name='district']").change();
        $('.o_search_area').find("select[name='village']").change();
        $('.o_search_area').find("select[name='area']").change();
        $('.o_search_area').find("select[name='zipcode']").change();
        $('.o_search_area').find("select[name='company']").change();
        
    }


});