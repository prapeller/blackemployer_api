'use strict'

$('input#search_elems').keyup( e => {
    e.preventDefault()

    let input = e.target
    let searchStr = input.value

    $.ajax(
        {
            url: `/djangofront/search_elems_with_ajax/?search_str=${searchStr}`,
            success: data => {
                $('.search_companies').html(data.companies_list_html)
                $('.search_cases').html(data.cases_list_html)
            }
        })
})
