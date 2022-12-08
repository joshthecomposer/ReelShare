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
                    $("#test").html(data);
                }
            })
        }
    })
    $(document).ajaxSuccess(function () {
        setInterval('location.reload()', 1000);
    });
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
                    success: function (data) {
                        $("#test").html(data);
                        window.location.reload();
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
        $(blurElement).css({
            'filter':filterVal,
            'webkitFilter':filterVal,
            'mozFilter':filterVal,
            'oFilter':filterVal,
            'msFilter':filterVal,
            'transition':'all 0.5s ease-out',
            '-webkit-transition':'all 0.5s ease-out',
            '-moz-transition':'all 0.5s ease-out',
            '-o-transition':'all 0.5s ease-out'
        }); 
    
        $.ajax({
            method: "POST",
            url: "/reveal_reel_creation_box",
            cache: false,
            success: function (data) {
                window.location.reload();
            }
        })
        return false;
}

async function hideReelCreation() {
        var opacity = 'opacity(0)';
        var filterVal = 'blur(0px)';
        $(hideElement).css({
            'filter':opacity,
            'webkitFilter':opacity,
            'mozFilter':opacity,
            'oFilter':opacity,
            'msFilter':opacity,
            'transition':'all 0.5s ease-out',
            '-webkit-transition':'all 0.5s ease-out',
            '-moz-transition':'all 0.5s ease-out',
            '-o-transition':'all 0.5s ease-out'
        });
        $(blurElement).css({
            'filter':filterVal,
            'webkitFilter':filterVal,
            'mozFilter':filterVal,
            'oFilter':filterVal,
            'msFilter':filterVal,
            'transition':'all 0.5s ease-out',
            '-webkit-transition':'all 0.5s ease-out',
            '-moz-transition':'all 0.5s ease-out',
            '-o-transition':'all 0.5s ease-out'
        });
        $.ajax({
            method: "POST",
            url: "/reveal_reel_creation_box",
            cache: false,
            success: function (data) {
                window.location.reload();
            }
        })
        return false;
}