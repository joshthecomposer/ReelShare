let blurElement = document.querySelector('#blur');
let reel_creation = document.getElementById('reel_creation');

$(document).ready(function () {
    $("ul.sortable").sortable({
        update: function (event, ui) {
            item_order = updateOrder();
            console.log("Item order is: ", item_order);
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
    // $(document).ajaxSuccess(function () {
    //     location.reload();
    // });
});

    $( function() {
        $(".draggable").draggable({
            helper: "clone",
            revert: "invalid"
        });
        $(".droppable").droppable({
            drop: function (event, ui) {
                console.log(event)
                console.log (event.target.children.length)
                // for (var i = 0; i < event.target.children.length; i++) {
                //     if (event.target.children[i].id == ui.draggable.id)
                //         window.location.reload();
                //         return
                // }

                //TODO: SPACER NEEDS TO BE REMOVED. THAT' WHY REEL MESSES UP HEIGHT WHEN DRAGGING.
                console.log(event.target.children, "is the event target's chidlrean")
                console.log(ui.draggable[0])
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
                    beforeSend: function () {
                        event.target.style.height = '0px'
                    } 
                    ,
                        
                    cache: false,
                    success: function (data) {
                        $("#test").html(data);
                        // window.location.reload();
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
}

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
    console.log()
}
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
}
    
function audioPlayer(element) {
    $('a.reel-a').click(function (e) {
        e.preventDefault()
        $(this).unbind('click')
    })
    let audio = element.children[0]
    let parentID = element.parentElement.id
    let progress = element.parentElement.children[2].children[0];
    console.log(progress)
    if (element.id == 'play-icon') {
        element.id = 'pause-icon'
        audio.play()
        element.parentElement.style.backgroundColor = 'rgba(97, 97, 97, .5)'
        //progressbar functionality:
        audio.addEventListener('timeupdate', function () {
            progress.style.width = ((audio.currentTime / audio.duration) * 100) + '%';
        })
    } else {
        element.id = 'play-icon'
        audio.pause()
        element.parentElement.style.backgroundColor = 'transparent'
    }
}