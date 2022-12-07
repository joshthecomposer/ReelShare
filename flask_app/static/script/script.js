$(document).ready(function () {
    $("ul.sortable").sortable({
        update: function(event, ui) {
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
    });

    $( function() {
        $(".draggable").draggable({
            helper: "clone",
            revert: "invalid"
        });
        $( ".droppable" ).droppable({
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
                    }
                })
                }
        });
    });
});

function updateOrder() {
    var item_order = new Array();
    $('ul.sortable li').each(function(){
        item_order.push($(this).attr("id"));
    })
    return item_order;
}
$(document).ajaxSuccess(function () {
    window.location.reload();
});