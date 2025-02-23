window.onload = function () {
    $(window).scroll(function () {
        if ($(this).scrollTop()) {
            $('#back-to-top').fadeIn();
            // $('.menu').css({ "background": "rgba(30,42,121, 0.7)" });
        } else {
            $('#back-to-top').fadeOut();
            // $('.menu').css({ "background": "#1e2a79" });
        }
    });
    $("#back-to-top").click(function () {
        $("html, body").animate({ scrollTop: 0 }, 100);
    });
    $("#txt-search").on('click', function (e) {
        $(".overlay").show();
        $(".list-cate-ajax").hide();
        $("#chevron").css({ 'transform': "rotate(0)" });
        $(this).data('status', 'off');
    })
    $(".overlay").on('click', function () {
        $(this).hide();
        $("#list-suggest").html('');
    });

    $("#show-menu").on('click', function (e) {
        $(".mobile-menu").css({ left: 0 });
        $(".overlay-full").show();
        e.stopPropagation();
    });
    $(".close-mobile").on('click', function () {
        $(".mobile-menu").css({ left: "-300px" });
        $(".overlay-full").hide();
    })
    $(".overlay-full").on('click', function () {
        $(".mobile-menu").css({ left: "-300px" });
        $(this).hide();
    })

    $("#expand").on('click', function () {
        $("#iframehtml5").addClass("force_full_screen");
        $("#_exit_full_screen").removeClass('hidden');
        requestFullScreen(document.body);
    });

    $("#_exit_full_screen").on('click', cancelFullScreen);

    $('input[name="keywords"]').on('keyup', async function (e) {
        let value = $(this).val();
        let url = "/query.ajax"
        if (value.length == 0) {
            $("#list-suggest").html('');
            return;
        }
        $.ajax({
            type: "POST",
            url: url,
            data: { q: value },
            success: function (data) {
                let parser_data = JSON.parse(data);
                $("#list-suggest").html(parser_data);
            }
        });
        return;
    });

    add_plugin();
}
function add_plugin() {
    let url = "/add-plugin.ajax";
    if (typeof id_game != 'undefined' && typeof url_game != 'undefined') {
        $.ajax({
            type: "POST",
            url: url,
            data: { id: id_game, url: url_game },
            success: function (data) {
                if (data) {
                    let html = JSON.parse(data);
                    if (html.html_rate) {
                        $("#append-rate").html(html.html_rate);
                    }
                    if (html.html_comment) {
                        $("#append-comment").html(html.html_comment);
                    }
                }
            }
        });
    }
}


function paging(p) {
    $(".gif").removeClass("hidden");
    let url = '/paging.ajax';
    let current_url = location.origin + location.pathname;
    $.ajax({
        type: "POST",
        url: url,
        data: {
            page: p,
            keywords: keywords,
            tag_id: tag_id,
            category_id: category_id,
            field_order: field_order,
            order_type: order_type,
            is_hot: is_hot,
            is_new: is_new,
            limit: limit
        },
        success: function (xxxx) {
            $(".gif").addClass("hidden");
            $("html, body").animate({ scrollTop: 0 }, 0);
            if (xxxx !== '') {
                let data = JSON.parse(xxxx);
                $("#ajax-append").html(data.content);
            }
        }
    });
}
function scrollToDiv(element) {
    if ($(element).length) {
        $('html,body').animate({ scrollTop: $(element).offset().top - 100 });
    }
}
function closeBox() {
    $(".close-sharing-box").hide();
    $(".clipboard-share").addClass("hide-zindex");
}

function showSharingBox() {
    $(".close-sharing-box").show();
    $(".clipboard-share").removeClass("hide-zindex");
}


function expand() {
    $("#expand").on('click', function () {
        $("#_exit_full_screen").removeClass('hidden');
        $("#iframehtml5").addClass("force_full_screen");
        requestFullScreen(document.body);
    });
    $("#_exit_full_screen").on('click', cancelFullScreen);
    $(".site-sort").on('click', function () {
        $(".site-sort").removeClass("active");
        $(this).addClass("active");
        let data_sort = $(this).data('sort');
        field_order = data_sort;
        paging(1);
    });
}
function runValidate() {
    jQuery("#contact-form").validate({
        focusInvalid: false,
        onfocusout: false,
        ignore: ".ignore",
        errorElement: "div",
        errorPlacement: function (error, element) {
            error.appendTo("div#contact_err");
        },
        rules: {
            Name: {
                required: true,
                maxlength: 255,
            },
            Email: {
                required: true,
                email: true,
                maxlength: 100
            },
            Website: {
                required: false,
                maxlength: 255,
            },
            Topic: {
                required: false,
                maxlength: 255,
            },
            Message: {
                required: true,
                maxlength: 65525
            },
            "contactChecked": {
                required: true
            }
        },
        messages: {
            Name: {
                required: "Please type your name!",
                maxlength: "255"
            },
            Email: {
                required: "Please type your email!",
                email: "Please check a valid email!",
                maxlength: "100"
            },
            Message: {
                required: "Please type your message!",
                maxlength: "65525"
            },
            "contactChecked": {
                required: "Please agree to the terms and conditions before comment."
            }
        },
        submitHandler: function () {
            let question_ajax = "/make-contact.ajax";
            let name = jQuery("#Name").val();
            let email = jQuery("#Email").val();
            let website = jQuery("#Website").val();
            let subject = jQuery("#Topic").val();
            let message = jQuery("#Message").val();
            let metadataload = {};
            metadataload.name = name;
            metadataload.email = email;
            metadataload.website = website;
            metadataload.subject = subject;
            metadataload.message = message;
            jQuery.ajax({
                url: question_ajax,
                data: metadataload,
                type: 'POST',
                success: function (data) {
                    if (data != 0 || data != '0') {
                        showSuccessMessage();
                    }
                }
            });
        }
    });
}
function showSuccessMessage(message) {
    document.getElementById('fcf-status').innerHTML = '';
    document.getElementById('fcf-form').style.display = 'none';
    document.getElementById('fcf-thank-you').style.display = 'block';
}

function resetFormDemo() {
    document.getElementById('fcf-form').style.display = "block";
    document.getElementById('fcf-thank-you').style.display = "none";
}
function requestFullScreen(element) {
    $("#iframehtml5").removeClass("force_half_full_screen");
    $(".header-game").removeClass("header_game_enable_half_full_screen");
    // Supports most browsers and their versions.
    var requestMethod = element.requestFullScreen || element.webkitRequestFullScreen || element.mozRequestFullScreen || element.msRequestFullScreen;
    if (requestMethod) { // Native full screen.
        requestMethod.call(element);
    } else if (typeof window.ActiveXObject !== "undefined") { // Older IE.
        var wscript = new ActiveXObject("WScript.Shell");
        if (wscript !== null) {
            wscript.SendKeys("{F11}");
        }
    }
}

function cancelFullScreen() {
    $("#_exit_full_screen").addClass('hidden');
    $("#iframehtml5").removeClass("force_full_screen");
    $("#iframehtml5").removeClass("force_half_full_screen");
    $(".header-game").removeClass("header_game_enable_half_full_screen");
    document.body.style.overflow = "unset";
    var requestMethod = document.cancelFullScreen || document.webkitCancelFullScreen || document.mozCancelFullScreen || document.exitFullScreenBtn;
    if (requestMethod) { // cancel full screen.
        requestMethod.call(document);
    } else if (typeof window.ActiveXObject !== "undefined") { // Older IE.
        var wscript = new ActiveXObject("WScript.Shell");
        if (wscript !== null) {
            wscript.SendKeys("{F11}");
        }
    }
}

if (document.addEventListener) {
    document.addEventListener('webkitfullscreenchange', exitHandler, false);
    document.addEventListener('mozfullscreenchange', exitHandler, false);
    document.addEventListener('fullscreenchange', exitHandler, false);
    document.addEventListener('MSFullscreenChange', exitHandler, false);
}

function exitHandler() {
    if (document.webkitIsFullScreen === false
        || document.mozFullScreen === false
        || document.msFullscreenElement === false) {
        cancelFullScreen();
    }
}