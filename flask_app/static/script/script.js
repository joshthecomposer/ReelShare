let blurElement = document.getElementById('not_blurry');
let hideElement = document.getElementById('reel_creation');

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
                    cache: false,
                    beforeSend: function () {
                        $(event.target).removeAttr('style');
                    },
                    success: function (data) {
                        $("#test").html(data);
                        location.reload();
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

async function revealReelCreation() {
    var filterVal = 'blur(30px)';
    var opacity = 'opacity(100%)'
    
        $.ajax({
            method: "POST",
            url: "/reveal_reel_creation_box",
            cache: false,
            beforeSend: function () {
                $(hideElement).fadeIn()
            },
            success: function (data) {
                location.reload();
            }
        })
        
}

//TODO: Reel creation can be done client-side instead of duplicating the reels stuff.

async function hideReelCreation() {
        $.ajax({
            method: "POST",
            url: "/reveal_reel_creation_box",
            cache: false,
            beforeSend: function () {
                $(hideElement).fadeOut()
            },
            success: function (data) {
                location.reload();
            }
        })
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