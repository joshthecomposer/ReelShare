let blurElement = document.querySelector('#blur');
let reel_creation = document.getElementById('reel_creation');
let loginElement = document.getElementById('login');
let regElement = document.getElementById('registration');
let isBlurry = false;
let reel_view = false;

$(function () {
    $("ul.sortable").sortable({
        update: function (event, ui) {
            item_order = updateOrder();
            order_string = 'order=' + item_order;
            item_order = order_string
            $.ajax({
                method: "POST",
                url: "/tracklist_update",
                data: item_order,
                cache: false,
                success: function (data) {
                    location.reload();
                }
            })
        }
    })
});

$( function() {
    $(".draggable").draggable({
        helper: "clone",
        revert: 'invalid'
    });
    $(".droppable").droppable({
        drop: function (event, ui) {
            for (var i = 0; i < event.target.children.length; i++) {
                if (ui.draggable.attr('id') == event.target.children[i].id) {
                    return false;
                }
            }
            if (event.target.children[0].id == 'reel-placeholder') {
                event.target.children[0].remove()
            }
            $(event.target).append(
                ui.draggable
            )
            $.ajax({
                method: "POST",
                url: "/save_track_to_reel",
                data: {
                    target_id : event.target.id,
                    origin_id : ui.draggable[0].id
                },
                cache: false,
                success: function () {
                    location.reload()
                    return false;
                }
            })
            }
    });
});

function updateOrder() {
    var item_order = new Array();
    $('ul.sortable li').each(function(){
        item_order.push($(this).attr("id"));
    })
    return item_order;
};

function revealReelCreation() {
    filterVal = "blur(15px)"
    $(reel_creation).fadeIn(500)
    $(blurElement).css({
        'filter':filterVal,
        'webkitFilter':filterVal,
        'mozFilter':filterVal,
        'oFilter':filterVal,
        'msFilter': filterVal,
        'transition':'all 0.5s ease-in',
        '-webkit-transition':'all 0.5s ease-in',
        '-moz-transition':'all 0.5s ease-in',
        '-o-transition':'all 0.5s ease-in'
    });
};

function revealLogin() {
    filterVal = "blur(15px)"
    if (isBlurry == true) {
        setTimeout(function () { 
            $(loginElement).fadeIn(500)
        }, 500)
        $(regElement).fadeOut(500)
    } else {
        $(loginElement).fadeIn(500)
        $(regElement).fadeOut(500)
        $(blurElement).css({
            'filter':filterVal,
            'webkitFilter':filterVal,
            'mozFilter':filterVal,
            'oFilter':filterVal,
            'msFilter': filterVal,
            'transition':'all 0.5s ease-in',
            '-webkit-transition':'all 0.5s ease-in',
            '-moz-transition':'all 0.5s ease-in',
            '-o-transition':'all 0.5s ease-in'
        });
    }
};

function revealReg() {
    filterVal = "blur(15px)"
    if (isBlurry == true) {
        setTimeout(function () { 
            $(regElement).fadeIn(500)
        }, 500)
        $(loginElement).fadeOut(500)
    } else {
        $(regElement).fadeIn(500)
        $(loginElement).fadeOut(500)
        $(blurElement).css({
            'filter':filterVal,
            'webkitFilter':filterVal,
            'mozFilter':filterVal,
            'oFilter':filterVal,
            'msFilter': filterVal,
            'transition':'all 0.5s ease-in',
            '-webkit-transition':'all 0.5s ease-in',
            '-moz-transition':'all 0.5s ease-in',
            '-o-transition':'all 0.5s ease-in'
        });
    }
};

function hideReelCreation() {
    filterVal = "blur(0)"
    $(reel_creation).fadeOut(500)
    $(blurElement).css({
        'filter':filterVal,
        'webkitFilter':filterVal,
        'mozFilter':filterVal,
        'oFilter':filterVal,
        'msFilter':filterVal,
        'transition':'all 0.5s ease-in',
        '-webkit-transition':'all 0.5s ease-in',
        '-moz-transition':'all 0.5s ease-in',
        '-o-transition':'all 0.5s ease-in'
    });
    isBlurry = false;
};

function hideLogin() {
    filterVal = "blur(0)"
    $(loginElement).fadeOut(500)
    $(blurElement).css({
        'filter':filterVal,
        'webkitFilter':filterVal,
        'mozFilter':filterVal,
        'oFilter':filterVal,
        'msFilter':filterVal,
        'transition':'all 0.5s ease-in',
        '-webkit-transition':'all 0.5s ease-in',
        '-moz-transition':'all 0.5s ease-in',
        '-o-transition':'all 0.5s ease-in'
    });
    isBlurry = false;
};

function hideReg() {
    filterVal = "blur(0)"
    $(regElement).fadeOut(500)
    $(blurElement).css({
        'filter':filterVal,
        'webkitFilter':filterVal,
        'mozFilter':filterVal,
        'oFilter':filterVal,
        'msFilter':filterVal,
        'transition':'all 0.5s ease-in',
        '-webkit-transition':'all 0.5s ease-in',
        '-moz-transition':'all 0.5s ease-in',
        '-o-transition':'all 0.5s ease-in'
    });
    isBlurry = false;
};

function audioPlayer(element) {
    $('a.reel-a').click(function (e) {
        e.preventDefault()
        $(this).unbind('click')
    })
    let audio = element.children[0]
    let parentID = element.parentElement.id
    let progress = element.parentElement.children[2].children[0];
    if (element.id == 'play-icon') {
        element.id = 'pause-icon'
        audio.play()
        element.parentElement.style.backgroundColor = 'rgba(97, 97, 97, .5)'
        audio.addEventListener('timeupdate', function () {
            progress.style.width = ((audio.currentTime / audio.duration) * 100) + '%';
        })
    } else {
        element.id = 'play-icon'
        audio.pause()
        element.parentElement.style.backgroundColor = 'transparent'
    }
};

function audioPlayerReel(element) {
    $('a.reel-a').click(function (e) {
        e.preventDefault()
        $(this).unbind('click')
    })
    let audio = element.children[0]
    let progress = element.parentElement.children[2].children[0];
    if (element.id == 'play-icon-reel') {
        element.id = 'pause-icon-reel'
        audio.play()
        element.parentElement.style.backgroundColor = 'rgba(97, 97, 97, .5)'
        audio.addEventListener('timeupdate', function () {
            progress.style.width = ((audio.currentTime / audio.duration) * 100) + '%';
        })
    } else {
        element.id = 'play-icon-reel'
        audio.pause()
        element.parentElement.style.backgroundColor = 'transparent'
    }
};

function deleteReel(reel) {
    $('a.reel-a').click(function (e) {
        e.preventDefault()
        $(this).unbind('click')
    })
    data = 'reel_id=' + reel
    $.ajax({
        method: "POST",
        url: "/delete_reel",
        data: data,
        cache: false,
        success: function () {
            location.reload()
        }
    })
}

function deleteFile(file) {
    $('a.reel-a').click(function (e) {
        e.preventDefault()
        $(this).unbind('click')
    })
    data = 'file_id=' + file
    console.log(data)
    $.ajax({
        method: "POST",
        url: "/delete_file",
        data: data,
        cache: false,
        success: function () {
            location.reload()
        }
    })
}