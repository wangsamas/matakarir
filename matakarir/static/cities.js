odoo.define('matakarir.cities', function (require) {
'use strict';
    
    require('web.dom_ready');
    
    if ($('.o_three_levels').length) {
        var level2_options = $("select[name='level2']:enabled option:not(:first)");
        var level3_options = $("select[name='level3']:enabled option:not(:first)");
        var add_level1 = $("a[id='new_level1']");
        var add_level2 = $("a[id='new_level2']");
        var add_level3 = $("a[id='new_level3']");
        var input_level1 = $("td[id='input_level1']");
        var input_level2 = $("td[id='input_level2']");
        var input_level3 = $("td[id='input_level3']");
        
        $('.o_three_levels').ready(function () {
            add_level1.parent().show();
            add_level2.parent().show();
            add_level3.parent().hide();
            var select_level1 = $("select[name='level1']");
            var select_level3 = $("select[name='level3']");
            level3_options.detach();
            var displayed_level3 = level3_options.filter("[data-level1="+($(select_level1).val() || 0)+"]");
            var nb_level3 = displayed_level3.appendTo(select_level3).show().size();
            select_level3.parent().toggle(nb_level3>=1);
        });
        
        $('.o_three_levels').on('change', "select[name='level1']", function () {
            var select_level2 = $("select[name='level2']");
            var select_level3 = $("select[name='level3']");
            level2_options.detach();
            level3_options.detach();
            var displayed_level2 = level2_options.filter("[data-level1="+($(this).val() || 0)+"]");
            var displayed_level3 = level3_options.filter("[data-level1="+($(this).val() || 0)+"]").filter("[data-level2="+($(select_level2).val() || 0)+"]");
            var nb_level2 = displayed_level2.appendTo(select_level2).show().size();
            var nb_level3 = displayed_level3.appendTo(select_level3).show().size();
            select_level2.parent().toggle(nb_level2>=1);
            select_level3.parent().toggle(nb_level3>=1);
            add_level1.parent().show();
            add_level2.parent().show();
            add_level3.parent().hide();
            input_level1.hide();
            input_level2.hide();
            input_level3.hide();
        });
        $('.o_three_levels').on('change', "select[name='level2']", function () {
            var select_level3 = $("select[name='level3']");
            level3_options.detach();
            var displayed_level3 = level3_options.filter("[data-level2="+($(this).val() || 0)+"]");
            var nb_level3 = displayed_level3.appendTo(select_level3).show().size();
            select_level3.parent().toggle(nb_level3>=1);
            add_level1.parent().hide();
            add_level2.parent().show();
            add_level3.parent().show();
            input_level1.hide();
            input_level2.hide();
            input_level3.hide();
        });
        $('.o_three_levels').on('change', "select[name='level3']", function () {
            add_level1.parent().hide();
            add_level2.parent().hide();
            add_level3.parent().show();
            input_level1.hide();
            input_level2.hide();
            input_level3.hide();
        });
        
        $('.o_three_levels').on('click', "a[id='new_level1']", function () {
            add_level1.parent().hide();
            add_level2.parent().hide();
            add_level3.parent().hide();
            input_level1.show();
            input_level2.show();
            input_level3.show();
        });
        $('.o_three_levels').on('click', "a[id='new_level2']", function () {
            add_level1.parent().hide();
            add_level2.parent().hide();
            add_level3.parent().hide();
            input_level2.show();
            input_level3.show();
        });
        $('.o_three_levels').on('click', "a[id='new_level3']", function () {
            add_level1.parent().hide();
            add_level2.parent().hide();
            add_level3.parent().hide();
            input_level3.show();
        });
		
        $('.o_three_levels').find("select[name='level1']").change();
        $('.o_three_levels').find("select[name='level2']").change();
        $('.o_three_levels').find("select[name='level3']").change();        
    }

    if ($('.o_country_object').length) {
        var object_options = $("select[name='object_id']:enabled option:not(:first)");
        $('.o_country_object').on('change', "select[name='country_id']", function () {
            var select = $("select[name='object_id']");
            object_options.detach();
            var displayed_object = object_options.filter("[data-country_id="+($(this).val() || 0)+"]");
            var nb = displayed_object.appendTo(select).show().size();
            select.parent().toggle(nb>=1);
        });
        $('.o_country_object').on('click', "a[id='new_country']", function () {
            $("a[id='new_country']").parent().hide();
            $("td[id='input_country']").show();
        });
        $('.o_country_object').on('click', "a[id='new_object']", function () {
            $("a[id='new_object']").parent().hide();
            $("td[id='input_object']").show();
        });
        $('.o_country_object').find("select[name='country_id']").change();
        $('.o_country_object').find("select[name='object_id']").change();
    }

    if ($('.o_add_object').length) {
        $('.o_add_object').on('click', "a[id='new_object']", function () {
            $("a[id='new_object']").parent().hide();
            $("td[id='input_object']").show();
            });
    }
        
    if ($('.o_add_skill').length) {
        $('.o_add_skill').on('click', "a[id='new_skill']", function () {
            $("a[id='new_skill']").parent().hide();
            $("td[id='input_skill']").show();
            });
    }
        
    if ($('.o_edit_citizen').length) {
        $('.o_edit_citizen').on('click', "a[id='new_citizen']", function () {
            $("a[id='new_citizen']").parent().hide();
            $("td[id='input_citizen']").show();
            });
    }
        
    if ($('.o_edit_ethnic').length) {
        $('.o_edit_ethnic').on('click', "a[id='new_ethnic']", function () {
            $("a[id='new_ethnic']").parent().hide();
            $("td[id='input_ethnic']").show();
            });
    }
        
    if ($('.o_edit_religion').length) {
        $('.o_edit_religion').on('click', "a[id='new_religion']", function () {
            $("a[id='new_religion']").parent().hide();
            $("td[id='input_religion']").show();
            });
    }
        
    if ($('.o_edit_job_level').length) {
        $('.o_edit_job_level').on('click', "a[id='new_level']", function () {
            $("a[id='new_level']").parent().hide();
            $("td[id='input_level']").show();
            });
    }
        
    if ($('.o_edit_department').length) {
        $('.o_edit_department').on('click', "a[id='new_department']", function () {
            $("a[id='new_department']").parent().hide();
            $("td[id='input_department']").show();
            });
    }

    if ($('.o_edit_industry').length) {
        $('.o_edit_industry').on('click', "a[id='new_industry']", function () {
            $("a[id='new_industry']").parent().hide();
            $("td[id='input_industry']").show();
            });
    }
        
    if ($('.o_edit_companytype').length) {
        $('.o_edit_companytype').on('click', "a[id='new_companytype']", function () {
            $("a[id='new_companytype']").parent().hide();
            $("td[id='input_companytype']").show();
            });
    }
        
    if ($('.o_edit_e_status').length) {
        $('.o_edit_e_status').on('click', "a[id='new_e_status']", function () {
            $("a[id='new_e_status']").parent().hide();
            $("td[id='input_e_status']").show();
            });
    }
        
    if ($('.o_edit_faculty').length) {
        $('.o_edit_faculty').on('click', "a[id='new_faculty']", function () {
            $("a[id='new_faculty']").parent().hide();
            $("td[id='input_faculty']").show();
            });
    }
        
    if ($('.o_edit_major').length) {
        $('.o_edit_major').on('click', "a[id='new_major']", function () {
            $("a[id='new_major']").parent().hide();
            $("td[id='input_major']").show();
            });
    }
        
    if ($('.o_edit_degree').length) {
        $('.o_edit_degree').on('click', "a[id='new_degree']", function () {
            $("a[id='new_degree']").parent().hide();
            $("td[id='input_degree']").show();
            });
    }
        
    
    if ($('.o_area_selections').length) {
        var state_options = $("select[name='state']:enabled option:not(:first)");
        var city_options = $("select[name='city']:enabled option:not(:first)");
        var district_options = $("select[name='district']:enabled option:not(:first)");
        var village_options = $("select[name='village']:enabled option:not(:first)");
        var area_options = $("select[name='area']:enabled option:not(:first)");
        var zipcode_options = $("select[name='zipcode']:enabled option:not(:first)");
        var company_options = $("select[name='company']:enabled option:not(:first)");
        var add_country = $("a[id='new_country']");
        var add_state = $("a[id='new_state']");
        var add_city = $("a[id='new_city']");
        var add_district = $("a[id='new_district']");
        var add_village = $("a[id='new_village']");
        var add_area = $("a[id='new_area']");
        var add_zipcode = $("a[id='new_zipcode']");
        var add_company = $("a[id='new_company']");
        var input_country = $("td[id='input_country']");
        var input_state = $("td[id='input_state']");
        var input_city = $("td[id='input_city']");
        var input_district = $("td[id='input_district']");
        var input_village = $("td[id='input_village']");
        var input_area = $("td[id='input_area']");
        var input_zipcode = $("td[id='input_zipcode']");
        var input_company = $("td[id='input_company']");
        
        $('.o_area_selections').ready(function () {
            add_country.parent().show();
            add_state.parent().show();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            var select_country = $("select[name='country']");
            var select_company = $("select[name='company']");
            company_options.detach();
            var displayed_company = company_options.filter("[data-country="+($(select_country).val() || 0)+"]");
            var nb_company = displayed_company.appendTo(select_company).show().size();
        });
        
        $('.o_area_selections').on('change', "select[name='country']", function () {
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
            add_country.parent().show();
            add_state.parent().show();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        $('.o_area_selections').on('change', "select[name='state']", function () {
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
            add_country.parent().hide();
            add_state.parent().show();
            add_city.parent().show();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        $('.o_area_selections').on('change', "select[name='city']", function () {
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
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().show();
            add_district.parent().show();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        $('.o_area_selections').on('change', "select[name='district']", function () {
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
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().show();
            add_village.parent().show();
            add_zipcode.parent().hide();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        $('.o_area_selections').on('change', "select[name='village']", function () {
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
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().show();
            add_area.parent().show();
            add_zipcode.parent().hide();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        $('.o_area_selections').on('change', "select[name='area']", function () {
            var select_zipcode = $("select[name='zipcode']");
            var select_company = $("select[name='company']");
            zipcode_options.detach();
            company_options.detach();
            var displayed_zipcode = zipcode_options.filter("[data-area="+($(this).val() || 0)+"]");
            var displayed_company = company_options.filter("[data-area="+($(this).val() || 0)+"]");
            var nb_zipcode = displayed_zipcode.appendTo(select_zipcode).show().size();
            var nb_company = displayed_company.appendTo(select_company).show().size();
            select_zipcode.parent().toggle(nb_zipcode>=1);
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().show();
            add_zipcode.parent().show();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        $('.o_area_selections').on('change', "select[name='zipcode']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().show();
            input_country.hide();
            input_state.hide();
            input_city.hide();
            input_district.hide();
            input_village.hide();
            input_area.hide();
            input_zipcode.hide();
        });
        
        $('.o_area_selections').on('click', "a[id='new_country']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_country.show();
            input_state.show();
            input_city.show();
            input_district.show();
            input_village.show();
            input_area.show();
            input_zipcode.show();
        });
        $('.o_area_selections').on('click', "a[id='new_state']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_state.show();
            input_city.show();
            input_district.show();
            input_village.show();
            input_area.show();
            input_zipcode.show();
        });
        $('.o_area_selections').on('click', "a[id='new_city']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_city.show();
            input_district.show();
            input_village.show();
            input_area.show();
            input_zipcode.show();
        });
        $('.o_area_selections').on('click', "a[id='new_district']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_district.show();
            input_village.show();
            input_area.show();
            input_zipcode.show();
        });
        $('.o_area_selections').on('click', "a[id='new_village']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_village.show();
            input_area.show();
            input_zipcode.show();
        });
        $('.o_area_selections').on('click', "a[id='new_area']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_area.show();
            input_zipcode.show();
        });
        $('.o_area_selections').on('click', "a[id='new_zipcode']", function () {
            add_country.parent().hide();
            add_state.parent().hide();
            add_city.parent().hide();
            add_district.parent().hide();
            add_village.parent().hide();
            add_area.parent().hide();
            add_zipcode.parent().hide();
            input_zipcode.show();
        });

        $('.o_area_selections').on('click', "a[id='new_company']", function () {
            $("a[id='new_company']").parent().hide();
            input_company.show();
            $('.company_info').show();
        });

        $('.o_area_selections').find("select[name='country']").change();
        $('.o_area_selections').find("select[name='state']").change();
        $('.o_area_selections').find("select[name='city']").change();
        $('.o_area_selections').find("select[name='district']").change();
        $('.o_area_selections').find("select[name='village']").change();
        $('.o_area_selections').find("select[name='area']").change();
        $('.o_area_selections').find("select[name='zipcode']").change();
        $('.o_area_selections').find("select[name='company']").change();
        
    }

    if ($('.o_city_selections').length) {
        var state_options = $("select[name='state_id']:enabled option:not(:first)");
        var city_options = $("select[name='city_id']:enabled option:not(:first)");
        
        $('.o_city_selections').on('change', "select[name='country_id']", function () {
            var select_state = $("select[name='state_id']");
            var select_city = $("select[name='city_id']");
            state_options.detach();
            city_options.detach();
            var displayed_state = state_options.filter("[data-country="+($(this).val() || 0)+"]");
            var displayed_city = city_options.filter("[data-country="+($(this).val() || 0)+"]").filter("[data-state="+($(select_state).val() || 0)+"]");
            var nb_state = displayed_state.appendTo(select_state).show().size();
            var nb_city = displayed_city.appendTo(select_city).show().size();
            select_state.parent().toggle(nb_state>=1);
            select_city.parent().toggle(nb_city>=1);
        });
        $('.o_city_selections').on('change', "select[name='state_id']", function () {
            var select_city = $("select[name='city_id']");
            city_options.detach();
            var displayed_city = city_options.filter("[data-state="+($(this).val() || 0)+"]");
            var nb_city = displayed_city.appendTo(select_city).show().size();
            select_city.parent().toggle(nb_city>=1);
        });
        $('.o_city_selections').find("select[name='country_id']").change();
        $('.o_city_selections').find("select[name='state_id']").change();
        $('.o_city_selections').find("select[name='city_id']").change();        
    }
    

});